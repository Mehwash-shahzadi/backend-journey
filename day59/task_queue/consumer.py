import time
from redis_client import RedisClient
from tasks import send_email_task

# Connect to Redis
redis_url = "redis://localhost:6379"
redis_client = RedisClient(redis_url)

# Queue name
QUEUE_NAME = "email_queue"

print("Worker started. Listening for tasks...")

while True:
    # Pop a task from the queue
    task = redis_client.pop_from_queue(QUEUE_NAME)
    
    if task:
        # # Simulate email processing
        # print(f"Processing task: {task}")
        # time.sleep(2)  # Simulate time taken to send email
        # print(f"Task completed: {task}")
        send_email_task(task)
    else:
        # Sleep briefly if no task
        time.sleep(1)
