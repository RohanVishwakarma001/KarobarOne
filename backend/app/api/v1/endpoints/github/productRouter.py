from typing import List
from uuid import UUID

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from app.controllers.github.productController import (
    productController,
)
from app.db.session import getSyncDb
from app.schemas.github.productSchema import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
)

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.post(
    "/",
    response_model=ProductResponse,
    status_code=201
)
def createProduct(
    product: ProductCreate,
    db: Session = Depends(getSyncDb)
):
    return productController.create(
        db,
        product
    )


@router.get(
    "/",
    response_model=List[ProductResponse]
)
def getProducts(
    db: Session = Depends(getSyncDb)
):
    return productController.getAll(db)


@router.get(
    "/{productId}",
    response_model=ProductResponse
)
def getProduct(
    productId: UUID,
    db: Session = Depends(getSyncDb)
):
    return productController.getById(
        db,
        productId
    )


@router.put(
    "/{productId}",
    response_model=ProductResponse
)
def updateProduct(
    productId: UUID,
    product: ProductUpdate,
    db: Session = Depends(getSyncDb)
):
    return productController.update(
        db,
        productId,
        product
    )


@router.delete(
    "/{productId}"
)
def deleteProduct(
    productId: UUID,
    db: Session = Depends(getSyncDb)
):
    return productController.delete(
        db,
        productId
    )