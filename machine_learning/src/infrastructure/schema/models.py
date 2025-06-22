from typing import TYPE_CHECKING

from sqlalchemy import Column, Float, Integer, String, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

if TYPE_CHECKING:
    from sqlalchemy.orm import DeclarativeBase

    Base = DeclarativeBase


class Calendar(Base):  # type: ignore[valid-type,misc]
    __tablename__ = "calendar"
    date = Column(String, primary_key=True)
    wm_yr_wk = Column(Integer)
    weekday = Column(String)
    wday = Column(Integer)
    month = Column(Integer)
    year = Column(Integer)
    date_id = Column(Integer)
    event_name_1 = Column(String)
    event_type_1 = Column(String)
    event_name_2 = Column(String)
    event_type_2 = Column(String)
    snap_ca = Column(Integer)
    snap_tx = Column(Integer)
    snap_wi = Column(Integer)


class Prices(Base):  # type: ignore[valid-type,misc]
    __tablename__ = "prices"
    key = Column(String, primary_key=True)
    store_id = Column(String)
    item_id = Column(String)
    wm_yr_wk = Column(Integer)
    sell_price = Column(Float)
    __table_args__ = (
        UniqueConstraint(
            "store_id", "item_id", "wm_yr_wk", name="uix_prices_store_item_week"
        ),
    )


class Sales(Base):  # type: ignore[valid-type,misc]
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


class Prediction(Base):  # type: ignore[valid-type,misc]
    __tablename__ = "prediction"
    store_id = Column(String, primary_key=True)
    item_id = Column(String, primary_key=True)
    date_id = Column(Integer, primary_key=True)
    prediction = Column(Float)
