from abc import ABC, abstractmethod
import asyncio

class EventHandler(ABC):
    @abstractmethod
    async def handle(self, event: dict):
        pass

class SendWelcomeEmailHandler(EventHandler):
    async def handle(self, event: dict):
        print(f"[EMAIL SIMULATION] Sending welcome email to {event.get('email', 'unknown')} for user ID {event.get('user_id')}")
        await asyncio.sleep(0.5)  

class LogAnalyticsHandler(EventHandler):
    async def handle(self, event: dict):
        print(f"[ANALYTICS LOG] Event logged: Type={event.get('event_type')}, Details={event}")
        await asyncio.sleep(0.3)  