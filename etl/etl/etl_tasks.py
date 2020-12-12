"""Celery task files"""
from celery_app import celery
from etl.etl_functions import extract_teams, get_match_detail_from_match_id
from etl.utils import flat_list, insert_data_to_tables,\
    get_sql_explorer_req_from_date, read_parse_sql_file, request_from_url
from os import environ
import mysql.connector
import random


@celery.task(ignore_result=True)
def get_matchs_metadata_from_date(date="01/01/2020", len_sample=None):
    """
    Extract len_sample random matchs metadata (start_time, match_id, winner)
    from dota2 API opendota.com at date

    Parameters
    ----------
        date (str): date under "dd/MM/YYYY" format
        len_sample (int): number of matchs to extract
    Returns
    -------
        (list of dictionnary): list of data matchs of dictionary
            with start_time and id_matchs
    """
    # Build query
    sql_explorer_opendota_request = get_sql_explorer_req_from_date(date=date)
    # Run query
    response_matchs_metadata = request_from_url(sql_explorer_opendota_request)
    matchs_metadata = response_matchs_metadata.json()['rows']
    # Sample results
    if len_sample:
        matchs_metadata = random.sample(matchs_metadata, len_sample)
    return matchs_metadata


@celery.task(ignore_result=True)
def complete_match_metadata_with_teams(
    match_metadata,
    api_key
):
    """
    Complete matchs metadata with teams composition
    from Steam API

    Parameters
    ----------
        match_metadata (dict): a match metadata
        api_key (str): api steam key
    Returns
    -------
        (dict): match_metadata with the winner and
        looser team composition as keys
    """
    # Request Steam API
    match_detail = get_match_detail_from_match_id(
        match_metadata['match_id'],
        api_key=api_key
    )
    # Extract matchs
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
    """
    Preprocess a list of matchs to push data
    to matchs_heroes and matchs table
    Then update custom tables to recompute
    indicators

    Parameters
    ----------
        matchs_completed (list of dict): list of matchs metadata completed
    Returns
    -------
        (bool): True
    """
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
    cursor = insert_data_to_tables(
        matchs_heroes, cursor, 'matchs_heroes',
        ['match_id', 'hero_id', 'is_win'], bool_columns=['is_win']
    )
    print("re building custom tables")
    sql_queries = read_parse_sql_file('etl/sql/3_custom_tables.sql')
    for line in sql_queries:
        cursor.execute(line)
    print("commit changes ...")
    db.commit()
    print("changes commited")
    return True
