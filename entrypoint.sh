#!/bin/sh
python manage.py makemigrations api --noinput
python manage.py migrate --noinput
python manage.py collectstatic --noinput
if [ "$tesmode" = true ]; then
  python manage.py test 
fi
exec "$@"
