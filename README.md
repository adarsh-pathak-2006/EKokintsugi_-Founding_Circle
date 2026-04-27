# EkoKintsugi Founding Circle Pilot System

Database-backed Django application for the 10-user circular footwear pilot.

## Stack

- Django 6
- SQLite
- Server-rendered templates
- Static CSS
- File uploads for weekly review images

## Features

- Login and signup
- Role-based pilot users: intern, team, supporter
- Admin dashboard for:
  - user management
  - review tracking
  - return tracking
  - points management
- User dashboard with:
  - shoe details
  - symbolic tree details
  - points summary
  - QR access page
  - weekly review flow
  - return request flow
- Real database models for:
  - users
  - shoes
  - trees
  - points accounts
  - point transactions
  - weekly reviews
  - return requests

## Setup

From the project folder:

```powershell
python manage.py migrate
python manage.py seed_pilot
python manage.py runserver
```

Open:

`http://127.0.0.1:8000/`

## Demo Credentials

- Admin: `admin@ekokintsugi.com` / `admin123`
- User: `pilot1@ekokintsugi.com` / `pilot123`

## Notes

- Database file: `db.sqlite3`
- Uploaded review files are stored in `media/reviews/`
- QR pages are user-specific routes backed by a UUID token
- The seed command creates the admin plus 10 pilot users
