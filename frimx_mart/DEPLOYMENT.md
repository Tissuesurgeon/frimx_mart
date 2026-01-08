# Deployment Guide for OpenMart

## Pre-Deployment Checklist

Before pushing to GitHub and deploying to production:

### 1. Environment Variables Setup

✅ **Create `.env` file** (already created, but update for production):
- Copy `.env.example` to `.env`
- Update `SECRET_KEY` with a new secure key (use `python manage.py shell -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
- Set `DEBUG=False` for production
- Update `ALLOWED_HOSTS` with your domain
- Configure production database settings
- Set up email backend for production

### 2. Security Settings

For production, update these in `.env`:
```
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

### 3. Database Migration

```bash
python manage.py migrate
```

### 4. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### 5. Create Superuser

```bash
python manage.py createsuperuser
```

### 6. Seed Categories (Optional)

```bash
python manage.py seed_categories
```

## GitHub Deployment

### Before Pushing:

1. ✅ Verify `.gitignore` includes:
   - `.env` file
   - `db.sqlite3`
   - `__pycache__/`
   - `media/` and `staticfiles/`
   - Virtual environment folders

2. ✅ Ensure `.env.example` is committed (template for others)

3. ✅ Verify no sensitive data in code:
   - No hardcoded SECRET_KEY
   - No hardcoded passwords
   - No API keys in code

### Push to GitHub:

```bash
git init
git add .
git commit -m "Initial commit: OpenMart marketplace"
git branch -M main
git remote add origin <your-repo-url>
git push -u origin main
```

## Production Deployment (Example: Render, Heroku, etc.)

### Environment Variables to Set:

- `SECRET_KEY` - Generate new secret key
- `DEBUG=False`
- `ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com`
- `DATABASE_ENGINE=django.db.backends.postgresql`
- `DATABASE_NAME`, `DATABASE_USER`, `DATABASE_PASSWORD`, `DATABASE_HOST`, `DATABASE_PORT`
- `EMAIL_BACKEND`, `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`
- `SITE_URL=https://yourdomain.com`

### Commands to Run:

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py seed_categories  # Optional
gunicorn frimx_mart.wsgi:application
```

## Generate New Secret Key

For production, generate a new secret key:

```bash
python manage.py shell -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the output and add it to your `.env` file.
