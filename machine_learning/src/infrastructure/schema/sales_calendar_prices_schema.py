from src.infrastructure.schema.abstract_schema import AbstractSchema


class SalesCalendarPrices(AbstractSchema):
    id: str
    item_id: str
    dept_id: str
    cat_id: str
    store_id: str
    state_id: str
    date_id: int
    sales: float
    wm_yr_wk: int
    event_name_1: str | None
    event_type_1: str | None
    event_name_2: str | None
    event_type_2: str | None
    snap_ca: bool
    snap_tx: bool
    snap_wi: bool
    sell_price: float | None

    class Config:
        frozen = True
        extra = "forbid" 