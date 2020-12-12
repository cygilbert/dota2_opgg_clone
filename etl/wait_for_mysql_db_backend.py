import os
import sys
import mysql.connector
import time
from mysql.connector.errors import DatabaseError
from os import environ

if __name__ == "__main__":
    host = environ.get('MYSQL_HOST', 'db')
    port = environ.get('MYSQL_PORT', 3306)
    user = environ.get('MYSQL_USER', 'root')
    password = environ.get('MYSQL_PASSWORD', 'root')
    db_backend = environ.get('MYSQL_DB_CELERY_BACKEND', 'celery_backend')
    for i in range(0, 1000):
        while True:
            try:
                db = mysql.connector.connect(
                    host=host,
                    port=port,
                    user=user,
                    password=password,
                    database=db_backend
                )
            except DatabaseError:
                print('MySQL Backend Database not ready, go to sleep')
                time.sleep(1)
                continue
            break
    print('MySQL Backend Database ready !')
    os.system(sys.argv[1])
