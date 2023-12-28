#!/bin/sh

# if [ "$DATABASE" = "postgres" ]
# then
#     echo "Waiting for postgres..."

#     while ! nc -z $SQL_HOST $SQL_PORT; do
#       sleep 0.1
#     done

#     echo "PostgreSQL started"
# fi

# python manage.py flush --no-input
# python manage.py migrate

# exec "$@"




python manage.py migrate                  # Apply database migrations

python manage.py collectstatic --noinput  # Collect static files

# Prepare log files
touch /gunicorn/logs/access.log
touch /gunicorn/logs/error.log


# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn stipe_app.wsgi:application \
    --bind 0.0.0.0:8080 \
    --workers 3 \
    --log-level=info \
    --access-logfile=/gunicorn/logs/access.log \
    --error-logfile=/gunicorn/logs/error.log \
    --capture-output \
    "$@"
