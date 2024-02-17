from pydantic import BaseModel
from pydantic import Extra


class Sales(BaseModel):
    store_id: str
    item_id: str
    date_id: int
    sales: float

    class Config:
        allow_mutation = False
        extra = Extra.forbid


class Prediction(BaseModel):
    store_id: str    
    item_id: str
    date_id: int
    prediction: float

    class Config:
        allow_mutation = False
        extra = Extra.forbid