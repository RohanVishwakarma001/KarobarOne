import uuid

from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.db.baseGithub import BaseGithub


class User(BaseGithub):

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    first_name = Column(String(100), nullable=False)

    last_name = Column(String(100))

    email = Column(String(255), unique=True, nullable=False)

    mobile = Column(String(15))

    whatsapp_mobile = Column(String(15))

    password_hash = Column(String(255), nullable=False)

    is_active = Column(Boolean, default=True)

    is_email_verified = Column(Boolean, default=False)

    is_mobile_verified = Column(Boolean, default=False)

    last_login_at = Column(DateTime(timezone=True))

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    deleted_at = Column(DateTime(timezone=True))