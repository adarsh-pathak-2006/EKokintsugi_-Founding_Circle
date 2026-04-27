# Deploy This Django Project on Render

This project is now set up for Render using:

- Django web service
- SQLite database on a Render persistent disk
- WhiteNoise for static files
- Gunicorn for the app server

The key deployment files already exist:

- `render.yaml`
- `build.sh`
- `requirements.txt`
- `config/settings.py`

## What This Setup Does

Instead of using a separate Postgres database, this setup uses:

- `db.sqlite3` stored on a Render persistent disk
- uploaded media stored on that same disk
- static files served by WhiteNoise

That is a good fit for this project because it is a small pilot system, not a high-scale app.

## Important Tradeoff

SQLite on Render is fine for this pilot, but keep in mind:

- the app should stay on a single web instance
- attached persistent disks are not for horizontal scaling
- this is good for demo / pilot / low traffic
- for future scale, Postgres is the better long-term option

## Step 1: Push This Project to GitHub

From this folder:

```powershell
git init
git add .
git commit -m "Prepare Render deployment"
```

Then connect it to GitHub:

```powershell
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPO.git
git branch -M main
git push -u origin main
```

## Step 2: Create the Render Service

1. Log in to Render
2. Click `New +`
3. Choose `Blueprint`
4. Connect your GitHub repository
5. Select this repo
6. Render will detect `render.yaml`
7. Create the service

Render will automatically create:

- one Python web service
- one persistent disk mounted at `/var/data`

## Step 3: What Render Will Run

Render will use:

### Build command

```bash
bash build.sh
```

### Start command

```bash
gunicorn config.wsgi:application
```

## Step 4: Environment Variables Already Defined in `render.yaml`

These are already configured:

- `SECRET_KEY` generated automatically
- `DJANGO_DEBUG=false`
- `SQLITE_PATH=/var/data/db.sqlite3`
- `MEDIA_ROOT=/var/data/media`

Because of that:

- the SQLite database will live on the persistent disk
- uploaded files will also persist

## Step 5: First Deploy

During the first deploy, Render will run:

```bash
mkdir -p "$(dirname "${SQLITE_PATH:-db.sqlite3}")"
mkdir -p "${MEDIA_ROOT:-media}"
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
```

That means the service will:

- create the SQLite location
- create the media folder
- install dependencies
- collect static files
- run migrations

## Step 6: Seed the Demo Data

After the first successful deploy:

1. Open the Render service
2. Open `Shell`
3. Run:

```bash
python manage.py seed_pilot
```

That creates:

- 1 admin user
- 10 demo pilot users
- shoes
- trees
- points
- reviews
- sample return request

## Step 7: Login Credentials

After seeding:

- Admin: `admin@ekokintsugi.com` / `admin123`
- User: `pilot1@ekokintsugi.com` / `pilot123`

## Step 8: Redeploying Later

Whenever you push code to GitHub:

```powershell
git add .
git commit -m "Update app"
git push
```

Render will auto-deploy again.

Your SQLite database and uploaded files will remain safe because they live on the persistent disk, not in the temporary deploy filesystem.

## How This Project Detects Render

The Render-specific behavior is already built into `config/settings.py`:

- uses `RENDER_EXTERNAL_HOSTNAME` for allowed hosts
- uses `SQLITE_PATH` for the database file
- uses `MEDIA_ROOT` for uploaded files
- turns debug off on Render
- uses WhiteNoise for static files

## If You Need Manual Render Setup Instead of Blueprint

If you do not want to use `render.yaml`, create a normal Render web service and use:

- Build Command: `bash build.sh`
- Start Command: `gunicorn config.wsgi:application`

Add these environment variables manually:

- `SECRET_KEY` = any strong secret
- `DJANGO_DEBUG` = `false`
- `SQLITE_PATH` = `/var/data/db.sqlite3`
- `MEDIA_ROOT` = `/var/data/media`

Then attach a persistent disk:

- Mount path: `/var/data`
- Size: `1 GB` or more

## Common Problems

### Static files not loading

Check:

- `collectstatic` ran successfully in build logs
- `whitenoise` exists in `requirements.txt`

### `DisallowedHost`

This project already supports Render hostnames automatically.

If you add a custom domain later, set:

- `ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com`
- `CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com`

### Data disappears after redeploy

Cause:

- no persistent disk attached

Fix:

- attach the Render disk
- confirm `SQLITE_PATH` points inside `/var/data`
- confirm `MEDIA_ROOT` points inside `/var/data`

## Files You Should Commit

- `render.yaml`
- `build.sh`
- `requirements.txt`
- `manage.py`
- `config/`
- `pilot/`
- `templates/`
- `static/`

## Final Note

This app is now deployment-ready for Render using SQLite on a persistent disk.

If you want, I can do one more final polish pass and add:

1. a `.gitignore`
2. a `runtime.txt`
3. a custom 500 / 404 page

Those are optional, but they make the deployment feel more complete.
