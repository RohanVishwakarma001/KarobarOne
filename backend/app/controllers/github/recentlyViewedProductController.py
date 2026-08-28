from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.github.recentlyViewedProductSchema import (
    RecentlyViewedProductCreate,
)
from app.services.github.recentlyViewedProductService import (
    recentlyViewedProductService,
)


class RecentlyViewedProductController:

    def create(self, db: Session, view: RecentlyViewedProductCreate):
        return recentlyViewedProductService.create(db, view)

    def getAll(self, db: Session):
        return recentlyViewedProductService.getAll(db)

    def getById(self, db: Session, recentlyViewedId: UUID):
        item = recentlyViewedProductService.getById(
            db,
            recentlyViewedId,
        )

        if item is None:
            raise HTTPException(
                status_code=404,
                detail="Recently Viewed Product not found",
            )

        return item

    def delete(self, db: Session, recentlyViewedId: UUID):
        deleted = recentlyViewedProductService.delete(
            db,
            recentlyViewedId,
        )

        if not deleted:
            raise HTTPException(
                status_code=404,
                detail="Recently Viewed Product not found",
            )

        return {
            "message": "Recently viewed product deleted successfully"
        }


recentlyViewedProductController = RecentlyViewedProductController()