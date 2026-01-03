from fastapi import FastAPI
from pydantic import BaseModel
from redis_client import RedisClient

# Create FastAPI app
app = FastAPI()

# Define the email task schema
class EmailTask(BaseModel):
    recipient_email: str
    subject: str
    body: str

# Connect to Redis
redis_url = "redis://localhost:6379"
redis_client = RedisClient(redis_url)

# POST endpoint to add tasks to Redis queue
@app.post("/send-email")
def send_email(task: EmailTask):
    # Push task to Redis queue named "email_queue"
    redis_client.push_to_queue("email_queue", task.dict())
    # Respond immediately to API caller (non-blocking)
    return {"status": "queued", "task": task.dict()}
