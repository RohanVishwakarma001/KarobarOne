# Owner: mousamdas156@gmail.com
# ================================================================================
# FILE: services/conversationService.py — Chat Conversation Service
# ================================================================================
# Why this file is used:
#   - Manages communication rooms for live chats.
#
# What components are inside:
#   - ConversationService:
#       - getOrCreateConversation() -> Resolves active communication rooms,
#                                     building rooms if none exist.
# ================================================================================
from sqlalchemy import select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.conversation import Conversation

class ConversationService:
    @staticmethod
    async def getOrCreateConversation(
        session: AsyncSession,
        chatType: str,
        userId1: int,
        userId2: int,
        storeId: int | None = None
    ) -> Conversation:
        stmt = select(Conversation).where(
            and_(
                Conversation.chatType == chatType,
                Conversation.storeId == storeId,
                or_(
                    and_(Conversation.participant1 == userId1, Conversation.participant2 == userId2),
                    and_(Conversation.participant1 == userId2, Conversation.participant2 == userId1)
                )
            )
        )
        result = await session.execute(stmt)
        conversation = result.scalars().first()

        if conversation:
            return conversation

        conversation = Conversation(
            chatType=chatType,
            storeId=storeId,
            participant1=userId1,
            participant2=userId2
        )
        session.add(conversation)
        await session.commit()
        await session.refresh(conversation)
        return conversation