"""Email ORM model — recruiter emails ingested from Gmail (Phase 2)."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum as SqlEnum, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base
from app.schemas.common import EmailClassification

if TYPE_CHECKING:
    from app.models.application import Application


class Email(Base):
    __tablename__ = "emails"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # If linked to a known application; null while we haven't matched it yet
    application_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("applications.id", ondelete="SET NULL"), nullable=True, index=True
    )

    # Gmail metadata
    gmail_message_id: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    thread_id: Mapped[str | None] = mapped_column(String(100), nullable=True)

    # Content
    subject: Mapped[str] = mapped_column(String(500), nullable=False)
    sender: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    snippet: Mapped[str | None] = mapped_column(Text, nullable=True)
    received_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)

    # ML output (Phase 2)
    classification: Mapped[EmailClassification] = mapped_column(
        SqlEnum(EmailClassification, native_enum=False, length=32),
        nullable=False,
        default=EmailClassification.UNCLASSIFIED,
        index=True,
    )
    classification_confidence: Mapped[float | None] = mapped_column(Float, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    application: Mapped[Application | None] = relationship("Application", back_populates="emails")

    def __repr__(self) -> str:
        return f"<Email id={self.id} from={self.sender!r} class={self.classification.value}>"
