from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.github.productRepository import (
    productRepository,
)
from app.schemas.github.productSchema import (
    ProductCreate,
    ProductUpdate,
)


class ProductService:

    def create(
        self,
        db: Session,
        product: ProductCreate
    ):
        return productRepository.create(
            db=db,
            obj=product
        )

    def getAll(
        self,
        db: Session
    ):
        return productRepository.get_all(db)

    def getById(
        self,
        db: Session,
        productId: UUID
    ):
        return productRepository.get(
            db=db,
            obj_id=productId,
            id_field=productRepository.model.id
        )

    def update(
        self,
        db: Session,
        productId: UUID,
        product: ProductUpdate
    ):
        dbProduct = self.getById(
            db,
            productId
        )

        if dbProduct is None:
            return None

        return productRepository.update(
            db=db,
            db_obj=dbProduct,
            obj=product
        )

    def delete(
        self,
        db: Session,
        productId: UUID
    ):
        dbProduct = self.getById(
            db,
            productId
        )

        if dbProduct is None:
            return False

        productRepository.delete(
            db=db,
            db_obj=dbProduct
        )

        return True


productService = ProductService()