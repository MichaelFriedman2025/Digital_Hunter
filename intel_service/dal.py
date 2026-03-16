from database import Intel,Target


def insert_data_to_intel_table(session,data):
    data = Intel(**data)
    session.add(data)
    session.commit()

def insert_data_to_target_table(session,data):
    data = Target(**data)
    session.add(data)
    session.commit()

def update_data(session,entity_id,priority_level,lat,lon,calculating_travel_distance):
    data = session.get(Target,entity_id)
    data.priority_level = priority_level
    data.reported_lat = lat
    data.reported_lon = lon
    data.calculating_travel_distance = calculating_travel_distance
    session.commit()

def check_if_entity_id_exist(session,entity_id):
    return session.get(Target,entity_id)









