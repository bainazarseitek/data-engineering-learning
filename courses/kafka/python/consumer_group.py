from confluent_kafka import Consumer

config = {
    "bootstrap.servers": "localhost:9092",
    "group.id": "my-python-application",
    "auto.offset.reset": "earliest",
}

consumer = Consumer(config)


def on_assign(consumer, partitions):
    numbers = [p.partition for p in partitions]
    print(f">>> ASSIGNED partitions: {numbers}")


def on_revoke(consumer, partitions):
    numbers = [p.partition for p in partitions]
    print(f"<<< REVOKED partitions: {numbers}")


consumer.subscribe(["demo_python"], on_assign=on_assign, on_revoke=on_revoke)

print("Waiting for messages... (Ctrl + C to stop)")

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print("ERROR:", msg.error())
            continue
        print(f"partition={msg.partition()} offset={msg.offset()} value={msg.value().decode()}")

except KeyboardInterrupt:
    print("Shutting down...")

finally:
    consumer.close()
