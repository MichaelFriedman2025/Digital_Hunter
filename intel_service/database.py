from sqlalchemy import Column,Integer,String,Float,Boolean,create_engine
from sqlalchemy.orm import declarative_base,sessionmaker



def get_connection():
    db_url = "mysql+pymysql://user:password@localhost/mydb"
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


Base = declarative_base()
class Intel(Base):
    __tablename__ = "intel"
    signal_id = Column(String(100),primary_key=True) 
    entity_id = Column(String(100))
    reported_lat = Column(Float)
    reported_lon = Column(Float)
    signal_type = Column(String(10))
    priority_level = Column(Integer)
    calculating_travel_distance = Column(Float)
    timestamp = Column(String(100))


class Target(Base):
    __tablename__ = "target"
    entity_id = Column(String(100),primary_key=True)
    priority_level = Column(Integer)
    reported_lat = Column(Float)
    reported_lon = Column(Float)
    calculating_travel_distance = Column(Float)
    is_attacted = Column(Boolean)