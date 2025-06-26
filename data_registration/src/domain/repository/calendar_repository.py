from abc import ABC, abstractmethod
from typing import List

from src.infrastructure.database.db_client import AbstractDBClient
from src.infrastructure.schema.calendar_schema import Calendar


class AbstractCalendarRepository(ABC):
    def __init__(
        self,
        db_client: AbstractDBClient,
    ) -> None:
        self.db_client = db_client

    @abstractmethod
    def bulk_insert(
        self,
        records: List[Calendar],
    ) -> None:
        raise NotImplementedError
