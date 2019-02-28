#!/usr/bin/env bash
set -e
python manage.py makemigrations --noinput
python manage.py migrate --noinput

#python manage.py collectstatic —-noinput
echo yes | python manage.py collectstatic

#python manage.py runserver 0.0.0.0:80
exec gunicorn --bind=0.0.0.0:80 configuration.wsgi --workers=5 --log-level=info --log-file=---access-logfile=- --error-logfile=- --timeout 30000 --reload