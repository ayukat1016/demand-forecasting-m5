from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import aliased

from src.domain.repository.sales_calendar_prices_repository import (
    AbstractSalesCalendarPricesRepository,
)
from src.infrastructure.database.db_client import AbstractDBClient
from src.infrastructure.schema.models import Calendar as CalendarModel
from src.infrastructure.schema.models import Prices as PricesModel
from src.infrastructure.schema.models import Sales as SalesModel
from src.infrastructure.schema.sales_calendar_prices_schema import SalesCalendarPrices
from src.infrastructure.schema.tables_schema import TABLES


class SalesCalendarPricesRepository(AbstractSalesCalendarPricesRepository):
    def __init__(
        self,
        db_client: AbstractDBClient,
    ) -> None:
        super().__init__(db_client=db_client)
        self.sales_table = TABLES.SALES.value
        self.calendar_table = TABLES.CALENDAR.value
        self.prices_table = TABLES.PRICES.value

    def select(
        self,
        date_from: Optional[int] = None,
        date_to: Optional[int] = None,
        limit: int = 1000,
        offset: int = 0,
    ) -> List[SalesCalendarPrices]:
        with self.db_client.get_session() as session:
            # まず、sales と calendar を結合
            sales = aliased(SalesModel)
            calendar = aliased(CalendarModel)
            prices = aliased(PricesModel)

            # サブクエリで sales と calendar を結合
            sales_calendar_subq = (
                select(
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
                )
                .select_from(sales)
                .join(calendar, calendar.date_id == sales.date_id)
                .order_by(sales.store_id, sales.item_id, sales.date_id)
            )

            if date_from is not None:
                sales_calendar_subq = sales_calendar_subq.where(
                    sales.date_id >= date_from
                )
            if date_to is not None:
                sales_calendar_subq = sales_calendar_subq.where(
                    sales.date_id <= date_to
                )

            sales_calendar_subq = sales_calendar_subq.alias()  # type: ignore[assignment]

            # メインクエリで prices を結合
            query = (
                select(
                    sales_calendar_subq.c.id,
                    sales_calendar_subq.c.item_id,
                    sales_calendar_subq.c.dept_id,
                    sales_calendar_subq.c.cat_id,
                    sales_calendar_subq.c.store_id,
                    sales_calendar_subq.c.state_id,
                    sales_calendar_subq.c.date_id,
                    sales_calendar_subq.c.sales,
                    sales_calendar_subq.c.wm_yr_wk,
                    sales_calendar_subq.c.event_name_1,
                    sales_calendar_subq.c.event_type_1,
                    sales_calendar_subq.c.event_name_2,
                    sales_calendar_subq.c.event_type_2,
                    sales_calendar_subq.c.snap_ca,
                    sales_calendar_subq.c.snap_tx,
                    sales_calendar_subq.c.snap_wi,
                    prices.sell_price,
                )
                .select_from(sales_calendar_subq)  # type: ignore[arg-type]
                .join(
                    prices,
                    (prices.store_id == sales_calendar_subq.c.store_id)
                    & (prices.item_id == sales_calendar_subq.c.item_id)
                    & (prices.wm_yr_wk == sales_calendar_subq.c.wm_yr_wk),
                    isouter=True,
                )
                .order_by(
                    sales_calendar_subq.c.store_id,
                    sales_calendar_subq.c.item_id,
                    sales_calendar_subq.c.date_id,
                )
            )

            results = session.execute(query.offset(offset).limit(limit)).all()
            data = [
                SalesCalendarPrices(
                    id=row.id,
                    item_id=row.item_id,
                    dept_id=row.dept_id,
                    cat_id=row.cat_id,
                    store_id=row.store_id,
                    state_id=row.state_id,
                    date_id=row.date_id,
                    sales=row.sales,
                    wm_yr_wk=row.wm_yr_wk,
                    event_name_1=row.event_name_1,
                    event_type_1=row.event_type_1,
                    event_name_2=row.event_name_2,
                    event_type_2=row.event_type_2,
                    snap_ca=row.snap_ca,
                    snap_tx=row.snap_tx,
                    snap_wi=row.snap_wi,
                    sell_price=row.sell_price,
                )
                for row in results
            ]
        return data
