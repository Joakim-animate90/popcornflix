# Popcornflix

A Django web application for movie streaming platform.

## Version 1.0.0

### Features
- ✅ Django 5.2.4 project setup
- ✅ PostgreSQL database configuration
- ✅ Environment variables for secure configuration
- ✅ Pre-commit hooks for code quality
- ✅ Linting with Black, isort, and flake8
- ✅ Git flow workflow

## Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Joakim-animate90/popcornflix.git
   cd popcornflix
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

5. **Set up pre-commit hooks**
   ```bash
   pip install -r requirements-dev.txt
   pre-commit install
   ```

6. **Run migrations**
   ```bash
   python manage.py migrate
   ```

7. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

8. **Run the development server**
   ```bash
   python manage.py runserver
   ```

## Environment Variables

Required environment variables (see `.env.example`):

- `DB_ENGINE` - Database backend
- `DB_NAME` - Database name
- `DB_USER` - Database username
- `DB_PASSWORD` - Database password
- `DB_HOST` - Database host
- `DB_PORT` - Database port
- `SECRET_KEY` - Django secret key
- `DEBUG` - Debug mode (True/False)
- `ALLOWED_HOSTS` - Comma-separated allowed hosts

## Development

This project uses:
- **Git Flow** for branching strategy
- **Pre-commit hooks** for code quality
- **Black** for code formatting
- **isort** for import sorting
- **flake8** for linting

## License

[Add your license here]
# Test commit to trigger workflows
