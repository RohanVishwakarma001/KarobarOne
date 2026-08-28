# Owner: mousamdas156@gmail.com
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    chatType = Column("chat_type", String(30), nullable=False)
    storeId = Column("store_id", Integer, nullable=True)
    participant1 = Column("participant_1", Integer, nullable=False)
    participant2 = Column("participant_2", Integer, nullable=False)
    createdAt = Column("created_at", DateTime, default=datetime.utcnow, nullable=False)
    updatedAt = Column("updated_at", DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")
