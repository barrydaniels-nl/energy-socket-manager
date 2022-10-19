#!/bin/bash
apt-get update
apt-get upgrade -y
celery -A energy worker -E -l info