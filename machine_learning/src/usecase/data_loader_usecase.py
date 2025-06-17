from typing import List

import numpy as np
import pandas as pd

from src.domain.model.raw_data import RawDataset, RawDataWithTargetDates
from src.domain.repository.calendar_repository import AbstractCalendarRepository
from src.domain.repository.prices_repository import AbstractPricesRepository
from src.domain.repository.sales_calendar_prices_repository import AbstractSalesCalendarPricesRepository
from src.infrastructure.schema.calendar_schema import Calendar
from src.infrastructure.schema.prices_schema import Prices
from src.infrastructure.schema.sales_calendar_prices_schema import SalesCalendarPrices
from src.middleware.logger import configure_logger

logger = configure_logger(__name__)


class DataLoaderUsecase(object):
    def __init__(
        self,
        calendar_repository: AbstractCalendarRepository,
        prices_repository: AbstractPricesRepository,
        sales_calendar_prices_repository: AbstractSalesCalendarPricesRepository,
    ):
        """Data loader usecase.

        Args:
            calendar_repository (AbstractCalendarRepository): Repository to load data for calendar.
            prices_repository (AbstractPricesRepository): Repository to load data for prices.
            sales_calendar_prices_repository (AbstractSalesCalendarPricesRepository): Repository to load joined data for training.
        """

        self.calendar_repository = calendar_repository
        self.prices_repository = prices_repository
        self.sales_calendar_prices_repository = sales_calendar_prices_repository

    def load_dataset(
        self,
        training_date_from: int,
        training_date_to: int,
        validation_date_from: int,
        validation_date_to: int,
        prediction_date_from: int,
        prediction_date_to: int,
    ) -> RawDataset:
        """Load dataset for training, validation and prediction.

        Args:
            training_date_from (int): Starting date for training data.
            training_date_to (int): Last date for training data.
            validation_date_from (int): Starting date for validation data.
            validation_date_to (int): Last date for validation data.
            prediction_date_from (int): Starting date for prediction data.
            prediction_date_to (int): Last date for prediction data.

        Returns:
            RawDataset: Data loaded from database.
        """
        training_data, prices_df, release_df = self.make_training_data(
            date_from=training_date_from,
            date_to=validation_date_to,
        )

        train_mask = training_data["date_id"] <= training_date_to
        valid_mask = (validation_date_from <= training_data["date_id"]) & (
            training_data["date_id"] <= validation_date_to
        )

        training_data_with_target_dates = RawDataWithTargetDates(
            data=training_data[train_mask],
            date_from=training_date_from,
            date_to=training_date_to,
        )

        validation_data_with_target_dates = RawDataWithTargetDates(
            data=training_data[valid_mask],
            date_from=validation_date_from,
            date_to=validation_date_to,
        )

        prediction_data = self.make_prediction_data(
            training_data=training_data,
            date_from=prediction_date_from,
            date_to=prediction_date_to,
            prices_df=prices_df,
            release_df=release_df,
        )

        prediction_data_with_target_dates = RawDataWithTargetDates(
            data=prediction_data,
            date_from=prediction_date_from,
            date_to=prediction_date_to,
        )

        return RawDataset(
            training_data=training_data_with_target_dates,
            validation_data=validation_data_with_target_dates,
            prediction_data=prediction_data_with_target_dates,
        )

    def make_training_data(
        self,
        date_from: int,
        date_to: int,
    ) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Load data.

        Args:
            date_from (int): Starting date.
            date_to (int): Last date.

        Returns:
            tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]: Training and validation data, prices data, and release data.
        """

        logger.info(f"load data from: {date_from} to {date_to}")
        data = self.load_sales_calendar_prices_data(
            date_from=date_from,
            date_to=date_to,
        )
        dataset_dict = [d.model_dump() for d in data]
        df = pd.DataFrame(dataset_dict)

        prices_data = self.load_prices_data()
        prices_dataset_dict = [d.model_dump() for d in prices_data]
        prices_df = pd.DataFrame(prices_dataset_dict)

        release_df = (
            prices_df.groupby(["store_id", "item_id"])["wm_yr_wk"]
            .agg(["min"])
            .reset_index()
        )
        release_df.columns = pd.Index(["store_id", "item_id", "release"])
        release_df["release"] = release_df["release"] - release_df["release"].min()
        df = df.merge(release_df, on=["store_id", "item_id"], how="left")

        df = df.sort_values(["store_id", "item_id", "date_id"]).reset_index(drop=True)
        logger.info(f"loaded: {df.shape}")
        logger.info(
            f"""df:
{df}
column:
{df.columns}
type:
{df.dtypes}
        """
        )
        return df, prices_df, release_df

    def make_prediction_data(
        self,
        training_data: pd.DataFrame,
        date_from: int,
        date_to: int,
        prices_df: pd.DataFrame,
        release_df: pd.DataFrame,
    ) -> pd.DataFrame:
        """Make prediction data from prices and calendar table.

        Args:
            training_data (pd.DataFrame): Training data.
            date_from (int): Starting date for prediction data.
            date_to (int): Last date for prediction data.
            prices_df (pd.DataFrame): Prices data.
            release_df (pd.DataFrame): Release data.

        Returns:
            pd.DataFrame: Prediction data.
        """

        logger.info(f"load data from: {date_from} to {date_to} ")

        pred_df = pd.DataFrame()
        for i in range(date_from, date_to + 1):
            temp_df = training_data[
                ["id", "item_id", "dept_id", "cat_id", "store_id", "state_id"]
            ]
            temp_df = temp_df.drop_duplicates()
            temp_df["date_id"] = i
            temp_df["sales"] = np.nan
            pred_df = pd.concat([pred_df, temp_df])

        pred_df = pred_df.reset_index(drop=True)

        calendar_data = self.load_calendar_data()
        calendar_dataset_dict = [d.model_dump() for d in calendar_data]
        calendar_df = pd.DataFrame(calendar_dataset_dict)

        pred_df = pred_df.merge(
            calendar_df[
                [
                    "wm_yr_wk",
                    "date_id",
                    "event_name_1",
                    "event_type_1",
                    "event_name_2",
                    "event_type_2",
                    "snap_ca",
                    "snap_tx",
                    "snap_wi",
                ]
            ],
            on="date_id",
            how="left",
        )
        pred_df = pred_df.merge(
            prices_df[["store_id", "item_id", "wm_yr_wk", "sell_price"]],
            on=["store_id", "item_id", "wm_yr_wk"],
            how="left",
        )
        pred_df = pred_df.merge(release_df, on=["store_id", "item_id"], how="left")

        df = pred_df
        df = df.sort_values(["store_id", "item_id", "date_id"]).reset_index(drop=True)
        logger.info(f"loaded: {df.shape}")
        logger.info(
            f"""df:
{df}
column:
{df.columns}
type:
{df.dtypes}
        """
        )
        return df

    def load_sales_calendar_prices_data(
        self,
        date_from: int,
        date_to: int,
    ) -> List[SalesCalendarPrices]:
        """Load data from sales, calendar and prices tables as training and validation data.

        Args:
            date_from (int): Starting date.
            date_to (int): Last date.

        Returns:
            List[SalesCalendarPrices]: training and validation data.
        """

        data: List[SalesCalendarPrices] = []
        position = 0
        limit = 10000
        while True:
            sales_calendar_prices_data = self.sales_calendar_prices_repository.select(
                date_from=date_from,
                date_to=date_to,
                limit=limit,
                offset=position,
            )
            if len(sales_calendar_prices_data) == 0:
                break
            data.extend(sales_calendar_prices_data)
            position += len(sales_calendar_prices_data)
            logger.info(f"done loading {position}...")
        return data

    def load_calendar_data(self) -> List[Calendar]:
        """Load data from calendar table.

        Returns:
            List[Calendar]: calendar data.
        """

        data: List[Calendar] = []
        position = 0
        limit = 1000
        while True:
            calendar_data = self.calendar_repository.select(
                limit=limit,
                offset=position,
            )
            if len(calendar_data) == 0:
                break
            data.extend(calendar_data)
            position += len(calendar_data)
            logger.info(f"done loading {position}...")
        return data

    def load_prices_data(self) -> List[Prices]:
        """Load data from prices table.

        Returns:
            List[Prices]: prices data.
        """

        data: List[Prices] = []
        position = 0
        limit = 10000
        while True:
            prices_data = self.prices_repository.select(
                limit=limit,
                offset=position,
            )
            if len(prices_data) == 0:
                break
            data.extend(prices_data)
            position += len(prices_data)
            logger.info(f"done loading {position}...")
        return data
