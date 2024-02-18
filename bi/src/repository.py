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
        self.table_name = TABLES.SALES.value

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
            {self.table_name}.store_id as store_id,
            {self.table_name}.item_id as item_id,
            {self.table_name}.date_id as date_id,
            {self.table_name}.sales as sales
        FROM
            {self.table_name}
        """

        where = "where"

        if store is not None:
            query += f"""
            {where}
                {self.table_name}.store_id = %s
            """
            parameters.append(store)
            where = "AND"

        if item is not None:
            query += f"""
            {where}
                {self.table_name}.item_id = %s
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
        self.table_name = TABLES.PREDICTION.value

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
            {self.table_name}.store_id as store_id,
            {self.table_name}.item_id as item_id,
            {self.table_name}.date_id as date_id,
            {self.table_name}.prediction as prediction
        FROM
            {self.table_name}
        """

        where = "where"

        if store is not None:
            query += f"""
            {where}
                {self.table_name}.store_id = %s
            """
            parameters.append(store)
            where = "AND"

        if item is not None:
            query += f"""
            {where}
                {self.table_name}.item_id = %s
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
