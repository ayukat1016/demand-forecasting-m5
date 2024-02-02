from src.infrastructure.database import AbstractDBClient
from src.middleware.file_reader import read_text_file
from src.middleware.logger import configure_logger
from src.repository.abstract_repository import AbstractTableRepository

logger = configure_logger(__name__)


class TableRepository(AbstractTableRepository):
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
