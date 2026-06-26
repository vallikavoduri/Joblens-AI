"""Application ORM model — the core entity in JobLens.

One row = one job you applied to.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import TYPE_CHECKING

from sqlalchemy import Date, DateTime, Enum as SqlEnum, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base
from app.schemas.common import Source, Status

if TYPE_CHECKING:
    from app.models.email import Email
    from app.models.status_history import StatusHistory


class Application(Base):
    __tablename__ = "applications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # Required
    company: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    role: Mapped[str] = mapped_column(String(200), nullable=False)
    source: Mapped[Source] = mapped_column(
        SqlEnum(Source, native_enum=False, length=32), nullable=False, default=Source.OTHER
    )
    applied_date: Mapped[date] = mapped_column(Date, nullable=False, default=date.today, index=True)
    status: Mapped[Status] = mapped_column(
        SqlEnum(Status, native_enum=False, length=32), nullable=False, default=Status.APPLIED, index=True
    )

    # Optional
    link: Mapped[str | None] = mapped_column(String(500), nullable=True)
    location: Mapped[str | None] = mapped_column(String(200), nullable=True)
    salary_range: Mapped[str | None] = mapped_column(String(100), nullable=True)
    job_description: Mapped[str | None] = mapped_column(Text, nullable=True)  # used in Phase 3
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    # ML-derived (Phase 3)
    match_score: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Timestamps (DB-managed)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # Relationships
    emails: Mapped[list[Email]] = relationship(
        "Email", back_populates="application", cascade="all, delete-orphan"
    )
    status_history: Mapped[list[StatusHistory]] = relationship(
        "StatusHistory", back_populates="application", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Application id={self.id} {self.company!r} {self.role!r} {self.status.value}>"
