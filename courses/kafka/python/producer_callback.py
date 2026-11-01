from confluent_kafka import Producer

config = {
    "bootstrap.servers": "localhost:9092",
}

producer = Producer(config)


# The library calls this once per message, when Kafka answers
def delivery_report(err, msg):
    if err is not None:
        print("FAILED:", err)
    else:
        print(
            f"delivered: topic={msg.topic()} "
            f"partition={msg.partition()} "
            f"offset={msg.offset()}"
        )


for i in range(10):
    producer.produce(
        "demo_python",
        value=f"hello {i}",
        callback=delivery_report,  # "call this function when you know the result"
    )
    producer.poll(0)  # "any callbacks ready? run them now"

producer.flush()
