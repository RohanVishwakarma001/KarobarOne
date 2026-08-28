# Owner: shlokpallav@gmail.com

"""
===============================================================================
CHECKOUT ROUTER
===============================================================================

Checkout API Endpoints

POST /checkout

===============================================================================
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.controllers.github.checkoutController import checkoutController
from app.db.session import getSyncDb
from app.schemas.github.checkoutSchema import (
    CheckoutRequest,
    CheckoutResponse,
)

router = APIRouter(
    prefix="/checkout",
    tags=["Checkout"],
)


@router.post(
    "",
    response_model=CheckoutResponse,
    status_code=status.HTTP_200_OK,
)
def checkout(
    request: CheckoutRequest,
    db: Session = Depends(getSyncDb),
):
    return checkoutController.checkout(
        db=db,
        request=request,
    )