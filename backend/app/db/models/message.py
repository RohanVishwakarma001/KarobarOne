# Owner: mousamdas156@gmail.com
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    conversationId = Column("conversation_id", Integer, ForeignKey("conversations.id"), nullable=False)
    senderId = Column("sender_id", Integer, nullable=False)
    message = Column(Text, nullable=True)
    messageType = Column("message_type", String(20), default="text", nullable=False)
    fileUrl = Column("file_url", String(500), nullable=True)
    isRead = Column("is_read", Boolean, default=False, nullable=False)
    createdAt = Column("created_at", DateTime, default=datetime.utcnow, nullable=False)

    conversation = relationship("Conversation", back_populates="messages")
