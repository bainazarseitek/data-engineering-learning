import time
from confluent_kafka import Producer

config = {
    "bootstrap.servers": "localhost:9092",
}

producer = Producer(config)

for i in range(10):
    message = f"message number {i}"
    producer.produce("demo_python", value=message)
    print("sent:", message)
    time.sleep(1)   # wait 1 second, like "a new event every second"

producer.flush()
print("Done")
