# import logging
# from abc import ABC, abstractmethod

from src.middleware.file_reader import read_csv_to_list
from src.middleware.logger import configure_logger
from src.middleware.file_reader import read_text_file
from src.middleware.strings import get_uuid
from src.model.calendar_model import Calendar
from src.model.prices_model import Prices
from src.model.sales_model import Sales
from src.repository.abstract_repository import AbstractBulkInsertRepository
from src.repository.abstract_repository import AbstractCreateTablesRepository
# from src.repository.calendar_repository import CalendarRepository
# from src.repository.prices_repository import PricesRepository
# from src.repository.sales_repository import SalesRepository
# from src.repository.table_repository import TableRepository

logger = configure_logger(__name__)

# class AbstractDataInitializationUsecase(ABC):
#     def __init__(
#         self,
#         create_sql_filepath: str,
#         calendar_filepath: str,
#         prices_filepath: str,
#         sales_filepath: str,
#         table_repository: AbstractTableRepository,
#         calendar_repository: AbstractCalendarRepository,
#         prices_repository: AbstractPricesRepository,
#         sales_repository: AbstractSalesRepository,
#     ):
#         self.create_sql_filepath = create_sql_filepath
#         self.calendar_filepath = calendar_filepath
#         self.prices_filepath = prices_filepath
#         self.sales_filepath = sales_filepath
#         self.table_repository = table_repository
#         self.calendar_repository = calendar_repository
#         self.prices_repository = prices_repository
#         self.sales_repository = sales_repository
#         self.logger = logging.getLogger(__name__)

#     @abstractmethod
#     def create_table(self):
#         raise NotImplementedError

#     @abstractmethod
#     def register_calendar(self):
#         raise NotImplementedError

#     @abstractmethod
#     def register_prices(self):
#         raise NotImplementedError

#     @abstractmethod
#     def register_sales(self):
#         raise NotImplementedError


class DataRegisterUsecase(object):
    def __init__(
        self,
        create_sql_filepath: str,
        calendar_filepath: str,
        prices_filepath: str,
        sales_filepath: str,
        table_repository: AbstractCreateTablesRepository,
        calendar_repository: AbstractBulkInsertRepository,
        prices_repository: AbstractBulkInsertRepository,
        sales_repository: AbstractBulkInsertRepository,
    ):
        # super().__init__(
        self.create_sql_filepath = create_sql_filepath
        self.calendar_filepath = calendar_filepath
        self.prices_filepath = prices_filepath
        self.sales_filepath = sales_filepath
        self.table_repository = table_repository
        self.calendar_repository = calendar_repository
        self.prices_repository = prices_repository
        self.sales_repository = sales_repository
        # )

    def create_table(self):
        query = read_text_file(file_path=self.create_sql_filepath)
        self.table_repository.create_tables(query=query)

    def register_calendar(self):
        data = read_csv_to_list(
            csv_file=self.calendar_filepath,
            header=None,
            is_first_line_header=True,
        )
        limit = 1000
        i = 0
        records = []
        while i < len(data):
            d = data[i]
            records.append(
                Calendar(
                    date=d["date"],
                    wm_yr_wk=d["wm_yr_wk"],
                    weekday=d["weekday"],
                    wday=d["wday"],
                    month=d["month"],
                    year=d["year"],
                    date_id=d["date_id"],
                    event_name_1=d["event_name_1"],
                    event_type_1=d["event_type_1"],
                    event_name_2=d["event_name_2"],
                    event_type_2=d["event_type_2"],
                    snap_ca=d["snap_CA"],
                    snap_tx=d["snap_TX"],
                    snap_wi=d["snap_WI"], 
                )
            )
            i += 1
            if i % limit == 0:
                self.calendar_repository.bulk_insert(records=records)
                logger.info(f"calendar: {i} ...")
        if len(records) > 0:
            self.calendar_repository.bulk_insert(records=records)
            logger.info(f"calendar: {i} ...")

    def register_prices(self):
        data = read_csv_to_list(
            csv_file=self.prices_filepath,
            header=None,
            is_first_line_header=True,
        )
        limit = 10000
        i = 0
        records = []
        while i < len(data):
            d = data[i]
            records.append(
                Prices(
                    key=get_uuid(),
                    store_id=d["store_id"],
                    item_id=d["item_id"],
                    wm_yr_wk=d["wm_yr_wk"],
                    sell_price=d["sell_price"],
                )
            )
            i += 1
            if i % limit == 0:
                self.prices_repository.bulk_insert(records=records)
                logger.info(f"prices: {i} ...")
        if len(records) > 0:
            self.prices_repository.bulk_insert(records=records)
            logger.info(f"prices: {i} ...")

    def register_sales(self):
        data = read_csv_to_list(
            csv_file=self.sales_filepath,
            header=None,
            is_first_line_header=True,
        )
        limit = 10000
        i = 0
        records = []
        while i < len(data):
            d = data[i]
            records.append(
                Sales(
                    key=get_uuid(),                    
                    id=d["id"],
                    item_id=d["item_id"],
                    dept_id=d["dept_id"],
                    cat_id=d["cat_id"],
                    store_id=d["store_id"],
                    state_id=d["state_id"],
                    date_id=d["date_id"],
                    sales=d["sales"],
                )
            )
            i += 1            
            if i % limit == 0:
                self.sales_repository.bulk_insert(records=records)
                logger.info(f"sales: {i} ...")
        if len(records) > 0:
            self.sales_repository.bulk_insert(records=records)
            logger.info(f"sales: {i} ...")
