import os
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple

from src.exceptions.exceptions import DatabaseException
from src.middleware.logger import configure_logger

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError

logger = configure_logger(__name__)

Base = declarative_base()


class AbstractDBClient(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def execute_create_query(
        self,
        query: str,
        parameters: Optional[Tuple] = None,
    ):
        raise NotImplementedError

    @abstractmethod
    def execute_bulk_insert_or_update_query(
        self,
        query: str,
        parameters: Optional[List[Tuple]] = None,
    ):
        raise NotImplementedError

    @abstractmethod
    def execute_select(
        self,
        query: str,
        parameters: Optional[Tuple] = None,
    ) -> List[Dict[str, Any]]:
        raise NotImplementedError


class PostgreSQLClient(AbstractDBClient):
    def __init__(self):
        user = os.getenv("POSTGRES_USER", "postgres")
        password = os.getenv("POSTGRES_PASSWORD", "password")
        host = os.getenv("POSTGRES_HOST", "postgres")
        port = os.getenv("POSTGRES_PORT", "5432")
        dbname = os.getenv("POSTGRES_DBNAME", "demand_forecasting_m5")
        url = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
        self.engine = create_engine(url)
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)

    def get_session(self) -> Session:
        return self.Session()

    def execute_create_query(
        self,
        query: str,
        parameters: Optional[Tuple] = None,
    ):
        logger.debug(f"create query: {query}, parameters: {parameters}")
        with self.get_session() as session:
            try:
                session.execute(query, parameters)
                session.commit()
            except SQLAlchemyError as e:
                session.rollback()
                raise DatabaseException(
                    message=f"failed to execute create query: {e}",
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
                session.execute(query, parameters)
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
            cursor = session.execute(query, parameters)
            columns = [desc[0] for desc in cursor.keys()]
            rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
        logger.debug(f"rows: {rows}")
        return rows
