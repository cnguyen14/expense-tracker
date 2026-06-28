# Expense Tracker — Project Context

## Overview
A simple web-based expense tracking app built with FastAPI + SQLite + Jinja2 templates. Single-user, no authentication. Supports adding expenses, filtering by category and date, and viewing a summary of spending by category.

## Tech Stack
- Python 3.11, FastAPI, SQLAlchemy 2.0, SQLite
- Jinja2 templates, plain CSS
- pytest + httpx for testing
- Docker + Docker Compose

## Key Commands
```bash
# Install dependencies
pip install -r requirements.txt

# Run dev server
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Run tests
pytest -v

# Docker
docker compose up --build
```

## File Structure
```
src/
├── __init__.py
├── main.py          # FastAPI app + routes
├── config.py        # Settings
├── database.py      # SQLAlchemy engine
├── models.py        # Expense model
├── schemas.py       # Pydantic schemas
└── routes.py        # API endpoints
templates/
├── base.html
├── index.html
├── add.html
└── summary.html
static/
└── style.css
tests/
├── conftest.py
├── test_models.py
└── test_routes.py
```

## Code Standards
- Python: PEP 8, type hints on all functions
- SQLAlchemy 2.0 style (mapped_column, declarative_base)
- Pydantic v2 style (model_validate, model_dump)
- Test file naming: test_*.py
- Commit messages: feat(scope): description (fixes #N)

## Database
- SQLite file: expenses.db (gitignored)
- Single table: `expenses`

| Column      | Type     | Notes                                  |
|-------------|----------|----------------------------------------|
| id          | Integer  | primary key                            |
| amount      | Float    | not null                               |
| category    | String   | not null                               |
| description | String   | nullable                               |
| date        | Date     | not null, defaults to today            |
| created_at  | DateTime | not null, timezone-aware UTC timestamp |

- Categories: food, transport, shopping, entertainment, utilities, other

## IMPORTANT
- Default git branch is `master` (not `main`)
- Always push to `origin master`
- Run tests before committing
- Use `pytest` not `python -m pytest`
