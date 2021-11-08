FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-slim

COPY ./requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

COPY ./{{cookiecutter.project_slug}}/ /app/{{cookiecutter.project_slug}}


ENV MODULE_NAME="{{cookiecutter.project_slug}}.entrypoints.api.main"
ENV VARIABLE_NAME="api"
ENV WORKERS_PER_CORE=2
