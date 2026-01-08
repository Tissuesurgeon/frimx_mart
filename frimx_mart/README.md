# OpenMart - Social Marketplace

A modern social marketplace platform built with Django where users can buy, sell, and connect with their local community.

## Features

- User authentication and profiles
- Product listings with images
- Category-based browsing
- Real-time chat messaging
- Reviews and ratings
- Saved listings
- Admin dashboard
- User dashboard
- Report system

## Installation

### Prerequisites

- Python 3.10+
- pip
- virtualenv (recommended)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd frimx_mart/frimx_mart
   ```

2. **Create and activate virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env file with your configuration
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Seed categories (optional)**
   ```bash
   python manage.py seed_categories
   ```

7. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

8. **Run development server**
   ```bash
   python manage.py runserver
   ```

## Environment Variables

Create a `.env` file in the project root with the following variables:

- `SECRET_KEY` - Django secret key (generate a new one for production)
- `DEBUG` - Set to `False` in production
- `ALLOWED_HOSTS` - Comma-separated list of allowed hosts
- `DATABASE_ENGINE` - Database backend (sqlite3 for dev, postgresql for production)
- `EMAIL_BACKEND` - Email backend configuration
- `SITE_URL` - Your site URL for email links

See `.env.example` for a complete template.

## Production Deployment

1. Set `DEBUG=False` in `.env`
2. Generate a new `SECRET_KEY`
3. Configure production database (PostgreSQL recommended)
4. Set up proper email backend
5. Configure `ALLOWED_HOSTS` with your domain
6. Set `SECURE_SSL_REDIRECT=True` if using HTTPS
7. Collect static files: `python manage.py collectstatic`
8. Use a production WSGI server (Gunicorn, uWSGI)

## Project Structure

```
frimx_mart/
├── accounts/          # User authentication and profiles
├── listings/          # Product listings and categories
├── chat/             # Messaging system
├── reports/          # Reporting system
├── dashboard/        # User and admin dashboards
├── templates/        # HTML templates
├── static/           # Static files (CSS, JS, images)
├── media/            # User-uploaded media files
└── frimx_mart/       # Project settings
```

## License

Copyright © 2026 OpenMart. All rights reserved.
