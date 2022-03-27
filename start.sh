#!/bin/bash
export PATH=$PATH:/app/
#python manage.py makemigrations app
python manage.py migrate
python manage.py runserver 0.0.0.0:8000 &

sleep 2m
python consumer.py

wait
exit $?