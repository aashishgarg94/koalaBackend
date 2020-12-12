FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

RUN pip install pipenv
COPY Pipfile* /tmp/
RUN cd /tmp && pipenv lock --requirements > requirements.txt
RUN pip install -r /tmp/requirements.txt
COPY ./koala /app/koala/

HEALTHCHECK CMD curl --fail http://127.0.0.1/healthcheck || exit 1