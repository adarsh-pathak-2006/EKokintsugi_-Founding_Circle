# EkoKintsugi Pilot System

Django application for the EkoKintsugi Founding Circle pilot.

## Requirements

- Python 3.14+
- pip
- Git

## Local Setup

1. Clone the repository:

```powershell
git clone https://github.com/YOUR-USERNAME/YOUR-REPO.git
cd YOUR-REPO
```

2. Create a virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

3. Install dependencies:

```powershell
pip install -r requirements.txt
```

4. Run migrations:

```powershell
python manage.py migrate
```

5. Seed demo data:

```powershell
python manage.py seed_pilot
```

6. Start the development server:

```powershell
python manage.py runserver
```

7. Open:

`http://127.0.0.1:8000/`

## Demo Credentials

- Admin: `admin@ekokintsugi.com` / `admin123`
- User: `pilot1@ekokintsugi.com` / `pilot123`

## Production Environment Variables

Set these values in production:

- `SECRET_KEY`
- `DJANGO_DEBUG=false`
- `SQLITE_PATH=/var/data/db.sqlite3`
- `MEDIA_ROOT=/var/data/media`

Optional:

- `ALLOWED_HOSTS`
- `CSRF_TRUSTED_ORIGINS`

## Render Deployment

Use a standard Render Web Service.

### Service Configuration

- Environment: `Python 3`
- Build Command: `bash build.sh`
- Start Command: `gunicorn config.wsgi:application`

### Persistent Disk

Attach a persistent disk with:

- Mount Path: `/var/data`

### Environment Variables

Add:

- `SECRET_KEY`
- `DJANGO_DEBUG=false`
- `SQLITE_PATH=/var/data/db.sqlite3`
- `MEDIA_ROOT=/var/data/media`

### Deploy

After the first deploy, open the Render shell and run:

```bash
python manage.py seed_pilot
```

## Build Script

`build.sh` runs:

```bash
mkdir -p "$(dirname "${SQLITE_PATH:-db.sqlite3}")"
mkdir -p "${MEDIA_ROOT:-media}"
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
```

## Core Files

- `config/settings.py`
- `build.sh`
- `requirements.txt`
- `render.yaml`
- `pilot/`
- `templates/`
- `static/`
