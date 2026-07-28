"""
Database abstraction layer.

Responsible only for:
- Oracle connectivity
- CSV reading
- Returning pandas DataFrame
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import oracledb
import pandas as pd


class DatabaseManager:
    """
    Database abstraction layer.

    This class intentionally avoids any preprocessing
    or business logic.
    """

    def __init__(self, config: dict[str, Any]) -> None:
        self.config = config

    def read_csv(self) -> pd.DataFrame:
        """
        Reads dataset from CSV.
        """

        BASE_DIR = Path(__file__).resolve().parent.parent

        csv_path = BASE_DIR / self.config["dataset"]["csv_path"]

        if not csv_path.exists():
            raise FileNotFoundError(
                f"Dataset not found: {csv_path}"
            )

        return pd.read_csv(csv_path)

    def get_oracle_connection(self):
        """
        Returns Oracle connection.

        Version 1 provides reusable connectivity only.
        """

        database = self.config["database"]

        dsn = oracledb.makedsn(
            database["host"],
            database["port"],
            service_name=database["service_name"],
        )

        connection = oracledb.connect(
            user=database["username"],
            password=database["password"],
            dsn=dsn,
        )

        return connection

    def read_from_database(self) -> pd.DataFrame:
        """
        Executes configured SQL query and
        returns DataFrame.
        """

        connection = self.get_oracle_connection()

        try:
            dataframe = pd.read_sql(
                self.config["database"]["query"],
                connection,
            )

            return dataframe

        finally:
            connection.close()
