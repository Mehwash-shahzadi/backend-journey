from fastapi import APIRouter, HTTPException, Depends, Request, Body
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
import json
import logging
import os

from database import get_db
from services.gemini_service import GeminiService
from services.ai_utils import (
    generate_cache_key,
    get_cached_result,
    set_cached_result,
    build_summarize_prompt,
    build_moderate_prompt,
    build_classify_prompt,
    build_generate_prompt,
    SUMMARIZE_CACHE_TTL,
    MODERATE_CACHE_TTL,
    CLASSIFY_CACHE_TTL,
    GENERATE_CACHE_TTL,
    TEMPLATE_PROMPTS,
)

# Day 73: Security imports
from security.prompt_safety import (
    detect_prompt_injection,
    validate_llm_response
)

# Day 73: Import rate limiter (avoid circular import by using separate limiter module)
from limiter import limiter

router = APIRouter(prefix="/ai", tags=["AI Features"])
logger = logging.getLogger(__name__)



# ==================== Pydantic Models ====================

class TextInput(BaseModel):
    """Input model for text processing endpoints."""
    text: str = Field(
        ...,
        min_length=1,
        max_length=4000,
        description="Text to process (max 4000 characters)"
    )


class SummarizeResponse(BaseModel):
    """Response model for text summarization."""
    summary: str = Field(..., description="Summarized text")
    original_length: int = Field(..., description="Original text length in characters")
    summary_length: int = Field(..., description="Summary length in characters")
    cached: bool = Field(default=False, description="Whether result was retrieved from cache")
    
    class Config:
        json_schema_extra = {
            "example": {
                "summary": "This is a concise summary of the original text.",
                "original_length": 500,
                "summary_length": 80,
                "cached": False
            }
        }


class ModerateResponse(BaseModel):
    """Response model for content moderation."""
    is_toxic: bool = Field(..., description="Whether content is toxic/harmful")
    toxicity_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Toxicity score from 0 (safe) to 1 (toxic)"
    )
    flagged_terms: list[str] = Field(
        default_factory=list,
        description="Specific harmful terms or issues detected"
    )
    cached: bool = Field(default=False, description="Whether result was retrieved from cache")
    
    class Config:
        json_schema_extra = {
            "example": {
                "is_toxic": True,
                "toxicity_score": 0.85,
                "flagged_terms": ["offensive language", "hate speech"],
                "cached": False
            }
        }


# ==================== Day 72: Classification & Generation Models ====================

class ClassifyResponse(BaseModel):
    """Response model for text classification with sentiment."""
    category: str = Field(
        ...,
        description="Content category: news, tech, sports, politics, entertainment, other"
    )
    sentiment: str = Field(
        ...,
        description="Detected sentiment: positive, negative, or neutral"
    )
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence score for the classification (0-1)"
    )
    cached: bool = Field(default=False, description="Whether result was retrieved from cache")
    
    class Config:
        json_schema_extra = {
            "example": {
                "category": "tech",
                "sentiment": "positive",
                "confidence": 0.92,
                "cached": False
            }
        }


class GenerateRequest(BaseModel):
    """Request model for template-based text generation."""
    template_type: str = Field(
        ...,
        description="Template type: email, blog, product_description"
    )
    parameters: dict = Field(
        ...,
        description="Template-specific parameters (e.g., topic, tone, length)"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "template_type": "email",
                "parameters": {
                    "topic": "Product launch announcement",
                    "tone": "professional",
                    "length": "short"
                }
            }
        }


class GenerateResponse(BaseModel):
    """Response model for text generation."""
    generated_text: str = Field(..., description="Generated content based on template")
    cached: bool = Field(default=False, description="Whether result was retrieved from cache")
    
    class Config:
        json_schema_extra = {
            "example": {
                "generated_text": "Dear Team,\n\nI'm excited to announce...",
                "cached": False
            }
        }


# ==================== Summarization Endpoint ====================

