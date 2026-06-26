"""Dashboard aggregations — powers the KPI cards + charts.

All computed on-the-fly with SQL aggregates. Cheap for the dataset sizes we expect
(hundreds, not millions). If it ever gets slow we'd add a materialised view or cache.
"""

from __future__ import annotations

from collections import defaultdict
from datetime import date, datetime, timedelta

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.application import Application
from app.schemas.common import Source, Status

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


class DailyCount(BaseModel):
    day: date
    count: int


class CategoryCount(BaseModel):
    label: str
    count: int


class DashboardStats(BaseModel):
    total: int
    active: int                     # applied + screening + interview
    offers: int
    rejections: int
    ghosted: int
    response_rate: float            # 1 - (ghosted / total), 0..1
    current_streak_days: int        # consecutive days with ≥1 application up to today
    longest_streak_days: int

    daily_counts: list[DailyCount]  # last N days
    by_status: list[CategoryCount]
    by_source: list[CategoryCount]


def _compute_streaks(applied_dates: set[date], today: date) -> tuple[int, int]:
    """Given the set of dates with at least one application, compute:
    - current streak: consecutive days ending today (or yesterday) with applications
    - longest streak overall
    """
    if not applied_dates:
        return 0, 0

    sorted_days = sorted(applied_dates)

    longest = 1
    run = 1
    for i in range(1, len(sorted_days)):
        if (sorted_days[i] - sorted_days[i - 1]).days == 1:
            run += 1
            longest = max(longest, run)
        else:
            run = 1

    # Current streak: count back from today
    current = 0
    cursor = today
    if cursor not in applied_dates:
        # Allow grace: if user hasn't applied today yet but did yesterday, still counts
        cursor = today - timedelta(days=1)
    while cursor in applied_dates:
        current += 1
        cursor = cursor - timedelta(days=1)

    return current, longest


@router.get("/stats", response_model=DashboardStats, summary="All KPIs + chart data in one call")
def dashboard_stats(
    db: Session = Depends(get_db),
    days: int = Query(30, ge=7, le=180, description="Window for the daily-counts chart"),
) -> DashboardStats:
    today = date.today()
    window_start = today - timedelta(days=days - 1)

    total = db.scalar(select(func.count()).select_from(Application)) or 0

    # Per-status
    rows = db.execute(select(Application.status, func.count()).group_by(Application.status)).all()
    by_status_map = {row[0]: row[1] for row in rows}
    by_status = [CategoryCount(label=k.value, count=v) for k, v in sorted(by_status_map.items(), key=lambda kv: -kv[1])]

    active = sum(by_status_map.get(s, 0) for s in (Status.APPLIED, Status.SCREENING, Status.INTERVIEW))
    offers = by_status_map.get(Status.OFFER, 0)
    rejections = by_status_map.get(Status.REJECTED, 0)
    ghosted = by_status_map.get(Status.GHOSTED, 0)

    response_rate = (1 - (ghosted / total)) if total else 0.0

    # Per-source
    src_rows = db.execute(select(Application.source, func.count()).group_by(Application.source)).all()
    by_source = [
        CategoryCount(label=k.value, count=v)
        for k, v in sorted({row[0]: row[1] for row in src_rows}.items(), key=lambda kv: -kv[1])
    ]

    # Daily counts in the window
    daily_rows = db.execute(
        select(Application.applied_date, func.count())
        .where(Application.applied_date >= window_start)
        .group_by(Application.applied_date)
    ).all()
    daily_map: dict[date, int] = defaultdict(int)
    for d, c in daily_rows:
        daily_map[d] = c
    daily_counts = [
        DailyCount(day=window_start + timedelta(days=i), count=daily_map.get(window_start + timedelta(days=i), 0))
        for i in range(days)
    ]

    # Streaks — pulled from ALL applications, not just the window
    all_days_rows = db.execute(select(Application.applied_date).distinct()).all()
    applied_set: set[date] = {row[0] for row in all_days_rows}
    current_streak, longest_streak = _compute_streaks(applied_set, today)

    return DashboardStats(
        total=total,
        active=active,
        offers=offers,
        rejections=rejections,
        ghosted=ghosted,
        response_rate=response_rate,
        current_streak_days=current_streak,
        longest_streak_days=longest_streak,
        daily_counts=daily_counts,
        by_status=by_status,
        by_source=by_source,
    )
