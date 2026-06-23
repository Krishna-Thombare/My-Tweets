#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

# Write CA cert from environment variable to absolute path
if [ -n "$DB_SSL_CA_CERT" ]; then
    echo "$DB_SSL_CA_CERT" > /opt/render/project/src/mytweet/ca.pem
fi

python manage.py collectstatic --noinput
python manage.py migrate