@router.post(
    "/summarize",
    response_model=SummarizeResponse,
    summary="Summarize text using AI",
    description="Uses Gemini to create a concise summary of provided text. Results cached for 1 hour. Day 73: Rate limited to 10 req/min."
)
@limiter.limit("10/minute")
async def summarize_text(
    request: Request,
    text_input: TextInput = Body(...),
    db: AsyncSession = Depends(get_db),
    gemini: GeminiService = Depends(lambda: GeminiService(os.getenv("GEMINI_API_KEY")))
):
    """
    Condense text to ~50% of its original length.
    Smart summarization that targets specific character count.
    """
    
    # Validate input length
    if len(text_input.text) > 4000:
        raise HTTPException(
            status_code=400,
            detail="Text must be 4000 characters or less"
        )
    
    # ===== DAY 73 SECURITY: Detect prompt injection =====
    if detect_prompt_injection(text_input.text):
        raise HTTPException(
            status_code=400,
            detail="Potential prompt injection detected. Request blocked for security."
        )
    
    # Generate cache key
    cache_key = generate_cache_key(text_input.text, prefix="ai:summarize")
    
    # Check Redis cache first
    cached_result = await get_cached_result(cache_key)
    if cached_result:
        return SummarizeResponse(
            **cached_result,
            cached=True  # Mark as cached
        )
    
    try:
        text_length = len(text_input.text)
        target_length = int(text_length * 0.5)  # Always target 50% of original
        
        # Calculate target sentence count based on input size
        if text_length < 500:
            sentence_count = "2 sentences"
        elif text_length < 1000:
            sentence_count = "2-3 sentences"
        elif text_length < 2000:
            sentence_count = "3-4 sentences"
        else:
            sentence_count = "4-5 sentences"
        
        # Build STRICT prompt that emphasizes character limit
        dynamic_prompt = f"""CRITICAL: The summary MUST be approximately {target_length} characters long (50% of original).

Summarize this text in exactly {sentence_count}.
Rules:
1. Be EXTREMELY concise - remove ALL unnecessary words
2. Keep ONLY the most essential information
3. NO repeated information
4. NO filler text or elaboration
5. Target exactly {target_length} characters (this is mandatory)

Original text ({text_length} chars):
{text_input.text}

VERY SHORT summary ({sentence_count}, approximately {target_length} characters):"""
        
        # Initialize Gemini service
        gemini_service = GeminiService(os.getenv("GEMINI_API_KEY"))
        
        # Get summary from Gemini (collecting all chunks)
        summary_text = ""
        async for chunk in gemini_service.generate_stream([], dynamic_prompt):
            if chunk.startswith("data: "):
                text_chunk = chunk[6:].strip()
                if text_chunk != "[DONE]":
                    summary_text += text_chunk
        
        summary_text = summary_text.strip()
        
        # ===== DAY 73 SECURITY: Validate LLM response (filter PII, check safety) =====
        try:
            summary_text, _ = validate_llm_response(summary_text)
        except ValueError as e:
            raise HTTPException(
                status_code=403,
                detail=f"Response blocked for safety: {str(e)}"
            )
        
        # ENFORCE LENGTH: If summary is too long, truncate at sentence boundary
        summary_length = len(summary_text)
        max_allowed = int(target_length * 1.3)  # Allow 30% tolerance
        
        if summary_length > max_allowed:
            # Find the last complete sentence that fits
            sentences = summary_text.split('. ')
            truncated = ""
            
            for i, sentence in enumerate(sentences):
                # Add 2 chars for '. ' separator (except last sentence)
                separator = '. ' if i < len(sentences) - 1 else ''
                test_length = len(truncated) + len(sentence) + len(separator)
                
                if test_length <= max_allowed:
                    truncated += sentence + separator
                else:
                    break
            
            # Remove trailing '. ' if present
            summary_text = truncated.rstrip('. ')
            
            if not summary_text:
                # Fallback: just truncate to max_allowed
                summary_text = summary_text[:max_allowed]
            
            logger.info(f"Summary TRUNCATED: {summary_length} → {len(summary_text)} chars to enforce 50% rule")
        
        summary_length = len(summary_text)
        reduction_percent = (summary_length / text_length) * 100
        
        # Log the results
        logger.info(f"Summarized: {text_length} chars → {summary_length} chars ({reduction_percent:.1f}% - target 50%)")
        
        # Build response
        response_data = {
            "summary": summary_text,
            "original_length": text_length,
            "summary_length": summary_length,
        }
        
        # Cache the result for 1 hour
        await set_cached_result(cache_key, response_data, SUMMARIZE_CACHE_TTL)
        
        return SummarizeResponse(**response_data, cached=False)
    
    except Exception as e:
        logger.error(f"Summarization error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Summarization failed: {str(e)}"
        )
# ==================== Content Moderation Endpoint ====================

