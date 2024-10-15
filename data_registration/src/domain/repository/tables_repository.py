from abc import ABC, abstractmethod

from src.infrastructure.database.db_client import AbstractDBClient


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
