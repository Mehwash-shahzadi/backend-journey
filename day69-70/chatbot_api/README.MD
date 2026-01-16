# AI Chatbot Backend with Persistent Storage

A production-ready chatbot backend built over Days 69-70. Features conversation management, message history, intelligent context trimming, and real-time streaming - all stored in PostgreSQL.

## What This Does

A complete backend for a ChatGPT-like application with:

- Multiple conversations per user
- Full message history stored in database
- Auto-generated conversation titles
- Smart context window management (prevents token overflow)
- Streaming responses for better UX
- Token usage tracking

## Features

**Conversation Management:**

- Create multiple chat conversations
- List all user conversations
- Auto-generate titles from first message
- Track creation and update times

**Message Handling:**

- Store complete chat history
- Track tokens used per message
- Stream responses in real-time
- Automatic context window trimming

**Smart Context:**

- Keeps last 20 messages for AI context
- Auto-trims old messages when limit exceeded
- Always preserves minimum 10 messages
- Prevents unbounded token growth

## Project Structure

```
day69-70/chatbot_api/
├── main.py                   # FastAPI application
├── config.py                 # Settings (context limits, etc.)
├── database.py               # Database connection
├── models/
│   ├── conversation.py       # Conversation table
│   └── message.py            # Messages table
├── schemas/
│   ├── conversation.py       # Request/response models
│   └── message.py
├── crud/
│   ├── conversation.py       # Database operations
│   └── message.py
├── services/
│   └── gemini_service.py     # Gemini API integration
└── routers/
    └── chat.py               # All endpoints
```

## Quick Setup

### 🐳 Option 1: Using Docker (Easiest - Recommended!)

Everything runs in containers. Your computer stays clean!

**What you need:**

- Docker and Docker Compose installed
- That's it! No need to install PostgreSQL locally.

**Let's go:**

1. **Start the database (PostgreSQL in a container):**

```bash
docker-compose up -d
```

Docker will download the PostgreSQL image and start it. You'll see:

```
Creating chatbot-postgres ... done
```

Verify it's running:

```bash
docker-compose ps
```

You should see the `chatbot-postgres` container listed and running

2. **Set up your Gemini API key:**

```bash
# Create .env file with your key
echo 'GEMINI_API_KEY=your_api_key_here' > .env
```

3. **Install Python packages and run the app:**

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

4. **Visit the API:**

- Open http://localhost:8000/docs
- Try it out! 🚀

**Handy Docker commands:**

```bash
# See what's running
docker-compose ps

# View database logs (helpful for debugging)
docker-compose logs db

# Stop everything (data is saved)
docker-compose down

# Stop and delete everything (fresh start)
docker-compose down -v

# Restart after changes
docker-compose restart
```

**Database details (inside Docker):**

- Host: `localhost`
- Port: `5433` (host) → maps to `5432` (container)
- User: `postgres`
- Password: `postgres`
- Database: `chatbot_db`

---

### 💻 Option 2: Local Setup (Without Docker)

Want to run everything on your machine directly?

**What you need:**

- Python 3.11+
- PostgreSQL installed locally
- Port 5432 available

**Let's go:**

1. **Install Python dependencies:**

```bash
pip install -r requirements.txt
```

2. **Create your `.env` file:**

```env
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/chatbot_db
GEMINI_API_KEY=your_api_key_here
```

(Replace `password` with your PostgreSQL password)

3. **Create the database:**

```bash
createdb chatbot_db
```

(If you're on Windows or that doesn't work, use pgAdmin or your PostgreSQL tool)

4. **Run migrations to create tables:**

```bash
alembic upgrade head
```

This creates the `conversations` and `messages` tables.

5. **Start the server:**

```bash
uvicorn main:app --reload
```

6. **Open http://localhost:8000/docs** and start chatting!

---

## Docker Troubleshooting

### "Port already in use"

If you get an error about port 5433 being in use:

```bash
# See what's using the port
lsof -i :5433  # macOS/Linux
netstat -ano | findstr :5433  # Windows

# Kill the process or change the port in docker-compose.yml
# Change "5433:5432" to "5434:5432" for example
```

### "Can't connect to database"

Make sure Docker container is running:

```bash
docker-compose ps
```

If not running, start it:

```bash
docker-compose up -d
```

### "Permission denied" on docker commands

Try adding `sudo` (macOS/Linux):

```bash
sudo docker-compose up -d
```

Or restart Docker Desktop if on Windows/Mac.

### Want to see database contents?

```bash
# Connect to PostgreSQL inside Docker
docker-compose exec db psql -U postgres -d chatbot_db

# Inside psql, try:
SELECT * FROM conversations;
SELECT * FROM messages;
\q  # Exit psql
```

### Fresh start (delete all data)

```bash
# Stop containers and remove volumes (data)
docker-compose down -v

# Start fresh
docker-compose up -d
```

---

## API Endpoints

### Create Conversation

```bash
POST /chat/conversations
{
  "user_id": "alice"
}

Response:
{
  "id": "uuid-here",
  "user_id": "alice",
  "title": null,
  "created_at": "2026-01-16T10:30:00Z"
}
```

### Send Message (Get AI Response)

