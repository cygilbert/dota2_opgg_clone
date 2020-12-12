from datetime import datetime, timedelta
from requests.exceptions import HTTPError
import pandas as pd
import requests


# per default user agent
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0)" +
    " Gecko/20100101 Firefox/40.0"
}


def request_from_url(
        url,
        headers=headers,
        params=None):
    """
    Function to request an endpoint from a url
    and provide the reponse under json format
    Parameters:
        url (str): url of endpoint
        headers (dict): headers for the GET request
        params (dict): params for the GET request
    Returns:
        (json): response of the GET request under json
    """
    try:
        response = requests.get(url, headers=headers, params=params)
        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        pass
    except Exception as err:
        print(f'Other error occurred: {err}')
        pass
    else:
        return response


def get_interval_date_unix(date):
    start_date = datetime.strptime(date, "%d/%m/%Y")
    end_date = start_date + timedelta(days=1)
    return int(start_date.timestamp()),\
        int(end_date.timestamp())


def get_sql_explorer_req_from_date(
        date,
        base_explorer_api="https://api.opendota.com/api/explorer?sql="):
    """
    Build SQL request to request steam api
    """
    # convert to unix
    start_unix_time, end_unix_time = get_interval_date_unix(date=date)
    sql_request = f'\
SELECT match_id, avg_mmr, cluster, radiant_win, start_time \
FROM public_matches \
WHERE start_time > {start_unix_time} AND \
start_time < {end_unix_time} AND \
avg_mmr IS NOT NULL'
    return base_explorer_api + sql_request


flat_list = (lambda t: [item for sublist in t for item in sublist])


def read_parse_sql_file(path_sql_script):
    """
    Function to read and parse a sql file
    Parameters:
        path_sql_script (str): path of the sql script to read and parse
    Returns:
        (list): list of string of sql requests
    """
    with open(path_sql_script, 'r') as dml_file:
        dml = dml_file.read().strip().split(';')[:-1]
    return dml


def insert_data_to_tables(
    data,
    cursor,
    table_name,
    columns,
    bool_columns=None
):
    """
    TO DO
    """
    df = pd.DataFrame(data)[columns]
    if bool_columns:
        for col in bool_columns:
            df[col] = df[col].map(int)
    tuples_data = [tuple(x) for x in df.applymap(str).to_numpy()]
    cursor.executemany(
        f'''INSERT INTO {table_name} ({' ,'.join(columns)})
        VALUES ({' ,'.join(['%s']*len(columns))})''',
        tuples_data
    )
    return cursor
