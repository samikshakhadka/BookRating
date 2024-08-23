FROM python:3.12.5-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /BookRatingCode

COPY requirements.txt /BookRatingCode/
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

    RUN apt-get update && \
    apt-get install -y redis-tools 
    
RUN pip install -r requirements.txt

COPY . /BookRatingCode/