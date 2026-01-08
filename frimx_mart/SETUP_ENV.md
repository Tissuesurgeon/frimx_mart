# Environment Setup Guide

## Quick Start

1. **Copy the example environment file:**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` file** with your actual values:
   - Generate a new `SECRET_KEY` for production
   - Set `DEBUG=False` for production
   - Configure your database settings
   - Set up email configuration

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Seed categories (optional):**
   ```bash
   python manage.py seed_categories
   ```

## Generate Secret Key

For production, generate a secure secret key:

```bash
python manage.py shell -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the output and update `SECRET_KEY` in your `.env` file.

## Environment Variables Explained

### Required Variables

- **SECRET_KEY**: Django secret key (MUST be unique and secret in production)
- **DEBUG**: Set to `False` in production
- **ALLOWED_HOSTS**: Comma-separated list of allowed domains

### Database Variables

For SQLite (Development):
- `DATABASE_ENGINE=django.db.backends.sqlite3`
- `DATABASE_NAME=db.sqlite3`

For PostgreSQL (Production):
- `DATABASE_ENGINE=django.db.backends.postgresql`
- `DATABASE_NAME=your_database_name`
- `DATABASE_USER=your_database_user`
- `DATABASE_PASSWORD=your_database_password`
- `DATABASE_HOST=localhost` (or your DB host)
- `DATABASE_PORT=5432`

### Email Variables

For Development (Console):
- `EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend`

For Production (SMTP):
- `EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend`
- `EMAIL_HOST=smtp.gmail.com` (or your SMTP server)
- `EMAIL_PORT=587`
- `EMAIL_USE_TLS=True`
- `EMAIL_HOST_USER=your-email@gmail.com`
- `EMAIL_HOST_PASSWORD=your-email-password`

### Security Variables (Production)

- `SECURE_SSL_REDIRECT=True` (if using HTTPS)
- `SESSION_COOKIE_SECURE=True` (if using HTTPS)
- `CSRF_COOKIE_SECURE=True` (if using HTTPS)

## Important Notes

⚠️ **NEVER commit `.env` file to Git!**

✅ **DO commit `.env.example`** as a template for other developers.

The `.gitignore` file is configured to ignore `.env` but allow `.env.example`.
