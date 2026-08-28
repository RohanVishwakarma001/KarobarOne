from uuid import UUID

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from app.controllers.github.revenueSummaryController import (
    revenueSummaryController,
)
from app.db.session import getSyncDb
from app.schemas.github.revenueSummarySchema import (
    RevenueSummaryCreate,
    RevenueSummaryUpdate,
)

router = APIRouter(
    prefix="/revenue-summary",
    tags=["Revenue Summary"]
)


@router.post("/")
def create(
    revenue: RevenueSummaryCreate,
    db: Session = Depends(getSyncDb)
):
    return revenueSummaryController.create(
        db,
        revenue
    )


@router.get("/")
def getAll(
    db: Session = Depends(getSyncDb)
):
    return revenueSummaryController.getAll(db)


@router.get("/{revenueId}")
def getById(
    revenueId: UUID,
    db: Session = Depends(getSyncDb)
):
    return revenueSummaryController.getById(
        db,
        revenueId
    )


@router.put("/{revenueId}")
def update(
    revenueId: UUID,
    revenue: RevenueSummaryUpdate,
    db: Session = Depends(getSyncDb)
):
    return revenueSummaryController.update(
        db,
        revenueId,
        revenue
    )


@router.delete("/{revenueId}")
def delete(
    revenueId: UUID,
    db: Session = Depends(getSyncDb)
):
    return revenueSummaryController.delete(
        db,
        revenueId
    )