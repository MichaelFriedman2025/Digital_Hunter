from kafka_consumer import KafkaConsumer
from kafka_producer import KafkaProducer
from schemas import AttackData
from database import get_connection
from dal import check_if_entity_id_exist,update_data,insert_data_to_attack_table


kafka_consumer = KafkaConsumer()
kafka_producer = KafkaProducer()
session = get_connection()

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
        res_check = check_if_entity_id_exist(session,data["entity_id"])
        if res_check:
            if res_check.status_result != "destroyed":
                update_data(session,data["entity_id"])
                insert_data_to_attack_table(session,data)

except KeyboardInterrupt:
    print("\n🔴 Stopping consumer")

finally:
    kafka_consumer.consumer.close()