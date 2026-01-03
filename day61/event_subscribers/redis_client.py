import redis
import json

class RedisClient:
    def __init__(self, redis_url: str):
        # decode_responses=True returns str instead of bytes
        self.client = redis.from_url(redis_url, decode_responses=True)

    def subscribe(self, channel: str):
        pubsub = self.client.pubsub()
        pubsub.subscribe(channel)
        return pubsub

    def publish_event(self, channel: str, data: dict):
        self.client.publish(channel, json.dumps(data))
