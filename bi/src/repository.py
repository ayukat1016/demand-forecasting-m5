from typing import List

from database import AbstractDBClient
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
        limit: int = 200,
        offset: int = 0,
    ) -> List[Sales]:
        query = f"""
        SELECT
            {self.table_name}.key,
            {self.table_name}.id as id,
            {self.table_name}.item_id as item_id,
            {self.table_name}.dept_id as dept_id,
            {self.table_name}.cat_id as cat_id,
            {self.table_name}.store_id as store_id,
            {self.table_name}.state_id as state_id,
            {self.table_name}.date_id as date_id,
            {self.table_name}.sales as sales
        FROM
            {self.table_name}
        """

        query += f"""
        LIMIT
            {limit}
        OFFSET
            {offset}
        ;
        """
        records = self.db_client.execute_select(
            query=query,
        )
        data = [Sales(**r) for r in records]
        return data
    