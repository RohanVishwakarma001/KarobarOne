from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.github.revenueSummarySchema import (
    RevenueSummaryCreate,
    RevenueSummaryUpdate,
)
from app.services.github.revenueSummaryService import (
    revenueSummaryService,
)


class RevenueSummaryController:

    def create(
        self,
        db: Session,
        revenue: RevenueSummaryCreate
    ):
        return revenueSummaryService.create(
            db,
            revenue
        )

    def getAll(
        self,
        db: Session
    ):
        return revenueSummaryService.getAll(db)

    def getById(
        self,
        db: Session,
        revenueId: UUID
    ):
        revenue = revenueSummaryService.getById(
            db,
            revenueId
        )

        if revenue is None:
            raise HTTPException(
                status_code=404,
                detail="Revenue summary not found."
            )

        return revenue

    def update(
        self,
        db: Session,
        revenueId: UUID,
        revenue: RevenueSummaryUpdate
    ):
        dbRevenue = revenueSummaryService.update(
            db,
            revenueId,
            revenue
        )

        if dbRevenue is None:
            raise HTTPException(
                status_code=404,
                detail="Revenue summary not found."
            )

        return dbRevenue

    def delete(
        self,
        db: Session,
        revenueId: UUID
    ):
        deleted = revenueSummaryService.delete(
            db,
            revenueId
        )

        if not deleted:
            raise HTTPException(
                status_code=404,
                detail="Revenue summary not found."
            )

        return {
            "message": "Revenue summary deleted successfully."
        }


revenueSummaryController = RevenueSummaryController()