# Redis Basics - Pub/Sub & Queues

Introduction to Redis fundamentals using Python. This project demonstrates two core Redis patterns: real-time event broadcasting (Pub/Sub) and background job processing (Queues).

## What is Redis?

Redis is an in-memory data store that acts as a fast message broker. Think of it as a super-fast bulletin board where different parts of your app can leave messages for each other.

**Common Uses:**

- Event-driven systems (what we're learning)
- Background job queues
- Caching frequently accessed data
- Session storage
- Real-time features

## Project Structure

```
day58/redis_basics/
├── docker-compose.yml      # Redis container setup
├── redis_client.py         # Redis connection helper
├── publisher.py            # Publishes events (Pub/Sub)
├── subscriber.py           # Listens to events (Pub/Sub)
├── queue_producer.py       # Adds tasks to queue
├── queue_worker.py         # Processes tasks from queue
├── requirements.txt
└── README.md
```

## Setup

### Prerequisites

- Python 3.10+
- Docker

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Start Redis

Run Redis in Docker:

```bash
docker-compose up -d
```

Verify Redis is running:

```bash
redis-cli ping
```

Should return: `PONG`

## Pattern 1: Pub/Sub (Real-Time Events)

Pub/Sub is like a radio station - publishers broadcast messages, subscribers tune in and listen.

### How It Works

```
Publisher → Redis Channel → Multiple Subscribers
```

If no one is listening when you publish, the message disappears.

### Try It Out

**Step 1: Start the Subscriber (Listener)**

```bash
python subscriber.py
```

This waits for messages on the `order_events` channel.

**Step 2: Publish an Event**

Open another terminal:

```bash
python publisher.py
```

You'll see the subscriber receive the message instantly.

### When to Use Pub/Sub

- Real-time notifications
- Live updates (dashboards, chat)
- Broadcasting events to multiple services
- Activity feeds

**Key Point:** Messages aren't stored. If no one is listening, they're lost.

## Pattern 2: Queue (Background Jobs)

Queues are like a to-do list - producers add tasks, workers process them one at a time.

### How It Works

```
Producer → Redis Queue → Workers (pick tasks one by one)
```

Tasks stay in the queue until a worker processes them.

### Try It Out

**Step 1: Add Tasks to Queue (Producer)**

```bash
python queue_producer.py
```

This adds several tasks to the `task_queue`.

**Step 2: Process Tasks (Worker)**

```bash
python queue_worker.py
```

The worker:

1. Checks the queue continuously
2. Picks one task at a time
3. Processes it
4. Waits if queue is empty

**Scaling:** Run multiple workers in different terminals to process tasks faster.

### When to Use Queues

- Sending emails
- Processing orders
- Generating reports
- Image processing
- Any task that can happen in the background

**Key Point:** Tasks are stored until processed. Reliable for critical operations.

## Key Differences

| Feature      | Pub/Sub                  | Queue                          |
| ------------ | ------------------------ | ------------------------------ |
| **Purpose**  | Real-time events         | Background jobs                |
| **Delivery** | Many subscribers         | One worker                     |
| **Storage**  | No (lost if no listener) | Yes (until processed)          |
| **Use Case** | Live updates, broadcasts | Emails, order processing       |
| **Speed**    | Instant                  | As fast as workers can process |

## Redis Commands Used

**Pub/Sub:**

- `PUBLISH` - Send event to channel
- `SUBSCRIBE` - Listen to channel

**Queue:**

- `LPUSH` - Add task to queue (left side)
- `RPOP` - Remove task from queue (right side)

## Code Examples

### Publishing an Event

```python
# publisher.py
import redis

r = redis.Redis(host='localhost', port=6379)
r.publish('order_events', '{"order_id": 123, "status": "created"}')
```

### Subscribing to Events

```python
# subscriber.py
import redis

r = redis.Redis(host='localhost', port=6379)
pubsub = r.pubsub()
pubsub.subscribe('order_events')

for message in pubsub.listen():
    if message['type'] == 'message':
        print(f"Received: {message['data']}")
```

### Adding to Queue

```python
# queue_producer.py
import redis

r = redis.Redis(host='localhost', port=6379)
r.lpush('task_queue', 'send_email_to_user@example.com')
```

### Processing Queue

```python
# queue_worker.py
import redis
import time

r = redis.Redis(host='localhost', port=6379)

while True:
    task = r.rpop('task_queue')
    if task:
        print(f"Processing: {task.decode()}")
        time.sleep(1)  # Simulate work
    else:
        time.sleep(0.5)  # Wait if queue is empty
```

## What You Learn

After completing this exercise, you understand:

- How Redis works as a message broker
- Difference between Pub/Sub and Queues
- When to use each pattern
- How producers and consumers communicate
- Foundation for event-driven architecture

## Common Issues

**Redis not starting:**

```bash
docker-compose down
docker-compose up -d
```

**Connection refused:**
Make sure Redis is running on port 6379.

**Messages not received:**
For Pub/Sub, subscriber must be running before publishing.
