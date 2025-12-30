import redis
import json


def main():
    redis_url = "redis://localhost:6379"
    client = redis.from_url(redis_url)

    pubsub = client.pubsub()
    pubsub.subscribe("order_events")

    print("Listening for messages on 'order_events'...")

    for message in pubsub.listen():
        if message["type"] == "message":
            data = json.loads(message["data"])
            print("Received event:", data)


if __name__ == "__main__":
    main()
