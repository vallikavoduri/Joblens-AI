"""Pytest fixtures — gives every test a fresh, isolated SQLite database.

Why a separate test DB:
- Tests should never read/write your real `joblens.db` or you'd pollute your dashboard.
- An in-memory SQLite is fast and disappears at the end of the test session.
"""

from __future__ import annotations

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db import Base, get_db
from app.main import app

# Single shared in-memory DB across one test, but recreated per test
TEST_DB_URL = "sqlite:///:memory:"


@pytest.fixture()
def db_session() -> Generator:
    engine = create_engine(
        TEST_DB_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,  # keep the same connection (and the same in-memory DB) for all calls
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)
    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client(db_session) -> Generator[TestClient, None, None]:
    def _get_db_override():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_db_override
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
