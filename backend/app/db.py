"""SQLAlchemy database setup.

Loads DATABASE_URL from env (defaults to local SQLite). Exposes:

- `engine` — connection pool
- `SessionLocal` — factory for short-lived DB sessions per request
- `Base` — base class every ORM model inherits from
- `get_db` — FastAPI dependency that yields a session and closes it
"""

from __future__ import annotations

import os
from collections.abc import Generator

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./joblens.db")

# SQLite + threaded FastAPI: must disable single-thread check.
# Other DBs (Postgres) don't need this.
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args, echo=False, future=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    """All ORM models inherit from this."""


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency. Use as `db: Session = Depends(get_db)`."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
