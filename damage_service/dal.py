from database import Attack,Target,Damage


def insert_data_to_damage_table(session,data):
    data = Damage(**data)
    session.add(data)
    session.commit()


def update_data(session,entity_id,result):
    data = session.get(Target,entity_id)
    data.status_result = result
    session.commit()

def check_if_entity_id_exist(session,entity_id):
    return session.get(Target,entity_id)

def check_if_attack_id_exist(session,attack_id):
    return session.get(Attack,attack_id)