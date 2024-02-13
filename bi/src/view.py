from enum import Enum
from typing import List, Optional, Tuple

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from logger import configure_logger
from plotly.subplots import make_subplots
from service import SalesService

logger = configure_logger(__name__)


class BI(Enum):
    ITEM_SALES = "item_sales"
    ITEM_SALES_PREDICTION_EVALUATION = "item_sales_prediction_evaluation"
    SALES = "sales"


class TIME_FRAME(Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


def build_bi_selectbox() -> str:
    options = [None, BI.SALES.value, BI.ITEM_SALES_PREDICTION_EVALUATION.value]
    selected = st.sidebar.selectbox(
        label="BI",
        options=options,
    )
    return selected


# def build_store_selectbox(
#     store_service: StoreService,
#     region: Optional[str] = None,
# ) -> Optional[str]:
#     options = store_service.list_stores(region=region)
#     options.append("ALL")
#     selected = st.sidebar.selectbox(
#         label="store",
#         options=options,
#     )
#     return selected


# def build_item_selectbox(item_service: ItemService) -> Optional[str]:
#     options = item_service.list_items()
#     options.append("ALL")
#     selected = st.sidebar.selectbox(
#         label="item",
#         options=options,
#     )
#     return selected


def build(
    sales_service: SalesService,    
):
    st.markdown("# Hi, I am BI by streamlit; Let's have a fun!")
    st.markdown("# Item sales record")

    bi = build_bi_selectbox()

    if bi is None:
        return
    elif bi == BI.SALES.value:
        build_sales(
            sales_service=sales_service,
        )

    else:
        raise ValueError()
    

def build_sales(
    sales_service: SalesService,
    ):
    logger.info("build item sales BI...")
    _, _, stores, items, sales_df = build_base(    
        sales_service=sales_service,
    )

    show_daily_item_sales(
        df=sales_df,
        stores=stores,
        items=items,
    )


def build_base(
    sales_service: SalesService,
) -> Tuple[Optional[str], Optional[str], List[str], List[str], pd.DataFrame]:
    # store = build_store_selectbox(
    #     store_service=store_service,
    #     region=region,
    # )
    # item = build_item_selectbox(item_service=item_service)

    # if region == "ALL":
    #     region = None
    # if store == "ALL":
    #     store = None
    # if item == "ALL":
    #     item = None
    store = None
    item = None    
    sales_df = sales_service.retrieve_sales(
        # item=item,
        # store=store,
    )
    stores = sales_df.store_id.unique()
    items = sales_df.item_id.unique()

    return store, item, stores, items, sales_df


def show_daily_item_sales(
    df: pd.DataFrame,
    stores: List[str],
    items: List[str],
):
    st.markdown("### Daily summary")
    for s in stores:
        for i in items:
            _df = (
                df[(df.store_id == s) & (df.item_id == i)]
                .drop(["store_id", "item_id"], axis=1)
                .reset_index(drop=True)
                .sort_values("date_id")
            )
            # region = _df.region.unique()[0]
            # _df = _df.drop("region", axis=1)
            # sales_range_max = max(_df.sales.max() + 10, 150)
            with st.expander(
                label=f"STORE {s} ITEM {i}",
                expanded=True,
            ):
                st.dataframe(_df)

                fig = go.Figure()
                sales_trace = go.Bar(
                    x=_df.date_id,
                    y=_df.sales,
                )
                fig.add_trace(sales_trace)
                # fig.update_yaxes(range=[0, sales_range_max])
                st.plotly_chart(fig, use_container_width=True)
                logger.info(f"STORE {s} ITEM {i}")