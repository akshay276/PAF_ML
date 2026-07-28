"""
Data preprocessing module.
"""

from __future__ import annotations

from typing import Any

import pandas as pd


class DataProcessor:
    """
    Responsible for data validation,
    cleaning and feature engineering.
    """

    def __init__(self, config: dict[str, Any]) -> None:
        self.config = config

    def validate_dataset(
        self,
        dataframe: pd.DataFrame,
    ) -> None:
        """
        Validate incoming dataset.
        """

        if dataframe.empty:
            raise ValueError(
                "Dataset is empty."
            )

        required_columns = (
            self.config["dataset"]["feature_columns"]
            + [
                self.config["dataset"]["target_column"]
            ]
        )

        missing = [
            column
            for column in required_columns
            if column not in dataframe.columns
        ]

        if missing:
            raise ValueError(
                f"Missing columns: {missing}"
            )

    def clean_data(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Cleans dataset.
        """

        dataframe = dataframe.copy()

        dataframe.drop_duplicates(
            inplace=True
        )

        dataframe = dataframe.ffill()
        dataframe = dataframe.bfill()

        return dataframe

    def feature_engineering(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Performs lightweight
        feature engineering.
        """

        dataframe = dataframe.copy()

        if "Gender" in dataframe.columns:
            dataframe["Gender"] = (
                dataframe["Gender"]
                .map(
                    {
                        "Male": 1,
                        "Female": 0,
                    }
                )
                .astype(int)
            )

        return dataframe

    def process(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Executes preprocessing pipeline.
        """

        self.validate_dataset(
            dataframe
        )

        dataframe = self.clean_data(
            dataframe
        )

        dataframe = self.feature_engineering(
            dataframe
        )

        return dataframe
