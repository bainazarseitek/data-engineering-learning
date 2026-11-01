from confluent_kafka import Producer

config = {
    "bootstrap.servers": "localhost:9092",
}

producer = Producer(config)


def delivery_report(err, msg):
    if err is not None:
        print("FAILED:", err)
    else:
        print(f"key={msg.key().decode()} -> partition={msg.partition()}")


for round_number in range(2):          # send the same 10 keys twice
    print(f"--- round {round_number}")
    for i in range(10):
        producer.produce(
            "demo_python",
            key=f"id_{i}",
            value=f"hello {i}",
            callback=delivery_report,
        )
        producer.poll(0)
    producer.flush()   # wait for round 0 to finish before starting round 1
