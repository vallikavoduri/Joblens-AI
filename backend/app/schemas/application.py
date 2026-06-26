"""Pydantic schemas — the shapes of data flowing in/out of the API.

Three layers per resource:
- `*Create` — payload for `POST` (no id, no timestamps)
- `*Update` — payload for `PATCH` (everything optional)
- `*Out`    — server response (id, timestamps included)
"""

from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field, HttpUrl

from app.schemas.common import Source, Status


class ApplicationBase(BaseModel):
    company: str = Field(..., min_length=1, max_length=200)
    role: str = Field(..., min_length=1, max_length=200)
    source: Source = Source.OTHER
    applied_date: date = Field(default_factory=date.today)
    status: Status = Status.APPLIED
    link: HttpUrl | None = None
    location: str | None = Field(None, max_length=200)
    salary_range: str | None = Field(None, max_length=100)
    job_description: str | None = None
    notes: str | None = None


class ApplicationCreate(ApplicationBase):
    """Payload for `POST /applications`."""


class ApplicationUpdate(BaseModel):
    """Payload for `PATCH /applications/{id}`. Every field optional."""

    company: str | None = Field(None, min_length=1, max_length=200)
    role: str | None = Field(None, min_length=1, max_length=200)
    source: Source | None = None
    applied_date: date | None = None
    status: Status | None = None
    link: HttpUrl | None = None
    location: str | None = Field(None, max_length=200)
    salary_range: str | None = Field(None, max_length=100)
    job_description: str | None = None
    notes: str | None = None


class ApplicationOut(ApplicationBase):
    id: int
    match_score: float | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ApplicationListOut(BaseModel):
    items: list[ApplicationOut]
    total: int
    limit: int
    offset: int


class StatusHistoryOut(BaseModel):
    id: int
    old_status: Status | None
    new_status: Status
    source: str
    note: str | None = None
    changed_at: datetime

    model_config = ConfigDict(from_attributes=True)
