from abc import ABC, abstractmethod
from typing import List, Optional

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


class AbstractSelectRepository(ABC):
    def __init__(
        self,
        db_client: AbstractDBClient,
    ):
        self.db_client = db_client

    @abstractmethod
    def select(
        self,
        date_from: Optional[int] = None,
        date_to: Optional[int] = None,
        limit: int = 200,
        offset: int = 0,
    ) -> List[AbstractSchema]:
        raise NotImplementedError
