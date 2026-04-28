#!/usr/bin/env bash
set -o errexit

mkdir -p "$(dirname "${SQLITE_PATH:-db.sqlite3}")"
mkdir -p "${MEDIA_ROOT:-media}"

python manage.py migrate
exec gunicorn config.wsgi:application
