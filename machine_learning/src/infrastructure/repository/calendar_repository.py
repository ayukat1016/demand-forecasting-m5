from typing import List

from src.domain.repository.calendar_repository import AbstractCalendarRepository
from src.infrastructure.database.db_client import AbstractDBClient
from src.infrastructure.schema.calendar_schema import Calendar
from src.infrastructure.schema.tables_schema import TABLES
from src.infrastructure.schema.models import Calendar as CalendarModel


class CalendarRepository(AbstractCalendarRepository):
    def __init__(
        self,
        db_client: AbstractDBClient,
    ):
        super().__init__(db_client=db_client)
        self.table_name = TABLES.CALENDAR.value

    def select(
        self,
        limit: int = 200,
        offset: int = 0,
    ) -> List[Calendar]:
        with self.db_client.get_session() as session:
            query = session.query(CalendarModel).offset(offset).limit(limit)
            results = query.all()
            data = [Calendar(**{k: getattr(row, k) for k in Calendar.model_fields.keys()}) for row in results]
        return data
