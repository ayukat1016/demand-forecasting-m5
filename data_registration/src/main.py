from typing import Optional

import click

from src.infrastructure.database.db_client import PostgreSQLClient
from src.infrastructure.repository.calendar_repository import CalendarRepository
from src.infrastructure.repository.prices_repository import PricesRepository
from src.infrastructure.repository.sales_repository import SalesRepository
from src.infrastructure.repository.tables_repository import TablesRepository
from src.middleware.logger import configure_logger
from src.usecase.data_register_usecase import DataRegisterUsecase

logger = configure_logger(__name__)


@click.command()
@click.option(
    "--tables_filepath",
    type=str,
    required=False,
)
@click.option(
    "--calendar_filepath",
    type=str,
    required=False,
)
@click.option(
    "--prices_filepath",
    type=str,
    required=False,
)
@click.option(
    "--sales_filepath",
    type=str,
    required=False,
)
def main(
    tables_filepath: Optional[str] = None,
    calendar_filepath: Optional[str] = None,
    prices_filepath: Optional[str] = None,
    sales_filepath: Optional[str] = None,
) -> None:

    if tables_filepath is None:
        raise ValueError("tables_filepath cannot be None")

    if calendar_filepath is None:
        raise ValueError("calendar_filepath cannot be None")

    if prices_filepath is None:
        raise ValueError("prices_filepath cannot be None")

    if sales_filepath is None:
        raise ValueError("sales_filepath cannot be None")

    logger.info("START data_registration")
    logger.info(
        f"""
options:
tables_filepath: {tables_filepath}
calendar_filepath: {calendar_filepath}
prices_filepath: {prices_filepath}
sales_filepath: {sales_filepath}
    """
    )
    db_client = PostgreSQLClient()
    tables_repository = TablesRepository(db_client=db_client)
    calendar_repository = CalendarRepository(db_client=db_client)
    prices_repository = PricesRepository(db_client=db_client)
    sales_repository = SalesRepository(db_client=db_client)

    data_register_usecase = DataRegisterUsecase(
        tables_filepath=tables_filepath,
        calendar_filepath=calendar_filepath,
        prices_filepath=prices_filepath,
        sales_filepath=sales_filepath,
        tables_repository=tables_repository,
        calendar_repository=calendar_repository,
        prices_repository=prices_repository,
        sales_repository=sales_repository,
    )

    logger.info("create table")
    data_register_usecase.create_table()
    logger.info("done create table")

    logger.info("register calendar")
    data_register_usecase.register_calendar()
    logger.info("done register calendar")

    logger.info("register prices")
    data_register_usecase.register_prices()
    logger.info("done register prices")

    logger.info("register sales")
    data_register_usecase.register_sales()
    logger.info("done register sales")

    logger.info("DONE data_registration")


if __name__ == "__main__":
    main()
