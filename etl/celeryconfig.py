#!/usr/bin/python
# -*- coding: utf-8 -*-
from os import environ, path
from dotenv import load_dotenv

# Access to env variable
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

# Broker and Backend
BROKER_URL = environ.get(
    'REDIS_URL',
    'redis://redis:6379/0'
)
CELERY_RESULT_BACKEND = BROKER_URL

# MySQL paramas
mysql_params = {
    'host': environ.get('MYSQL_HOST', 'db'),
    'port': int(environ.get('MYSQL_PORT', 3306)),
    'user': environ.get('MYSQL_USER', 'root'),
    'password': environ.get('MYSQL_PASSWORD', 'root'),
    'database': environ.get('MYSQL_DB', 'dota2_datawarehouse')
}

# Import, timezone schreduler
CELERY_IMPORTS = ['etl.etl_workflow', 'etl.etl_tasks']
CELERY_TASK_RESULT_EXPIRES = 30
CELERY_TIMEZONE = 'UTC'
CELERY_ACCEPT_CONTENT = ['json', 'msgpack', 'yaml']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERYBEAT_SCHEDULE = {'test-celery': {
    'task': 'etl.etl_workflow.workflow',
    'schedule': 40, 'args': (10, environ.get('API_KEY_STEAM'), mysql_params)
    }
}

# Rate limit setting
CELERY_ANNOTATIONS = {
    'etl.etl_tasks.complete_match_metadata_with_teams': {
        'rate_limit': '400/m'
    }
}
