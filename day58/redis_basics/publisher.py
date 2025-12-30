from redis_client import RedisClient


def main():
    redis_url = "redis://localhost:6379"
    redis_client = RedisClient(redis_url)

    event_data = {
        "event": "OrderCreated",
        "order_id": 123
    }

    redis_client.publish_event("order_events", event_data)
    print("Event published:", event_data)


if __name__ == "__main__":
    main()
