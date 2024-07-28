import pandas as pd
from src.algorithm.abstract_algorithm import AbstractExtractor
from src.entity.common_data import XY
from src.entity.preprocessed_data import PreprocessedDataset
from src.entity.raw_data import RawDataset
from src.middleware.logger import configure_logger

logger = configure_logger(__name__)


class PreprocessUsecase(object):
    def __init__(
        self,
        prices_extractor: AbstractExtractor,
        lag_sales_extractor: AbstractExtractor,
    ):
        """Preprocess usecase.

        Args:
            prices_extractor (AbstractExtractor): Algorithm to extract prices statitics.
            lag_sales_extractor (AbstractExtractor): Algorithm to extract lag sales data.
        """
        self.prices_extractor=prices_extractor
        self.lag_sales_extractor=lag_sales_extractor

    def preprocess_dataset(
        self,
        dataset: RawDataset,
    ) -> PreprocessedDataset:
        """Run preprocess for raw dataset.

        Args:
            dataset (RawDataset): Dataset to be transformed.

        Returns:
            PreprocessedDataset: Preprocessed data with separated to training, validation and prediction.
        """

        df_training = dataset.training_data.data
        df_validation = dataset.validation_data.data
        df_prediction = dataset.prediction_data.data
        df_all = pd.concat([df_training, df_validation, df_prediction], axis=0, ignore_index=True)
 
        df_price = self.prices_extractor.run(df=df_all)
        df_lag = self.lag_sales_extractor.run(df=df_all)
        df = pd.concat([df_all, df_price, df_lag], axis=1)

        train_mask = df["date_id"] <= dataset.training_data.date_to
        valid_mask = (dataset.validation_data.date_from <= df["date_id"]) & (df["date_id"] <= dataset.validation_data.date_to)
        preds_mask = dataset.prediction_data.date_from <= df["date_id"]

        logger.info(f"transform training data...")
        training_data = self.split_dataset(
            raw_data=df[train_mask],            
        )

        logger.info(f"transform validation data...")
        validation_data = self.split_dataset(
            raw_data=df[valid_mask],
        )

        logger.info(f"transform prediction data...")
        prediction_data = self.split_dataset(
           raw_data=df[preds_mask],            
        )
        return PreprocessedDataset(
            training_data=training_data,
            validation_data=validation_data,
            prediction_data=prediction_data,
        )

    def split_dataset(
        self,
        raw_data: pd.DataFrame,
    ) -> XY:
        """Transform DataFrame.

        Args:
            raw_data (pd.DataFrame): input data. Refer src/entity/raw_data/RawDataSchemafor the data format.

        Returns:
            XY: dataset to be used for model training, evaluation and prediction.
        """
        df = raw_data
        df = df.sort_values(["store_id", "item_id", "date_id"]).reset_index(drop=True)

        keys = df[["store_id", "item_id", "date_id"]]
        data = self.split_data_target(
            keys=keys,
            data=df,
        )        

        logger.info(
            f"""done preprocessing dataset:
x columns:
{data.x.columns}
x:
{data.x}
y:
{data.y}
        """
        )
        return data

    def split_data_target(
        self,
        keys: pd.DataFrame,
        data: pd.DataFrame,
    ) -> XY:
        """Split data into training data x and target data y.

        Args:
            keys (pd.DataFrame): keys in order.
            data (pd.DataFrame): data in order.

        Returns:
            XY: training data x and target data y.
        """
        y = data[["sales"]]
        x = data.drop(["id", "cat_id", "store_id", "state_id", "date_id", "sales", "wm_yr_wk"], axis=1)
        return XY(
            keys=keys,
            x=x,
            y=y,
        )
