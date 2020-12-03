#!/bin/bash

# echo "hello world"

python manage.py sqlflush

python manage.py loaddata db.json