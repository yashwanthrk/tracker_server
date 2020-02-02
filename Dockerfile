FROM python:3.6.8

WORKDIR /usr/src/app

COPY requirements.txt .
COPY install.sh .

RUN sh install.sh

ENV TZ 'Asia/Kolkata'

# CMD python3 app.py



