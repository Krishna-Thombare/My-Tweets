#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

# Write CA cert from environment variable to file
if [ -n "$DB_SSL_CA_CERT" ]; then
    echo "$DB_SSL_CA_CERT" > ca.pem
fi

python manage.py collectstatic --no-input
python manage.py migrate