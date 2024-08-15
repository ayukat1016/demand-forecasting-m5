from abc import ABC, abstractmethod

from src.infrastructure.database import AbstractDBClient


class AbstractTablesRepository(ABC):
    def __init__(
        self,
        db_client: AbstractDBClient,
    ):
        self.db_client = db_client

    @abstractmethod
    def create_tables(
        self,
        query: str,
    ):
        raise NotImplementedError


class TablesRepository(AbstractTablesRepository):
    def __init__(
        self,
        db_client: AbstractDBClient,
    ):
        super().__init__(db_client=db_client)

    def create_tables(
        self,
        query: str,
    ):
        self.db_client.execute_create_query(query=query)
