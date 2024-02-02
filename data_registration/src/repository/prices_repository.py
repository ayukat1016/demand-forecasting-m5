from typing import List

from src.infrastructure.database import AbstractDBClient
from src.model.prices import Prices
from src.model.table import TABLES
from src.repository.abstract_repository import AbstractRepository


# class AbstractPricesRepository(ABC):
#     def __init__(
#         self,
#         db_client: AbstractDBClient,
#     ):
#         self.db_client = db_client
#         self.table_name = TABLES.PRICES.value

#     @abstractmethod
#     def bulk_insert(
#         self,
#         sales: List[Prices],
#     ):
#         raise NotImplementedError


class PricesRepository(AbstractRepository):
    def __init__(
        self,
        db_client: AbstractDBClient,
    ):
        super().__init__(db_client=db_client)
        self.table_name = TABLES.PRICES.value

    def bulk_insert(
        self,
        records: List[Prices],
    ):
        data = records[0].dict()
        _columns = list(data.keys())
        columns = ",".join(_columns)
        query = f"""
        INSERT INTO
            {self.table_name}
            ({columns})
        VALUES
            %s
        ON CONFLICT
            (key)
        DO NOTHING
        ;
        """

        parameters = []
        for d in records:
            values = tuple(d.dict().values())
            parameters.append(values)
        self.db_client.execute_bulk_insert_or_update_query(
            query=query,
            parameters=parameters,
        )
