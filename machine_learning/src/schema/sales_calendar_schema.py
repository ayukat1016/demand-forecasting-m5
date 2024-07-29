from src.schema.abstract_schema import AbstractSchema


class SalesCalendar(AbstractSchema):
    id: str
    item_id: str
    dept_id: str
    cat_id: str
    store_id: str
    state_id: str
    date_id: int
    sales: float
    wm_yr_wk: int
    event_name_1: str
    event_type_1: str
    event_name_2: str
    event_type_2: str
    snap_ca: int
    snap_tx: int
    snap_wi: int

    class Config:
        allow_mutation = False
        extra = "forbid"
