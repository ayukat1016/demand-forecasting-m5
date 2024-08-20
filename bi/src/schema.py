from pydantic import BaseModel


class Sales(BaseModel):
    store_id: str
    item_id: str
    date_id: int
    date: str
    wm_yr_wk: int
    event_name_1: str
    event_type_1: str
    event_name_2: str
    event_type_2: str
    snap_ca: int
    snap_tx: int
    snap_wi: int
    sales: float

    class Config:
        frozen = True
        extra = "forbid"


class Prediction(BaseModel):
    store_id: str
    item_id: str
    date_id: int
    date: str
    prediction: float

    class Config:
        frozen = True
        extra = "forbid"
