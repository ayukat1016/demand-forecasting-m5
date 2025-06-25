import os
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker

from src.logger import configure_logger

logger = configure_logger(__name__)


class AbstractDBClient(ABC):
    def __init__(self) -> None:
        pass

    @property
    @abstractmethod
    def engine(self) -> Any:
        raise NotImplementedError

    @abstractmethod
    def get_session(self) -> Session:
        raise NotImplementedError

    @abstractmethod
    def execute_select(
        self,
        query: str,
        parameters: Optional[Tuple] = None,
    ) -> List[Dict[str, Any]]:
        raise NotImplementedError


class PostgreSQLClient(AbstractDBClient):
    def __init__(self) -> None:
        user = os.getenv("POSTGRES_USER", "postgres")
        password = os.getenv("POSTGRES_PASSWORD", "password")
        host = os.getenv("POSTGRES_HOST", "postgres")
        port = os.getenv("POSTGRES_PORT", "5432")
        dbname = os.getenv("POSTGRES_DBNAME", "demand_forecasting_m5")
        url = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
        self._engine = create_engine(url)
        self.Session = sessionmaker(bind=self._engine)

    @property
    def engine(self) -> Any:
        return self._engine

    def get_session(self) -> Session:
        return self.Session()

    def execute_select(
        self,
        query: str,
        parameters: Optional[Tuple] = None,
    ) -> List[Dict[str, Any]]:
        logger.debug(f"select query: {query}, parameters: {parameters}")
        with self.get_session() as session:
            cursor = session.execute(text(query), parameters)
            columns = [desc[0] for desc in cursor.keys()]
            rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
        logger.debug(f"rows: {rows}")
        return rows
