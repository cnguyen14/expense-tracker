"""Tests for the Expense model."""

from datetime import date

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.database import Base
from src.models import Expense


def test_expense_model_create() -> None:
    """An Expense can be persisted and its fields read back correctly."""
    engine = create_engine(
        "sqlite:///:memory:", connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(engine)
    TestingSession = sessionmaker(bind=engine)

    with TestingSession() as session:
        expense = Expense(
            amount=12.50,
            category="food",
            description="Lunch",
            date=date(2026, 6, 28),
        )
        session.add(expense)
        session.commit()
        session.refresh(expense)

        assert expense.id is not None
        assert expense.amount == 12.50
        assert expense.category == "food"
        assert expense.description == "Lunch"
        assert expense.date == date(2026, 6, 28)
        assert expense.created_at is not None
