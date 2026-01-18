from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from models.message import Message
from schemas.message import MessageOut
from uuid import UUID
import logging
from config import CONTEXT_WINDOW_MESSAGES, MIN_MESSAGES_TO_KEEP

logger = logging.getLogger(__name__)

async def get_messages(db: AsyncSession, conv_id: UUID, limit: int = None) -> list[MessageOut]:
    """Get messages for a conversation, optionally limited to recent messages"""
    result = await db.execute(
        select(Message)
        .where(Message.conversation_id == conv_id)
        .order_by(Message.created_at)
    )
    messages = result.scalars().all()
    
    # Return all messages or limited set based on limit parameter
    if limit:
        return [MessageOut.from_orm(m) for m in messages[-limit:]]
    return [MessageOut.from_orm(m) for m in messages]

async def create_message(db: AsyncSession, conv_id: UUID, role: str, content: str, tokens_used: int):
    """Create a message and manage context window"""
    message = Message(
        conversation_id=conv_id,
        role=role,
        content=content,
        tokens_used=tokens_used
    )
    db.add(message)
    await db.commit()
    
    # Trim old messages if context window exceeded
    await trim_old_messages(db, conv_id)
    
    await db.refresh(message)
    return message

async def trim_old_messages(db: AsyncSession, conv_id: UUID):
    """
    Remove old messages if conversation exceeds context window size.
    Keeps at least MIN_MESSAGES_TO_KEEP messages to preserve conversation structure.
    """
    result = await db.execute(
        select(Message)
        .where(Message.conversation_id == conv_id)
        .order_by(Message.created_at)
    )
    all_messages = result.scalars().all()
    
    # Only trim if we exceed the context window
    if len(all_messages) > CONTEXT_WINDOW_MESSAGES:
        # Calculate how many to delete
        messages_to_delete = len(all_messages) - MIN_MESSAGES_TO_KEEP
        messages_to_delete = min(messages_to_delete, len(all_messages) - MIN_MESSAGES_TO_KEEP)
        
        # Get oldest messages to delete (keep most recent MIN_MESSAGES_TO_KEEP)
        messages_to_remove = all_messages[:messages_to_delete]
        
        logger.info(f"Trimming {len(messages_to_remove)} messages from conversation {conv_id}")
        
        for msg in messages_to_remove:
            await db.delete(msg)
        
        await db.commit()

async def delete_messages(db: AsyncSession, conv_id: UUID):
    """Delete all messages in a conversation"""
    await db.execute(
        delete(Message).where(Message.conversation_id == conv_id)
    )
    await db.commit()
