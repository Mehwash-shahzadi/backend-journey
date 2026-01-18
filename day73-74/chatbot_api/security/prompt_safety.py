import re
import logging

logger = logging.getLogger(__name__)


# ==================== PROMPT INJECTION DETECTION ====================

def detect_prompt_injection(user_input: str) -> bool:
    """
    Detect common jailbreak and prompt injection patterns.
    
    Args:
        user_input: User-provided text to check
        
    Returns:
        True if potential injection detected, False otherwise
        
    Security Note:
        Blocks patterns like "ignore previous instructions", "forget all", 
        "system:", "you are now", "act as", etc.
    """
    
    # Common jailbreak/injection patterns
    injection_patterns = [
        "ignore previous instructions",
        "forget all",
        "system:",
        "you are now",
        "act as",
        "disregard",
        "new role",
        "role:",
        "prompt:",
        "jailbreak",
        "override",
        "bypass",
        "ignore safety",
        "disable filters",
        "pretend",
        "imagine you",
        "hypothetically",
        "in this scenario"
    ]
    
    user_input_lower = user_input.lower().strip()
    
    # Check each pattern
    for pattern in injection_patterns:
        if pattern in user_input_lower:
            logger.warning(f"Prompt injection detected: pattern='{pattern}' in user input")
            return True
    
    return False


# ==================== PII DETECTION & REDACTION ====================

def filter_pii_from_response(response: str) -> tuple[str, int]:
    """
    Detect and redact personally identifiable information (PII) from LLM responses.
    
    Redacts:
    - Email addresses (user@example.com)
    - Phone numbers (123-456-7890, +1 234 567 8900)
    - Credit card numbers (4532-1234-5678-9010)
    - Social Security Numbers (123-45-6789)
    - API keys (sk-..., starts with patterns)
    
    Args:
        response: LLM response text to filter
        
    Returns:
        Tuple of (filtered_response, pii_count) where pii_count is number of items redacted
    """
    
    original = response
    pii_count = 0
    
    # Email addresses (simple pattern)
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    matches = len(re.findall(email_pattern, response))
    if matches > 0:
        response = re.sub(email_pattern, '[REDACTED_EMAIL]', response)
        pii_count += matches
        logger.warning(f"Found {matches} email(s) in LLM response - redacting")
    
    # Phone numbers (multiple formats)
    phone_pattern = r'\b(?:\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})\b'
    matches = len(re.findall(phone_pattern, response))
    if matches > 0:
        response = re.sub(phone_pattern, '[REDACTED_PHONE]', response)
        pii_count += matches
        logger.warning(f"Found {matches} phone number(s) in LLM response - redacting")
    
    # Credit card numbers (simple: 16 digits)
    cc_pattern = r'\b(?:\d{4}[-\s]?){3}\d{4}\b'
    matches = len(re.findall(cc_pattern, response))
    if matches > 0:
        response = re.sub(cc_pattern, '[REDACTED_CC]', response)
        pii_count += matches
        logger.warning(f"Found {matches} credit card number(s) in LLM response - redacting")
    
    # Social Security Numbers (XXX-XX-XXXX)
    ssn_pattern = r'\b\d{3}-\d{2}-\d{4}\b'
    matches = len(re.findall(ssn_pattern, response))
    if matches > 0:
        response = re.sub(ssn_pattern, '[REDACTED_SSN]', response)
        pii_count += matches
        logger.warning(f"Found {matches} SSN(s) in LLM response - redacting")
    
    # API keys (simple pattern: sk-... or similar)
    api_key_pattern = r'\b(sk-|api-|token-)[A-Za-z0-9_-]{20,}\b'
    matches = len(re.findall(api_key_pattern, response))
    if matches > 0:
        response = re.sub(api_key_pattern, '[REDACTED_KEY]', response)
        pii_count += matches
        logger.warning(f"Found {matches} API key(s) in LLM response - redacting")
    
    if pii_count > 0:
        logger.info(f"Total {pii_count} PII item(s) redacted from LLM response")
    
    return response, pii_count


# ==================== SAFETY CHECKS ====================

def check_response_safety(response: str) -> tuple[bool, str]:
    """
    Check if LLM response contains harmful/unsafe content.
    
    Blocks responses containing:
    - Hate speech keywords
    - Violence/harm instructions
    - Illegal content references
    
    Args:
        response: LLM response to check
        
    Returns:
        Tuple of (is_safe, reason) where is_safe is True if response passes safety check
    """
    
    # Safety-critical keywords that should not appear in responses
    unsafe_keywords = {
        "hate": ["hate speech", "kill", "die", "hurt", "murder", "suicide", "bomb"],
        "illegal": ["steal", "hack", "fraud", "launder", "traffick", "illegal drug"],
        "harm": ["self harm", "self-harm", "hurt yourself", "end your life", "overdose"],
        "exploitation": ["exploit", "abuse", "molest", "rape", "child"]
    }
    
    response_lower = response.lower()
    
    # Check each category
    for category, keywords in unsafe_keywords.items():
        for keyword in keywords:
            if keyword in response_lower:
                reason = f"Response contains unsafe content ({category}): {keyword}"
                logger.warning(f"Safety check failed: {reason}")
                return False, reason
    
    # Response passed safety check
    return True, "Response passed safety validation"


# ==================== COMBINED SAFETY CHECK ====================

def validate_llm_response(response: str) -> tuple[str, bool]:
    """
    Complete safety validation pipeline for LLM responses.
    
    1. Filters PII (redacts sensitive data)
    2. Checks for harmful/unsafe content
    
    Args:
        response: Raw LLM response
        
    Returns:
        Tuple of (filtered_response, is_safe) where:
        - filtered_response: Response with PII redacted
        - is_safe: True if response passed all safety checks
        
    Raises:
        ValueError: If response contains unsafe content
    """
    
    # Step 1: Redact PII
    filtered_response, pii_count = filter_pii_from_response(response)
    
    # Step 2: Check safety
    is_safe, safety_reason = check_response_safety(filtered_response)
    
    if not is_safe:
        raise ValueError(f"Response failed safety check: {safety_reason}")
    
    return filtered_response, is_safe
