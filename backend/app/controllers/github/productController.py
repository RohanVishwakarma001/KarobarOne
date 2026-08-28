from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.github.productSchema import (
    ProductCreate,
    ProductUpdate,
)
from app.services.github.productService import (
    productService,
)


class ProductController:

    def create(
        self,
        db: Session,
        product: ProductCreate
    ):
        return productService.create(
            db,
            product
        )

    def getAll(
        self,
        db: Session
    ):
        return productService.getAll(db)

    def getById(
        self,
        db: Session,
        productId: UUID
    ):
        product = productService.getById(
            db,
            productId
        )

        if product is None:
            raise HTTPException(
                status_code=404,
                detail="Product not found."
            )

        return product

    def update(
        self,
        db: Session,
        productId: UUID,
        product: ProductUpdate
    ):
        updatedProduct = productService.update(
            db,
            productId,
            product
        )

        if updatedProduct is None:
            raise HTTPException(
                status_code=404,
                detail="Product not found."
            )

        return updatedProduct

    def delete(
        self,
        db: Session,
        productId: UUID
    ):
        deleted = productService.delete(
            db,
            productId
        )

        if not deleted:
            raise HTTPException(
                status_code=404,
                detail="Product not found."
            )

        return {
            "message": "Product deleted successfully."
        }


productController = ProductController()