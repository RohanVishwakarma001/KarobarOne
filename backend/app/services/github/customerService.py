from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.db.models.github.customer import Customer
from app.repositories.github.customerRepository import customerRepository
from app.schemas.github.customerSchema import CustomerCreate

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


class CustomerService:

    def hashPassword(
        self,
        password: str
    ):
        return pwd_context.hash(password[:72])

    def createCustomer(
        self,
        db: Session,
        customer: CustomerCreate
    ):

        existingEmail = customerRepository.getByEmail(
            db,
            customer.email
        )

        if existingEmail:
            return None

        existingCode = customerRepository.getByCustomerCode(
            db,
            customer.customer_code
        )

        if existingCode:
            raise ValueError(
                "Customer code already exists"
            )

        dbCustomer = Customer(
            tenant_id=customer.tenant_id,
            store_id=customer.store_id,
            customer_code=customer.customer_code,
            first_name=customer.first_name,
            last_name=customer.last_name,
            email=customer.email,
            mobile=customer.mobile,
            password_hash=(
                self.hashPassword(customer.password)
                if customer.password
                else None
            ),
            status="ACTIVE",
            is_guest_customer=False,
            is_email_verified=False,
            is_mobile_verified=False,
        )

        db.add(dbCustomer)
        db.commit()
        db.refresh(dbCustomer)

        return dbCustomer

    def getCustomersByStore(
        self,
        db: Session,
        store_id
    ):
        return customerRepository.getAllByStore(
            db,
            store_id
        )


customerService = CustomerService()