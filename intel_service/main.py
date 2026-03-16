from kafka_consumer import KafkaConsumer
from kafka_producer import KafkaProducer
from schemas import IntelData
from database import init_db, check_if_signal_id_exist,insert_data,update_data
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
            print(data["entity_id"])
            res_check = check_if_signal_id_exist(session,data["entity_id"])
            if res_check:
                location = res_check.reported_lat,res_check.reported_lon
                res_haversine_km = haversine_km(data["reported_lat"],data["reported_lon"],location[0],location[1])
                update_data(session,data["signal_id"],data["priority_level"],res_haversine_km)
                print("A")
            else:
                data["priority_level"] = 99
                data["calculating_travel_distance"] = 0
                insert_data(session,data)

except KeyboardInterrupt:
    print("\n🔴 Stopping consumer")

finally:
    kafka_consumer.consumer.close()