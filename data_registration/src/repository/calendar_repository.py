from typing import List

from src.infrastructure.database import AbstractDBClient
from src.model.calendar_model import Calendar
from src.model.table_model import TABLES
from src.repository.abstract_repository import AbstractBulkInsertRepository


class CalendarRepository(AbstractBulkInsertRepository):
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
        data = records[0].dict()
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
            values = tuple(d.dict().values())
            parameters.append(values)
        self.db_client.execute_bulk_insert_or_update_query(
            query=query,
            parameters=parameters,
        )
