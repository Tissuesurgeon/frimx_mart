# Installation Instructions for FrimxMart

## Fix for ModuleNotFoundError: No module named 'crispy_forms'

The error occurs because `django-crispy-forms` is not installed. Here are two solutions:

### Solution 1: Install the Required Packages (Recommended)

Run the following command in your terminal:

```bash
cd /home/frimx/Desktop/frimx_mart/frimx_mart
pip3 install django-crispy-forms==2.5 crispy-bootstrap5==2025.6
```

Or install all requirements:

```bash
cd /home/frimx/Desktop/frimx_mart/frimx_mart
pip3 install -r requirements.txt
```

### Solution 2: Use Virtual Environment (Best Practice)

1. Create a virtual environment:
```bash
cd /home/frimx/Desktop/frimx_mart
python3 -m venv venv
```

2. Activate the virtual environment:
```bash
source venv/bin/activate
```

3. Install dependencies:
```bash
cd frimx_mart
pip install -r requirements.txt
```

4. Run the project:
```bash
python manage.py runserver
```

### Solution 3: Remove crispy_forms Dependency (Temporary)

If you want to run the project without crispy_forms, you can temporarily comment it out in `settings.py`:

```python
INSTALLED_APPS = [
    # ... other apps ...
    # "crispy_forms",  # Commented out
    # "crispy_bootstrap5",  # Commented out
]
```

**Note:** The templates have been updated to work without crispy_forms, so the project should work even if you don't install it. However, installing it is recommended for better form styling.

## After Installation

Once the packages are installed, you can run:

```bash
cd /home/frimx/Desktop/frimx_mart/frimx_mart
python3 manage.py check
python3 manage.py migrate
python3 manage.py runserver
```

