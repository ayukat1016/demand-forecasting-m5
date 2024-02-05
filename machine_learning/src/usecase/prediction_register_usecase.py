from typing import List, Optional

import pandas as pd
from src.entity.prediction_data import PredictionDataSchema
from src.model.prediction_model import Predictions
from src.repository.abstract_repository import AbstractBulkInsertRepository
from src.middleware.logger import configure_logger

logger = configure_logger(__name__)


class PredictionRegisterUsecase(object):
    def __init__(
        self,
        predictions_repository: AbstractBulkInsertRepository
    ):
        self.predictions_repository = predictions_repository

    def register(
        self,
        predictions: pd.DataFrame,
        mlflow_experiment_id: Optional[int] = None,
        mlflow_run_id: Optional[str] = None,
    ):
        if mlflow_experiment_id is None or mlflow_run_id is None:
            raise ValueError("mlflow_experiment_id and mlflow_run_id must not be empty")
        self.register_db(
            predictions=predictions,
            mlflow_experiment_id=mlflow_experiment_id,
            mlflow_run_id=mlflow_run_id,
        )

    def register_db(
        self,
        predictions: pd.DataFrame,
        mlflow_experiment_id: int,
        mlflow_run_id: str,
    ):
        predictions = PredictionDataSchema.validate(predictions)
        records = predictions.to_dict(orient="records")
        predictions: List[Predictions] = []
        for r in records:
            predictions.append(
                Predictions(
                    store_id=r["store_id"],
                    item_id=r["item_id"],
                    date_id=r["date_id"],
                    prediction=float(r["prediction"]),
                    mlflow_experiment_id=mlflow_experiment_id,
                    mlflow_run_id=mlflow_run_id,
                ),
            )
        self.predictions_repository.bulk_insert(
            records=predictions,
        )
