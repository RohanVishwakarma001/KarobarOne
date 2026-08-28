from typing import List
from uuid import UUID

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from app.controllers.github.shippingExceptionController import (
    shippingExceptionController,
)

from app.db.session import getSyncDb

from app.schemas.github.shippingExceptionSchema import (
    ShippingExceptionCreate,
    ShippingExceptionUpdate,
    ShippingExceptionResponse,
)

router = APIRouter(
    prefix="/shipping-exceptions",
    tags=["Shipping Exceptions"]
)


@router.post(
    "/",
    response_model=ShippingExceptionResponse,
    status_code=201
)
def createShippingException(
    shippingException: ShippingExceptionCreate,
    db: Session = Depends(getSyncDb)
):

    return shippingExceptionController.create(
        db,
        shippingException
    )


@router.get(
    "/",
    response_model=List[ShippingExceptionResponse]
)
def getShippingExceptions(
    db: Session = Depends(getSyncDb)
):

    return shippingExceptionController.getAll(
        db
    )


@router.get(
    "/{shippingExceptionId}",
    response_model=ShippingExceptionResponse
)
def getShippingException(
    shippingExceptionId: UUID,
    db: Session = Depends(getSyncDb)
):

    return shippingExceptionController.getById(
        db,
        shippingExceptionId
    )


@router.put(
    "/{shippingExceptionId}",
    response_model=ShippingExceptionResponse
)
def updateShippingException(
    shippingExceptionId: UUID,
    shippingException: ShippingExceptionUpdate,
    db: Session = Depends(getSyncDb)
):

    return shippingExceptionController.update(
        db,
        shippingExceptionId,
        shippingException
    )


@router.delete(
    "/{shippingExceptionId}"
)
def deleteShippingException(
    shippingExceptionId: UUID,
    db: Session = Depends(getSyncDb)
):

    return shippingExceptionController.delete(
        db,
        shippingExceptionId
    )