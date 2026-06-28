"""Shared pytest fixtures: in-memory test database and HTTP client."""

from collections.abc import Iterator
from datetime import date

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from src.database import Base, get_db
from src.main import app
from src.models import Expense

# A single shared in-memory SQLite connection for the whole test session.
test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=test_engine
)


@pytest.fixture
def db_session() -> Iterator[Session]:
    """Provide a clean database and session for each test."""
    Base.metadata.create_all(bind=test_engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def client(db_session: Session) -> Iterator[TestClient]:
    """TestClient with get_db overridden to use the test session."""

    def override_get_db() -> Iterator[Session]:
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def sample_expenses(db_session: Session) -> list[Expense]:
    """Insert a known set of expenses spanning categories and dates."""
    expenses = [
        Expense(amount=10.0, category="food", description="Groceries",
                date=date(2026, 6, 1)),
        Expense(amount=20.0, category="transport", description="Bus pass",
                date=date(2026, 6, 5)),
        Expense(amount=15.0, category="food", description="Lunch",
                date=date(2026, 6, 10)),
        Expense(amount=30.0, category="shopping", description="Shoes",
                date=date(2026, 6, 20)),
    ]
    db_session.add_all(expenses)
    db_session.commit()
    for expense in expenses:
        db_session.refresh(expense)
    return expenses
