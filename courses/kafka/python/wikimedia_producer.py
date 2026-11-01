import requests
from confluent_kafka import Producer

TOPIC = "wikimedia.recentchange"
URL = "https://stream.wikimedia.org/v2/stream/recentchange"
HEADERS = {"User-Agent": "kafka-course-learning/0.1"}  # Wikimedia refuses requests without one

producer = Producer({"bootstrap.servers": "localhost:9092"})


def delivery_report(err, msg):
    if err is not None:
        print("FAILED:", err)  # print only problems: there will be thousands of messages


count = 0
try:
    with requests.get(URL, headers=HEADERS, stream=True, timeout=30) as response:
        response.raise_for_status()

        for line in response.iter_lines(decode_unicode=True):
            if not line.startswith("data: "):
                continue  # skip "event:", "id:" and empty lines

            event = line[len("data: "):]  # the JSON after "data: "
            producer.produce(TOPIC, value=event, callback=delivery_report)
            producer.poll(0)

            count += 1
            if count % 100 == 0:
                print(f"sent {count} events")

except KeyboardInterrupt:
    print("Stopping...")

finally:
    producer.flush()
    print(f"Total sent: {count}")
