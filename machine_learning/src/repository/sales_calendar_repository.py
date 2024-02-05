from typing import List, Optional, Union

from src.infrastructure.database import AbstractDBClient
from src.model.sales_calendar_model import SalesCalendar
from src.model.table_model import TABLES
from src.repository.abstract_repository import AbstractSelectRepository


class SalesCalendarRepository(AbstractSelectRepository):
    def __init__(
        self,
        db_client: AbstractDBClient,
    ):
        super().__init__(db_client=db_client)
        self.sales_table = TABLES.SALES.value
        self.calendar_table = TABLES.CALENDAR.value        

    def select(
        self,
        date_from: Optional[int] = None,
        date_to: Optional[int] = None,
        limit: int = 1000,
        offset: int = 0,
    ) -> List[SalesCalendar]:
        parameters: List[Union[int, str, bool, float]] = []

        query = f"""
        SELECT
            {self.sales_table}.id as id,
            {self.sales_table}.item_id as item_id,
            {self.sales_table}.dept_id as dept_id,
            {self.sales_table}.cat_id as cat_id,
            {self.sales_table}.store_id as store_id,
            {self.sales_table}.state_id as state_id,
            {self.sales_table}.date_id as date_id,
            {self.sales_table}.sales as sales,
            {self.calendar_table}.wm_yr_wk as wm_yr_wk,
            {self.calendar_table}.event_name_1 as event_name_1,
            {self.calendar_table}.event_type_1 as event_type_1,
            {self.calendar_table}.event_name_2 as event_name_2,
            {self.calendar_table}.event_type_2 as event_type_2,
            {self.calendar_table}.snap_ca as snap_ca,
            {self.calendar_table}.snap_tx as snap_tx,
            {self.calendar_table}.snap_wi as snap_wi
        FROM
            {self.sales_table}
        LEFT JOIN
            {self.calendar_table}
        ON
            {self.calendar_table}.date_id = {self.sales_table}.date_id
        """

        where = "where"

        if date_from is not None:
            query += f"""
            {where}
                {self.sales_table}.date_id >= %s
            """
            parameters.append(date_from)
            where = "AND"

        if date_to is not None:
            query += f"""
            {where}
                {self.sales_table}.date_id <= %s
            """
            parameters.append(date_to)
            where = "AND"        

        query += f"""        
        LIMIT
            {limit}
        OFFSET
            {offset}
        ;
        """
        records = self.db_client.execute_select(
            query=query,
            parameters=tuple(parameters),
        )
        data = [SalesCalendar(**r) for r in records]
        return data
