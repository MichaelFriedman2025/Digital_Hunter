from kafka_consumer import KafkaConsumer
from database import get_connection
from schemas import DamageData
from dal import check_if_entity_id_exist,check_if_attack_id_exist,update_data,insert_data_to_damage_table
from logger import log_event

kafka_consumer = KafkaConsumer()
session = get_connection()

try:
    log_event("info","damage service running...")
    while True:
        data = kafka_consumer.recive_data()
        if data is None:
            continue
        else:
            try:
                DamageData(**data)
                log_event("info","damage service validation work successfully")
            except Exception:
                log_event("error","damage service validation failed")
                continue
        res_check_entity = check_if_entity_id_exist(session,data["entity_id"])
        res_check_attack = check_if_attack_id_exist(session,data["attack_id"])
        if res_check_entity and res_check_attack:
            update_data(session,data["entity_id"],data["result"]) 
            log_event("info","damage service insert data successfully")

            

except KeyboardInterrupt:
    print("\n🔴 Stopping consumer")

finally:
    log_event("info","damage service finish.")
    kafka_consumer.consumer.close()
    session.close()