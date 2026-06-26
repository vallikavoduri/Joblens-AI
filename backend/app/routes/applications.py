"""REST endpoints for Applications."""

from __future__ import annotations

from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy import and_, func, or_, select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.application import Application
from app.models.status_history import StatusHistory
from app.schemas.application import (
    ApplicationCreate,
    ApplicationListOut,
    ApplicationOut,
    ApplicationUpdate,
    StatusHistoryOut,
)
from app.schemas.common import Source, Status

router = APIRouter(prefix="/applications", tags=["applications"])


@router.post(
    "",
    response_model=ApplicationOut,
    status_code=status.HTTP_201_CREATED,
    summary="Log a new job application",
)
def create_application(payload: ApplicationCreate, db: Session = Depends(get_db)) -> Application:
    data = payload.model_dump(exclude_none=False)
    # HttpUrl -> str for the SQLAlchemy String column
    if data.get("link") is not None:
        data["link"] = str(data["link"])
    app_row = Application(**data)

    db.add(app_row)
    db.flush()  # need app_row.id before logging history

    db.add(
        StatusHistory(
            application_id=app_row.id,
            old_status=None,
            new_status=app_row.status,
            source="manual",
            note="created",
        )
    )
    db.commit()
    db.refresh(app_row)
    return app_row


@router.get(
    "",
    response_model=ApplicationListOut,
    summary="List applications with filters + pagination",
)
def list_applications(
    db: Session = Depends(get_db),
    q: str | None = Query(None, description="Free-text search across company + role"),
    status_filter: Status | None = Query(None, alias="status"),
    source: Source | None = None,
    applied_from: date | None = Query(None, description="Inclusive"),
    applied_to: date | None = Query(None, description="Inclusive"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
) -> ApplicationListOut:
    stmt = select(Application)
    count_stmt = select(func.count()).select_from(Application)

    conditions = []
    if q:
        like = f"%{q}%"
        conditions.append(or_(Application.company.ilike(like), Application.role.ilike(like)))
    if status_filter:
        conditions.append(Application.status == status_filter)
    if source:
        conditions.append(Application.source == source)
    if applied_from:
        conditions.append(Application.applied_date >= applied_from)
    if applied_to:
        conditions.append(Application.applied_date <= applied_to)

    if conditions:
        stmt = stmt.where(and_(*conditions))
        count_stmt = count_stmt.where(and_(*conditions))

    total = db.scalar(count_stmt) or 0
    stmt = stmt.order_by(Application.applied_date.desc(), Application.id.desc()).limit(limit).offset(offset)

    items = db.scalars(stmt).all()
    return ApplicationListOut(items=items, total=total, limit=limit, offset=offset)


@router.get(
    "/{application_id}",
    response_model=ApplicationOut,
    summary="Fetch a single application",
)
def get_application(application_id: int, db: Session = Depends(get_db)) -> Application:
    obj = db.get(Application, application_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return obj


@router.patch(
    "/{application_id}",
    response_model=ApplicationOut,
    summary="Partial update (only send fields you want to change)",
)
def update_application(
    application_id: int, payload: ApplicationUpdate, db: Session = Depends(get_db)
) -> Application:
    obj = db.get(Application, application_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Application not found")

    changes = payload.model_dump(exclude_unset=True)
    if "link" in changes and changes["link"] is not None:
        changes["link"] = str(changes["link"])
    old_status = obj.status

    for key, value in changes.items():
        setattr(obj, key, value)

    # If status changed, log it
    if "status" in changes and changes["status"] != old_status:
        db.add(
            StatusHistory(
                application_id=obj.id,
                old_status=old_status,
                new_status=obj.status,
                source="manual",
            )
        )

    db.commit()
    db.refresh(obj)
    return obj


@router.delete(
    "/{application_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    summary="Delete an application (cascades to its emails + history)",
)
def delete_application(application_id: int, db: Session = Depends(get_db)) -> Response:
    obj = db.get(Application, application_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Application not found")
    db.delete(obj)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/{application_id}/history",
    response_model=list[StatusHistoryOut],
    summary="Status history (audit trail) for an application",
)
def application_history(application_id: int, db: Session = Depends(get_db)) -> list[StatusHistory]:
    obj = db.get(Application, application_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Application not found")
    stmt = (
        select(StatusHistory)
        .where(StatusHistory.application_id == application_id)
        .order_by(StatusHistory.changed_at.asc())
    )
    return list(db.scalars(stmt).all())
