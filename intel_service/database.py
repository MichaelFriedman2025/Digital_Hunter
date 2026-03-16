from sqlalchemy import Column,Integer,String,FLOAT,Date,create_engine
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
class Intel(Base):
    __tablename__ = "intel"
    signal_id = Column(String(100),primary_key=True) 
    entity_id = Column(String(100))
    reported_lat = Column(FLOAT)
    reported_lon = Column(FLOAT)
    signal_type = Column(String(10))
    priority_level = Column(Integer)
    timestamp = Column(String(100))
    calculating_travel_distance = Column(FLOAT)

def add_a_table(engine):
    Base.metadata.create_all(engine)
    
def init_db():
    engine = get_connection()
    session = get_session(engine)
    add_a_table(engine)
    return session

def insert_data(session,data):
    data = Intel(**data)
    session.add(data)
    session.commit()

def update_data(session,signal_id,priority_level,calculating_travel_distance):
    data = session.get(Intel,signal_id)
    data.priority_level = priority_level
    data.calculating_travel_distance = calculating_travel_distance
    session.commit()

def check_if_signal_id_exist(session,signal_id):
    return session.get(Intel,signal_id)









