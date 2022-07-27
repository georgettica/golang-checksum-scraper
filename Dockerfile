# syntax=docker/dockerfile:1

# Dockerfile pulled from https://docs.docker.com/language/python/build-images/

FROM python:3.11.0b5-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt --user

COPY . .

CMD [ "python3", "./golang-checksum-scraper.py"]
