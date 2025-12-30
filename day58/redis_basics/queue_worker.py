from redis_client import RedisClient
import time

def process_task(task):
    print(f"Processing task: {task}")
    # Simulate some work
    time.sleep(1)
    print(f"Finished task: {task['task_id']}")

def main():
    redis_url = "redis://localhost:6379"
    redis_client = RedisClient(redis_url)

    print("Worker started. Waiting for tasks...")

    while True:
        task = redis_client.pop_from_queue("task_queue")
        if task:
            process_task(task)
        else:
            time.sleep(1)  # Wait a bit if queue is empty

if __name__ == "__main__":
    main()
