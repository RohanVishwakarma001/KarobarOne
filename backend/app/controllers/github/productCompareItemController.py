from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.github.schemas import (
    ProductCompareItemCreate,
)
from app.services.github.productCompareItemService import (
    productCompareItemService,
)


class ProductCompareItemController:

    def create(
        self,
        db: Session,
        compareItem: ProductCompareItemCreate,
    ):
        return productCompareItemService.create(
            db,
            compareItem,
        )

    def getAll(
        self,
        db: Session,
    ):
        return productCompareItemService.getAll(db)

    def getById(
        self,
        db: Session,
        compareItemId: UUID,
    ):
        item = productCompareItemService.getById(
            db,
            compareItemId,
        )

        if item is None:
            raise HTTPException(
                status_code=404,
                detail="Product Compare Item not found",
            )

        return item

    def delete(
        self,
        db: Session,
        compareItemId: UUID,
    ):
        deleted = productCompareItemService.delete(
            db,
            compareItemId,
        )

        if not deleted:
            raise HTTPException(
                status_code=404,
                detail="Product Compare Item not found",
            )

        return {
            "message": "Product Compare Item deleted successfully"
        }


productCompareItemController = ProductCompareItemController()