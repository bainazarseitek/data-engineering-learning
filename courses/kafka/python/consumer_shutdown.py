from confluent_kafka import Consumer

config = {
    "bootstrap.servers": "localhost:9092",
    "group.id": "my-python-application",
    "auto.offset.reset": "earliest",
}

consumer = Consumer(config)
consumer.subscribe(["demo_python"])

print("Waiting for messages... (Ctrl + C to stop)")

try:
    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            continue

        if msg.error():
            print("ERROR:", msg.error())
            continue

        key = msg.key().decode() if msg.key() else None
        value = msg.value().decode()
        print(f"key={key} value={value} partition={msg.partition()} offset={msg.offset()}")

except KeyboardInterrupt:
    print("Ctrl + C pressed, shutting down...")

finally:
    consumer.close()
    print("Consumer closed cleanly")

