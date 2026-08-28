from fastapi import HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.schemas.github.customerSchema import CustomerCreate
from app.services.github.customerService import customerService


class CustomerController:

    def createCustomer(
        self,
        db: Session,
        customer: CustomerCreate
    ):
        createdCustomer = customerService.createCustomer(
            db,
            customer
        )

        if createdCustomer is None:
            raise HTTPException(
                status_code=400,
                detail="Customer already exists"
            )

        return createdCustomer

    def getCustomersByStore(
        self,
        db: Session,
        store_id: UUID
    ):
        return customerService.getCustomersByStore(
            db,
            store_id
        )


customerController = CustomerController()