@router.post(
    "/moderate",
    response_model=ModerateResponse,
    summary="Moderate text content for toxicity",
    description="Uses Gemini to detect toxic, harmful, or offensive content. Results cached for 30 minutes. Day 73: Rate limited to 10 req/min."
)
@limiter.limit("10/minute")
async def moderate_content(
    request: Request,
    text_input: TextInput = Body(...),
    db: AsyncSession = Depends(get_db)
):
    """
    Check text for toxic, harmful, or offensive content.
    Returns a toxicity score (0-1) and flagged terms.
    """
    
    # Validate input length
    if len(text_input.text) > 4000:
        raise HTTPException(
            status_code=400,
            detail="Text must be 4000 characters or less"
        )
    
    # ===== DAY 73 SECURITY: Detect prompt injection =====
    if detect_prompt_injection(text_input.text):
        raise HTTPException(
            status_code=400,
            detail="Potential prompt injection detected. Request blocked for security."
        )
    
    # Generate cache key
    cache_key = generate_cache_key(text_input.text, prefix="ai:moderate")
    
    # Check Redis cache first
    cached_result = await get_cached_result(cache_key)
    if cached_result:
        return ModerateResponse(
            **cached_result,
            cached=True  # Mark as cached
        )
    
    try:
        # Build prompt for Gemini
        prompt = build_moderate_prompt(text_input.text)
        
        # Initialize Gemini service
        gemini = GeminiService(os.getenv("GEMINI_API_KEY"))
        
        # Get moderation result from Gemini
        response_text = ""
        async for chunk in gemini.generate_stream([], prompt):
            if chunk.startswith("data: "):
                text_chunk = chunk[6:].strip()
                if text_chunk != "[DONE]":
                    response_text += text_chunk
        
        # Parse JSON response from LLM
        try:
            # ===== DAY 73 SECURITY: Validate LLM response (filter PII, check safety) =====
            try:
                response_text, _ = validate_llm_response(response_text)
            except ValueError as e:
                raise HTTPException(
                    status_code=403,
                    detail=f"Response blocked for safety: {str(e)}"
                )
            
            # Extract JSON from response (in case LLM returns extra text)
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start == -1 or json_end == 0:
                raise ValueError("No JSON found in response")
            
            json_str = response_text[json_start:json_end]
            llm_response = json.loads(json_str)
            
            # Extract moderation data with defaults
            is_toxic = llm_response.get("toxic", False)
            toxicity_score = float(llm_response.get("score", 0.0))
            flagged_terms = llm_response.get("reasons", [])
            
            # Validate score is in range
            toxicity_score = max(0.0, min(1.0, toxicity_score))
            
        except (json.JSONDecodeError, ValueError, TypeError) as e:
            logger.warning(f"JSON parsing error in moderation response: {str(e)}")
            # Fallback if LLM response is malformed
            raise HTTPException(
                status_code=500,
                detail="Failed to parse moderation response"
            )
        
        # Build response
        response_data = {
            "is_toxic": is_toxic,
            "toxicity_score": toxicity_score,
            "flagged_terms": flagged_terms,
        }
        
        # Cache the result for 30 minutes
        await set_cached_result(cache_key, response_data, MODERATE_CACHE_TTL)
        
        log_level = "warning" if is_toxic else "info"
        logger.log(
            logging.WARNING if is_toxic else logging.INFO,
            f"Content moderated: toxic={is_toxic}, score={toxicity_score:.2f}"
        )
        
        return ModerateResponse(**response_data, cached=False)
    
    except HTTPException:
        # Re-raise HTTP exceptions (parsing errors)
        raise
    except Exception as e:
        logger.error(f"Moderation error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Moderation failed: {str(e)}"
        )


# ==================== Day 72: Classification Endpoint ====================

@router.post(
    "/classify",
    response_model=ClassifyResponse,
    summary="Classify text with sentiment analysis",
    description="Uses Gemini to categorize text and detect sentiment. Results cached for 30 minutes. Day 73: Rate limited to 10 req/min."
)
@limiter.limit("10/minute")
async def classify_text(
    request: Request,
    text_input: TextInput = Body(...),
    db: AsyncSession = Depends(get_db)
):
    """
    Categorize text and detect its sentiment.
    Returns category, sentiment (positive/negative/neutral), and confidence score.
    """
    
    # Validate input length
    if len(text_input.text) > 2000:
        raise HTTPException(
            status_code=400,
            detail="Text must be 2000 characters or less"
        )
    
    # ===== DAY 73 SECURITY: Detect prompt injection =====
    if detect_prompt_injection(text_input.text):
        raise HTTPException(
            status_code=400,
            detail="Potential prompt injection detected. Request blocked for security."
        )
    
    # Generate cache key
    cache_key = generate_cache_key(text_input.text, prefix="ai:classify")
    
    # Check Redis cache first
    cached_result = await get_cached_result(cache_key)
    if cached_result:
        return ClassifyResponse(
            **cached_result,
            cached=True
        )
    
    try:
        # Build prompt for Gemini
        prompt = build_classify_prompt(text_input.text)
        
        # Initialize Gemini service
        gemini = GeminiService(os.getenv("GEMINI_API_KEY"))
        
        # Get classification from Gemini
        response_text = ""
        async for chunk in gemini.generate_stream([], prompt):
            if chunk.startswith("data: "):
                text_chunk = chunk[6:].strip()
                if text_chunk != "[DONE]":
                    response_text += text_chunk
        
        # Parse JSON response from LLM
        try:
            # ===== DAY 73 SECURITY: Validate LLM response (filter PII, check safety) =====
            try:
                response_text, _ = validate_llm_response(response_text)
            except ValueError as e:
                raise HTTPException(
                    status_code=403,
                    detail=f"Response blocked for safety: {str(e)}"
                )
            
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start == -1 or json_end == 0:
                raise ValueError("No JSON found in response")
            
            json_str = response_text[json_start:json_end]
            llm_response = json.loads(json_str)
            
            # Extract classification data
            category = llm_response.get("category", "other").lower()
            sentiment = llm_response.get("sentiment", "neutral").lower()
            confidence = float(llm_response.get("confidence", 0.0))
            
            # Validate category
            valid_categories = ["news", "tech", "sports", "politics", "entertainment", "other"]
            if category not in valid_categories:
                category = "other"
            
            # Validate sentiment
            valid_sentiments = ["positive", "negative", "neutral"]
            if sentiment not in valid_sentiments:
                sentiment = "neutral"
            
            # Validate confidence
            confidence = max(0.0, min(1.0, confidence))
            
        except (json.JSONDecodeError, ValueError, TypeError) as e:
            logger.warning(f"JSON parsing error in classification response: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Failed to parse classification response"
            )
        
        # Build response
        response_data = {
            "category": category,
            "sentiment": sentiment,
            "confidence": confidence,
        }
        
        # Cache the result for 30 minutes
        await set_cached_result(cache_key, response_data, CLASSIFY_CACHE_TTL)
        
        logger.info(f"Text classified: {category} ({sentiment}, {confidence:.2f})")
        
        return ClassifyResponse(**response_data, cached=False)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Classification error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Classification failed: {str(e)}"
        )


