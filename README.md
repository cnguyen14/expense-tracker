# Expense Tracker

A simple web-based expense tracking app built with FastAPI, SQLite, and Jinja2 templates. Single-user, no authentication.

## Features

- **Add expenses** with amount, category, description, and date
- **Filter expenses** by category and date range
- **Summary by category** showing totals per spending category

## Tech Stack

- **Python 3.11** + **FastAPI** — web framework and API
- **SQLAlchemy 2.0** + **SQLite** — ORM and database
- **Jinja2** — server-rendered HTML templates
- **Docker** + Docker Compose — containerized deployment
- **pytest** + **httpx** — testing

## Quick Start

### With pip

```bash
# Install dependencies
pip install -r requirements.txt

# Run the dev server
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Then open http://localhost:8000 in your browser.

### With Docker

```bash
docker compose up --build
```

The app will be available at http://localhost:8000.

## Running Tests

```bash
pytest -v
```

## Project Structure

```
expense-tracker/
├── src/
│   ├── __init__.py
│   ├── main.py          # FastAPI app + routes
│   ├── config.py        # Settings
│   ├── database.py      # SQLAlchemy engine
│   ├── models.py        # Expense model
│   ├── schemas.py       # Pydantic schemas
│   └── routes.py        # API endpoints
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── add.html
│   └── summary.html
├── static/
│   └── style.css
├── tests/
│   ├── conftest.py
│   ├── test_models.py
│   └── test_routes.py
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## License

This project is licensed under the [MIT License](LICENSE).
