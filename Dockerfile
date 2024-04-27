FROM python:3.12-slim

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code
COPY requirements_docker.txt .
RUN pip install -r requirements_docker.txt
COPY . .

ENV DJANGO_SETTINGS_MODULE=config.settings_docker