import redis
import json

class RedisClient:
    def __init__(self, url: str):
        self.client = redis.from_url(url)

    def publish(self, channel: str, data: dict):
        message = json.dumps(data)
        self.client.publish(channel, message)
