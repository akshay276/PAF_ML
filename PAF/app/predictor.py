"""
Prediction module.
"""

from __future__ import annotations

import time
from pathlib import Path
from typing import Any

import joblib
import pandas as pd


class Predictor:
    """
    Loads trained model
    and performs prediction.
    """

    def __init__(
        self,
        config: dict[str, Any],
    ) -> None:
        self.config = config

    def load_model(self):
        """
        Load persisted model.
        """

        BASE_DIR = Path(__file__).resolve().parent.parent

        model_path = BASE_DIR / self.config["model"]["model_path"]

        if not model_path.exists():
            raise FileNotFoundError(
                f"Model not found: {model_path}"
            )

        return joblib.load(
            model_path
        )

    def predict(
        self,
        dataframe: pd.DataFrame,
    ) -> dict[str, Any]:
        """
        Perform prediction.
        """

        model = self.load_model()

        features = (
            self.config["dataset"]["feature_columns"]
        )

        start = time.perf_counter()

        prediction = model.predict(
            dataframe[features]
        )

        probability = model.predict_proba(
            dataframe[features]
        )

        prediction_time = (
            time.perf_counter() - start
        )

        return {
            "prediction": prediction.tolist(),
            "probability": probability.tolist(),
            "prediction_time": round(
                prediction_time,
                4,
            ),
        }
