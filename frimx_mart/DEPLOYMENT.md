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

**Required:**
- `SECRET_KEY` - Generate new secret key
- `DEBUG=False`
- `ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com`

**PostgreSQL Database (Production):**
- `DATABASE_ENGINE=django.db.backends.postgresql`
- `DATABASE_NAME=your_database_name` (required)
- `DATABASE_USER=your_database_user` (required)
- `DATABASE_PASSWORD=your_database_password` (required)
- `DATABASE_HOST=localhost` (or your DB host, default: localhost)
- `DATABASE_PORT=5432` (default: 5432)
- `DATABASE_CONN_MAX_AGE=0` (optional, connection pooling, default: 0)
- `DATABASE_CONNECT_TIMEOUT=10` (optional, connection timeout in seconds, default: 10)

**Email Configuration:**
- `EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend`
- `EMAIL_HOST=smtp.gmail.com` (or your SMTP server)
- `EMAIL_PORT=587`
- `EMAIL_USE_TLS=True`
- `EMAIL_HOST_USER=your-email@gmail.com`
- `EMAIL_HOST_PASSWORD=your-email-password`
- `DEFAULT_FROM_EMAIL=noreply@openmart.com`
- `SITE_URL=https://yourdomain.com`

### Commands to Run:

```bash
# Install dependencies (includes psycopg2-binary for PostgreSQL)
pip install -r requirements.txt

# Run migrations (creates tables in PostgreSQL)
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Seed categories (optional)
python manage.py seed_categories

# Create superuser (optional)
python manage.py createsuperuser

# Run with Gunicorn
gunicorn frimx_mart.wsgi:application
```

### PostgreSQL Setup Notes:

1. **Install PostgreSQL** (if not already installed):
   ```bash
   # Ubuntu/Debian
   sudo apt-get install postgresql postgresql-contrib
   
   # macOS (with Homebrew)
   brew install postgresql
   ```

2. **Create Database and User**:
   ```bash
   # Connect to PostgreSQL
   sudo -u postgres psql
   
   # Create database
   CREATE DATABASE your_database_name;
   
   # Create user
   CREATE USER your_database_user WITH PASSWORD 'your_database_password';
   
   # Grant privileges
   GRANT ALL PRIVILEGES ON DATABASE your_database_name TO your_database_user;
   
   # Exit PostgreSQL
   \q
   ```

3. **Update .env file** with PostgreSQL credentials:
   ```env
   DATABASE_ENGINE=django.db.backends.postgresql
   DATABASE_NAME=your_database_name
   DATABASE_USER=your_database_user
   DATABASE_PASSWORD=your_database_password
   DATABASE_HOST=localhost
   DATABASE_PORT=5432
   ```

4. **Test Connection**:
   ```bash
   python manage.py check --database default
   python manage.py migrate
   ```

## Generate New Secret Key

For production, generate a new secret key:

```bash
python manage.py shell -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the output and add it to your `.env` file.
