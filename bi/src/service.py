from typing import List, Optional

import pandas as pd
from database import AbstractDBClient
from logger import configure_logger
from repository import PredictionRepository
from repository import SalesRepository
from schema import Prediction
from schema import Sales

logger = configure_logger(__name__)


class BaseService(object):
    def __init__(
        self,
        db_client: AbstractDBClient,
    ):
        self.db_client = db_client


class SalesService(BaseService):
    def __init__(
        self,
        db_client: AbstractDBClient,
    ):
        super().__init__(db_client=db_client)
        self.sales_repository = SalesRepository(db_client=db_client)

    def retrieve_sales(
        self,
        store: Optional[str] = None,
        item: Optional[str] = None,
    ) -> pd.DataFrame:
        dataset = self.list_sales(
            store=store,
            item=item,
        )
        df = pd.DataFrame([d.dict() for d in dataset])
        df.sort_values(by=["store_id", "item_id", "date_id"])
        return df

    def list_sales(
        self,
        store: Optional[str] = None,
        item: Optional[str] = None,
    ) -> List[Sales]:
        data: List[Sales] = []        
        limit = 10000
        offset = 0
        while True:
            sales_data = self.sales_repository.select(
                store=store,
                item=item,
                limit=limit,
                offset=offset,
            )
            if len(sales_data) == 0:
                logger.info(f"done loading {len(sales_data)} records")
                break
            data.extend(sales_data)
            offset += limit
            logger.info(f"found {len(sales_data)} records...")
            logger.info(f"found {sales_data} ")
        return data


class PredictionService(BaseService):
    def __init__(
        self,
        db_client: AbstractDBClient,
    ):
        super().__init__(db_client=db_client)
        self.prediction_repository = PredictionRepository(db_client=db_client)

    def retrieve_prediction(
        self,
        store: Optional[str] = None,
        item: Optional[str] = None,
    ) -> pd.DataFrame:
        dataset = self.list_prediction(
            store=store,
            item=item,
        )
        df = pd.DataFrame([d.dict() for d in dataset])
        df.sort_values(by=["store_id", "item_id", "date_id"])
        return df

    def list_prediction(
        self,
        store: Optional[str] = None,
        item: Optional[str] = None,
    ) -> List[Prediction]:
        data: List[Prediction] = []        
        limit = 10000
        offset = 0
        while True:
            prediction_data = self.prediction_repository.select(
                store=store,
                item=item,
                limit=limit,
                offset=offset,
            )
            if len(prediction_data) == 0:
                logger.info(f"done loading {len(prediction_data)} records")
                break
            data.extend(prediction_data)
            offset += limit
            logger.info(f"found {len(prediction_data)} records...")
        return data

