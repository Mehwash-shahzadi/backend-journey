import hashlib
import json
import redis.asyncio as redis
import logging
from typing import Optional, Any

logger = logging.getLogger(__name__)

# Redis configuration
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0

# Cache expiration times (in seconds)
SUMMARIZE_CACHE_TTL = 3600      # 1 hour for summaries
MODERATE_CACHE_TTL = 1800       # 30 minutes for moderation
CLASSIFY_CACHE_TTL = 1800       # 30 minutes for classification
GENERATE_CACHE_TTL = 3600       # 1 hour for generation


async def get_redis_client() -> redis.Redis:
    """
    Get or create Redis async client.
    Connection is lazy - established on first use.
    """
    try:
        client = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=REDIS_DB,
            decode_responses=True,  # Auto-decode bytes to strings
            socket_connect_timeout=5
        )
        # Test connection
        await client.ping()
        return client
    except Exception as e:
        logger.error(f"Redis connection failed: {str(e)}")
        raise


def generate_cache_key(text: str, prefix: str = "ai") -> str:
    """
    Generate a cache key using SHA256 hash of the text.
    
    Args:
        text: The text to hash
        prefix: Redis key prefix (e.g., "ai:summarize", "ai:moderate")
        
    Returns:
        Redis key like "ai:summarize:a3c2b1..."
    """
    text_hash = hashlib.sha256(text.encode()).hexdigest()[:16]  # First 16 chars of hash
    return f"{prefix}:{text_hash}"


async def get_cached_result(key: str) -> Optional[Any]:
    """
    Retrieve a cached result from Redis.
    
    Args:
        key: Redis cache key
        
    Returns:
        Parsed JSON data if found and valid, None otherwise
    """
    try:
        client = await get_redis_client()
        cached = await client.get(key)
        
        if cached:
            logger.info(f"Cache HIT: {key}")
            return json.loads(cached)  # Parse JSON string
        
        logger.debug(f"Cache MISS: {key}")
        return None
    except Exception as e:
        logger.warning(f"Cache retrieval error: {str(e)}")
        return None  # Return None on cache error, allow request to proceed


async def set_cached_result(key: str, data: Any, ttl: int) -> bool:
    """
    Store a result in Redis with TTL.
    
    Args:
        key: Redis cache key
        data: Python object to cache
        ttl: Time to live in seconds
        
    Returns:
        True if cached successfully, False otherwise
    """
    try:
        client = await get_redis_client()
        json_data = json.dumps(data)  # Convert to JSON string
        await client.setex(key, ttl, json_data)
        logger.info(f"Cached result: {key} (TTL: {ttl}s)")
        return True
    except Exception as e:
        logger.warning(f"Cache write error: {str(e)}")
        return False  # Don't fail request if caching fails


# ==================== Prompt Engineering ====================
# Day 74: Optimized prompts for 25-35% cost reduction

SUMMARIZE_PROMPT = """Summarize in 3-5 sentences:

{text}

Summary:"""


MODERATE_PROMPT = """Analyze toxicity. Return JSON only:
{{"toxic": bool, "score": 0-1, "reasons": [list]}}

Text:
{text}

JSON:"""


def build_summarize_prompt(text: str) -> str:
    """Build the prompt for text summarization (Day 74: Optimized)."""
    return SUMMARIZE_PROMPT.format(text=text)


def build_moderate_prompt(text: str) -> str:
    """Build the prompt for content moderation (Day 74: Optimized)."""
    return MODERATE_PROMPT.format(text=text)


# ==================== Day 72: Classification & Generation Prompts ====================
# Day 74: Optimized for cost reduction

CLASSIFY_PROMPT = """Classify & sentiment. JSON only:
{{"category": "news|tech|sports|politics|entertainment|other", "sentiment": "positive|negative|neutral", "confidence": 0-1}}

Text:
{text}

JSON:"""


# Template-specific prompts for text generation
# Day 74: Optimized for 25-35% cost reduction
EMAIL_TEMPLATE_PROMPT = """Email: {topic} ({tone} tone, {length}):

"""

BLOG_TEMPLATE_PROMPT = """Blog post ({length} words, {tone}):
Topic: {topic}

"""

PRODUCT_TEMPLATE_PROMPT = """Product description: {topic}

"""

# Mapping template types to their prompts
TEMPLATE_PROMPTS = {
    "email": EMAIL_TEMPLATE_PROMPT,
    "blog": BLOG_TEMPLATE_PROMPT,
    "product_description": PRODUCT_TEMPLATE_PROMPT,
}


def build_classify_prompt(text: str) -> str:
    """Build the prompt for text classification with sentiment."""
    return CLASSIFY_PROMPT.format(text=text)


def build_generate_prompt(template_type: str, parameters: dict) -> str:
    """Build the prompt for template-based text generation.
    
    Args:
        template_type: One of 'email', 'blog', 'product_description'
        parameters: Dict with template-specific keys (topic, tone, length, etc.)
        
    Returns:
        Formatted prompt string
        
    Raises:
        ValueError: If template_type is not recognized
    """
    if template_type not in TEMPLATE_PROMPTS:
        raise ValueError(f"Invalid template type: {template_type}")
    
    template_prompt = TEMPLATE_PROMPTS[template_type]
    return template_prompt.format(**parameters)