import os
from typing import Any, Dict, List, Optional

import pandas as pd
import yaml
from lightgbm import Booster, LGBMRegressor
import lightgbm as lgb
from src.algorithm.abstract_algorithm import AbstractModel
from src.entity.evaluation_data import FeatureImportance

LGB_REGRESSION_DEFAULT_PARAMS = {
    "boosting_type": "gbdt",
    "objective": "regression_l1",
    "metric": "mean_absolute_error",
    "learning_rate": 0.05,
    "num_leaves": 32,
    "subsample": 0.7,
    "subsample_freq": 1,
    "feature_fraction": 0.8,
    "min_data_in_leaf": 50,
    "min_sum_hessian_in_leaf": 50,
    "n_estimators": 1000,
    "random_state": 123,
    "importance_type": "gain",
}

LGB_REGRESSION_TRAIN_PARAMS = {
    "early_stopping_rounds": 10,
    "log_evaluation": 10,
}


class LightGBMRegression(AbstractModel):
    def __init__(
        self,
        params: Dict[str, Any] = LGB_REGRESSION_DEFAULT_PARAMS,
        train_params: Dict[str, Any] = LGB_REGRESSION_TRAIN_PARAMS,
    ):
        super().__init__()
        self.name = "light_gbm_regression"
        self.params = params
        self.train_params = train_params

        self.model: LGBMRegressor = None
        self.reset_model(params=self.params)

    def reset_model(
        self,
        params: Optional[Dict] = None,
        train_params: Optional[Dict] = None,
    ):
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
        y_train: pd.DataFrame,
        x_test: Optional[pd.DataFrame] = None,
        y_test: Optional[pd.DataFrame] = None,
    ):
        self.logger.info(f"start train for model: {self.model}")
        eval_set = [(x_train, y_train)]
        eval_names = ["train"]
        if x_test is not None and y_test is not None:
            eval_set.append((x_test, y_test))
            eval_names.append("valid")
        self.model.fit(
            X=x_train,
            y=y_train,
            eval_set=eval_set,
            eval_names=eval_names,
            callbacks=[lgb.early_stopping(self.train_params["early_stopping_rounds"], verbose=True), 
                       lgb.log_evaluation(self.train_params["log_evaluation"])],
        )

    def predict(
        self,
        x: pd.DataFrame,
    ) -> List[float]:
        predictions = self.model.predict(x).tolist()
        return predictions

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
    ):
        self.logger.info(f"load model: {file_path}")
        self.model = Booster(model_file=file_path)

    def get_feature_importance(self) -> List[FeatureImportance]:
        feature_importances = [
            FeatureImportance(
                feature_name=n,
                importance=i,
            )
            for n, i in zip(self.model.feature_name_, self.model.feature_importances_)
        ]
        return feature_importances
