from typing import List, Optional, Union

from database import AbstractDBClient
from models import Sales as SalesModel, Prediction as PredictionModel
from schema import Prediction, Sales
from tables import TABLES


class BaseRepository(object):
    def __init__(
        self,
        db_client: AbstractDBClient,
    ):
        self.db_client = db_client


class SalesRepository(BaseRepository):
    def __init__(
        self,
        db_client: AbstractDBClient,
    ):
        super().__init__(db_client=db_client)
        self.sales_table = TABLES.SALES.value

    def select(
        self,
        store: Optional[str] = None,
        item: Optional[str] = None,
        limit: int = 200,
        offset: int = 0,
    ) -> List[Sales]:
        with self.db_client.get_session() as session:
            sales = session.query(SalesModel)
            if store is not None:
                sales = sales.filter(SalesModel.store_id == store)
            if item is not None:
                sales = sales.filter(SalesModel.item_id == item)
            sales = sales.order_by(SalesModel.store_id, SalesModel.item_id, SalesModel.date_id)
            sales = sales.limit(limit).offset(offset)
            results = sales.all()
            data = [Sales.from_orm(row) for row in results]
        return data

    def list_stores(self) -> list:
        with self.db_client.get_session() as session:
            stores = session.query(SalesModel.store_id).distinct().all()
            return [s[0] for s in stores]

    def list_items(self) -> list:
        with self.db_client.get_session() as session:
            items = session.query(SalesModel.item_id).distinct().all()
            return [i[0] for i in items]


class PredictionRepository(BaseRepository):
    def __init__(
        self,
        db_client: AbstractDBClient,
    ):
        super().__init__(db_client=db_client)
        self.prediction_table = TABLES.PREDICTION.value

    def select(
        self,
        store: Optional[str] = None,
        item: Optional[str] = None,
        limit: int = 200,
        offset: int = 0,
    ) -> List[Prediction]:
        with self.db_client.get_session() as session:
            prediction = session.query(PredictionModel)
            if store is not None:
                prediction = prediction.filter(PredictionModel.store_id == store)
            if item is not None:
                prediction = prediction.filter(PredictionModel.item_id == item)
            prediction = prediction.order_by(PredictionModel.store_id, PredictionModel.item_id, PredictionModel.date_id)
            prediction = prediction.limit(limit).offset(offset)
            results = prediction.all()
            data = [Prediction.from_orm(row) for row in results]
        return data
