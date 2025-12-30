# Day 57: Event-Driven Architecture - Planning & Design

## Quick Intro

Hey fellow developer! Today, I'm diving into Event-Driven Architecture (EDA) for my modular e-commerce FastAPI project. Think of it as upgrading from a single-threaded script to a bustling team where everyone works asynchronously. EDA lets different parts of my app communicate via events instead of direct calls, making the system faster, more scalable, and easier to maintain. For my e-commerce backend, this means handling user registrations, orders, and stock updates without blocking the main flow – perfect for a growing online store!

## What is Event-Driven Architecture? (Simple Analogy)

Imagine a busy restaurant kitchen. In the old synchronous way, the chef waits for each order to be fully cooked before taking the next one – slow and inefficient. With EDA, it's like an office bulletin board: the chef posts a note ("Order ready!") and moves on, while waiters, cleaners, and managers react asynchronously to their tasks.

Synchronous: Everything happens in sequence, one step at a time.
Asynchronous: Events trigger actions in parallel, no waiting.

Here's the core flow in ASCII:

```
Producers (e.g., Orders Module) --> [Message Broker] --> Consumers (e.g., Email, Analytics)
```

The broker acts like the bulletin board, holding events until consumers pick them up.

## Key Patterns

EDA has two main patterns to handle events:

- **Pub/Sub**: One event goes to many consumers. Like broadcasting a newsletter – everyone interested gets a copy.
- **Queue**: Tasks go to workers one at a time. Like a to-do list where only one person handles each item.

ASCII diagrams:

Pub/Sub (fan-out):

```
Publisher --> Event --> Consumer1
                    --> Consumer2
                    --> Consumer3
```

Queue (load-balanced):

```
Queue: [Task1] [Task2] [Task3]
Worker1 <-- Task1
Worker2 <-- Task2
```

## Synchronous vs Asynchronous Example

Let's compare with FastAPI code snippets for order creation.

**Synchronous (slow, blocking):**

```python
@app.post("/orders")
async def create_order(order_data: OrderCreate, db: Session = Depends(get_db)):
    # Create order in DB
    order = create_order_in_db(db, order_data)
    # Wait for email to send (blocks!)
    send_confirmation_email(order.email)
    # Wait for stock update (blocks!)
    update_stock(db, order.items)
    return order
```

Response time: Slow, as each step waits.

**Asynchronous (fast, event-driven):**

```python
@app.post("/orders")
async def create_order(order_data: OrderCreate, db: Session = Depends(get_db)):
    order = create_order_in_db(db, order_data)
    # Publish events, don't wait
    publish_event("OrderCreated", {"order_id": order.id, "email": order.email, "items": order.items})
    return order  # Fast response!
```

Benefits: Faster responses (user gets order ID instantly), loose coupling (modules don't depend on each other), scalability (handle more load by adding consumers).

## E-Commerce Event Catalog

Here are 7 key events for my project:

1. **UserRegistered**

   - Producer: Auth module
   - Sample JSON: `{"user_id": 123, "email": "user@example.com", "timestamp": "2023-10-01T10:00:00Z"}`
   - Consumers: Email (welcome), Analytics (new user count)
   - Processing: Background

2. **OrderCreated**

   - Producer: Orders module
   - Sample JSON: `{"order_id": 456, "user_id": 123, "total": 99.99, "items": [{"product_id": 1, "quantity": 2}]}`
   - Consumers: Stock (deduct), Email (confirmation), Analytics (sales)
   - Processing: Background

3. **OrderPaid**

   - Producer: Orders module
   - Sample JSON: `{"order_id": 456, "payment_id": "pay_789", "amount": 99.99}`
   - Consumers: Shipping (notify), Analytics (revenue)
   - Processing: Background

4. **ProductReviewed**

   - Producer: Products module
   - Sample JSON: `{"product_id": 1, "user_id": 123, "rating": 5, "comment": "Great!"}`
   - Consumers: Analytics (avg rating), Moderation (check spam)
   - Processing: Background

5. **StockLow**

   - Producer: Products module
   - Sample JSON: `{"product_id": 1, "current_stock": 5, "threshold": 10}`
   - Consumers: Admin (alert), Suppliers (reorder)
   - Processing: Background

6. **UserBanned**

   - Producer: Admin module
   - Sample JSON: `{"user_id": 123, "reason": "spam", "banned_by": "admin@example.com"}`
   - Consumers: Auth (block login), Email (notification)
   - Processing: Immediate

7. **PaymentFailed**
   - Producer: Orders module
   - Sample JSON: `{"order_id": 456, "error": "insufficient funds"}`
   - Consumers: User (notify), Orders (cancel)
   - Processing: Immediate

## Event Flow Example: OrderCreated

Here's how it flows:

```
Orders Module --> Publish "OrderCreated" --> [Broker] --> Stock Consumer (deduct inventory)
                                                       --> Email Consumer (send confirmation)
                                                       --> Analytics Consumer (update sales data)
```

Multiple consumers react independently, keeping the system decoupled.

## Immediate vs Background Processing

Classifying the events:

| Event           | Processing | Reason                               |
| --------------- | ---------- | ------------------------------------ |
| UserBanned      | Immediate  | Security action needs instant effect |
| PaymentFailed   | Immediate  | User needs quick feedback            |
| UserRegistered  | Background | Welcome email can wait               |
| OrderCreated    | Background | Stock/email/analytics not urgent     |
| OrderPaid       | Background | Shipping/analytics can be async      |
| ProductReviewed | Background | Rating updates are not time-critical |
| StockLow        | Background | Alerts can be batched                |

## Message Broker Comparison

Choosing a broker is key. Here's a comparison:

| Broker   | Speed  | Ease of Setup | Persistence | Reliability | Best For                | My Fit                   |
| -------- | ------ | ------------- | ----------- | ----------- | ----------------------- | ------------------------ |
| Redis    | Fast   | Easy          | Optional    | Good        | Simple pub/sub, caching | Great for starting small |
| RabbitMQ | Medium | Medium        | Yes         | Excellent   | Complex routing, queues | Good for enterprise      |
| Kafka    | Fast   | Hard          | Yes         | Excellent   | High-throughput, logs   | Overkill for my project  |

Recommendation: Start with Redis – it's simple, fast, and fits my needs perfectly.

## Why This Fits My Project

- **Scalability**: Handle more users/orders without slowing down.
- **Reliability**: Events retry if consumers fail.
- **Modularity**: New features (like notifications) add easily via new consumers.
- **Performance**: Users get instant responses, background tasks run smoothly.
- **Maintenance**: Less coupling means easier updates.

## Next Steps

Tomorrow, I'll set up Redis as my message broker and start integrating it into the FastAPI app. Excited to see this in action!

Day 57 Complete 🚀
