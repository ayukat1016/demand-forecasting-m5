from abc import ABC, abstractmethod

from src.infrastructure.database import AbstractDBClient
from src.middleware.logger import configure_logger
from src.model.abstract_model import AbstractModel

logger = configure_logger(__name__)


class AbstractRepository(ABC):
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


class AbstractTableRepository(ABC):
    def __init__(
        self,
        db_client: AbstractDBClient,
    ):
        self.db_client = db_client

    @abstractmethod
    def create_tables(
        self,
        # file_path: str,
        query: str,        
    ):
        raise NotImplementedError
