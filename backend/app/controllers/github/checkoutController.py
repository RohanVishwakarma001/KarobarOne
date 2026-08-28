# Owner: shlokpallav@gmail.com

"""
===============================================================================
CHECKOUT CONTROLLER
===============================================================================

Handles Checkout API requests.

Responsibilities:
- Receive Checkout requests
- Call CheckoutService
- Return Checkout response

Business logic must NOT exist here.

===============================================================================
"""

from sqlalchemy.orm import Session

from app.schemas.github.checkoutSchema import (
    CheckoutRequest,
    CheckoutResponse,
)
from app.services.github.checkoutService import checkoutService


class CheckoutController:

    def checkout(
        self,
        db: Session,
        request: CheckoutRequest,
    ) -> CheckoutResponse:

        return checkoutService.checkout(
            db=db,
            request=request,
        )


checkoutController = CheckoutController()