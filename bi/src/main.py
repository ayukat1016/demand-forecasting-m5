from database import PostgreSQLClient
from logger import configure_logger
from service import PredictionService, SalesService
from view import build

logger = configure_logger(__name__)


def main():
    logger.info("now loading...")
    logger.info("start fun time")
    db_client = PostgreSQLClient()
    sales_service = SalesService(db_client=db_client)
    prediction_service = PredictionService(db_client=db_client)
    build(
        sales_service=sales_service,
        prediction_service=prediction_service,
    )


if __name__ == "__main__":
    main()
