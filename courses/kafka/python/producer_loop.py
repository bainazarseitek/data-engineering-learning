import time
from confluent_kafka import Producer

producer = Producer({"bootstrap.servers": "localhost:9092"})

i = 0
try:
    while True:
        producer.produce("demo_python", key=f"id_{i % 10}", value=f"event {i}")
        producer.poll(0)
        i += 1
        time.sleep(0.5)     # 2 messages per second
except KeyboardInterrupt:
    pass
finally:
    producer.flush()
    print(f"Producer stopped after {i} messages")
