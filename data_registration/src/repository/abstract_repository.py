from abc import ABC, abstractmethod

from src.infrastructure.database import AbstractDBClient
from src.schema.abstract_schema import AbstractSchema


class AbstractBulkInsertRepository(ABC):
    def __init__(
        self,
        db_client: AbstractDBClient,
    ):
        self.db_client = db_client

    @abstractmethod
    def bulk_insert(
        self,
        record: AbstractSchema,
    ):
        raise NotImplementedError


class AbstractCreateTablesRepository(ABC):
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
