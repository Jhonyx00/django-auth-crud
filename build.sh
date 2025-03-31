#!/usr/bin/env bash
# exit on eror
set -o errexit

# poetry install
pip install -r requirements.txt

puthon manage.py collectstatic --no-input
python manage.py migrate