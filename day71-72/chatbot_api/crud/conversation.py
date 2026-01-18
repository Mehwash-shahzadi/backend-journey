from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
from models.conversation import Conversation
from schemas.conversation import ConversationCreate, ConversationOut
from uuid import UUID
from datetime import datetime

async def create_conversation(db: AsyncSession, conv: ConversationCreate) -> ConversationOut:
    db_conv = Conversation(user_id=conv.user_id)
    if conv.title:
        db_conv.title = conv.title
    else:
        db_conv.title = f"Chat {datetime.utcnow().date()}"

    db.add(db_conv)
    await db.commit()
    await db.refresh(db_conv)
    return ConversationOut.from_orm(db_conv)

async def get_conversations(db: AsyncSession, user_id: str) -> list[ConversationOut]:
    result = await db.execute(
        select(Conversation).where(Conversation.user_id == user_id)
    )
    conversations = result.scalars().all()
    return [ConversationOut.from_orm(c) for c in conversations]

async def get_conversation(db: AsyncSession, conv_id: UUID) -> Conversation | None:
    result = await db.execute(
        select(Conversation).where(Conversation.id == conv_id)
    )
    return result.scalar_one_or_none()