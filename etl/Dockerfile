FROM python:3.6.6

EXPOSE 5555

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONUNBUFFERED=1

WORKDIR /etl

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY etl etl
COPY celeryconfig.py celery_app.py wait_for_mysql_db_backend.py ./
