#!/bin/sh

# wait for PSQL server to start
sleep 10

python manage.py makemigrations app
python manage.py migrate

python manage.py make_triggers

python manage.py runserver 0.0.0.0:8000