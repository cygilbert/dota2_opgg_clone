from app import mysql_app as mysql
import pandas as pd


def preprocess_rows(rows, columns):
    df = pd.DataFrame(rows, columns=columns)
    df['url_img'] = df['name_hero'].map(lambda x: f"heroes_stats/assets/heroes_pic/{x.replace('npc_dota_hero_', '')}.png")
    df['name_hero_readable'] = df['name_hero'].map(lambda x: ' '.join(x.replace('npc_dota_hero_', '').split('_')).title())
    df['primary_attr'] = df['primary_attr'].map(lambda x: x.upper())
    df.drop(['name_hero'], axis=1)
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

def query_to_rows(query):
    cursor = mysql.connection.cursor()
    cursor.execute(query)
    return cursor.fetchall()


def get_data_hero_against_with(id_hero, relation='against', top=5):
    data = {}
    columns = [f'hero_id', 'name_hero', 'roles', 'attack_type', 'primary_attr', 'win_rate', 'n_matchs']
    query = f'''
    SELECT pw.hero_{relation}_id AS hero_id, heroes.name_hero, heroes.roles, heroes.attack_type,
        heroes.primary_attr, pw.win_rate, pw.n_matchs AS n_matchs 
    FROM (
        SELECT * 
        FROM dota2_datawarehouse.grouped_matchs_heroes_{relation}
        WHERE hero_id = {id_hero}
    ) AS pw
    LEFT JOIN heroes_custom as heroes ON pw.hero_{relation}_id = heroes.hero_id
    '''
    rows = query_to_rows(query)
    rows_cleaned = preprocess_rows(rows, columns)
    for indicator in ['win_rate', 'n_matchs']:
        data[f'{indicator}_{relation}'] = sorted(rows_cleaned, key=lambda dict_hero: dict_hero[indicator], reverse=True)[:top]
    return data