from src.database import PostgreSQLClient
from src.logger import configure_logger
from src.service import PredictionService, SalesService
from src.view import build

logger = configure_logger(__name__)


def main() -> None:
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
