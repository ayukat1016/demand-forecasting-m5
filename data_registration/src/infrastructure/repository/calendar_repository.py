from typing import List

from sqlalchemy.dialects.postgresql import insert

from src.domain.repository.calendar_repository import AbstractCalendarRepository
from src.infrastructure.database.db_client import AbstractDBClient
from src.infrastructure.schema.calendar_schema import Calendar
from src.infrastructure.schema.models import Calendar as CalendarModel
from src.infrastructure.schema.tables_schema import TABLES


class CalendarRepository(AbstractCalendarRepository):
    def __init__(
        self,
        db_client: AbstractDBClient,
    ) -> None:
        super().__init__(db_client=db_client)
        self.table_name = TABLES.CALENDAR.value

    def bulk_insert(
        self,
        records: List[Calendar],
    ) -> None:
        with self.db_client.get_session() as session:
            values = [
                {
                    k: v
                    for k, v in record.model_dump().items()
                    if k in CalendarModel.__table__.columns.keys()
                }
                for record in records
            ]
            stmt = insert(CalendarModel).values(values)
            stmt = stmt.on_conflict_do_nothing(index_elements=["date"])
            session.execute(stmt)
            session.commit()
