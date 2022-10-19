#!/bin/bash
apt-get update
apt-get upgrade -y
python manage.py migrate
python manage.py runserver 0.0.0.0:8000