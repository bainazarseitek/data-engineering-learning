from confluent_kafka import Consumer

config = {
    "bootstrap.servers": "localhost:9092",
    "group.id": "my-python-application",
    "auto.offset.reset": "earliest",
}

consumer = Consumer(config)
consumer.subscribe(["demo_python"])

print("Waiting for messages... (Ctrl + C to stop)")

while True:
    msg = consumer.poll(1.0)   # wait up to 1 second for a message

    if msg is None:            # nothing arrived in that second
        continue

    if msg.error():            # something went wrong
        print("ERROR:", msg.error())
        continue

    key = msg.key().decode() if msg.key() else None
    value = msg.value().decode()
    print(f"key={key} value={value} partition={msg.partition()} offset={msg.offset()}")
