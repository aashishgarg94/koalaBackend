FROM tiangolo/uvicorn-gunicorn:python3.8
LABEL maintainer="Sebastian Ramirez <tiangolo@gmail.com>"
RUN pip3 install --upgrade pip
RUN pip3 install pipenv
COPY ./koala Pipfile* Pipfile.lock /app/koala/
RUN cd /app/koala/ && pipenv install --ignore-pipfile --system

HEALTHCHECK CMD curl --fail http://127.0.0.1/healthcheck || exit 1