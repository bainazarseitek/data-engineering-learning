import sys
from confluent_kafka import Consumer

config = {
    "bootstrap.servers": "localhost:9092",
    "group.id": "my-cooperative-application",  # all members of one group must use the same strategy
    "auto.offset.reset": "earliest",
    "partition.assignment.strategy": "cooperative-sticky",  # move only the partitions that must move
}

# Optional fixed name: uv run consumer_cooperative.py c1  -> static membership
if len(sys.argv) > 1:
    config["group.instance.id"] = sys.argv[1]

consumer = Consumer(config)


# With cooperative-sticky these lists hold only the change, not the full assignment
def on_assign(consumer, partitions):
    print(f">>> ASSIGNED partitions: {[p.partition for p in partitions]}")


def on_revoke(consumer, partitions):
    print(f"<<< REVOKED partitions: {[p.partition for p in partitions]}")


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
