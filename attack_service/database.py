from sqlalchemy import Column,String,create_engine
from sqlalchemy.orm import declarative_base,sessionmaker


def get_connection():
    db_url = "sqlite:///mydb.db"
    engine = create_engine(db_url)
    return engine

def get_session(engine):
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

Base = declarative_base()
class Attack(Base):
    __tablename__ = "attack"
    timestamp = Column(String(100))
    attack_id = Column(String(100))
    entity_id = Column(String(100))
    weapon_type = Column(String(100))

def add_a_table(engine):
    Base.metadata.create_all(engine)
    
def init_db():
    engine = get_connection()
    session = get_session(engine)
    add_a_table(engine)
    return session

def insert_data(session,data):
    data = Attack(**data)
    session.add(data)
    session.commit()











