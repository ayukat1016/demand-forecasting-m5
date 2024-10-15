from typing import List

from src.domain.repository.prices_repository import AbstractPricesRepository
from src.infrastructure.database.db_client import AbstractDBClient
from src.infrastructure.schema.prices_schema import Prices
from src.infrastructure.schema.tables_schema import TABLES


class PricesRepository(AbstractPricesRepository):
    def __init__(
        self,
        db_client: AbstractDBClient,
    ):
        super().__init__(db_client=db_client)
        self.table_name = TABLES.PRICES.value

    def select(
        self,
        limit: int = 200,
        offset: int = 0,
    ) -> List[Prices]:
        query = f"""
        SELECT
            {self.table_name}.key,
            {self.table_name}.store_id,
            {self.table_name}.item_id,
            {self.table_name}.wm_yr_wk,
            {self.table_name}.sell_price
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
        data = [Prices(**r) for r in records]
        return data
