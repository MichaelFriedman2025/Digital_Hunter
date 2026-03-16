from kafka_consumer import KafkaConsumer
from kafka_producer import KafkaProducer
from schemas import AttackData


kafka_consumer = KafkaConsumer()
kafka_producer = KafkaProducer()

try:
    while True:
        data = kafka_consumer.recive_data()
        if data is None:
            continue
        else:
            try:
                AttackData(**data)
            except Exception as e:
                kafka_producer.prduce_data(data)
                continue
            print(data)


except KeyboardInterrupt:
    print("\n🔴 Stopping consumer")

finally:
    kafka_consumer.consumer.close()