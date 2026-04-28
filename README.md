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

For production on Render, set these values:

- `SECRET_KEY`
- `DJANGO_DEBUG=false`
- `DATABASE_URL`
- `PYTHON_VERSION=3.13.5`

Optional:

- `ALLOWED_HOSTS`
- `CSRF_TRUSTED_ORIGINS`

## Render Deployment

Use the simple Render setup:

- 1 Render `PostgreSQL` database
- 1 Render `Web Service`
- no `render.yaml`
- no persistent disk

### Build and Start Commands

Use these values in the Render dashboard:

- Build Command:

```bash
bash build.sh
```

- Start Command:

```bash
python manage.py migrate && gunicorn config.wsgi:application
```

### Environment Variables

Add these in Render:

- `SECRET_KEY`
- `DJANGO_DEBUG=false`
- `DATABASE_URL=<your Render Postgres internal URL>`
- `PYTHON_VERSION=3.13.5`

### First Deploy

After your web service deploys successfully, open the Render shell and run:

```bash
python manage.py seed_pilot
```

## Core Files

- `config/settings.py`
- `build.sh`
- `requirements.txt`
- `pilot/`
- `templates/`
- `static/`
