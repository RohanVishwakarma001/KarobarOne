from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base
from datetime import datetime
import uuid

class ChatUser(Base):
    __tablename__ = "chat_users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(20), default="customer", nullable=False)
    storeId = Column("store_id", UUID(as_uuid=True), nullable=True)
    createdAt = Column("created_at", DateTime, default=datetime.utcnow, nullable=False)

