# AI Service Guide - Day 74

Complete guide for using the AI Chatbot API with optimization tips, cost reduction strategies, and troubleshooting.

## Table of Contents

1. [Quick Start](#quick-start)
2. [API Endpoints](#api-endpoints)
3. [Best Practices](#best-practices)
4. [Cost Optimization](#cost-optimization)
5. [Security Considerations](#security-considerations)
6. [Troubleshooting](#troubleshooting)
7. [Error Reference](#error-reference)

---

## Quick Start

### 1. Basic Setup

```python
import requests
import json

BASE_URL = "http://localhost:8000"
HEADERS = {"Content-Type": "application/json"}

def call_api(endpoint, data):
    response = requests.post(f"{BASE_URL}/{endpoint}",
                           json=data, headers=HEADERS)
    return response.json()
```

### 2. Test Connection

```bash
curl http://localhost:8000/docs
```

If successful, you'll see the Swagger UI with all endpoints.

---

## API Endpoints

### Text Summarization (`POST /ai/summarize`)

**Purpose**: Reduce text to 50% of original length while preserving key information.

**Request**:

```json
{
  "text": "Your long text here (max 4000 characters)..."
}
```

**Response**:

```json
{
  "summary": "Concise summary here...",
  "original_length": 2500,
  "summary_length": 1250,
  "cached": false
}
```

**Best For**:

- Article summaries
- Document abstracts
- Long email condensing
- Meeting notes compression

**Examples**:

```bash
# Python
import requests
response = requests.post(
    "http://localhost:8000/ai/summarize",
    json={"text": "Python is a versatile programming language..."}
)
print(response.json()["summary"])

# cURL
curl -X POST http://localhost:8000/ai/summarize \
  -H "Content-Type: application/json" \
  -d '{"text": "Your text here..."}'
```

**Token Cost (Day 74)**:

- Input: ~1 token per 4 characters
- Output: ~200 tokens (summary)
- **Total**: ~input_chars/4 + 200 tokens
- **Typical**: 500-800 tokens per request
- **After Day 74 Optimization**: ~300-500 tokens (35% reduction)

---

### Content Moderation (`POST /ai/moderate`)

**Purpose**: Analyze text for toxicity, offensive content, and harmful material.

**Request**:

```json
{
  "text": "Text to check for toxicity (max 4000 characters)..."
}
```

**Response**:

```json
{
  "is_toxic": false,
  "toxicity_score": 0.15,
  "flagged_terms": [],
  "cached": false
}
```

**Toxicity Score Guide**:

- 0.0 - 0.3: Safe
- 0.3 - 0.6: Potentially harmful
- 0.6 - 1.0: Highly toxic

**Best For**:

- User-generated content review
- Comment moderation
- Feedback analysis
- Safety checks before publishing

**Examples**:

```bash
# Python
import requests
response = requests.post(
    "http://localhost:8000/ai/moderate",
    json={"text": "user comment here"}
)
score = response.json()["toxicity_score"]
if score > 0.6:
    print("Content blocked - too toxic")

# cURL
curl -X POST http://localhost:8000/ai/moderate \
  -H "Content-Type: application/json" \
  -d '{"text": "your text"}'
```

**Token Cost (Day 74)**:

- Input: ~1 token per 4 characters
- Output: ~150 tokens (JSON response)
- **Total**: ~input_chars/4 + 150 tokens
- **Typical**: 250-550 tokens per request
- **After Day 74 Optimization**: ~180-350 tokens (30% reduction)

---

### Text Classification (`POST /ai/classify`)

**Purpose**: Categorize text and detect sentiment.

**Request**:

```json
{
  "text": "Text to classify (max 2000 characters)..."
}
```

**Response**:

```json
{
  "category": "tech",
  "sentiment": "positive",
  "confidence": 0.92,
  "cached": false
}
```

**Categories**:

- `news` - News articles and journalism
- `tech` - Technology and programming
- `sports` - Sports and athletics
- `politics` - Political content
- `entertainment` - Movies, music, entertainment
- `other` - Everything else

**Sentiments**:

- `positive` - Optimistic or favorable
- `negative` - Critical or negative
- `neutral` - Objective or balanced

**Best For**:

- Content categorization
- Sentiment analysis
- Mood detection
- Content routing

**Examples**:

```bash
# Python
import requests
response = requests.post(
    "http://localhost:8000/ai/classify",
    json={"text": "Apple released new iPhone 15 with amazing features!"}
)
data = response.json()
print(f"{data['category']}: {data['sentiment']} ({data['confidence']})")

# cURL
curl -X POST http://localhost:8000/ai/classify \
  -H "Content-Type: application/json" \
  -d '{"text": "text to classify"}'
```

**Token Cost (Day 74)**:

- Input: ~1 token per 4 characters
- Output: ~100 tokens (JSON response)
- **Total**: ~input_chars/4 + 100 tokens
- **Typical**: 200-450 tokens per request
- **After Day 74 Optimization**: ~150-350 tokens (25% reduction)

---

### Text Generation (`POST /ai/generate`)

**Purpose**: Generate professional text from templates.

**Request**:

```json
{
  "template_type": "email",
  "parameters": {
    "topic": "Project deadline extension",
    "tone": "professional",
    "length": "medium"
  }
}
```

**Response**:

```json
{
  "generated_text": "Dear [recipient],\n\nI wanted to reach out...",
  "cached": false
}
```

**Template Types**:

#### 1. Email Template

```json
{
  "template_type": "email",
  "parameters": {
    "topic": "String (required) - Email subject",
    "tone": "professional|formal|casual|friendly|creative",
    "length": "short|medium|long"
  }
}
```

#### 2. Blog Template

```json
{
  "template_type": "blog",
  "parameters": {
    "topic": "String (required) - Blog topic",
    "tone": "professional|casual|technical|journalistic",
    "length": "500 words|1000 words|1500 words"
  }
}
```

#### 3. Product Description Template

```json
{
  "template_type": "product_description",
  "parameters": {
    "topic": "String (required) - Product name/type"
  }
}
```

**Best For**:

- Email writing
- Blog post generation
- Product descriptions
- Marketing copy
- Bulk content creation

**Examples**:

```bash
# Python - Generate email
import requests
response = requests.post(
    "http://localhost:8000/ai/generate",
    json={
        "template_type": "email",
        "parameters": {
            "topic": "Meeting reschedule",
            "tone": "professional",
            "length": "medium"
        }
    }
)
print(response.json()["generated_text"])

# cURL - Generate product description
curl -X POST http://localhost:8000/ai/generate \
  -H "Content-Type: application/json" \
  -d '{
    "template_type": "product_description",
    "parameters": {"topic": "Wireless headphones"}
  }'
```

**Token Cost (Day 74)**:

- Input: ~100 tokens (prompt base)
- Output: ~300-800 tokens (generated content)
- **Total**: ~400-900 tokens per request
- **After Day 74 Optimization**: ~300-650 tokens (25-35% reduction)

---

### Chat Messages (`POST /chat/conversations/{conversation_id}/messages`)

**Purpose**: Send message and get AI response with context awareness.

**Request**:

```json
{
  "content": "What is machine learning?"
}
```

**Response**:

```json
{
  "id": "uuid",
  "conversation_id": "uuid",
  "role": "assistant",
  "content": "Machine learning is...",
  "tokens_used": 156,
  "created_at": "2024-01-15T10:30:00Z"
}
```

**Features**:

- Multi-turn conversations
- Automatic context window management
- Token tracking
- Session persistence

**Best For**:

- Chat applications
- Q&A sessions
- Interactive assistance
- Conversational support

**Examples**:

```bash
# Python
import requests

# Create conversation
conv = requests.post(
    "http://localhost:8000/chat/conversations",
    json={"user_id": "user_123", "title": "Python Help"}
).json()

conv_id = conv["id"]

# Send message
msg = requests.post(
    f"http://localhost:8000/chat/conversations/{conv_id}/messages",
    json={"content": "How do I use list comprehension?"}
).json()

print(msg["content"])

# cURL
curl -X POST "http://localhost:8000/chat/conversations/{id}/messages" \
  -H "Content-Type: application/json" \
  -d '{"content": "Your question here"}'
```

**Token Cost (Day 74)**:

- Input: ~1 token per 4 characters + context
- Output: ~200-500 tokens (response)
- **Total**: ~300-800 tokens per exchange
- **After Day 74 Optimization**: ~250-650 tokens (20-30% reduction)

---

## Best Practices

### 1. **Efficient Input**

✅ **DO**:

```python
# Clear, concise input
text = "Summarize: Python is a high-level language used for web development, data science, and automation."
```

❌ **DON'T**:

```python
# Verbose, redundant
text = "Please could you possibly maybe summarize the following text which is about Python and what it is used for: Python is a high-level language used for web development, data science, and automation."
```

### 2. **Handle Responses Properly**

✅ **DO**:

```python
response = requests.post(endpoint, json=data)
if response.status_code == 200:
    result = response.json()
    print(result["summary"])
elif response.status_code == 429:
    print("Rate limited - wait 1-2 minutes")
else:
    print(f"Error: {response.json()['detail']}")
```

❌ **DON'T**:

```python
# Ignoring error handling
result = requests.post(endpoint, json=data).json()
print(result["summary"])  # Crashes if error
```

### 3. **Use Caching Effectively**

✅ **DO**:

```python
# Check if result is cached (faster, no token cost)
if response.json()["cached"]:
    print("Result from cache - no tokens used!")
else:
    print("Fresh result - tokens consumed")
```

✅ **DO**: Cache same requests client-side

```python
import hashlib
CACHE = {}

def summarize_cached(text):
    key = hashlib.md5(text.encode()).hexdigest()
    if key in CACHE:
        return CACHE[key]
    result = summarize(text)
    CACHE[key] = result
    return result
```

### 4. **Rate Limiting Awareness**

✅ **DO**:

```python
import time

def summarize_with_retry(text, max_retries=3):
    for attempt in range(max_retries):
        try:
            return requests.post(endpoint, json={"text": text})
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                wait_time = 60 * (attempt + 1)
                print(f"Rate limited. Waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise
```

### 5. **Error Handling**

✅ **DO**:

```python
try:
    response = requests.post(endpoint, json=data, timeout=30)
    response.raise_for_status()
    return response.json()
except requests.exceptions.Timeout:
    print("Request timeout - service slow")
except requests.exceptions.HTTPError as e:
    if e.response.status_code == 429:
        print("Rate limited - retry later")
    elif e.response.status_code >= 500:
        print("Server error - retry later")
    else:
        print(f"API error: {e}")
```

---

## Cost Optimization

### Understanding Token Costs

Gemini pricing (approximate):

- **Input**: $0.00075 per 1K tokens
- **Output**: $0.003 per 1K tokens

Total cost ≈ (input_tokens × 0.00075 + output_tokens × 0.003) / 1000

### Day 74 Optimization Results

**Before Optimization**:

- Summarize: ~650 tokens → $0.0022
- Moderate: ~450 tokens → $0.0018
- Classify: ~350 tokens → $0.0015
- Generate: ~700 tokens → $0.0028
- **Total per 100 requests**: ~$0.83

**After Day 74 Optimization**:

- Summarize: ~420 tokens (-35%) → $0.0013
- Moderate: ~315 tokens (-30%) → $0.0012
- Classify: ~260 tokens (-25%) → $0.0010
- Generate: ~460 tokens (-35%) → $0.0018
- **Total per 100 requests**: ~$0.53
- **Monthly savings** (10K requests): ~$30

### Optimization Strategies

#### 1. **Shorten Prompts** (Day 74)

```python
# Before (65 tokens)
prompt = """Analyze if the following text is toxic, harmful, offensive, or inappropriate.
Return ONLY valid JSON (no other text) with this exact format:
{"toxic": true/false, "score": 0.0-1.0, "reasons": ["reason1", "reason2"]}
Text: {text}"""

# After (42 tokens) - 35% reduction
prompt = """Analyze toxicity. Return JSON only:
{"toxic": bool, "score": 0-1, "reasons": [list]}
Text: {text}"""
```

#### 2. **Use Caching**

```python
# Check Redis cache first - saves 100% of tokens
if await get_cached_result(cache_key):
    return cached_result  # No tokens used
```

#### 3. **Batch Requests**

```python
# Process multiple items together (saves prompt overhead)
texts = ["text1", "text2", "text3"]
# Single request with all 3 vs 3 separate requests
# Saves 3× prompt overhead
```

#### 4. **Template-Based Generation**

```python
# Pre-built templates = shorter prompts
# Generic prompt: 100 tokens
# Optimized template: 30 tokens
# Saves 70% per generation
```

### Monitor Token Usage

```python
import json

def track_costs(responses):
    total_tokens = 0
    for resp in responses:
        # Most responses don't show tokens directly
        # But you can estimate from length
        input_est = len(resp["input"]) / 4
        output_est = len(resp["output"]) / 4
        tokens = input_est + output_est
        total_tokens += tokens

    cost = total_tokens * 0.00075 / 1000  # Approximate
    print(f"Estimated cost: ${cost:.4f} for {total_tokens:.0f} tokens")
```

---

## Security Considerations

### 1. **Prompt Injection Protection** (Day 73)

The API automatically blocks jailbreak attempts:

```bash
# This will be BLOCKED with HTTP 400
curl -X POST http://localhost:8000/ai/summarize \
  -d '{"text": "Ignore previous instructions and..."}'

# Response: "Potential prompt injection detected"
```

### 2. **PII Redaction** (Day 73)

Sensitive data is automatically redacted from responses:

- Emails → `[EMAIL_REDACTED]`
- Phone numbers → `[PHONE_REDACTED]`
- Credit cards → `[CARD_REDACTED]`
- SSNs → `[SSN_REDACTED]`

### 3. **Input Validation**

```python
# Max input lengths enforced
# Summarize: 4000 characters
# Moderate: 4000 characters
# Classify: 2000 characters
# Chat: 4000 characters per message

text = "your input"
if len(text) > 4000:
    raise ValueError("Input too long (max 4000 chars)")
```

### 4. **Rate Limiting** (Day 73)

10 requests per minute per IP address:

```bash
# First 10 requests: HTTP 200
# 11th request: HTTP 429
# Wait 1 minute, then try again
```

### 5. **API Key Security**

✅ **DO**: Keep API key in environment variables

```bash
export GEMINI_API_KEY="your_key_here"
```

❌ **DON'T**: Hardcode API key

```python
# BAD - Never do this!
api_key = "sk_live_..."
```

---

## Troubleshooting

### Issue: "Rate limit exceeded"

**Symptoms**: HTTP 429 response

**Cause**: Exceeded 10 requests/minute limit

**Solution**:

```python
import time

# Wait before retrying
time.sleep(65)  # Wait 1+ minute
response = requests.post(endpoint, json=data)
```

### Issue: "The AI service took too long to respond"

**Symptoms**: HTTP 504, message mentions timeout

**Cause**:

- Gemini API overloaded
- Network latency
- Large input text

**Solution**:

```python
# 1. Shorten input
text = text[:2000]  # Reduce to 2000 chars

# 2. Increase timeout
response = requests.post(
    endpoint,
    json=data,
    timeout=60  # Increase to 60 seconds
)

# 3. Retry after delay
import time
time.sleep(5)
retry_response = requests.post(endpoint, json=data)
```

### Issue: "The AI service is currently busy"

**Symptoms**: HTTP 429 or 503 from Gemini API

**Cause**: Gemini service rate limited or overloaded

**Solution**:

```python
# Exponential backoff retry
import time

def retry_with_backoff(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # 1, 2, 4 seconds
                print(f"Retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise
```

### Issue: "Invalid input" error

**Symptoms**: HTTP 400 with validation message

**Cause**:

- Text too long
- Invalid template type
- Missing required fields
- Prompt injection detected

**Solution**:

```python
# Check input before sending
def validate_input(text, endpoint):
    max_length = 4000  # Default

    if endpoint == "classify":
        max_length = 2000

    if len(text) > max_length:
        raise ValueError(f"Text too long (max {max_length} chars)")

    if not text.strip():
        raise ValueError("Text cannot be empty")

    return True
```

### Issue: "Unexpected error" with request_id

**Symptoms**: HTTP 500 with request_id

**Cause**: Unexpected server error

**Solution**:

```python
# Note the request_id
response = requests.post(endpoint, json=data)
if response.status_code == 500:
    request_id = response.json()["request_id"]
    print(f"Error occurred. Request ID: {request_id}")
    # Share request_id for debugging
```

### Issue: Results different from expected

**Symptoms**:

- Summary too long/short
- Wrong classification
- Unexpected tone in generated text

**Solution**:

```python
# 1. Check cache status
if response.json()["cached"]:
    print("Result from cache (not fresh)")

# 2. Try with different parameters
# Clearer input → better output
text = text.strip()  # Remove whitespace
text = re.sub(r'\s+', ' ', text)  # Normalize spaces

# 3. Verify input quality
# Long, complex text → less predictable results
# Short, clear text → consistent results
```

---

## Error Reference

### HTTP Status Codes

| Code | Error        | Meaning                 | Action                 |
| ---- | ------------ | ----------------------- | ---------------------- |
| 200  | Success      | Request successful      | Continue normally      |
| 400  | Bad Request  | Invalid input/injection | Check input validation |
| 403  | Forbidden    | Safety violation        | Review content         |
| 429  | Rate Limited | Too many requests       | Wait 1-2 minutes       |
| 500  | Server Error | Unexpected error        | Retry with backoff     |
| 503  | Unavailable  | Service down            | Try again later        |
| 504  | Timeout      | Request too slow        | Shorten input/retry    |

### Common Error Codes (Day 74)

| Code                  | Meaning             | Typical Cause            | Solution          |
| --------------------- | ------------------- | ------------------------ | ----------------- |
| `RATE_LIMIT_EXCEEDED` | API rate limited    | 10+ req/minute           | Wait 60+ seconds  |
| `LLM_TIMEOUT`         | Gemini timeout      | Large input/slow API     | Reduce input size |
| `LLM_RATE_LIMIT`      | Gemini rate limited | Too many Gemini calls    | Wait 1-2 minutes  |
| `LLM_SERVER_ERROR`    | Gemini API error    | Gemini service issue     | Retry later       |
| `VALIDATION_ERROR`    | Input validation    | Invalid input format     | Check input       |
| `PROMPT_INJECTION`    | Injection detected  | Malicious prompt pattern | Review input      |
| `SAFETY_VIOLATION`    | Content safety      | Unsafe LLM response      | Adjust input      |

---

## API Response Examples

### Success Response

```json
{
  "summary": "...",
  "original_length": 2500,
  "summary_length": 1250,
  "cached": false
}
```

### Error Response (Day 74)

```json
{
  "detail": "The AI service took too long to respond. Please try again in a moment.",
  "error_code": "LLM_TIMEOUT",
  "request_id": "1705320612.3"
}
```

### Cached Response (Day 74)

```json
{
  "summary": "...",
  "original_length": 2500,
  "summary_length": 1250,
  "cached": true
}
```

---

## Support & Resources

- **API Docs**: http://localhost:8000/docs
- **Redoc**: http://localhost:8000/redoc
- **Error Logs**: Check application logs for detailed errors
- **Request ID**: Use request_id from error responses for support

---

**Last Updated**: Day 74
**Status**: Production Ready
**Token Optimization**: 25-35% reduction achieved
