from typing import List, Optional

import pandas as pd
from src.entity.prediction_data import PredictionDataSchema
from src.model.prediction_model import Prediction
from src.repository.abstract_repository import AbstractBulkInsertRepository
from src.middleware.logger import configure_logger

logger = configure_logger(__name__)


class PredictionRegisterUsecase(object):
    def __init__(
        self,
        prediction_repository: AbstractBulkInsertRepository
    ):
        self.prediction_repository = prediction_repository

    def register_prediction(
        self,
        predictions: pd.DataFrame,
        mlflow_experiment_id: Optional[int] = None,
        mlflow_run_id: Optional[str] = None,
    ):
        logger.info("register prediction")
        if mlflow_experiment_id is None or mlflow_run_id is None:
            raise ValueError("mlflow_experiment_id and mlflow_run_id must not be empty")
        self.register_db(
            predictions=predictions,
            mlflow_experiment_id=mlflow_experiment_id,
            mlflow_run_id=mlflow_run_id,
        )
        logger.info("done register prediction")

    def register_db(
        self,
        predictions: pd.DataFrame,
        mlflow_experiment_id: int,
        mlflow_run_id: str,
    ):
        predictions = PredictionDataSchema.validate(predictions)
        records = predictions.to_dict(orient="records")
        predictions: List[Prediction] = []
        for r in records:
            predictions.append(
                Prediction(
                    store_id=r["store_id"],
                    item_id=r["item_id"],
                    date_id=r["date_id"],
                    prediction=float(r["prediction"]),
                    mlflow_experiment_id=mlflow_experiment_id,
                    mlflow_run_id=mlflow_run_id,
                ),
            )
        self.prediction_repository.bulk_insert(
            records=predictions,
        )
