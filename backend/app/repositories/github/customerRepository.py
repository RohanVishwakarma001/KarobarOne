from sqlalchemy.orm import Session

from app.db.models.github.customer import Customer
from app.repositories.github.base import BaseRepository

class CustomerRepository(
    BaseRepository[Customer]
):

    def __init__(self):
        super().__init__(Customer)

    def getByEmail(
        self,
        db: Session,
        email: str
    ):
        return (
            db.query(Customer)
            .filter(Customer.email == email)
            .first()
        )

    def getByCustomerCode(
        self,
        db: Session,
        customer_code: str
    ):
        return (
            db.query(Customer)
            .filter(
                Customer.customer_code == customer_code
            )
            .first()
        )

    def getAllByStore(
        self,
        db: Session,
        store_id
    ):
        return (
            db.query(Customer)
            .filter(Customer.store_id == store_id)
            .all()
        )


customerRepository = CustomerRepository()