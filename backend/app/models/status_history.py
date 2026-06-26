"""StatusHistory — audit trail of every status change on an Application.

Why this exists:
1. The dashboard "funnel" needs to know when each application *first* entered each stage.
2. When the email classifier auto-changes a status (Phase 2), we want to know which event drove it.
3. Lets us answer "how long does the average application stay in Screening before Interview?"
"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum as SqlEnum, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base
from app.schemas.common import Status

if TYPE_CHECKING:
    from app.models.application import Application


class StatusHistory(Base):
    __tablename__ = "status_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    application_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("applications.id", ondelete="CASCADE"), nullable=False, index=True
    )

    old_status: Mapped[Status | None] = mapped_column(
        SqlEnum(Status, native_enum=False, length=32), nullable=True
    )
    new_status: Mapped[Status] = mapped_column(
        SqlEnum(Status, native_enum=False, length=32), nullable=False
    )

    # Where did this change come from?
    source: Mapped[str] = mapped_column(String(50), nullable=False, default="manual")
    note: Mapped[str | None] = mapped_column(Text, nullable=True)

    changed_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False, index=True)

    application: Mapped[Application] = relationship("Application", back_populates="status_history")
