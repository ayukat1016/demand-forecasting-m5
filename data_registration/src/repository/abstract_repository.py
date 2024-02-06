from abc import ABC, abstractmethod

from src.infrastructure.database import AbstractDBClient
from src.middleware.logger import configure_logger
from src.model.abstract_model import AbstractModel

logger = configure_logger(__name__)


class AbstractBulkInsertRepository(ABC):
    def __init__(
        self,
        db_client: AbstractDBClient,
    ):
        self.db_client = db_client

    @abstractmethod
    def bulk_insert(
        self,
        record: AbstractModel,
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
