import redis
import json

class RedisClient:
    def __init__(self, url: str):
        # Connect to Redis using URL
        self.client = redis.from_url(url)

    def push_to_queue(self, queue_name: str, data: dict):
        """
        Push a task to a Redis queue (left push)
        """
        message = json.dumps(data)  # Convert Python dict to JSON
        self.client.lpush(queue_name, message)

    def pop_from_queue(self, queue_name: str):
        """
        Pop a task from a Redis queue (right pop)
        Returns Python dict or None if queue empty
        """
        message = self.client.rpop(queue_name)
        if message:
            return json.loads(message)
        return None
