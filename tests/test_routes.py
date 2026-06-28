"""Tests for the expense CRUD API routes."""

from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models import Expense


def test_create_expense(client: TestClient, db_session: Session) -> None:
    response = client.post(
        "/add",
        data={
            "amount": "42.50",
            "category": "food",
            "description": "Dinner",
            "date": "2026-06-15",
        },
    )
    assert response.status_code == 200  # redirect followed to GET /

    expenses = db_session.execute(select(Expense)).scalars().all()
    assert len(expenses) == 1
    assert expenses[0].amount == 42.50
    assert expenses[0].category == "food"
    assert expenses[0].description == "Dinner"


def test_create_expense_rejects_invalid_amount(client: TestClient) -> None:
    response = client.post(
        "/add",
        data={"amount": "-5", "category": "food", "date": "2026-06-15"},
    )
    assert response.status_code == 400


def test_list_expenses(client: TestClient, sample_expenses: list[Expense]) -> None:
    response = client.get("/?format=json")
    assert response.status_code == 200
    body = response.json()
    assert len(body) == len(sample_expenses)
    # Ordered by date DESC -> newest (shopping, 2026-06-20) first.
    assert body[0]["category"] == "shopping"


def test_filter_by_category(
    client: TestClient, sample_expenses: list[Expense]
) -> None:
    response = client.get("/?category=food&format=json")
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 2
    assert all(item["category"] == "food" for item in body)


def test_filter_by_date_range(
    client: TestClient, sample_expenses: list[Expense]
) -> None:
    response = client.get(
        "/?date_from=2026-06-04&date_to=2026-06-15&format=json"
    )
    assert response.status_code == 200
    body = response.json()
    # transport (06-05) and food (06-10) fall in range.
    assert len(body) == 2
    categories = {item["category"] for item in body}
    assert categories == {"transport", "food"}


def test_delete_expense(
    client: TestClient, db_session: Session, sample_expenses: list[Expense]
) -> None:
    target = sample_expenses[0]
    response = client.post(f"/delete/{target.id}")
    assert response.status_code == 200  # redirect followed to GET /

    remaining = db_session.execute(select(Expense)).scalars().all()
    assert len(remaining) == len(sample_expenses) - 1
    assert all(e.id != target.id for e in remaining)


def test_summary(client: TestClient, sample_expenses: list[Expense]) -> None:
    response = client.get("/summary?format=json")
    assert response.status_code == 200
    body = response.json()
    assert body["by_category"]["food"] == 25.0
    assert body["by_category"]["transport"] == 20.0
    assert body["by_category"]["shopping"] == 30.0
    assert body["total"] == 75.0
