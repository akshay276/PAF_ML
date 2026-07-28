"""
Model training module.
"""

from __future__ import annotations

import time
from pathlib import Path
from typing import Any

import joblib
import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)

from sklearn.model_selection import train_test_split

from model import ModelFactory


class Trainer:
    """
    Responsible for

    - Train/Test Split
    - Model Training
    - Model Evaluation
    - Model Persistence
    """

    def __init__(
        self,
        config: dict[str, Any],
    ) -> None:
        self.config = config

    def train(
        self,
        dataframe: pd.DataFrame,
    ) -> dict[str, Any]:
        """
        Train machine learning model.
        """

        feature_columns = (
            self.config["dataset"]["feature_columns"]
        )

        target_column = (
            self.config["dataset"]["target_column"]
        )

        x = dataframe[feature_columns]

        y = dataframe[target_column]

        x_train, x_test, y_train, y_test = train_test_split(
            x,
            y,
            test_size=self.config["training"]["test_size"],
            random_state=self.config["training"]["random_seed"],
            stratify=y,
        )

        model = ModelFactory.create()

        start = time.perf_counter()

        model.fit(
            x_train,
            y_train,
        )

        training_time = (
            time.perf_counter() - start
        )

        prediction = model.predict(
            x_test
        )

        metrics = {
            "accuracy": accuracy_score(
                y_test,
                prediction,
            ),
            "precision": precision_score(
                y_test,
                prediction,
                zero_division=0,
            ),
            "recall": recall_score(
                y_test,
                prediction,
                zero_division=0,
            ),
            "f1_score": f1_score(
                y_test,
                prediction,
                zero_division=0,
            ),
            "confusion_matrix": confusion_matrix(
                y_test,
                prediction,
            ).tolist(),
            "training_time": round(
                training_time,
                4,
            ),
            "rows_read": len(
                dataframe
            ),
            "features_used": feature_columns,
            "algorithm": self.config["training"]["algorithm"],
        }

        self.save_model(
            model
        )

        return metrics

    def save_model(
        self,
        model,
    ) -> None:
        """
        Persist trained model.
        """

        BASE_DIR = Path(__file__).resolve().parent.parent

        model_path = BASE_DIR / self.config["model"]["model_path"]

        model_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        print(f"Saving model to: {model_path}")

        joblib.dump(
            model,
            model_path,
        )
        print("Model saved successfully.")
