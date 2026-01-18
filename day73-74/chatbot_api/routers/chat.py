from fastapi import APIRouter, Depends, HTTPException, Query, Path, Request
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from crud.conversation import create_conversation, get_conversation, get_conversations
from crud.message import get_messages, create_message, trim_old_messages
from schemas.conversation import ConversationCreate, ConversationOut
from schemas.message import MessageOut
from database import get_db
from services.gemini_service import GeminiService
from security.prompt_safety import detect_prompt_injection, validate_llm_response
from middleware.error_handler import log_error_context
from fastapi.responses import StreamingResponse
import os
from uuid import UUID
import logging
from config import CONTEXT_WINDOW_MESSAGES, DEFAULT_TITLE_WORD_LIMIT

# Day 73: Import rate limiter (avoid circular import by using separate limiter module)
from limiter import limiter

router = APIRouter(prefix="/chat", tags=["chat"])

logger = logging.getLogger(__name__)


# Pydantic Models

class MessageCreate(BaseModel):
    """Request model for creating a new message"""
    content: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "content": "What is machine learning?"
            }
        }


class MessageResponse(BaseModel):
    """Response model for messages with token tracking"""
    id: UUID
    conversation_id: UUID
    role: str
    content: str
    tokens_used: int
    created_at: str
    
    class Config:
        from_attributes = True


#  Helper Functions 

def auto_generate_title(message_content: str) -> str:
    """
    Auto-generate a conversation title from the first user message.
    Takes first N meaningful words and capitalizes them.
    
    Args:
        message_content: The user's first message
        
    Returns:
        A formatted title string
    """
    words = message_content.split()[:DEFAULT_TITLE_WORD_LIMIT]
    title = " ".join(words).strip()
    
    # Capitalize properly
    if title:
        return title[0].upper() + title[1:] if len(title) > 1 else title.upper()
    return "New Chat"


# API Endpoints 

