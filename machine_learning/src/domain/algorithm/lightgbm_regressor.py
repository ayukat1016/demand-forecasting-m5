import os
from abc import ABC, abstractmethod
from logging import getLogger
from typing import Any, Dict, List, Optional

import lightgbm as lgb
import pandas as pd
import yaml
from lightgbm import Booster, LGBMRegressor

from src.domain.model.evaluation_data import FeatureImportance

LGB_REGRESSION_DEFAULT_PARAMS: Dict[str, Any] = {
    "boosting_type": "gbdt",
    "n_estimators": 1000,
    "objective": "rmse",
    "metric": "rmse",
    "learning_rate": 0.05,
    "num_leaves": 32,
    "subsample": 0.7,
    "subsample_freq": 1,
    "feature_fraction": 0.8,
    "min_data_in_leaf": 50,
    "random_state": 123,
    "importance_type": "gain",
}

LGB_REGRESSION_TRAIN_PARAMS: Dict[str, Any] = {
    "early_stopping_rounds": 10,
    "log_evaluation": 10,
}


class AbstractModel(ABC):
    def __init__(self) -> None:
        self.name: str = "base_model"
        self.params: Dict[str, Any] = {}
        self.train_params: Dict[str, Any] = {}
        self.model: Optional[Any] = None
        self.logger = getLogger(__name__)

    @abstractmethod
    def reset_model(
        self,
        params: Optional[Dict] = None,
    ):
        raise NotImplementedError

    @abstractmethod
    def train(
        self,
        x_train: pd.DataFrame,
        y_train: pd.Series,
        x_test: Optional[pd.DataFrame] = None,
        y_test: Optional[pd.Series] = None,
    ):
        raise NotImplementedError

    @abstractmethod
    def predict(
        self,
        x: pd.DataFrame,
    ) -> List[float]:
        raise NotImplementedError

    @abstractmethod
    def save(
        self,
        file_path: str,
    ) -> str:
        raise NotImplementedError

    @abstractmethod
    def load(
        self,
        file_path: str,
    ):
        raise NotImplementedError

    @abstractmethod
    def get_feature_importance(self) -> List[FeatureImportance]:
        raise NotImplementedError


class LightGBMRegression(AbstractModel):
    def __init__(
        self,
        params: Dict[str, Any] = LGB_REGRESSION_DEFAULT_PARAMS,
        train_params: Dict[str, Any] = LGB_REGRESSION_TRAIN_PARAMS,
    ) -> None:
        super().__init__()
        self.name = "lightgbm_regression"
        self.params = params
        self.train_params = train_params

        self.model: LGBMRegressor
        self.reset_model(params=self.params)

    def reset_model(
        self,
        params: Optional[Dict[str, Any]] = None,
        train_params: Optional[Dict[str, Any]] = None,
    ) -> None:
        if params is not None:
            self.params = params
        if train_params is not None:
            self.train_params = train_params
        self.logger.info(f"params: {self.params}")
        self.model = LGBMRegressor(**self.params)
        self.logger.info(f"initialized model: {self.model}")

    def train(
        self,
        x_train: pd.DataFrame,
        y_train: pd.Series,
        x_test: Optional[pd.DataFrame] = None,
        y_test: Optional[pd.Series] = None,
    ) -> None:
        self.logger.info(f"start train for model: {self.model}")
        eval_set: List[tuple] = [(x_train, y_train)]
        eval_names = ["train"]
        if x_test is not None and y_test is not None:
            eval_set.append((x_test, y_test))
            eval_names.append("valid")
        self.model.fit(
            X=x_train,
            y=y_train,
            eval_set=[(x, y) for x, y in eval_set],
            eval_names=eval_names,
            callbacks=[
                lgb.early_stopping(
                    self.train_params["early_stopping_rounds"], verbose=True
                ),
                lgb.log_evaluation(self.train_params["log_evaluation"]),
            ],
        )

    def predict(
        self,
        x: pd.DataFrame,
    ) -> List[float]:
        prediction = self.model.predict(x).tolist()
        return prediction

    def save_model_params(
        self,
        file_path: str,
    ) -> str:
        file, ext = os.path.splitext(file_path)
        if ext != ".yaml":
            file_path = f"{file}.yaml"
        self.logger.info(f"save model params: {file_path}")
        with open(file_path, "w") as f:
            yaml.dump(self.params, f)
        return file_path

    def save(
        self,
        file_path: str,
    ) -> str:
        file, ext = os.path.splitext(file_path)
        if ext != ".txt":
            file_path = f"{file}.txt"
        self.logger.info(f"save model: {file_path}")
        self.model.booster_.save_model(file_path)
        return file_path

    def load(
        self,
        file_path: str,
    ) -> None:
        self.logger.info(f"load model: {file_path}")
        booster = Booster(model_file=file_path)
        self.model = LGBMRegressor(model=booster)

    def get_feature_importance(self) -> List[FeatureImportance]:
        feature_importances = [
            FeatureImportance(
                feature_name=n,
                importance=i,
            )
            for n, i in zip(self.model.feature_name_, self.model.feature_importances_)
        ]
        return feature_importances
