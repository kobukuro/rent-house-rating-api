#!/bin/sh
# set -e stops the execution of a script if a command or pipeline has an error -
# which is the opposite of the default shell behaviour, which is to ignore errors in scripts.
set -e

python manage.py wait_for_db
python manage.py collectstatic --noinput
python manage.py migrate
python manage.py execute sqls
# run uwsgi service
# --master:make sure runs in the foreground in the container, so the output will be saved in logs
uwsgi --socket :9000 --workers 4 --master --enable-threads --module rent_house_rating_api.wsgi
