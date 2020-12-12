"""Routes for heroes stats web app"""
from flask import render_template
from app.heroes_stats import bp
from app.heroes_stats.utils import preprocess_rows, query_to_rows,\
    get_data_hero_against_with


@bp.route('/', methods=['GET', 'POST'])
def heroes():
    """
    Query and all heroes data in the MySQL DB
    Data are ranked according:
        - alphabetic order
        - win_rate^2 * pick_rate desc
    and send to 'heroes_stats/homepage.html'
    available at '/'

    Parameters
    ----------
    Returns
    -------
        (flask.render_template): the template 'heroes_stats/homepage.html'
            rendered with all data heroes
    """
    # Build query
    columns = [
        'hero_id', 'name_hero', 'roles', 'attack_type',
        'primary_attr', 'win_rate', 'pick_rate'
    ]
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
    data['alpha_sort'] = sorted(
        rows_cleaned,
        key=(lambda dict_hero: dict_hero['name_hero_readable'])
    )
    data['indicator_sort'] = rows_cleaned
    return render_template('heroes_stats/homepage.html', data=data)


@bp.route('/focus/<id_hero>', methods=['GET', 'POST'])
def coucou(id_hero=None):
    """
    Get best allies and worst opponents hero of id_hero
    in terms of number of matchs played and the win_rate.
    Data is a dictionary of 5 keys:
        - most played match hero data against id_hero
        - best win_rate hero data against id_hero
        - most played match hero data with id_hero
        - best win_rate hero data with id_hero
        - id_hero data info
        send to 'heroes_stats/focus_page.html' available
        at '/focus/<id_hero>'

    Parameters
    ----------
        id_hero (int): the id of the hero focused
    Returns
    -------
        (flask.render_template): the template 'heroes_stats/focus_page.html'
            rendered with data dictionary
    """
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
    data['hero_info'] = preprocess_rows(
        rows,
        columns=[
            'hero_id', 'name_hero', 'roles', 'attack_type', 'primary_attr'
        ]
    )[0]
    return render_template('heroes_stats/focus_page.html', data=data)
