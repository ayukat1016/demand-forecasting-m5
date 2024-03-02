from typing import List, Optional, Union

from database import AbstractDBClient
from schema import Prediction
from schema import Sales
from table import TABLES

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
        self.calendar_table = TABLES.CALENDAR.value

    def select(
        self,
        store: Optional[str] = None,
        item: Optional[str] = None,
        limit: int = 200,
        offset: int = 0,
    ) -> List[Sales]:
        parameters: List[Union[int, str, bool, float]] = []
        query = f"""
        SELECT
            {self.sales_table}.store_id as store_id,
            {self.sales_table}.item_id as item_id,
            {self.sales_table}.date_id as date_id,
            {self.calendar_table}.date as date,
            {self.calendar_table}.wm_yr_wk as wm_yr_wk,
            {self.calendar_table}.event_name_1 as event_name_1,
            {self.calendar_table}.event_type_1 as event_type_1,
            {self.calendar_table}.event_name_2 as event_name_2,
            {self.calendar_table}.event_type_2 as event_type_2,
            {self.calendar_table}.snap_ca as snap_ca,
            {self.calendar_table}.snap_tx as snap_tx,
            {self.calendar_table}.snap_wi as snap_wi,
            {self.sales_table}.sales as sales
        FROM
            {self.sales_table}
        LEFT JOIN
            {self.calendar_table}
        ON
            {self.calendar_table}.date_id = {self.sales_table}.date_id
        """

        where = "where"

        if store is not None:
            query += f"""
            {where}
                {self.sales_table}.store_id = %s
            """
            parameters.append(store)
            where = "AND"

        if item is not None:
            query += f"""
            {where}
                {self.sales_table}.item_id = %s
            """
            parameters.append(item)
            where = "AND"

        query += f"""
        LIMIT
            {limit}
        OFFSET
            {offset}
        ;
        """
        records = self.db_client.execute_select(
            query=query,
            parameters=tuple(parameters),
        )
        data = [Sales(**r) for r in records]
        return data


class PredictionRepository(BaseRepository):
    def __init__(
        self,
        db_client: AbstractDBClient,
    ):
        super().__init__(db_client=db_client)
        self.prediction_table = TABLES.PREDICTION.value
        self.calendar_table = TABLES.CALENDAR.value

    def select(
        self,
        store: Optional[str] = None,
        item: Optional[str] = None,
        limit: int = 200,
        offset: int = 0,
    ) -> List[Prediction]:
        parameters: List[Union[int, str, bool, float]] = []
        query = f"""
        SELECT
            {self.prediction_table}.store_id as store_id,
            {self.prediction_table}.item_id as item_id,
            {self.prediction_table}.date_id as date_id,
            {self.calendar_table}.date as date,
            {self.prediction_table}.prediction as prediction
        FROM
            {self.prediction_table}
        LEFT JOIN
            {self.calendar_table}
        ON
            {self.calendar_table}.date_id = {self.prediction_table}.date_id
        """

        where = "where"

        if store is not None:
            query += f"""
            {where}
                {self.prediction_table}.store_id = %s
            """
            parameters.append(store)
            where = "AND"

        if item is not None:
            query += f"""
            {where}
                {self.prediction_table}.item_id = %s
            """
            parameters.append(item)
            where = "AND"

        query += f"""
        LIMIT
            {limit}
        OFFSET
            {offset}
        ;
        """
        records = self.db_client.execute_select(
            query=query,
            parameters=tuple(parameters),
        )
        data = [Prediction(**r) for r in records]
        return data
