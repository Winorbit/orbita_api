#!/bin/sh
python manage.py makemigrations api --noinput
python manage.py migrate --noinput
python manage.py collectstatic --noinput
exec "$@"