from typing import List

from src.domain.repository.calendar_repository import AbstractCalendarRepository
from src.infrastructure.database.db_client import AbstractDBClient
from src.infrastructure.schema.calendar_schema import Calendar
from src.infrastructure.schema.tables_schema import TABLES


class CalendarRepository(AbstractCalendarRepository):
    def __init__(
        self,
        db_client: AbstractDBClient,
    ):
        super().__init__(db_client=db_client)
        self.table_name = TABLES.CALENDAR.value

    def bulk_insert(
        self,
        records: List[Calendar],
    ):
        data = records[0].model_dump()
        _columns = list(data.keys())
        columns = ",".join(_columns)
        query = f"""
        INSERT INTO
            {self.table_name}
            ({columns})
        VALUES
            %s
        ON CONFLICT
            (date)
        DO NOTHING
        ;
        """

        parameters = []
        for d in records:
            values = tuple(d.model_dump().values())
            parameters.append(values)
        self.db_client.execute_bulk_insert_or_update_query(
            query=query,
            parameters=parameters,
        )
