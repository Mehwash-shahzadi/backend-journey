import json
import asyncio  
from redis_client import RedisClient
from events.handlers import EventHandler, SendWelcomeEmailHandler, LogAnalyticsHandler
from typing import Dict, List

class EventSubscriber:
    def __init__(self, redis_client: RedisClient, handler_registry: Dict[str, List[EventHandler]]):
        self.redis_client = redis_client
        self.handler_registry = handler_registry

    def subscribe(self, channels: List[str]):
        pubsub = self.redis_client.client.pubsub()
        pubsub.subscribe(*channels)
        print(f"[SUBSCRIBER] Listening on channels: {channels}")

        for message in pubsub.listen():
            if message.get('type') == 'message':  
                try:
                    event_data = json.loads(message['data'])
                    event_type = event_data.get('event_type')
                    
                    if event_type and event_type in self.handler_registry:
                        for handler in self.handler_registry[event_type]:
                            # Run the async handler in its own event loop
                            asyncio.run(handler.handle(event_data))
                    else:
                        print(f"[WARNING] No handlers registered for event type: {event_type or 'unknown'}")
                except json.JSONDecodeError:
                    print("[ERROR] Invalid JSON in message")
                except Exception as e:
                    print(f"[ERROR] Handler failed: {str(e)}")