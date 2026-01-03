from fastapi import FastAPI
from redis_client import RedisClient
from events.publisher import EventPublisher
from events.schemas import UserRegisteredEvent, OrderCreatedEvent

app = FastAPI()

redis_client = RedisClient("redis://localhost:6379")
event_publisher = EventPublisher(redis_client)


@app.post("/register")
def register_user(user_id: int, email: str):
    event = UserRegisteredEvent(
        user_id=user_id,
        email=email,
        timestamp=None
    )
    event_publisher.publish_event("user_events", event)
    return {"message": "User registered"}


@app.post("/order")
def create_order(order_id: int, user_id: int, total: float):
    event = OrderCreatedEvent(
        order_id=order_id,
        user_id=user_id,
        total=total,
        timestamp=None
    )
    event_publisher.publish_event("order_events", event)
    return {"message": "Order created"}
