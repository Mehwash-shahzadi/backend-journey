from redis_client import RedisClient
from datetime import datetime

class EventPublisher:
    def __init__(self, redis_client: RedisClient):
        self.redis_client = redis_client

    def publish_event(self, channel: str, event):
        event_data = event.dict()
        event_data["timestamp"] = datetime.utcnow().isoformat()
        self.redis_client.publish(channel, event_data)
        print(f"Event published: {event_data}")
