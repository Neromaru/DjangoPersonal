FROM python:3.7-alpine

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

EXPOSE 8090

COPY . /django_app
WORKDIR /django_app

RUN pip install -r requirements.txt
RUN python manage.py makemigrations &&\
    python manage.py migrate

ENTRYPOINT python manage.py runserver 0.0.0.0:8090