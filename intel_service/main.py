from kafka_consumer import KafkaConsumer
from schemas import IntelData

kafka_consumer = KafkaConsumer()

try:
    while True:
        data = kafka_consumer.recive_data()
        if data is None:
            continue
        else:
            try:
                IntelData(**data)
            except Exception as e:
                print(data)
except KeyboardInterrupt:
    print("\n🔴 Stopping consumer")

finally:
    kafka_consumer.consumer.close()