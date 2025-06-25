from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Sales(Base):  # type: ignore
    __tablename__ = "sales"
    key = Column(String, primary_key=True)
    id = Column(String)
    item_id = Column(String)
    dept_id = Column(String)
    cat_id = Column(String)
    store_id = Column(String)
    state_id = Column(String)
    date_id = Column(Integer)
    sales = Column(Float)


class Prediction(Base):  # type: ignore
    __tablename__ = "prediction"
    store_id = Column(String, primary_key=True)
    item_id = Column(String, primary_key=True)
    date_id = Column(Integer, primary_key=True)
    prediction = Column(Float)
