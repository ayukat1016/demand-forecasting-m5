from typing import List

from src.infrastructure.database import AbstractDBClient
from src.repository.abstract_repository import AbstractSelectRepository
from src.schema.calendar_schema import Calendar
from src.schema.table_schema import TABLES


class CalendarRepository(AbstractSelectRepository):
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
        query = f"""
        SELECT
            {self.table_name}.date as date,
            {self.table_name}.wm_yr_wk as wm_yr_wk,
            {self.table_name}.weekday as weekday,
            {self.table_name}.wday as wday,
            {self.table_name}.month as month,
            {self.table_name}.year as year,
            {self.table_name}.date_id as date_id,
            {self.table_name}.event_name_1 as event_name_1,
            {self.table_name}.event_type_1 as event_type_1,
            {self.table_name}.event_name_2 as event_name_2,
            {self.table_name}.event_type_2 as event_type_2,
            {self.table_name}.snap_ca as snap_ca,
            {self.table_name}.snap_tx as snap_tx,
            {self.table_name}.snap_wi as snap_wi
        FROM
            {self.table_name}
        """

        query += f"""
        LIMIT
            {limit}
        OFFSET
            {offset}
        ;
        """
        records = self.db_client.execute_select(
            query=query,
        )
        data = [Calendar(**r) for r in records]
        return data
