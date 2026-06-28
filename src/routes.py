"""API routes for expense management (CRUD + filtering + summary)."""

from datetime import date as date_type
from pathlib import Path

from fastapi import APIRouter, Depends, Form, HTTPException, Query, Request
from fastapi.responses import JSONResponse, RedirectResponse, Response
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from src.database import get_db
from src.models import Expense
from src.schemas import ExpenseCreate, ExpenseResponse

router = APIRouter()

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


def _template_exists(name: str) -> bool:
    """Return True if the named template file is available on disk."""
    return (TEMPLATES_DIR / name).is_file()


def _parse_date(value: str | None) -> date_type | None:
    """Parse an ISO date string, raising a 400 on malformed input."""
    if value is None or value == "":
        return None
    try:
        return date_type.fromisoformat(value)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=f"Invalid date: {value}") from exc


@router.get("/add")
def add_form(request: Request) -> Response:
    """Render the add-expense form."""
    if _template_exists("add.html"):
        return templates.TemplateResponse(request, "add.html")
    return JSONResponse({"detail": "add form"})


@router.post("/add")
def add_expense(
    amount: float = Form(...),
    category: str = Form(...),
    description: str | None = Form(None),
    date: str | None = Form(None),
    db: Session = Depends(get_db),
) -> Response:
    """Create a new expense from submitted form data, then redirect to the list."""
    expense_date = _parse_date(date) or date_type.today()
    try:
        payload = ExpenseCreate(
            amount=amount,
            category=category.strip(),
            description=description,
            date=expense_date,
        )
    except ValidationError as exc:
        raise HTTPException(status_code=400, detail=exc.errors()) from exc

    expense = Expense(**payload.model_dump())
    db.add(expense)
    db.commit()
    return RedirectResponse(url="/", status_code=303)


@router.get("/")
def list_expenses(
    request: Request,
    category: str | None = Query(None),
    date_from: str | None = Query(None),
    date_to: str | None = Query(None),
    format: str | None = Query(None),
    db: Session = Depends(get_db),
) -> Response:
    """List expenses (newest first) with optional category/date-range filtering."""
    stmt = select(Expense)
    if category:
        stmt = stmt.where(Expense.category == category)
    parsed_from = _parse_date(date_from)
    if parsed_from is not None:
        stmt = stmt.where(Expense.date >= parsed_from)
    parsed_to = _parse_date(date_to)
    if parsed_to is not None:
        stmt = stmt.where(Expense.date <= parsed_to)
    stmt = stmt.order_by(Expense.date.desc(), Expense.id.desc())

    expenses = db.execute(stmt).scalars().all()

    if format != "json" and _template_exists("index.html"):
        return templates.TemplateResponse(
            request,
            "index.html",
            {
                "expenses": expenses,
                "filters": {
                    "category": category,
                    "date_from": date_from,
                    "date_to": date_to,
                },
            },
        )
    return JSONResponse(
        [ExpenseResponse.model_validate(e).model_dump(mode="json") for e in expenses]
    )


@router.post("/delete/{expense_id}")
def delete_expense(expense_id: int, db: Session = Depends(get_db)) -> Response:
    """Delete an expense by ID (idempotent), then redirect to the list."""
    expense = db.get(Expense, expense_id)
    if expense is not None:
        db.delete(expense)
        db.commit()
    return RedirectResponse(url="/", status_code=303)


@router.get("/summary")
def summary(
    request: Request,
    format: str | None = Query(None),
    db: Session = Depends(get_db),
) -> Response:
    """Return total spending grouped by category, plus an overall total."""
    stmt = (
        select(Expense.category, func.sum(Expense.amount))
        .group_by(Expense.category)
        .order_by(func.sum(Expense.amount).desc())
    )
    rows = db.execute(stmt).all()
    by_category = {category: float(total) for category, total in rows}
    total = float(sum(by_category.values()))

    if format != "json" and _template_exists("summary.html"):
        return templates.TemplateResponse(
            request,
            "summary.html",
            {"by_category": by_category, "total": total},
        )
    return JSONResponse({"by_category": by_category, "total": total})
