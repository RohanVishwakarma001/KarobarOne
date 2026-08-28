from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controllers.github.customerController import customerController
from app.db.session import getSyncDb
from app.schemas.github.customerSchema import (
    CustomerCreate,
    CustomerResponse,
)

router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
)


@router.post(
    "/",
    response_model=CustomerResponse,
    status_code=201,
)
def create_customer(
    customer: CustomerCreate,
    db: Session = Depends(getSyncDb),
):
    return customerController.createCustomer(
        db,
        customer,
    )


@router.get(
    "/store/{store_id}",
)
def get_customers_by_store(
    store_id: UUID,
    db: Session = Depends(getSyncDb),
):
    return customerController.getCustomersByStore(
        db,
        store_id,
    )