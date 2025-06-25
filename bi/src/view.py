from enum import Enum
from typing import List, Optional, Tuple

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from logger import configure_logger
from service import PredictionService, SalesService

logger = configure_logger(__name__)


class BI(Enum):
    SALES = "sales"
    PREDICTION = "prediction"


def build_bi_selectbox() -> Optional[str]:
    options = [None, BI.SALES.value, BI.PREDICTION.value]
    selected = st.sidebar.selectbox(
        label="BI",
        options=options,
    )
    return selected


def build_store_sales_selectbox(sales_service: SalesService) -> Optional[str]:
    stores = sales_service.list_stores()
    if not stores:
        return None
    stores = sorted(stores)
    selected = st.sidebar.selectbox(
        label="store",
        options=stores,
    )
    return selected


def build_item_sales_selectbox(sales_service: SalesService) -> Optional[str]:
    items = sales_service.list_items()
    if not items:
        return None
    items = sorted(items)
    selected = st.sidebar.selectbox(
        label="item",
        options=items,
    )
    return selected


def build_store_prediction_selectbox(
    prediction_service: PredictionService,
) -> Optional[str]:
    prediction_df = prediction_service.retrieve_prediction()
    if prediction_df.empty or "store_id" not in prediction_df.columns:
        st.warning("予測データがありません")
        return None
    options = prediction_df.store_id.unique()
    selected = st.sidebar.selectbox(
        label="store",
        options=options,
    )
    return selected


def build_item_prediction_selectbox(
    prediction_service: PredictionService,
) -> Optional[str]:
    prediction_df = prediction_service.retrieve_prediction()
    if prediction_df.empty or "item_id" not in prediction_df.columns:
        st.warning("予測データがありません")
        return None
    options = prediction_df.item_id.unique()
    selected = st.sidebar.selectbox(
        label="item",
        options=options,
    )
    return selected


def build(
    sales_service: SalesService,
    prediction_service: PredictionService,
) -> None:
    st.markdown("# demand-forecasting-m5")

    bi = build_bi_selectbox()

    if bi is None:
        return
    elif bi == BI.SALES.value:
        build_sales(
            sales_service=sales_service,
        )
    elif bi == BI.PREDICTION.value:
        build_prediction(
            prediction_service=prediction_service,
        )

    else:
        raise ValueError()


def build_sales(
    sales_service: SalesService,
) -> None:
    logger.info("build sales BI...")
    _, _, stores, items, sales_df = build_sales_base(
        sales_service=sales_service,
    )

    if sales_df.empty:
        return
    else:
        show_sales_daily(
            df=sales_df,
            stores=stores,
            items=items,
        )


def build_prediction(
    prediction_service: PredictionService,
) -> None:
    logger.info("build prediction BI...")
    _, _, stores, items, prediction_df = build_prediction_base(
        prediction_service=prediction_service,
    )

    if (
        prediction_df.empty
        or "store_id" not in prediction_df.columns
        or "item_id" not in prediction_df.columns
    ):
        return  # メッセージはbuild_prediction_baseで表示済み

    show_prediction_daily(
        df=prediction_df,
        stores=stores,
        items=items,
    )


def build_sales_base(
    sales_service: SalesService,
) -> Tuple[Optional[str], Optional[str], List[str], List[str], pd.DataFrame]:
    sales_df = sales_service.retrieve_sales()
    if (
        sales_df.empty
        or "store_id" not in sales_df.columns
        or "item_id" not in sales_df.columns
    ):
        st.warning("売上データがありません")
        return None, None, [], [], sales_df
    store = build_store_sales_selectbox(sales_service=sales_service)
    item = build_item_sales_selectbox(sales_service=sales_service)
    sales_df = sales_service.retrieve_sales(
        store=store,
        item=item,
    )
    stores = sales_df.store_id.unique().tolist()
    items = sales_df.item_id.unique().tolist()
    return store, item, stores, items, sales_df


def build_prediction_base(
    prediction_service: PredictionService,
) -> Tuple[Optional[str], Optional[str], List[str], List[str], pd.DataFrame]:
    prediction_df = prediction_service.retrieve_prediction()
    if (
        prediction_df.empty
        or "store_id" not in prediction_df.columns
        or "item_id" not in prediction_df.columns
    ):
        st.warning("予測データがありません")
        return None, None, [], [], prediction_df

    store = build_store_prediction_selectbox(prediction_service=prediction_service)
    item = build_item_prediction_selectbox(prediction_service=prediction_service)

    prediction_df = prediction_service.retrieve_prediction(
        store=store,
        item=item,
    )
    stores = prediction_df.store_id.unique().tolist()
    items = prediction_df.item_id.unique().tolist()

    return store, item, stores, items, prediction_df


def show_sales_daily(
    df: pd.DataFrame,
    stores: List[str],
    items: List[str],
) -> None:
    st.markdown("### Daily summary")
    for s in stores:
        for i in items:
            _df = (
                df[(df.store_id == s) & (df.item_id == i)]
                .drop(["store_id", "item_id"], axis=1)
                .sort_values("date_id")
                .set_index("date_id")
            )
            with st.expander(
                label=f"STORE {s} ITEM {i}",
                expanded=True,
            ):
                st.dataframe(_df)

                fig = go.Figure()
                sales_trace = go.Bar(
                    x=_df.index,
                    y=_df.sales,
                )
                fig.add_trace(sales_trace)
                st.plotly_chart(fig, use_container_width=True)
                logger.info(f"STORE {s} ITEM {i}")


def show_prediction_daily(
    df: pd.DataFrame,
    stores: List[str],
    items: List[str],
) -> None:
    st.markdown("### Daily summary")
    for s in stores:
        for i in items:
            _df = (
                df[(df.store_id == s) & (df.item_id == i)]
                .drop(["store_id", "item_id"], axis=1)
                .sort_values("date_id")
                .set_index("date_id")
            )
            with st.expander(
                label=f"STORE {s} ITEM {i}",
                expanded=True,
            ):
                st.dataframe(_df)

                fig = go.Figure()
                sales_trace = go.Bar(
                    x=_df.index,
                    y=_df.prediction,
                )
                fig.add_trace(sales_trace)
                st.plotly_chart(fig, use_container_width=True)
                logger.info(f"STORE {s} ITEM {i}")
