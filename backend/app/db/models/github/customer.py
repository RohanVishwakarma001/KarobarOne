import uuid

from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.db.baseGithub import BaseGithub


class Customer(BaseGithub):

    __tablename__ = "customers"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    tenant_id = Column(
        UUID(as_uuid=True),
        nullable=False
    )

    store_id = Column(
        UUID(as_uuid=True),
        nullable=False
    )

    customer_code = Column(
        String(30),
        nullable=False
    )

    first_name = Column(
        String(100),
        nullable=False
    )

    last_name = Column(
        String(100)
    )

    email = Column(
        String(255),
        nullable=False
    )

    mobile = Column(
        String(15),
        nullable=False
    )

    password_hash = Column(
        String(255)
    )

    status = Column(
        String(20),
        nullable=False
    )

    is_guest_customer = Column(
        Boolean,
        default=False
    )

    is_email_verified = Column(
        Boolean,
        default=False
    )

    is_mobile_verified = Column(
        Boolean,
        default=False
    )

    last_login_at = Column(
        DateTime(timezone=True)
    )

    registered_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    deleted_at = Column(
        DateTime(timezone=True)
    )