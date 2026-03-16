from kafka_consumer import KafkaConsumer
from kafka_producer import KafkaProducer
from schemas import AttackData
from database import get_connection
from dal import check_if_entity_id_exist,update_data,insert_data_to_attack_table
from logger import log_event


kafka_consumer = KafkaConsumer()
kafka_producer = KafkaProducer()
session = get_connection()

try:
    log_event("info","attck service running...")
    while True:
        data = kafka_consumer.recive_data()
        if data is None:
            continue
        else:
            try:
                AttackData(**data)
                log_event("info","attack service validation work successfully")
            except Exception:
                log_event("error","attack service validation failed")
                kafka_producer.prduce_data(data)
                continue
        res_check = check_if_entity_id_exist(session,data["entity_id"])
        if res_check:
            if res_check.status_result != "destroyed":
                update_data(session,data["entity_id"])
                insert_data_to_attack_table(session,data)
                log_event("info","attack service insert data successfully")

except KeyboardInterrupt:
    print("\n🔴 Stopping consumer")

finally:
    log_event("info","attack service finish.")
    kafka_consumer.consumer.close()
    session.close()