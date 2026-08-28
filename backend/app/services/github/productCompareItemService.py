from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.github.productCompareItemRepository import (
    productCompareItemRepository,
)
from app.schemas.github.schemas import (
    ProductCompareItemCreate,
)


class ProductCompareItemService:

    def create(
        self,
        db: Session,
        compareItem: ProductCompareItemCreate,
    ):
        return productCompareItemRepository.create(
            db,
            compareItem,
        )

    def getAll(
        self,
        db: Session,
    ):
        return productCompareItemRepository.get_all(db)

    def getById(
        self,
        db: Session,
        compareItemId: UUID,
    ):
        return productCompareItemRepository.get(
            db,
            compareItemId,
            productCompareItemRepository.model.id,
        )

    def delete(
        self,
        db: Session,
        compareItemId: UUID,
    ):
        dbItem = self.getById(
            db,
            compareItemId,
        )

        if dbItem is None:
            return False

        productCompareItemRepository.delete(
            db,
            dbItem,
        )

        return True


productCompareItemService = ProductCompareItemService()