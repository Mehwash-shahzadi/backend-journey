# Task Queue System - Producer-Consumer Pattern

A practical implementation of the producer-consumer pattern using Redis and FastAPI. This demonstrates how to handle background tasks asynchronously without blocking API responses.

## The Problem

APIs should never make users wait for slow operations like:

- Sending emails (2-5 seconds)
- Generating reports (10-30 seconds)
- Processing images (5-15 seconds)
- External API calls (varies)

## The Solution

**Task Queue Pattern:**

```
User Request → API (instant response) → Redis Queue → Worker (processes in background)
```

User gets immediate response. Heavy work happens later.

## Project Structure

```
day59/task_queue/
├── producer.py           # FastAPI endpoint (adds tasks to queue)
├── consumer.py           # Worker (processes tasks from queue)
├── tasks.py              # Task definitions (email sending logic)
├── redis_client.py       # Redis connection helper
├── requirements.txt
└── README.md
```

## How It Works

### 1. Producer (API)

FastAPI endpoint receives request and adds task to queue:

```python
@app.post("/send-email")
async def send_email(email_data: EmailTask):
    # Add to queue immediately
    redis_client.lpush("email_queue", json.dumps(email_data.dict()))
    return {"status": "queued", "message": "Email task added to queue"}
```

**Response time:** ~50ms (instant)

### 2. Redis Queue

Acts as a buffer between API and workers:

```
[Task1] [Task2] [Task3] [Task4] ... waiting to be processed
```

### 3. Consumer (Worker)

Continuously processes tasks from queue:

```python
while True:
    task = redis_client.rpop("email_queue")
    if task:
        send_email_task(json.loads(task))
    else:
        time.sleep(1)  # Wait if queue is empty
```

## Setup Instructions

### Prerequisites

- Redis running (from Day 58)
- Python 3.10+

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Start Redis

```bash
docker-compose up -d
```

## Running the System

### Step 1: Start the API (Producer)

```bash
uvicorn producer:app --reload
```

API runs at http://localhost:8000

### Step 2: Start Worker(s)

Open new terminal:

```bash
python consumer.py
```

You can start multiple workers for faster processing:

```bash
# Terminal 2
python consumer.py

# Terminal 3
python consumer.py
```

### Step 3: Send Tasks

**Using curl:**

```bash
curl -X POST http://localhost:8000/send-email \
  -H "Content-Type: application/json" \
  -d '{
    "recipient_email": "user@example.com",
    "subject": "Welcome!",
    "body": "Thank you for signing up."
  }'
```

**Response:**

```json
{
  "status": "queued",
  "message": "Email task added to queue"
}
```

**Using Swagger UI:**
Visit http://localhost:8000/docs and try the endpoint.

## Code Overview

### Task Definition (tasks.py)

```python
import time
import logging

def send_email_task(task_data: dict):
    """Simulates sending email"""
    email = task_data["recipient_email"]
    subject = task_data["subject"]

    logging.info(f"Processing email to {email}")
    time.sleep(3)  # Simulate email sending
    logging.info(f"Email sent to {email}")
```

### Producer (producer.py)

```python
from fastapi import FastAPI
import json

app = FastAPI()

@app.post("/send-email")
async def send_email(email_data: EmailTask):
    # Push to queue (LPUSH = add to left)
    redis_client.lpush("email_queue", json.dumps(email_data.dict()))
    return {"status": "queued"}
```

### Consumer (consumer.py)

```python
import json
import time

while True:
    # Pop from queue (RPOP = remove from right, FIFO)
    task_json = redis_client.rpop("email_queue")

    if task_json:
        task_data = json.loads(task_json)
        send_email_task(task_data)
    else:
        time.sleep(1)  # Wait if queue empty
```

## Visual Flow

```
┌─────────────┐
│   User      │
└──────┬──────┘
       │ POST /send-email
       ▼
┌─────────────────┐
│  FastAPI API    │ ← Producer (adds to queue instantly)
└────────┬────────┘
         │ LPUSH
         ▼
┌──────────────────┐
│   Redis Queue    │ ← [Task1][Task2][Task3]...
└────────┬─────────┘
         │ RPOP
         ▼
┌──────────────────┐
│ Worker(s)        │ ← Consumer (processes tasks)
│ • Worker 1       │
│ • Worker 2       │
│ • Worker 3       │
└──────────────────┘
```

## Key Benefits

**Fast API Responses:**
User doesn't wait for email to actually send.

**Scalability:**
Add more workers to handle increased load.

**Reliability:**
If worker crashes, tasks stay in queue.

**Decoupling:**
API and workers are independent. Can restart workers without affecting API.

## Testing Scenarios

### Scenario 1: Single Task

1. Start API and one worker
2. Send one email task
3. Watch worker process it in 3 seconds

### Scenario 2: Multiple Tasks

1. Send 10 email tasks quickly
2. Watch worker process them one by one
3. Notice API responds instantly each time

### Scenario 3: Multiple Workers

1. Start API and 3 workers
2. Send 10 tasks
3. Watch all 3 workers process tasks in parallel
4. Tasks complete ~3x faster

### Scenario 4: Worker Restart

1. Send 5 tasks
2. Stop worker halfway
3. Tasks stay in Redis queue
4. Restart worker
5. Remaining tasks process normally

## What You Learn

- **Producer-Consumer Pattern:** Classic design pattern for async processing
- **Task Queues:** How background jobs work in production
- **Redis as Queue:** Simple but powerful queue implementation
- **Worker Scaling:** How to handle more load
- **Separation of Concerns:** API logic separate from task logic

## Common Use Cases

This pattern is used for:

- **Email notifications** (welcome emails, order confirmations)
- **Report generation** (PDF exports, analytics)
- **Image processing** (thumbnails, compression)
- **Data imports** (CSV uploads, bulk operations)
- **External API calls** (payment processing, notifications)

## Production Considerations

**Monitoring:**
Track queue size, worker count, processing time.

**Error Handling:**
Retry failed tasks, dead-letter queue for failures.

**Persistence:**
Redis can lose data on restart. Use RabbitMQ/Kafka for critical tasks.

**Priority Queues:**
Use multiple queues for different priority levels.
