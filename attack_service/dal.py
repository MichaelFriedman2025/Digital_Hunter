from database import Attack,Target


def insert_data_to_attack_table(session,data):
    data = Attack(**data)
    session.add(data)
    session.commit()


def update_data(session,entity_id):
    data = session.get(Target,entity_id)
    data.is_attacted = True
    session.commit()

def check_if_entity_id_exist(session,entity_id):
    return session.get(Target,entity_id)