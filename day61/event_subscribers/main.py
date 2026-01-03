import asyncio
from redis_client import RedisClient
from events.subscriber import EventSubscriber
from events.handlers import SendWelcomeEmailHandler, LogAnalyticsHandler

handler_registry = {
    "user.registered": [SendWelcomeEmailHandler()],
    "order.created": [LogAnalyticsHandler()],
}

redis_client = RedisClient("redis://localhost:6379")
subscriber = EventSubscriber(redis_client, handler_registry)

if __name__ == "__main__":
    channels = ["user_events", "order_events"]
    asyncio.run(subscriber.subscribe(channels))