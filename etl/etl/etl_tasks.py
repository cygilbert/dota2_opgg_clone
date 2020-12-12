from celery_app import celery
from celery import subtask, group, chord
from etl.utils import get_sql_explorer_req_from_date, request_from_url, flat_list, read_parse_sql_file, insert_data_to_tables
from etl.etl_functions import get_match_detail_from_match_id, extract_teams
from datetime import date, timedelta
import random
from os import environ
import mysql.connector
import pandas as pd


@celery.task(ignore_result=True)
def get_matchs_metadata_from_date(date="01/01/2020", len_sample=None):
    sql_explorer_opendota_request = get_sql_explorer_req_from_date(date=date)
    response_matchs_metadata = request_from_url(sql_explorer_opendota_request)
    matchs_metadata = response_matchs_metadata.json()['rows']
    if len_sample:
        matchs_metadata = random.sample(matchs_metadata, len_sample)
    return matchs_metadata


@celery.task(ignore_result=True)
def complete_match_metadata_with_teams(
    match_metadata,
    api_key
):
    match_detail = get_match_detail_from_match_id(
        match_metadata['match_id'],
        api_key=api_key
    )
    try:
        match_metadata['teams'] = extract_teams(
            match_detail['picks_bans'],
            match_metadata['radiant_win']
        )
        return match_metadata
    except KeyError:
        return


@celery.task()
def update_db(matchs_completed):
    print("cleaning data")
    matchs_completed = list(filter(None, matchs_completed))
    matchs_heroes = flat_list(
        [
            [{'match_id': match['match_id'], 'hero_id': hero, 'is_win': True}
             for hero in match['teams']['winners']]
            for match in matchs_completed
        ]
    ) + flat_list(
        [
            [{'match_id': match['match_id'], 'hero_id': hero, 'is_win': False}
             for hero in match['teams']['loosers']]
            for match in matchs_completed
        ]
    )
    print("pushing data")
    db = mysql.connector.connect(
        host='db',
        port=environ.get('MYSQL_PORT'),
        user=environ.get('MYSQL_USER'),
        password=environ.get('MYSQL_PASSWORD'),
        database=environ.get('MYSQL_DB')
    )
    cursor = db.cursor()
    cursor = insert_data_to_tables(matchs_completed, cursor, 'matchs', [
                                   'match_id', 'start_time'])
    cursor = insert_data_to_tables(matchs_heroes, cursor, 'matchs_heroes', [
                                   'match_id', 'hero_id', 'is_win'], bool_columns=['is_win'])
    print("re building custom tables")
    sql_queries = read_parse_sql_file('etl/sql/3_custom_tables.sql')
    for line in sql_queries:
        cursor.execute(line)
    # cursor.executemany(sql_queries)
    print("commit changes ...")
    db.commit()
    print("changes commited")
    return True


@celery.task()
def workflow(len_sample, api_key):
    day = (date.today() + timedelta(days=-1)).strftime("%d/%m/%Y")
    matchs_metadata = get_matchs_metadata_from_date(day, len_sample)
    # split your problem in embarrassingly parallel maps
    maps = [complete_match_metadata_with_teams.s(
        match_metadata, api_key) for match_metadata in matchs_metadata]
    # and put them in a chord that executes them in parallel and after they finish calls 'reduce'
    mapreduce = chord(maps)(update_db.s())
    return api_key