```bash
POST /chat/conversations/{conversation_id}/messages
{
  "content": "What is machine learning?"
}

Response:
{
  "id": "uuid-here",
  "conversation_id": "...",
  "role": "assistant",
  "content": "Machine learning is a subset of AI...",
  "tokens_used": 156,
  "created_at": "2026-01-16T10:31:00Z"
}
```

### Stream Response (Real-Time)

```bash
GET /chat/conversations/{conversation_id}/stream?message=Hello

Response (SSE):
data: Hello!
data: I'm here
data: to help
data: [DONE]
```

### Get Chat History

```bash
GET /chat/conversations/{conversation_id}/messages

Response:
[
  {
    "role": "user",
    "content": "What is Python?",
    "created_at": "..."
  },
  {
    "role": "assistant",
    "content": "Python is a programming language...",
    "tokens_used": 45,
    "created_at": "..."
  }
]
```

### List Conversations

```bash
GET /chat/conversations?user_id=alice

Response:
[
  {
    "id": "uuid-1",
    "title": "What is machine learning",
    "created_at": "...",
    "message_count": 8
  },
  {
    "id": "uuid-2",
    "title": "Python programming basics",
    "created_at": "...",
    "message_count": 5
  }
]
```

## Database Schema

**Conversations Table:**

```sql
CREATE TABLE conversations (
    id UUID PRIMARY KEY,
    user_id VARCHAR NOT NULL,
    title VARCHAR,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

**Messages Table:**

```sql
CREATE TABLE messages (
    id UUID PRIMARY KEY,
    conversation_id UUID REFERENCES conversations(id),
    role VARCHAR NOT NULL,      -- 'user' or 'assistant'
    content TEXT NOT NULL,
    tokens_used INTEGER,
    created_at TIMESTAMP
);
```

## Key Features Explained

### Context Window Management

Prevents token overflow by limiting conversation history:

```python
# Configuration
CONTEXT_WINDOW_MESSAGES = 20  # Max messages sent to AI
MIN_MESSAGES_TO_KEEP = 10     # Always preserve at least this many

# Automatic trimming when limit exceeded
if message_count > CONTEXT_WINDOW_MESSAGES:
    # Delete oldest messages, keep last 20
    delete_oldest_messages(conversation_id)
```

**Why This Matters:**

- AI models have token limits (e.g., 32K tokens)
- Long conversations exceed limits and fail
- Auto-trimming keeps conversations working forever
- Preserves recent context while controlling costs

### Auto-Generated Titles

First message automatically creates conversation title:

```python
# User sends: "What is the best way to learn Python for AI?"
# Auto-generated title: "What is the best way to learn"
# (First 8 words, lowercased)
```

Happens once per conversation, makes conversations easy to find.

### Token Tracking

Each message tracks tokens used:

```python
# Rough estimation
tokens = word_count * 2

# Stored per message for:
- Cost tracking
- Usage analytics
- Context window calculations
```

## Configuration

Edit `config.py` to customize:

```python
CONTEXT_WINDOW_MESSAGES = 20    # Messages sent to AI
MIN_MESSAGES_TO_KEEP = 10       # Minimum to preserve
DEFAULT_TITLE_WORD_LIMIT = 8    # Words in auto-title
```

## Error Handling

All endpoints handle common errors:

**404 Not Found:**

```json
{ "detail": "Conversation not found" }
```

**400 Bad Request:**

```json
{ "detail": "Invalid message format" }
```

**500 Server Error:**

```json
{ "detail": "AI service temporarily unavailable" }
```

Gemini API calls include retry logic.

## Testing Workflow

1. **Create conversation:**

```bash
   POST /chat/conversations {"user_id": "test"}
```

2. **Send first message (creates title):**

```bash
   POST /conversations/{id}/messages
   {"content": "Explain quantum computing"}
```

3. **Check auto-generated title:**

```bash
   GET /conversations/{id}
   # title: "Explain quantum computing"
```

4. **Continue conversation:**

```bash
   POST /conversations/{id}/messages
   {"content": "How does it differ from classical?"}
```

5. **View history:**

```bash
   GET /conversations/{id}/messages
   # Shows all messages with context
```

6. **Test streaming:**

```bash
   GET /conversations/{id}/stream?message=Tell me more
   # Watch response appear live
```

## What You Learn

- **Database persistence** for chat applications
- **Context window management** to prevent token overflow
- **Conversation state management** across multiple chats
- **Auto-title generation** using first message
- **Streaming vs batch responses** in production
- **Token tracking** for cost monitoring
- **Production patterns** used by ChatGPT, Claude, etc.

## Common Issues

**Database connection error:**
Check DATABASE_URL in `.env` and PostgreSQL is running.

**Context not working:**
Messages older than 20 are automatically trimmed. This is expected.

**Streaming not working:**
Use `-N` flag with curl or EventSource in JavaScript.

**Title not generating:**
Only happens on first message. Subsequent messages don't update title.

## Future Enhancements

Possible additions:

- User authentication with JWT
- Rate limiting per user
- Message search and filtering
- Conversation tags/categories
- Multi-model support (Claude, GPT-4)
- Message editing and deletion
- Conversation forking
