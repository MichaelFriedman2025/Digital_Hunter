from sqlalchemy import Column,Integer,String,Float,Boolean,create_engine
from sqlalchemy.orm import declarative_base,sessionmaker



def get_connection():
    db_url = "mysql+pymysql://user:password@localhost/mydb"
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


Base = declarative_base()
class Attack(Base):
    __tablename__ = "attack"
    attack_id = Column(String(100),primary_key=True) 
    entity_id = Column(String(100))
    weapon_type = Column(String(100))
    timestamp = Column(String(100))

class Damage(Base):
    __tablename__ = "demage"
    id = Column(Integer,primary_key=True,autoincrement=True)
    attack_id = Column(String(100)) 
    entity_id = Column(String(100))
    result = Column(String(10))
    timestamp = Column(String(100))

class Target(Base):
    __tablename__ = "target"
    entity_id = Column(String(100),primary_key=True)
    priority_level = Column(Integer)
    reported_lat = Column(Float)
    reported_lon = Column(Float)
    calculating_travel_distance = Column(Float)
    is_attacted = Column(Boolean)
    status_result = Column(String(10))