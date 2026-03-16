from kafka_consumer import KafkaConsumer
from kafka_producer import KafkaProducer
from schemas import IntelData
from database import init_db
from dal import check_if_entity_id_exist,insert_data_to_intel_table,insert_data_to_target_table,update_data
from haversine import haversine_km

kafka_consumer = KafkaConsumer()
kafka_producer = KafkaProducer()
session = init_db()
try:
    while True:
        data = kafka_consumer.recive_data()
        if data is None:
            continue
        else:
            try:
                IntelData(**data)
            except Exception as e:
                kafka_producer.prduce_data(data)
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
                
            print(f"data: {data}")
except KeyboardInterrupt:
    print("\n🔴 Stopping consumer")

finally:
    kafka_consumer.consumer.close()
    session.close()