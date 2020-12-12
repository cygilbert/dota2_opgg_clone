from flask import render_template
from app.heroes_stats import bp
from app.heroes_stats.utils import preprocess_rows, query_to_rows,\
    get_data_hero_against_with


@bp.route('/', methods=['GET', 'POST'])
def heroes():
    # Build query
    columns = ['hero_id', 'name_hero', 'roles', 'attack_type', 'primary_attr', 'win_rate', 'pick_rate']
    query = f'''
    SELECT {', '.join(['h.' + col for col in columns])}
    FROM dota2_datawarehouse.heroes_custom as h
    ORDER BY POWER(win_rate, 2) * pick_rate DESC;
    '''
    # Execute query
    rows = query_to_rows(query)
    # Preprocess results
    rows_cleaned = preprocess_rows(rows, columns=columns)
    # To data
    data = {}
    data['alpha_sort'] =  sorted(rows_cleaned, key=lambda dict_hero: dict_hero['name_hero_readable'])
    data['indicator_sort'] = rows_cleaned
    return render_template('heroes_stats/homepage.html', data=data)


@bp.route('/focus/<id_hero>', methods=['GET', 'POST'])
def coucou(id_hero = None):
    # Data 
    data = {
        **get_data_hero_against_with(id_hero=id_hero, relation='against'),
        **get_data_hero_against_with(id_hero=id_hero, relation='with')
    }
    # Hero info
    columns = ['hero_id', 'name_hero', 'roles', 'attack_type', 'primary_attr']
    query = f'''
    SELECT {', '.join(columns)}
    FROM dota2_datawarehouse.heroes_custom
    WHERE hero_id={id_hero}   
    '''
    rows = query_to_rows(query)
    data['hero_info'] = preprocess_rows(rows,  columns=['hero_id', 'name_hero', 'roles', 'attack_type', 'primary_attr'])[0]
    return render_template('heroes_stats/focus_page.html', data=data)
