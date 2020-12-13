# Use an official Python runtime as an image
FROM python:3.6

EXPOSE 5000

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


COPY app app
COPY config.py wsgi.py wait_for_mysql_db_backend.py boot.sh ./
RUN chmod +x boot.sh
ENTRYPOINT ["./boot.sh"]