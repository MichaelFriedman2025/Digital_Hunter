from kafka_consumer import KafkaConsumer
from kafka_producer import KafkaProducer
from schemas import IntelData
from database import get_connection
from dal import check_if_entity_id_exist,insert_data_to_intel_table,insert_data_to_target_table,update_data
from haversine import haversine_km
from logger import log_event

kafka_consumer = KafkaConsumer()
kafka_producer = KafkaProducer()
session = get_connection()

try:
    log_event("info","intel service running...")
    while True:
        data = kafka_consumer.recive_data()
        if data is None:
            continue
        else:
            try:
                IntelData(**data)
                log_event("info","intel service validation work successfully")
            except Exception as e:
                kafka_producer.prduce_data(data)
                log_event("error","intel service validation failed")
                continue

            res_check = check_if_entity_id_exist(session,data["entity_id"])
            if res_check:
                location = res_check.reported_lat,res_check.reported_lon
                res_haversine_km = haversine_km(data["reported_lat"],data["reported_lon"],location[0],location[1])
                data["calculating_travel_distance"] = res_haversine_km
                update_data(session,data["entity_id"],data["priority_level"],data["reported_lat"],data["reported_lon"],res_haversine_km)
                insert_data_to_intel_table(session,data)
            else:
                data["calculating_travel_distance"] = 0.0
                target_data = {"entity_id":data["entity_id"],
                               "priority_level":99,
                               "reported_lat":data["reported_lat"],
                               "reported_lon":data["reported_lon"],
                               "calculating_travel_distance":0.0}
                insert_data_to_intel_table(session,data)
                insert_data_to_target_table(session,target_data)
            log_event("info","intel service insert data successfully")

                
except KeyboardInterrupt:
    print("\n🔴 Stopping consumer")

finally:
    log_event("info","intel service finish.")
    kafka_consumer.consumer.close()
    session.close()