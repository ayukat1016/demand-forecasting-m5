from abc import ABC, abstractmethod
from typing import List

from src.infrastructure.database.db_client import AbstractDBClient
from src.infrastructure.schema.sales_schema import Sales


class AbstractSalesRepository(ABC):
    def __init__(
        self,
        db_client: AbstractDBClient,
    ) -> None:
        self.db_client = db_client

    @abstractmethod
    def bulk_insert(
        self,
        records: List[Sales],
    ) -> None:
        raise NotImplementedError
