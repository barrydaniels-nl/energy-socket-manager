#!/bin/bash
apt-get update
apt-get upgrade -y
pip install --upgrade pip
pip install -r requirements/base.txt
pip install -r requirements/production.txt