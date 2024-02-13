from typing import List, Optional

import numpy as np
import pandas as pd
from database import AbstractDBClient
from logger import configure_logger
from repository import SalesRepository

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

    def list_sales(
        self,
        # item: Optional[str] = None,
        # store: Optional[str] = None,
        # date_from: Optional[int] = None,
        # date_to: Optional[int] = None,
    ) -> List[Sales]:
        data: List[Sales] = []        
        limit = 10000
        offset = 0
        while True:
            sales_data = self.sales_repository.select(
                # date_from=date_from,
                # date_to=date_to,
                # item=item,
                # store=store,
                limit=limit,
                offset=offset,
            )
            if len(sales_data) == 0:
                logger.info(f"done loading {len(sales_data)} records")
                break
            data.extend(sales_data)
            offset += limit
            logger.info(f"found {len(sales_data)} records...")
        return data

    def retrieve_sales(
        self,
        # date_from: Optional[int] = None,
        # date_to: Optional[int] = None,
        # item: Optional[str] = None,
        # store: Optional[str] = None,
    ) -> pd.DataFrame:
        dataset = self.list_sales(
            # date_from=date_from,
            # date_to=date_to,
            # item=item,
            # store=store,
        )
        df = pd.DataFrame([d.dict() for d in dataset])
        # df["date"] = pd.to_datetime(df["date"])
        # df["month"] = df.date.dt.month
        # df["year"] = df.date.dt.year
        df = df.drop("id", axis=1)
        return df

    def retrieve_daily_sales(
        self,
        # date_from: Optional[date] = None,
        # date_to: Optional[date] = None,
        date_from: Optional[int] = None,
        date_to: Optional[int] = None,        
        # day_of_week: Optional[str] = None,
        item: Optional[str] = None,
        store: Optional[str] = None,
        # region: Optional[str] = None,
    ) -> pd.DataFrame:
        df = self.retrieve_sales(
            date_from=date_from,
            date_to=date_to,
            # day_of_week=day_of_week,
            item=item,
            store=store,
            # region=region,
        )
        logger.info(
            f"""
daily df
    df shape: {df.shape}
    df columns: {df.columns}
                """
        )
        logger.info(df)
        return df


