from typing import List

import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error

from src.domain.algorithm.lightgbm_regressor import AbstractModel
from src.domain.model.evaluation_data import Evaluation, FeatureImportances
from src.middleware.logger import configure_logger

logger = configure_logger(__name__)


class EvaluationUsecase(object):
    def __init__(self) -> None:
        pass

    def evaluate(
        self,
        store_id: List[str],
        item_id: List[str],
        date_id: List[int],
        y_true: List[float],
        y_pred: List[float],
    ) -> Evaluation:
        logger.info("start evaluation...")
        rmse = (
            mean_squared_error(
                y_true=y_true,
                y_pred=y_pred,
            )
            ** 0.5
        )
        mae = mean_absolute_error(
            y_true=y_true,
            y_pred=y_pred,
        )
        d = [
            dict(
                store_id=s,
                item_id=i,
                date_id=d,
                y_true=t,
                y_pred=p,
            )
            for s, i, d, t, p in zip(store_id, item_id, date_id, y_true, y_pred)
        ]
        data = (
            pd.DataFrame(d)
            .sort_values(["store_id", "item_id", "date_id"])
            .reset_index(drop=True)
        )
        logger.info("done evaluation")
        logger.info(
            f"""evaluation:
data:
{data}
mean_absolute_error: {mae}
root_mean_squared_error: {rmse}
        """
        )
        return Evaluation(
            data=data,
            root_mean_squared_error=rmse,
            mean_absolute_error=mae,
        )

    def export_feature_importance(
        self,
        model: AbstractModel,
    ) -> FeatureImportances:
        feature_importances = model.get_feature_importance()
        d = [f.model_dump() for f in feature_importances]
        data = (
            pd.DataFrame(d)
            .sort_values("importance", ascending=False)
            .reset_index(drop=True)
        )
        logger.info(
            f"""feature importances
{data}
        """
        )
        return FeatureImportances(feature_importances=data)