# ==================== Day 72: Text Generation Endpoint ====================

@router.post(
    "/generate",
    response_model=GenerateResponse,
    summary="Generate text from templates",
    description="Uses Gemini with template-based prompts to generate professional text. Results cached for 1 hour. Day 73: Rate limited to 10 req/min."
)
@limiter.limit("10/minute")
async def generate_text(
    request: Request,
    generate_request: GenerateRequest = Body(...),
    db: AsyncSession = Depends(get_db)
):
    """
    Generate text from templates (email, blog, product descriptions).
    Supports multiple tones and lengths for customized output.
    """
    
    # Validate template type
    if generate_request.template_type not in TEMPLATE_PROMPTS:
        raise HTTPException(
            status_code=422,
            detail=f"Invalid template_type. Must be one of: {', '.join(TEMPLATE_PROMPTS.keys())}"
        )
    
    # Generate cache key from both template type and parameters
    import json as json_module
    full_input = json_module.dumps({"type": generate_request.template_type, "params": generate_request.parameters}, sort_keys=True)
    cache_key = generate_cache_key(full_input, prefix="ai:generate")
    
    # Check Redis cache first
    cached_result = await get_cached_result(cache_key)
    if cached_result:
        return GenerateResponse(
            **cached_result,
            cached=True
        )
    
    try:
        # Build prompt based on template type
        try:
            prompt = build_generate_prompt(generate_request.template_type, generate_request.parameters)
        except KeyError as e:
            raise HTTPException(
                status_code=400,
                detail=f"Missing required parameter for {request.template_type} template: {str(e)}"
            )
        except ValueError as e:
            raise HTTPException(
                status_code=422,
                detail=str(e)
            )
        
        # Initialize Gemini service
        gemini = GeminiService(os.getenv("GEMINI_API_KEY"))
        
        # Get generated text from Gemini
        generated_text = ""
        retry_count = 0
        max_retries = 1
        
        while retry_count <= max_retries:
            try:
                async for chunk in gemini.generate_stream([], prompt):
                    if chunk.startswith("data: "):
                        text_chunk = chunk[6:].strip()
                        if text_chunk != "[DONE]":
                            generated_text += text_chunk
                break  # Success, exit retry loop
            except Exception as e:
                retry_count += 1
                if retry_count > max_retries:
                    raise  # Re-raise after max retries
                logger.warning(f"Generation attempt {retry_count} failed, retrying...")
        
        # ===== DAY 73 SECURITY: Validate LLM response (filter PII, check safety) =====
        try:
            generated_text, _ = validate_llm_response(generated_text.strip())
        except ValueError as e:
            raise HTTPException(
                status_code=403,
                detail=f"Response blocked for safety: {str(e)}"
            )
        
        # Build response
        response_data = {
            "generated_text": generated_text,
        }
        
        # Cache the result for 1 hour
        await set_cached_result(cache_key, response_data, GENERATE_CACHE_TTL)
        
        logger.info(f"Text generated: {request.template_type} ({len(generated_text)} chars)")
        
        return GenerateResponse(**response_data, cached=False)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Text generation error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Text generation failed: {str(e)}"
        )