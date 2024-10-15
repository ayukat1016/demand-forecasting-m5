from abc import ABC, abstractmethod
from typing import List, Optional

from src.infrastructure.database.db_client import AbstractDBClient
from src.infrastructure.schema.sales_calendar_schema import SalesCalendar


class AbstractSalesCalendarRepository(ABC):
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
    ) -> List[SalesCalendar]:
        raise NotImplementedError
