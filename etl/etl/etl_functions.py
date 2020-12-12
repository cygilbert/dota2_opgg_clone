from etl.utils import request_from_url


def get_match_detail_from_match_id(match_id, api_key):
    """
    Request STEAM API to get match match_id informations
    not present in match metadata (teams for example)
    Parameters
    ----------
        match_id (int)
        api_key (int): api steam key
    Returns
    -------
        (dictionary): matchs details
    """
    params = {'match_id': match_id}
    url_match_detail_endpoint = f'https://api.steampowered.com/\
IDOTA2Match_570/GetMatchDetails/V001/?key={api_key}'
    try:
        match_details = request_from_url(
            url_match_detail_endpoint, params=params
        ).json()['result']
    except AttributeError:
        return {}
    if 'error' in match_details:
        return {}
    else:
        return match_details


def extract_teams(picks_bans, radiant_win):
    """
    Unest teams field from STEAM API
    """
    teams = {
        'winners': [],
        'loosers': []
    }
    for pick_ban in picks_bans:
        if pick_ban['is_pick']:
            # radiant team id is 0
            is_win = (pick_ban['team'] != radiant_win)
            # add to the collection of the winner or looser team
            teams['winners' if is_win else 'loosers']\
                .append(pick_ban['hero_id'])
    for team in teams.keys():
        teams[team].sort()
    return teams
