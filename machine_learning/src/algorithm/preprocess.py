import numpy as np
import pandas as pd
from src.algorithm.abstract_algorithm import AbstractExtractor
from src.middleware.logger import configure_logger
from src.entity.preprocessed_data import ExtractedPriceSchema, ExtractedLagSalesSchema

logger = configure_logger(__name__)


class PricesExtractor(AbstractExtractor):
    def __init__(self):
        pass

    def run(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """Extract statistics from price column.

        Args:
            df (pd.DataFrame): Input Pandas DataFrame.

        Returns:
            pd.DataFrame: DataFrame with year, month and day of week extracted.
        """
        df_price = df[["id", "item_id", "store_id", "date_id", "sell_price"]].copy()
        df_price["price_max"] = df_price.groupby(["store_id", "item_id"])["sell_price"].transform("max")
        df_price["price_min"] = df_price.groupby(["store_id", "item_id"])["sell_price"].transform("min")
        df_price["price_std"] = df_price.groupby(["store_id", "item_id"])["sell_price"].transform("std")
        df_price["price_mean"] = df_price.groupby(["store_id", "item_id"])["sell_price"].transform("mean")
        df_price["price_norm"] = df_price["sell_price"] / df_price["price_max"]
        df_price["price_nunique"] = df_price.groupby(["store_id", "item_id"])["sell_price"].transform("nunique")
        df_price["item_nunique"] = df_price.groupby(["store_id", "sell_price"])["item_id"].transform("nunique")

        df=df_price.iloc[:, 5:]

        ExtractedPriceSchema.validate(df)
        logger.info(
            f"""price data extracted:
{df}
column:
{df.columns}
type:
{df.dtypes}
        """
        )
        return df


class LagSalesExtractor(AbstractExtractor):
    def __init__(self):
        pass

    def run(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """Extract lag from sales column.

        Args:
            df (pd.DataFrame): Input Pandas DataFrame.

        Returns:
            pd.DataFrame: DataFrame with year, month and day of week extracted.
        """

        df_lag = df[["id", "date_id", "sales"]]

        num_lag_day_list = []
        num_lag_day = 15
        predict_horizon = 7
        for col in range(predict_horizon, predict_horizon + num_lag_day):
            num_lag_day_list.append(col)

        num_rolling_day_list = [7, 14, 30, 60]
        num_shift_rolling_day_list = []
        for num_shift_day in [1, 7, 14]:
            for num_rolling_day in [7, 14, 30]:
                num_shift_rolling_day_list.append([num_shift_day, num_rolling_day])

        df_lag = df_lag.assign(**{
            "lag_{}_{}".format(col, l): df_lag.groupby(["id"])["sales"].transform(lambda x: x.shift(l))
            for l in num_lag_day_list
        })

        for col in list(df_lag):
            if "lag" in col:
                df_lag[col] = df_lag[col]

        for num_rolling_day in num_rolling_day_list:
            df_lag["rolling_mean_" + str(num_rolling_day)] = df_lag.groupby(["id"])["sales"].transform(
                lambda x: x.shift(predict_horizon).rolling(num_rolling_day).mean())
            df_lag["rolling_std_" + str(num_rolling_day)] = df_lag.groupby(["id"])["sales"].transform(
                lambda x: x.shift(predict_horizon).rolling(num_rolling_day).std())
            
        df=df_lag.iloc[:, 3:]

        ExtractedLagSalesSchema.validate(df)
        logger.info(
            f"""sales lag data extracted:
{df}
column:
{df.columns}
type:
{df.dtypes}
        """
        )
        return df
