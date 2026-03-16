import json
import os
from confluent_kafka import Consumer


class KafkaConsumer:
    def __init__(self):
        kafka_uri = os.getenv("KAFKA_URI","localhost:9092")
        consumer_config = {
            "bootstrap.servers": kafka_uri,
            "group.id": "attack-group",
            "auto.offset.reset": "earliest"
        }
        self.consumer = Consumer(consumer_config)
        self.consumer.subscribe(["attack"])

    def recive_data(self):
        msg = self.consumer.poll()
        if msg is None:
            return None
        if msg.error():
            print("❌ Error:", msg.error())
            return None
        try:
            value = msg.value().decode("utf-8")
            data = json.loads(value)
            return data
        except Exception:
            return None