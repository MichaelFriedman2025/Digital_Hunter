import json
import os
from confluent_kafka import Producer


class KafkaProducer:
    def __init__(self):
        kafka_uri = os.getenv("KAFKA_URI","localhost:9092")
        producer_config = {
            "bootstrap.servers": kafka_uri
        }
        self.producer = Producer(producer_config)


    def prduce_data(self,data):
        value = json.dumps(data).encode("utf-8")
        self.producer.produce(topic="intel_signals_dlq",value=value)
        self.producer.flush()
