"""Pydantic schemas for request/response validation."""

from datetime import date as date_type
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ExpenseCreate(BaseModel):
    """Schema for creating an expense."""

    amount: float = Field(..., gt=0)
    category: str = Field(..., min_length=1)
    description: str | None = None
    date: date_type = Field(default_factory=date_type.today)


class ExpenseResponse(BaseModel):
    """Schema for returning an expense."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    amount: float
    category: str
    description: str | None
    date: date_type
    created_at: datetime
