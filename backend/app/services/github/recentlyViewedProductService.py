
from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.github.recentlyViewedProductRepository import (
    recentlyViewedProductRepository,
)
from app.schemas.github.recentlyViewedProductSchema import (
    RecentlyViewedProductCreate,
)


class RecentlyViewedProductService:

    def create(
        self,
        db: Session,
        view: RecentlyViewedProductCreate,
    ):
        return recentlyViewedProductRepository.create(
            db,
            view,
        )

    def getAll(
        self,
        db: Session,
    ):
        return recentlyViewedProductRepository.get_all(db)

    def getById(
        self,
        db: Session,
        recentlyViewedId: UUID,
    ):
        return recentlyViewedProductRepository.get(
            db,
            recentlyViewedId,
            recentlyViewedProductRepository.model.id,
        )

    def delete(
        self,
        db: Session,
        recentlyViewedId: UUID,
    ):
        dbItem = self.getById(
            db,
            recentlyViewedId,
        )

        if dbItem is None:
            return False

        recentlyViewedProductRepository.delete(
            db,
            dbItem,
        )

        return True


recentlyViewedProductService = RecentlyViewedProductService()