# Owner: mousamdas156@gmail.com
# ================================================================================
# FILE: services/messageServices.py — Chat Message Service
# ================================================================================
# Why this file is used:
#   - Persists communication logs inside chat rooms.
#
# What components are inside:
#   - MessageService:
#       - createMessage() -> Adds messages inside communication rooms.
# ================================================================================
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.message import Message

class MessageService:
    @staticmethod
    async def createMessage(
        session: AsyncSession,
        conversationId: int,
        senderId: int,
        message: str
    ):
        dbMessage = Message(
            conversationId=conversationId,
            senderId=senderId,
            message=message
        )
        session.add(dbMessage)
        await session.commit()
        await session.refresh(dbMessage)
        return dbMessage