"""JobLens FastAPI entrypoint.

Run locally with:
    uvicorn app.main:app --reload

API docs auto-served at /docs (Swagger UI) and /redoc.
"""

from __future__ import annotations

import os
from contextlib import asynccontextmanager
from datetime import datetime, timezone

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Importing app.models registers ORM models against Base.metadata
from app import models  # noqa: F401
from app.db import Base, engine
from app.routes import applications as applications_routes
from app.routes import dashboard as dashboard_routes

load_dotenv()

APP_NAME = os.getenv("APP_NAME", "JobLens")
APP_ENV = os.getenv("APP_ENV", "development")
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Run once when the server starts.

    Phase 1: create SQLite tables if they don't exist. In production we'd use Alembic
    migrations instead — but for dev with a single-file SQLite, this is fine and zero-config.
    """
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=APP_NAME,
    description="AI-powered job application tracker.",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(applications_routes.router)
app.include_router(dashboard_routes.router)


class HealthResponse(BaseModel):
    status: str
    app: str
    env: str
    server_time_utc: str


@app.get("/health", response_model=HealthResponse, tags=["meta"])
def health() -> HealthResponse:
    """Liveness probe. Frontend pings this to confirm backend is reachable."""
    return HealthResponse(
        status="ok",
        app=APP_NAME,
        env=APP_ENV,
        server_time_utc=datetime.now(timezone.utc).isoformat(),
    )


@app.get("/", tags=["meta"])
def root() -> dict[str, str]:
    return {
        "message": f"Welcome to {APP_NAME} API.",
        "docs": "/docs",
        "health": "/health",
    }
