# Day 78: Logging & Monitoring

## What This Does

Adds structured JSON logging to track every request, response, error, and API call. Logs go to both the console (for development) and files (for parsing/monitoring in production).

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python main.py

# Check health
curl http://localhost:8000/health
```

## How Logging Works

All requests are logged automatically. Logs appear in two places:

### Console Output (Human-Readable)

```
2026-01-21 14:32:45 | __main__ | INFO | Request received
2026-01-21 14:32:45 | __main__ | INFO | Response sent
```

### Log Files (JSON for Parsing)

Logs are saved to:

- `logs/app.json` - All application logs
- `logs/error.json` - Errors only (for alerts)

Each log line is valid JSON:

```json
{
  "timestamp": "2026-01-21T14:32:45Z",
  "level": "INFO",
  "name": "middleware.logging_middleware",
  "message": "Response sent",
  "method": "GET",
  "path": "/health",
  "status": 200,
  "duration_ms": 1.23
}
```

## Example Log Lines

**When a request comes in:**

```
Request received | method=GET | path=/health | client=127.0.0.1
Response sent | status=200 | duration_ms=1.23
```

**When an error occurs:**

```
Request failed | path=/chat | error=ValueError | duration_ms=45.67 | [traceback included]
```

**On app startup:**

```
Application startup | version=1.0.0
```

## Reading Logs

### In Development

Watch console output in real-time:

```bash
python main.py
```

### In Production

Parse JSON logs with jq:

```bash
# Show last 10 requests
tail -10 logs/app.json | jq .

# Find all errors
grep "ERROR" logs/error.json | jq .

# Find slow requests (> 1000ms)
cat logs/app.json | jq 'select(.duration_ms > 1000)'
```

## Health Check

Test the server is running:

```bash
curl http://localhost:8000/health
```

Response:

```json
{
  "status": "healthy",
  "message": "Chatbot API is running",
  "version": "1.0.0"
}
```

## Finding AI Usage & Errors

When you add AI endpoints later, they'll automatically log:

- AI API calls (method, tokens, latency)
- Errors with full context
- Request/response metadata

All logs go to `logs/app.json`. Filter by severity:

```bash
# Show all errors
jq 'select(.level == "ERROR")' logs/app.json

# Show all API calls over 500ms
jq 'select(.duration_ms > 500)' logs/app.json
```

## What Gets Logged

1. **Every HTTP Request**
   - Method (GET, POST, etc.)
   - Path (/health, /chat, etc.)
   - Client IP address
   - Query parameters

2. **Every HTTP Response**
   - Status code (200, 404, 500, etc.)
   - Response time in milliseconds
   - Request duration

3. **Errors**
   - Exception type
   - Error message
   - Full traceback
   - Request context (method, path)

4. **Application Events**
   - Startup/shutdown
   - Custom log messages in your code

## Next Steps

When building AI endpoints:

```python
@app.post("/chat")
async def chat(request: ChatRequest):
    logger.info("Chat request", extra={"tokens": len(request.text)})
    # ... your code ...
    logger.info("Chat response", extra={"latency_ms": duration})
```

Then check logs:

```bash
tail logs/app.json | jq 'select(.message == "Chat response")'
```

## That's It!

Logging is automatic. No changes needed to existing code. Just run the app and logs appear in:

- Console (development)
- `logs/app.json` (all logs)
- `logs/error.json` (errors only)