@router.post(
    "/conversations",
    response_model=ConversationOut,
    summary="Create a new conversation",
    description="Creates a new conversation for a user. Title will be auto-generated from first message if not provided. Day 73: Rate limited to 10 req/min.",
    tags=["Conversations"]
)
@limiter.limit("10/minute")
async def create_new_conversation(
    request: Request,
    conv: ConversationCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Start a new chat conversation.
    Title auto-generates from your first message if not provided.
    """
    return await create_conversation(db, conv)


@router.get(
    "/conversations",
    response_model=list[ConversationOut],
    summary="List user's conversations",
    description="Retrieves all conversations for a specific user, ordered by creation date. Day 73: Rate limited to 10 req/min.",
    tags=["Conversations"]
)
@limiter.limit("10/minute")
async def list_conversations(
    request: Request,
    user_id: str = Query(..., description="The user ID to fetch conversations for"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all your conversations, sorted by date.
    """
    return await get_conversations(db, user_id)


@router.get(
    "/conversations/{conversation_id}/messages",
    response_model=list[MessageOut],
    summary="Get conversation history",
    description="Retrieves the complete message history for a conversation, including all user and assistant messages. Day 73: Rate limited to 10 req/min.",
    tags=["Messages"]
)
@limiter.limit("10/minute")
async def get_conversation_messages(
    request: Request,
    conversation_id: UUID = Path(..., description="The conversation ID"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get the full chat history for a conversation.
    """
    conv = await get_conversation(db, conversation_id)
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    messages = await get_messages(db, conversation_id)
    return messages


@router.post(
    "/conversations/{conversation_id}/messages",
    response_model=MessageOut,
    summary="Send message and get AI response",
    description="Sends a user message and returns the AI-generated response. Uses context window management to optimize token usage. Day 73: Rate limited to 10 req/min.",
    tags=["Messages"]
)
@limiter.limit("10/minute")
async def send_message(
    request: Request,
    conversation_id: UUID,
    message: MessageCreate,
    db: AsyncSession = Depends(get_db),
    gemini: GeminiService = Depends(lambda: GeminiService(os.getenv("GEMINI_API_KEY")))
):
    """
    Send a message and get AI response.
    Includes context management, auto-titles, and security checks.
    """
    conv = await get_conversation(db, conversation_id)
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # ===== DAY 73 SECURITY: Detect prompt injection =====
    if detect_prompt_injection(message.content):
        raise HTTPException(
            status_code=400,
            detail="Potential prompt injection detected. Request blocked for security."
        )

    # AUTO-GENERATE TITLE: Update title from first meaningful message if not set
    if not conv.title or conv.title == "string" or conv.title.startswith("Chat"):
        generated_title = auto_generate_title(message.content)
        if generated_title != "New Chat" or not conv.title:
            conv.title = generated_title
            await db.commit()
            await db.refresh(conv)
            logger.info(f"Auto-generated title for conversation {conversation_id}: {generated_title}")

    # CONTEXT WINDOW MANAGEMENT: Get only recent messages for model context
    history = await get_messages(db, conversation_id, limit=CONTEXT_WINDOW_MESSAGES)
    history_dicts = [{"role": "user" if m.role == "user" else "model", "parts": [{"text": m.content}]} for m in history]

    logger.info(f"Using {len(history)} messages from context window for conversation {conversation_id}")

    # Generate response from Gemini
    full_response = ""
    async for chunk in gemini.generate_stream(history_dicts, message.content):
        if chunk.startswith("data: "):
            text_chunk = chunk[6:].strip()
            if text_chunk != "[DONE]":
                full_response += text_chunk
    
    # ===== DAY 73 SECURITY: Validate LLM response (filter PII, check safety) =====
    try:
        full_response, _ = validate_llm_response(full_response)
    except ValueError as e:
        raise HTTPException(
            status_code=403,
            detail=f"Response blocked for safety: {str(e)}"
        )

    # Save user message
    await create_message(db, conversation_id, "user", message.content, tokens_used=0)

    # Save assistant response
    tokens_used = len(full_response.split()) * 2
    assistant_msg = await create_message(db, conversation_id, "assistant", full_response, tokens_used)

    logger.info(f"Message created for conversation {conversation_id}, tokens used: {tokens_used}")

    return MessageOut.from_orm(assistant_msg)


@router.get(
    "/conversations/{conversation_id}/stream",
    summary="Stream chat responses",
    description="Streams AI responses in real-time using Server-Sent Events (SSE). Ideal for progressive message display in frontend. Day 73: Rate limited to 10 req/min.",
    tags=["Messages"]
)
@limiter.limit("10/minute")
async def stream_chat(
    request: Request,
    conversation_id: UUID,
    message: str = Query(..., description="The user's message to send"),
    db: AsyncSession = Depends(get_db),
    gemini: GeminiService = Depends(lambda: GeminiService(os.getenv("GEMINI_API_KEY")))
):
    """
    Stream AI responses in real-time using Server-Sent Events.
    Perfect for progressive message display in your frontend.
    """
    conv = await get_conversation(db, conversation_id)
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # Update title if needed
    if not conv.title or conv.title == "string" or conv.title.startswith("Chat"):
        generated_title = auto_generate_title(message)
        if generated_title != "New Chat" or not conv.title:
            conv.title = generated_title
            await db.commit()
            await db.refresh(conv)

    # CONTEXT WINDOW: Get recent messages only
    history = await get_messages(db, conversation_id, limit=CONTEXT_WINDOW_MESSAGES)
    history_dicts = [
        {"role": "user" if m.role == "user" else "model", "parts": [{"text": m.content}]} 
        for m in history
    ]

    async def event_generator():
        """Stream chunks from Gemini API"""
        async for chunk in gemini.generate_stream(history_dicts, message):
            yield chunk

    return StreamingResponse(event_generator(), media_type="text/event-stream")