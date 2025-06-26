import os
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple

from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker

from src.exceptions.exceptions import DatabaseException
from src.infrastructure.schema.models import Base
from src.middleware.logger import configure_logger

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
    def execute_create_query(
        self,
        query: str,
        parameters: Optional[Tuple] = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def execute_bulk_insert_or_update_query(
        self,
        query: str,
        parameters: Optional[List[Tuple]] = None,
    ) -> bool:
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
        Base.metadata.create_all(self._engine)

    @property
    def engine(self) -> Any:
        return self._engine

    def get_session(self) -> Session:
        return self.Session()

    def execute_create_query(
        self,
        query: str,
        parameters: Optional[Tuple] = None,
    ) -> None:
        logger.debug(f"create query: {query}, parameters: {parameters}")
        with self.get_session() as session:
            try:
                session.execute(text(query), parameters)
                session.commit()
            except SQLAlchemyError as e:
                session.rollback()
                raise DatabaseException(
                    message=f"failed to insert or update query: {e}",
                    detail=f"{query} {parameters}: {e}",
                )

    def execute_bulk_insert_or_update_query(
        self,
        query: str,
        parameters: Optional[List[Tuple]] = None,
    ) -> bool:
        logger.debug(f"bulk insert or update query: {query}, parameters: {parameters}")
        with self.get_session() as session:
            try:
                session.execute(text(query), parameters)  # type: ignore[arg-type]
                session.commit()
                return True
            except SQLAlchemyError as e:
                session.rollback()
                raise DatabaseException(
                    message=f"failed to bulk insert or update query: {e}",
                    detail=f"{query} {parameters}: {e}",
                )

    def execute_select(
        self,
        query: str,
        parameters: Optional[Tuple] = None,
    ) -> List[Dict[str, Any]]:
        logger.debug(f"select query: {query}, parameters: {parameters}")
        with self.get_session() as session:
            result = session.execute(text(query), parameters)
            columns = [desc[0] for desc in result.keys()]
            rows = [dict(zip(columns, row)) for row in result.fetchall()]
        logger.debug(f"rows: {rows}")
        return rows
