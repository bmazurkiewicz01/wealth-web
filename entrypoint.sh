#!/bin/bash

echo "Apply databse migrations"
python manage.py migrate

exec "$@"