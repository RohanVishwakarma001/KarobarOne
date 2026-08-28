# Owner: mousamdas156@gmail.com
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError
from app.core.securityChat import decode_token
from app.db.models.chatUser import ChatUser
from app.services.conversationService import ConversationService
from app.services.messageServices import MessageService
from app.core.chatManager import manager
from app.db.session import getSessionFactory

router = APIRouter(tags=["Live Chat"])

class UserRole:
    CUSTOMER = "customer"
    STORE_OWNER = "store_owner"
    SUPPORT_AGENT = "support_agent"

ALLOWED_CHAT_RULES = {
    "customer_owner": {UserRole.CUSTOMER, UserRole.STORE_OWNER},
    "owner_support": {UserRole.STORE_OWNER, UserRole.SUPPORT_AGENT},
}

@router.websocket("/ws/chat/{userId}")
async def chatSocket(
    websocket: WebSocket,
    userId: int,
    token: str = Query(...)
):
    try:
        payload = decode_token(token)
        tokenUserId = int(payload.get("sub"))
        userRole = payload.get("role")

        if tokenUserId != userId:
            await websocket.close(code=4001)
            return

    except JWTError:
        await websocket.close(code=4001)
        return

    await manager.connect(userId, websocket)
    print(f"User {userId} connected")

    try:
        while True:
            data = await websocket.receive_json()
            print("JSON:", data)

            if data.get("event") == "message":
                chatType = data.get("chatType")

                if chatType not in ALLOWED_CHAT_RULES:
                    await websocket.send_json({
                        "event": "error",
                        "detail": f"Invalid chatType: {chatType}"
                    })
                    continue

                receiverId = None
                resolvedStoreId = None

                async with getSessionFactory()() as session:
                    if chatType == "customer_owner":
                        if userRole == UserRole.CUSTOMER:
                            storeIdInput = data.get("storeId")

                            if storeIdInput is None:
                                await websocket.send_json({
                                    "event": "error",
                                    "detail": "storeId is required for customer_owner chat"
                                })
                                continue

                            stmt = select(ChatUser).where(ChatUser.storeId == storeIdInput, ChatUser.role == UserRole.STORE_OWNER)
                            res = await session.execute(stmt)
                            receiver = res.scalars().first()

                            if not receiver:
                                await websocket.send_json({
                                    "event": "error",
                                    "detail": f"No store found with storeId: {storeIdInput}"
                                })
                                continue

                            receiverId = receiver.id
                            resolvedStoreId = storeIdInput

                        elif userRole == UserRole.STORE_OWNER:
                            receiverId = data.get("receiverId")

                            if receiverId is None:
                                await websocket.send_json({
                                    "event": "error",
                                    "detail": "receiverId is required"
                                })
                                continue

                            stmt = select(ChatUser).where(ChatUser.id == receiverId)
                            res = await session.execute(stmt)
                            receiver = res.scalars().first()

                            if not receiver:
                                await websocket.send_json({
                                    "event": "error",
                                    "detail": "Receiver not found"
                                })
                                continue

                            stmt = select(ChatUser).where(ChatUser.id == userId)
                            res = await session.execute(stmt)
                            sender = res.scalars().first()
                            resolvedStoreId = sender.storeId

                        else:
                            await websocket.send_json({
                                "event": "error",
                                "detail": f"Role mismatch for chatType: {chatType}"
                            })
                            continue

                    elif chatType == "owner_support":
                        receiverId = data.get("receiverId")

                        if receiverId is None:
                            await websocket.send_json({
                                "event": "error",
                                "detail": "receiverId is required"
                            })
                            continue

                        stmt = select(ChatUser).where(ChatUser.id == receiverId)
                        res = await session.execute(stmt)
                        receiver = res.scalars().first()

                        if not receiver:
                            await websocket.send_json({
                                "event": "error",
                                "detail": "Receiver not found"
                                })
                            continue

                        allowedRoles = ALLOWED_CHAT_RULES[chatType]
                        if not {userRole, receiver.role}.issubset(allowedRoles):
                            await websocket.send_json({
                                "event": "error",
                                "detail": f"Role mismatch for chatType: {chatType}"
                            })
                            continue

                        resolvedStoreId = None

                    conversation = await ConversationService.getOrCreateConversation(
                        session=session,
                        chatType=chatType,
                        userId1=userId,
                        userId2=receiverId,
                        storeId=resolvedStoreId
                    )

                    message = await MessageService.createMessage(
                        session=session,
                        conversationId=conversation.id,
                        senderId=userId,
                        message=data["message"]
                    )

                    print(f"Message Saved: {message.id} | Conversation: {conversation.id} | Store: {resolvedStoreId}")

                await manager.send_to_user(
                    receiverId,
                    {
                        "event": "message",
                        "conversationId": conversation.id,
                        "storeId": conversation.storeId,
                        "messageId": message.id,
                        "senderId": userId,
                        "message": message.message
                    }
                )

                await websocket.send_json({
                    "event": "message_sent",
                    "messageId": message.id,
                    "conversationId": conversation.id,
                    "storeId": conversation.storeId
                })

    except WebSocketDisconnect:
        manager.disconnect(userId)
        print(f"User {userId} disconnected.")

@router.get("/chat-test")
async def chatTest():
    return {"message": "Chat router working"}
