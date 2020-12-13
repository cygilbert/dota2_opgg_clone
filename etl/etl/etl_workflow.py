from celery import chord
from celery_app import celery
from datetime import date, timedelta
from etl.etl_tasks import complete_match_metadata_with_teams,\
    get_matchs_metadata_from_date, update_db
from etl.utils import test_steam_api_key


@celery.task()
def workflow(len_sample, api_key, mysql_params):
    """
    Complete workflow:
        - Get matchs metadata (start_time, match_id, winner) of yesterday
        - From ids request STEAM API to get looser and winner team composition
        - Preprocess data to push it MYSQL db and update custom tables
    Parameters
    ----------
        match_metadata (dict): a match metadata
        len_sample (int): number of matchs to extract
        mysql_params (dict): mysql connection info including
            host, port, user, password and database name
    Return
    ----------
    """
    if test_steam_api_key(api_key):
        # Yesterday under dd/MM/YYYY format
        day = (date.today() + timedelta(days=-1)).strftime("%d/%m/%Y")
        # Get matchs_metadata
        matchs_metadata = get_matchs_metadata_from_date(day, len_sample)
        # Maps all matchs to get their information
        maps = [complete_match_metadata_with_teams.s(
            match_metadata, api_key) for match_metadata in matchs_metadata]
        # Put it together and push to db
        reducer = chord(maps)(update_db.s(mysql_params=mysql_params))
        return reducer
    print(f'{api_key} is not a valid API Key, skip ETL Jobs')
    return
