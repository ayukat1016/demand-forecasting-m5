from pydantic import BaseModel


class Sales(BaseModel):
    key: str
    id: str
    item_id: str
    dept_id: str
    cat_id: str
    store_id: str
    state_id: str
    date_id: int
    sales: float

    class Config:
        frozen = True
        extra = "forbid"
        from_attributes = True


class Prediction(BaseModel):
    store_id: str
    item_id: str
    date_id: int
    prediction: float

    class Config:
        frozen = True
        extra = "forbid"
        from_attributes = True
