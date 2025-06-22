from enum import Enum
from typing import List, Type

from src.domain.algorithm.lightgbm_regressor import AbstractModel, LightGBMRegression


class MODEL(Enum):
    LIGHTGBM_REGRESSION = "lightgbm_regression"

    @staticmethod
    def get_list() -> List[str]:
        return [v.value for v in MODEL.__members__.values()]


def get_model(model: str) -> Type[AbstractModel]:
    if model == MODEL.LIGHTGBM_REGRESSION.value:
        return LightGBMRegression
    else:
        raise ValueError(f"invalid model name: {model}. Choose from {MODEL.get_list()}")
