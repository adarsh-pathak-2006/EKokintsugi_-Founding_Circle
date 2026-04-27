# Deploy This Django Project on Render

This project is now prepared for Render deployment.

Files already added for deployment:

- `requirements.txt`
- `build.sh`
- `config/settings.py` updated for:
  - `DATABASE_URL`
  - `SECRET_KEY`
  - Render host handling
  - WhiteNoise static files
  - PostgreSQL in production

## What You Need Before Starting

1. A GitHub account
2. A Render account
3. This project pushed to a GitHub repository

If this project is only on your laptop right now, run:

```powershell
git init
git add .
git commit -m "Prepare Django app for Render deployment"
```

Then create a new GitHub repo and push:

```powershell
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPO.git
git branch -M main
git push -u origin main
```

## Local Check Before Deploying

From the project folder:

```powershell
python manage.py check
python manage.py runserver
```

Open `http://127.0.0.1:8000/` and confirm the app works locally.

## Step 1: Create a PostgreSQL Database on Render

1. Log in to Render.
2. Click `New +`.
3. Choose `PostgreSQL`.
4. Give it a name like `ekokintsugi-db`.
5. Create the database.
6. After it is created, open the database details page.
7. Copy the `Internal Database URL`.

You will use that as `DATABASE_URL` in the web service.

## Step 2: Create the Django Web Service on Render

1. In Render, click `New +`.
2. Choose `Web Service`.
3. Connect your GitHub repository.
4. Select the repo for this project.
5. Choose the branch you want to deploy, usually `main`.
6. Set the following values:

- `Language`: `Python 3`
- `Build Command`: `bash build.sh`
- `Start Command`: `python -m gunicorn config.asgi:application -k uvicorn.workers.UvicornWorker`

## Step 3: Add Environment Variables

In the Render web service settings, add these environment variables:

- `DATABASE_URL` = paste the Internal Database URL from your Render Postgres instance
- `SECRET_KEY` = click `Generate` in Render or paste a strong random secret
- `WEB_CONCURRENCY` = `4`
- `DEBUG` = `false`

Optional:

- `ALLOWED_HOSTS` = comma-separated extra domains if you later add a custom domain
- `CSRF_TRUSTED_ORIGINS` = comma-separated full origins like `https://yourdomain.com`

Important:

- Render automatically provides `RENDER_EXTERNAL_HOSTNAME`
- this project already reads that value in `config/settings.py`
- because of that, the default Render `.onrender.com` domain should work without extra code changes

## Step 4: Deploy

After saving the web service:

1. Render will start the build
2. `build.sh` will run:

```bash
set -o errexit
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
```

3. When the deploy finishes, open your Render service URL

If the build fails, open the Render logs and check the exact error.

## Step 5: Seed the Demo Data

This project includes a seed command for:

- 1 admin account
- 10 pilot users
- shoes
- trees
- points
- sample reviews
- a sample return request

After the first successful deploy:

1. Open your Render web service
2. Open `Shell`
3. Run:

```bash
python manage.py seed_pilot
```

## Step 6: Login Credentials

After running the seed command:

- Admin: `admin@ekokintsugi.com` / `admin123`
- User: `pilot1@ekokintsugi.com` / `pilot123`

## Step 7: Future Updates

Whenever you push new code to GitHub:

```powershell
git add .
git commit -m "Update app"
git push
```

Render will automatically redeploy if auto-deploy is enabled.

## Uploaded Images / Media Files

This app allows weekly review image uploads.

Important for Render:

- static files are handled by WhiteNoise and are fine
- uploaded media files are different from static files
- if you store uploads only on the web service filesystem, they can be lost on redeploy or restart

For production-safe media handling, use one of these:

1. Attach a persistent disk on Render and point `MEDIA_ROOT` there
2. Store uploads in external object storage like AWS S3 or Cloudinary

If you skip this, image uploads may not persist reliably.

## If You Want a Custom Domain

After adding a custom domain in Render:

1. keep the domain attached to the Render service
2. set:

- `ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com`
- `CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com`

Then redeploy.

## Common Problems

### 1. `DisallowedHost`

Cause:
- custom domain not added to `ALLOWED_HOSTS`

Fix:
- set the `ALLOWED_HOSTS` environment variable in Render

### 2. Static files not loading

Cause:
- `collectstatic` did not run or build failed

Fix:
- confirm the build command is `bash build.sh`
- confirm `whitenoise` is in `requirements.txt`

### 3. Database connection error

Cause:
- wrong `DATABASE_URL`

Fix:
- use the `Internal Database URL` from the Render PostgreSQL service

### 4. Forms fail with CSRF errors on custom domain

Cause:
- missing trusted origin

Fix:
- set `CSRF_TRUSTED_ORIGINS` in Render

### 5. Images disappear later

Cause:
- media files stored only on ephemeral disk

Fix:
- use a persistent disk or external storage

## Exact Commands Used by This Project

### Start command

```bash
python -m gunicorn config.asgi:application -k uvicorn.workers.UvicornWorker
```

### Build command

```bash
bash build.sh
```

## Files to Make Sure You Commit

- `build.sh`
- `requirements.txt`
- `manage.py`
- `config/`
- `pilot/`
- `templates/`
- `static/`

Do not rely on `db.sqlite3` for production on Render. Production should use Render PostgreSQL.

## Official References

- Render Django deployment docs: https://render.com/docs/deploy-django
- Render web services docs: https://render.com/docs/web-services

These instructions were written to match this repo's current Django setup and Render's official Django deployment guidance.
