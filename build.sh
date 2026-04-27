#!/usr/bin/env bash
set -o errexit

mkdir -p "$(dirname "${SQLITE_PATH:-db.sqlite3}")"
mkdir -p "${MEDIA_ROOT:-media}"

python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
