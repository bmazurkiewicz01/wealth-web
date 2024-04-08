#!/bin/bash

echo "Apply databse migrations"
python manage.py makemigrations wealthweb
python manage.py migrate

exec "$@"