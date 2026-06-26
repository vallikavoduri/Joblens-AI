"""Shared enums used by both ORM models and Pydantic schemas.

Keeping them in one place avoids drift between "what the DB stores" and "what the API accepts".
"""

from __future__ import annotations

from enum import Enum


class Source(str, Enum):
    """Where the job was found / applied through."""

    LINKEDIN = "linkedin"
    NAUKRI = "naukri"
    INDEED = "indeed"
    FOUNDIT = "foundit"
    INTERNSHALA = "internshala"
    HIRIST = "hirist"
    TELEGRAM = "telegram"
    COMPANY_SITE = "company_site"
    REFERRAL = "referral"
    OTHER = "other"


class Status(str, Enum):
    """Lifecycle of an application."""

    APPLIED = "applied"
    SCREENING = "screening"
    INTERVIEW = "interview"
    OFFER = "offer"
    REJECTED = "rejected"
    GHOSTED = "ghosted"          # no response within X days
    WITHDRAWN = "withdrawn"      # you backed out


class EmailClassification(str, Enum):
    """Output of the email classifier (Phase 2)."""

    UNCLASSIFIED = "unclassified"
    CONFIRMATION = "confirmation"  # "Thanks for applying"
    INTERVIEW = "interview"        # "Let's schedule a call"
    REJECTION = "rejection"        # "Unfortunately…"
    OFFER = "offer"                # "Pleased to extend an offer"
    IRRELEVANT = "irrelevant"      # not job-related at all
