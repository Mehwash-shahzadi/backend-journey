# LLM API Setup & Comparison

Getting started with Large Language Model (LLM) APIs. This guide covers account setup, API testing, and understanding different LLM providers for backend integration.

## What Are LLM APIs?

LLM APIs let your backend applications access powerful AI models for tasks like:

- Text generation and completion
- Content summarization
- Question answering
- Code generation
- Translation
- Data extraction

Instead of running models locally (expensive and complex), you send requests to cloud APIs.

## Popular LLM Providers

### Google Gemini

- **Models**: Gemini Pro, Gemini Pro Vision
- **Free Tier**: Yes (60 requests/minute)
- **Pricing**: $0.00025/1K characters (very affordable)
- **Strengths**: Fast, good for production, multimodal
- **Best For**: General purpose, cost-effective apps

### OpenAI

- **Models**: GPT-4, GPT-3.5 Turbo
- **Free Tier**: Limited trial credits
- **Pricing**: $0.03/1K tokens (GPT-4)
- **Strengths**: Most powerful, best quality
- **Best For**: Complex reasoning, creative writing

### Anthropic Claude

- **Models**: Claude 3 Opus, Claude 3 Sonnet
- **Free Tier**: No
- **Pricing**: $0.015/1K tokens
- **Strengths**: Long context, safety-focused
- **Best For**: Document analysis, conversations

### Open Source (Ollama)

- **Models**: Llama 2, Mistral, CodeLlama
- **Free Tier**: Yes (self-hosted)
- **Pricing**: Free (infrastructure costs only)
- **Strengths**: Privacy, no API limits
- **Best For**: Sensitive data, unlimited usage

## Provider Comparison

| Feature            | Gemini     | OpenAI        | Claude    | Open Source |
| ------------------ | ---------- | ------------- | --------- | ----------- |
| **Free Tier**      | Yes        | Limited       | No        | Yes         |
| **Cost/1K tokens** | $0.00025   | $0.03         | $0.015    | Free        |
| **Speed**          | Fast       | Medium        | Fast      | Varies      |
| **Quality**        | Good       | Excellent     | Excellent | Good        |
| **Rate Limit**     | 60/min     | 3500/min      | 50/min    | Unlimited   |
| **Context Length** | 32K        | 128K          | 200K      | 4K-32K      |
| **Best Use Case**  | Production | Complex tasks | Long docs | Privacy     |

**My Choice:** Starting with Gemini for its generous free tier and good quality.

## Setup Instructions

### 1. Get Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with Google account
3. Click "Create API Key"
4. Copy the key (starts with `AIza...`)

### 2. Store API Key Securely

Create `.env` file:

```env
GEMINI_API_KEY=AIzaSy...your_key_here
GEMINI_MODEL=gemini-1.5-flash
```

Add to `.gitignore`:

```
.env
```

### 3. Test API with Curl

```bash
curl -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=YOUR_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "contents": [{
      "parts": [{
        "text": "Explain what FastAPI is in simple terms"
      }]
    }]
  }'
```

### 4. Test with Python

```python
import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"

payload = {
    "contents": [{
        "parts": [{
            "text": "Write a haiku about coding"
        }]
    }]
}

response = requests.post(url, json=payload)
result = response.json()

print(result["candidates"][0]["content"]["parts"][0]["text"])
```

## Understanding the Response

**Request:**

```json
{
  "contents": [
    {
      "parts": [
        {
          "text": "What is Python?"
        }
      ]
    }
  ]
}
```

**Response:**

```json
{
  "candidates": [
    {
      "content": {
        "parts": [
          {
            "text": "Python is a high-level programming language..."
          }
        ]
      },
      "finishReason": "STOP"
    }
  ],
  "usageMetadata": {
    "promptTokenCount": 4,
    "candidatesTokenCount": 45,
    "totalTokenCount": 49
  }
}
```

**Key Fields:**

- `candidates[0].content.parts[0].text` - The AI's response
- `finishReason` - Why it stopped (STOP = natural end, MAX_TOKENS = hit limit)
- `usageMetadata` - Token usage for billing

## Token Usage & Pricing

**What are tokens?**
Roughly 1 token = 4 characters in English. So "Hello World" ≈ 3 tokens.

**Gemini Pricing:**

- Input: $0.00025 per 1K characters
- Output: $0.00025 per 1K characters

**Example Cost:**

```
Prompt: 100 characters = $0.000025
Response: 400 characters = $0.0001
Total: $0.000125 (basically free)
```

**Free Tier Limits:**

- 60 requests per minute
- 1500 requests per day
- More than enough for development

## Rate Limiting

**Gemini Free Tier:**

- 60 requests/minute (RPM)
- 1500 requests/day (RPD)

**Handling Rate Limits:**

```python
import time

def call_gemini_with_retry(prompt, max_retries=3):
    for i in range(max_retries):
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 429:  # Rate limit
                wait_time = 2 ** i  # Exponential backoff
                time.sleep(wait_time)
                continue
            return response.json()
        except Exception as e:
            print(f"Error: {e}")
    return None
```

## Security Best Practices

**Never:**

- Commit API keys to Git
- Share keys in screenshots
- Use keys in client-side code
- Hardcode keys in files

**Always:**

- Store keys in `.env`
- Use environment variables
- Rotate keys periodically
- Monitor usage for anomalies

## Testing Checklist

- [ ] Created Google AI Studio account
- [ ] Generated API key
- [ ] Stored key in `.env`
- [ ] Tested API with curl
- [ ] Tested API with Python
- [ ] Understood response structure
- [ ] Calculated token costs
- [ ] Documented rate limits

## Common Issues

**401 Unauthorized:**
Check API key is correct and copied completely.

**429 Too Many Requests:**
Hit rate limit. Wait 60 seconds and retry.

**400 Bad Request:**
Check JSON structure matches API documentation.

**Empty Response:**
Model might be filtering content. Try different phrasing.

## What You Learn

- How to get and secure API keys
- LLM API request/response structure
- Token counting and pricing
- Rate limit handling
- Comparing different LLM providers
- Foundation for AI integration
