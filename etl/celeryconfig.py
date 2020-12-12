#!/usr/bin/python
# -*- coding: utf-8 -*-
from os import environ, path
from dotenv import load_dotenv

# Access to env variable
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

# Broker and Backend
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
BROKER_URL = environ.get(
    'REDIS_URL',
    'redis://{host}:{port}/0'.format(
        host=REDIS_HOST,
        port=str(REDIS_PORT)
    )
)

CELERY_RESULT_BACKEND = BROKER_URL

# Import, timezone schreduler
CELERY_IMPORTS = ['etl.etl_workflow', 'etl.etl_tasks']
CELERY_TASK_RESULT_EXPIRES = 30
CELERY_TIMEZONE = 'UTC'
CELERY_ACCEPT_CONTENT = ['json', 'msgpack', 'yaml']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERYBEAT_SCHEDULE = {'test-celery': {
    'task': 'etl.etl_workflow.workflow',
    'schedule': 40, 'args': (10, environ.get('API_KEY_STEAM'))
    }
}

# Rate limit setting
CELERY_ANNOTATIONS = {
    'etl.etl_tasks.complete_match_metadata_with_teams': {
        'rate_limit': '400/m'
    }
}
