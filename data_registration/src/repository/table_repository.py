from src.infrastructure.database import AbstractDBClient
from src.middleware.logger import configure_logger
from src.repository.abstract_repository import AbstractCreateTablesRepository

logger = configure_logger(__name__)


class TableRepository(AbstractCreateTablesRepository):
    def __init__(
        self,
        db_client: AbstractDBClient,
    ):
        super().__init__(db_client=db_client)

    def create_tables(
        self,
        query: str,
    ):
        self.db_client.execute_create_query(query=query)
