# EkoKintsugi Pilot System

Django application for the EkoKintsugi Founding Circle pilot.

## Requirements

- Python 3.12+
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

## Render Deployment (Manual Setup)

This project is ready for a manual Render Web Service deployment. You do not need to use the Blueprint flow or import `render.yaml`.

### Before You Start

1. Push this repo to GitHub.
2. Make sure your default branch contains:
   - `build.sh`
   - `requirements.txt`
   - `manage.py`
   - `config/settings.py`

### Create the Render Service

1. Log in to Render.
2. Click `New +`.
3. Choose `Web Service`.
4. Connect your GitHub repo.
5. Pick the branch you want to deploy.

### Configure the Web Service

Use these values on the setup screen:

- Name: anything you want, for example `ekokintsugi-pilot`
- Region: choose the closest region to your users
- Runtime: `Python 3`
- Build Command: `bash build.sh`
- Start Command: `bash start.sh`

This repo includes `.python-version` so Render should use Python `3.13`. If Render still chooses a different version, add `PYTHON_VERSION=3.13.5` in the service environment.

### Add a Persistent Disk

Before deploying, add a disk:

- Disk Name: `ekokintsugi-data`
- Mount Path: `/var/data`
- Size: `1 GB` is enough to start

This matters because the app stores:

- SQLite database at `/var/data/db.sqlite3`
- Uploaded media at `/var/data/media`

### Add Environment Variables

In the Render service settings, add:

- `SECRET_KEY`
- `DJANGO_DEBUG` = `false`
- `SQLITE_PATH` = `/var/data/db.sqlite3`
- `MEDIA_ROOT` = `/var/data/media`

Optional if you use a custom domain or extra hostnames:

- `ALLOWED_HOSTS`
- `CSRF_TRUSTED_ORIGINS`

### First Deploy

1. Click `Create Web Service`.
2. Wait for the build to finish.
3. The build script will:
   - install dependencies
   - collect static files

4. When the service starts, it will:
   - create the SQLite and media folders on the mounted disk
   - run migrations
   - start Gunicorn

### Seed Demo Data

After the first deploy succeeds:

1. Open your service in Render.
2. Go to `Shell`.
3. Run:

```bash
python manage.py seed_pilot
```

### Open the App

1. Visit your Render service URL.
2. Log in with:
   - Admin: `admin@ekokintsugi.com` / `admin123`
   - User: `pilot1@ekokintsugi.com` / `pilot123`

### If Something Fails

- If Render still uses Python `3.14.x`, add `PYTHON_VERSION=3.13.5` and redeploy.
- If login or forms fail with host or CSRF errors on a custom domain, set:
  - `ALLOWED_HOSTS=your-domain.onrender.com,yourdomain.com`
  - `CSRF_TRUSTED_ORIGINS=https://your-domain.onrender.com,https://yourdomain.com`
- If data disappears after redeploy, the disk is missing or mounted to the wrong path.

## Build Script

`build.sh` runs:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py collectstatic --no-input
```

`start.sh` runs:

```bash
mkdir -p "$(dirname "${SQLITE_PATH:-db.sqlite3}")"
mkdir -p "${MEDIA_ROOT:-media}"
python manage.py migrate
gunicorn config.wsgi:application
```

## Core Files

- `config/settings.py`
- `build.sh`
- `start.sh`
- `requirements.txt`
- `.python-version`
- `pilot/`
- `templates/`
- `static/`
