"""Utils fonctions used in Heroes stats web app"""
from app import mysql_app as mysql
import pandas as pd


def query_to_rows(query):
    """
    Execute sql query and get result

    Parameters
    ----------
        query (str): query to execute
    Returns
    -------
        (list of tuples): one tuple is a row of
        the query result
    """
    cursor = mysql.connection.cursor()
    cursor.execute(query)
    return cursor.fetchall()


def preprocess_rows(rows, columns):
    """
    Preprocess tuples values:
        - build url of hero image from name_hero and
            format it
        - format numerical variable to render on html page
    Put names on a tuples value (ie list of n tuples
    to a list of n dictionary where keys are a
    variable name and value are tuples values)

    Parameters
    ----------
        rows (list of tuples): list of tuple of len l
        columns (list of string): list of len l
            of variable name
    Returns
    -------
        (list of dictionary)
    """
    # Tuples to dataframe
    df = pd.DataFrame(rows, columns=columns)
    # Preprocess name_hero
    df['url_img'] = df['name_hero'].map(
        lambda x: f"heroes_stats/assets/heroes_pic/\
{x.replace('npc_dota_hero_', '')}.png"
    )
    df['name_hero_readable'] = df['name_hero'].map(
        lambda x: ' '.join(x.replace('npc_dota_hero_', '').split('_')).title()
    )
    df.drop(['name_hero'], axis=1)
    # Format numerical values
    df['primary_attr'] = df['primary_attr'].map(lambda x: x.upper())
    for indic in ['pick_rate', 'win_rate']:
        try:
            df[indic] = df[indic].map(lambda x: f'{x}%')
        except KeyError:
            pass
    for indic in ['n_matchs', 'n_matchs_won']:
        try:
            df[indic] = df[indic].map(lambda x: f'{x: }')
        except KeyError:
            pass
    return df.to_dict('records')


def get_data_hero_against_with(id_hero, relation='against', top_n=5):
    """
    Query grouped_matchs_heroes_against or grouped_matchs_heroes_with
    to get coupled win_rate and matchs played of id_hero matchs
    with all other heroes.
    Those informations are joined to heroes_custom to get heroes info
    and ranked to top_n

    Parameters
    ----------
        id_hero (int): the id of the hero focused
        relation (str): against or with (same or opponent team)
        top_n (int): top_n results
    Returns
    -------
        (dictionary): best win rate and most matchs played hero data sorted
    """
    data = {}
    # Build query
    columns = [
        'hero_id', 'name_hero', 'roles', 'attack_type',
        'primary_attr', 'win_rate', 'n_matchs'
    ]
    query = f'''
    SELECT pw.hero_{relation}_id AS hero_id, heroes.name_hero,
        heroes.roles, heroes.attack_type, heroes.primary_attr,
        pw.win_rate, pw.n_matchs AS n_matchs
    FROM (
        SELECT *
        FROM dota2_datawarehouse.grouped_matchs_heroes_{relation}
        WHERE hero_id = {id_hero}
    ) AS pw
    LEFT JOIN heroes_custom as heroes ON pw.hero_{relation}_id = heroes.hero_id
    '''
    # Query db and preprocess results
    rows = query_to_rows(query)
    rows_cleaned = preprocess_rows(rows, columns)
    # Sort results
    for indicator in ['win_rate', 'n_matchs']:
        data[f'{indicator}_{relation}'] = sorted(
            rows_cleaned,
            key=lambda dict_hero: dict_hero[indicator], reverse=True
        )[:top_n]
    return data
