FROM python:3.9-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

COPY ./requirements/develop.txt /app/requirements/develop.txt
COPY ./requirements/base.txt /app/requirements/base.txt
COPY ./requirements/production.txt /app/requirements/production.txt

RUN pip install --upgrade pip
RUN pip install -r /app/requirements/production.txt
RUN pip install gunicorn

COPY . .

EXPOSE 8000