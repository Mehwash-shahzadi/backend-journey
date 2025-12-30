import json
import redis


class RedisClient:
    def __init__(self, url: str):
        self.client = redis.from_url(url)

    def publish_event(self, channel: str, data: dict):
        message = json.dumps(data)
        self.client.publish(channel, message)

    def push_to_queue(self, queue: str, data: dict):
        message = json.dumps(data)
        self.client.lpush(queue, message)

    def pop_from_queue(self, queue: str):
        message = self.client.rpop(queue)
        if message:
            return json.loads(message)
        return None
