# Event-Driven Architecture - Planning & Design

Learning event-driven architecture for the e-commerce backend. This approach lets different parts of the app communicate through events instead of direct function calls, making everything faster and more scalable.

## What is Event-Driven Architecture?

Think of a restaurant kitchen. The old way: the chef waits for each order to finish before starting the next one. Event-driven: the chef posts "Order ready!" and moves on. Waiters and cleaners react to their own tasks independently.

**The Core Flow:**

```
Producer (Orders Module) → Message Broker → Consumers (Email, Stock, Analytics)
```

The broker is like a bulletin board holding messages until consumers pick them up.

## Two Main Patterns

**Pub/Sub (One-to-Many):**

```
Order Created → Stock Service
             → Email Service
             → Analytics Service
```

One event reaches multiple consumers.

**Queue (One-to-One):**

```
Task Queue: [Task1] [Task2] [Task3]
Worker1 processes Task1
Worker2 processes Task2
```

Tasks distributed to available workers.

## Synchronous vs Asynchronous

**Old Way (Blocking):**

```python
@app.post("/orders")
async def create_order(order_data):
    order = save_order(order_data)
    send_email(order)        # Wait...
    update_stock(order)      # Wait...
    return order             # Slow response
```

**New Way (Event-Driven):**

```python
@app.post("/orders")
async def create_order(order_data):
    order = save_order(order_data)
    publish_event("OrderCreated", order.dict())
    return order             # Fast response!
```

User gets immediate response. Email and stock updates happen in background.

## Key Events for E-Commerce

**UserRegistered**

- Producer: Auth module
- Consumers: Email (welcome), Analytics
- When: User signs up

**OrderCreated**

- Producer: Orders module
- Consumers: Stock (reduce), Email (confirm), Analytics
- When: User places order

**OrderPaid**

- Producer: Orders module
- Consumers: Shipping, Analytics
- When: Payment succeeds

**ProductReviewed**

- Producer: Products module
- Consumers: Analytics (update rating)
- When: User reviews product

**StockLow**

- Producer: Products module
- Consumers: Admin (alert)
- When: Product stock drops below threshold

**UserBanned**

- Producer: Admin module
- Consumers: Auth (block access)
- When: Admin bans user

**PaymentFailed**

- Producer: Orders module
- Consumers: User (notify), Orders (cancel)
- When: Payment fails

## Benefits for E-Commerce

**Faster Responses:**
User gets order confirmation instantly while background tasks run.

**Scalability:**
Handle more orders by adding more consumer workers.

**Reliability:**
Events retry automatically if consumers fail.

**Modularity:**
Add new features (notifications, recommendations) by adding new consumers.

**Loose Coupling:**
Modules don't depend on each other directly. Orders module doesn't know about Email service.

## Example Flow: Order Creation

```
1. User places order
2. Orders module saves to database
3. Publish "OrderCreated" event
4. Return order ID to user (instant!)

Meanwhile (background):
- Stock consumer reduces inventory
- Email consumer sends confirmation
- Analytics consumer updates sales stats
```

All happens independently without blocking the user.

## Message Broker Comparison

Choosing the right message broker depends on your needs:

| Broker   | Speed  | Setup   | Persistence | Reliability | Best For                    | My Assessment        |
| -------- | ------ | ------- | ----------- | ----------- | --------------------------- | -------------------- |
| Redis    | Fast   | Easy    | Optional    | Good        | Simple pub/sub, caching     | Perfect for starting |
| RabbitMQ | Medium | Medium  | Yes         | Excellent   | Complex routing, queues     | Good for enterprise  |
| Kafka    | Fast   | Complex | Yes         | Excellent   | High throughput, event logs | Overkill for now     |

**Why I Chose Redis:**

- Simple setup and configuration
- Fast enough for my use case
- Built-in pub/sub support
- Easy to learn and understand
- Can add persistence later if needed

## Immediate vs Background Processing

Not all events need the same urgency. Here's how I classified them:

| Event           | Processing | Reason                                     |
| --------------- | ---------- | ------------------------------------------ |
| UserBanned      | Immediate  | Security action requires instant effect    |
| PaymentFailed   | Immediate  | User needs quick feedback to retry         |
| UserRegistered  | Background | Welcome email can wait a few seconds       |
| OrderCreated    | Background | Stock/email/analytics aren't time-critical |
| OrderPaid       | Background | Shipping notification can be delayed       |
| ProductReviewed | Background | Rating updates don't need to be instant    |
| StockLow        | Background | Admin alerts can be batched                |

**Immediate Processing:**

- Affects user experience directly
- Security-related actions
- Requires instant feedback

**Background Processing:**

- Doesn't block user workflow
- Can tolerate some delay
- Improves response times
- Better resource utilization

## Why This Fits My Project

- **Scalability**: Handle more users/orders without slowing down.
- **Reliability**: Events retry if consumers fail.
- **Modularity**: New features (like notifications) add easily via new consumers.
- **Performance**: Users get instant responses, background tasks run smoothly.
- **Maintenance**: Less coupling means easier updates.
