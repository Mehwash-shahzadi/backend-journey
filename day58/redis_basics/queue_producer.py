from redis_client import RedisClient

def main():
    redis_url = "redis://localhost:6379"
    redis_client = RedisClient(redis_url)

    for i in range(5):
        task = {
            "task_id": i + 1,
            "task_name": "SendEmail",
            "user_email": f"user{i+1}@example.com"
        }
        redis_client.push_to_queue("task_queue", task)
        print(f"Pushed task to queue: {task}")

if __name__ == "__main__":
    main()
