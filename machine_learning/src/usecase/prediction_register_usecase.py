from typing import List

import pandas as pd

from src.domain.repository.prediction_repository import AbstractPredictionRepository
from src.infrastructure.schema.prediction_schema import Prediction
from src.middleware.logger import configure_logger

logger = configure_logger(__name__)


class PredictionRegisterUsecase(object):
    def __init__(self, prediction_repository: AbstractPredictionRepository) -> None:
        self.prediction_repository = prediction_repository

    def register_prediction(
        self,
        predictions: pd.DataFrame,
    ) -> None:
        logger.info("register prediction")
        self.register_db(
            predictions=predictions,
        )
        logger.info("done register prediction")

    def register_db(
        self,
        predictions: pd.DataFrame,
    ) -> None:
        data: List[dict] = predictions.to_dict(orient="records")
        records: List[Prediction] = []
        for d in data:
            records.append(
                Prediction(
                    store_id=d["store_id"],
                    item_id=d["item_id"],
                    date_id=d["date_id"],
                    prediction=float(d["prediction"]),
                ),
            )
        self.prediction_repository.bulk_insert(
            records=records,
        )
