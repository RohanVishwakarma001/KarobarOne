from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.github.revenueSummaryRepository import (
    revenueSummaryRepository,
)
from app.schemas.github.revenueSummarySchema import (
    RevenueSummaryCreate,
    RevenueSummaryUpdate,
)


class RevenueSummaryService:

    def create(
        self,
        db: Session,
        revenue: RevenueSummaryCreate
    ):
        return revenueSummaryRepository.create(
            db=db,
            obj=revenue
        )

    def getAll(
        self,
        db: Session
    ):
        return revenueSummaryRepository.get_all(db)

    def getById(
        self,
        db: Session,
        revenueId: UUID
    ):
        return revenueSummaryRepository.get(
            db=db,
            obj_id=revenueId,
            id_field=revenueSummaryRepository.model.id
        )

    def update(
        self,
        db: Session,
        revenueId: UUID,
        revenue: RevenueSummaryUpdate
    ):
        dbRevenue = self.getById(
            db,
            revenueId
        )

        if dbRevenue is None:
            return None

        return revenueSummaryRepository.update(
            db=db,
            db_obj=dbRevenue,
            obj=revenue
        )

    def delete(
        self,
        db: Session,
        revenueId: UUID
    ):
        dbRevenue = self.getById(
            db,
            revenueId
        )

        if dbRevenue is None:
            return False

        revenueSummaryRepository.delete(
            db=db,
            db_obj=dbRevenue
        )

        return True


revenueSummaryService = RevenueSummaryService()