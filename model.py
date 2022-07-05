
from sqlite3 import Timestamp
from pandas import DatetimeTZDtype
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Coins(Base):
    __tablename__ = 'Coins'  # if you use base it is obligatory
    id = Column(Integer, primary_key=True)  # obligatory
    name = Column(String)
    symbol = Column(String)
    data_added = Column(Text)
    last_updated = Column(Text)
    price = Column(Float)
    volume_24h = Column(Float)
   
    def start():
        db_string = "postgresql://postgres:Stack2022!@db1.cgmgkr9myokm.us-east-1.rds.amazonaws.com:5432/coins"
        engine = create_engine(db_string)
        Session = sessionmaker(bind=engine)
        session = Session()
        Base.metadata.create_all(engine)
        print ('\nTable created on database')
        return session, engine
