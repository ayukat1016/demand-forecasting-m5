from typing import List, Optional, Union

from src.domain.repository.sales_calendar_repository import (
    AbstractSalesCalendarRepository,
)
from src.infrastructure.database.db_client import AbstractDBClient
from src.infrastructure.schema.sales_calendar_schema import SalesCalendar
from src.infrastructure.schema.tables_schema import TABLES
from src.infrastructure.schema.models import Sales as SalesModel, Calendar as CalendarModel, SalesCalendar as SalesCalendarModel
from sqlalchemy.orm import aliased


class SalesCalendarRepository(AbstractSalesCalendarRepository):
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
        with self.db_client.get_session() as session:
            sales = aliased(SalesModel)
            calendar = aliased(CalendarModel)
            query = session.query(
                sales.id,
                sales.item_id,
                sales.dept_id,
                sales.cat_id,
                sales.store_id,
                sales.state_id,
                sales.date_id,
                sales.sales,
                calendar.wm_yr_wk,
                calendar.event_name_1,
                calendar.event_type_1,
                calendar.event_name_2,
                calendar.event_type_2,
                calendar.snap_ca,
                calendar.snap_tx,
                calendar.snap_wi,
            ).join(
                calendar, calendar.date_id == sales.date_id, isouter=True
            )
            if date_from is not None:
                query = query.filter(sales.date_id >= date_from)
            if date_to is not None:
                query = query.filter(sales.date_id <= date_to)
            results = query.offset(offset).limit(limit).all()
            data = [SalesCalendar(**{k: v for k, v in zip(SalesCalendar.model_fields.keys(), row)}) for row in results]
        return data
