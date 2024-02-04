from pydantic import Extra
from src.model.abstract_model import AbstractModel


class Predictions(AbstractModel):
    store_id: str    
    item_id: str
    date_id: int
    prediction: float
    mlflow_experiment_id: int
    mlflow_run_id: str    

    class Config:
        allow_mutation = False
        extra = Extra.forbid
