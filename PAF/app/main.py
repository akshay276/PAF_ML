"""
Application entry point.

Acts only as orchestration layer.
"""

from __future__ import annotations

import json
from pathlib import Path

from database import DatabaseManager
from data_processor import DataProcessor
from trainer import Trainer
from predictor import Predictor
from logger import get_logger


CONFIG_FILE = Path("../config/config.json")


class Application:
    """
    Main application orchestration.
    """

    def __init__(self) -> None:
        self.config = self.load_config()

        self.logger = get_logger(
            self.config["logging"]["log_path"]
        )

    @staticmethod
    def load_config() -> dict:
        """
        Loads JSON configuration.
        """

        with CONFIG_FILE.open(
            encoding="utf-8"
        ) as file:
            return json.load(file)

    def execute(self) -> None:
        """
        Executes complete ML workflow.
        """

        self.logger.info(
            "Starting Predictive Analytics Framework..."
        )

        database = DatabaseManager(
            self.config
        )

        processor = DataProcessor(
            self.config
        )

        trainer = Trainer(
            self.config
        )

        predictor = Predictor(
            self.config
        )

        dataframe = database.read_csv()

        processed = processor.process(
            dataframe
        )

        metrics = trainer.train(
            processed
        )

        predictions = predictor.predict(
            processed.head(5)
        )

        self.display_summary(
            metrics,
            predictions,
        )

        self.logger.info(
            "Execution completed successfully."
        )

    @staticmethod
    def display_summary(
        metrics: dict,
        predictions: dict,
    ) -> None:
        """
        Prints professional execution summary.
        """

        print("\n" + "=" * 70)
        print("TRAINING SUMMARY")
        print("=" * 70)

        print(
            f"Rows Read              : {metrics['rows_read']}"
        )

        print(
            f"Features Used          : {', '.join(metrics['features_used'])}"
        )

        print(
            f"Algorithm              : {metrics['algorithm']}"
        )

        print(
            f"Accuracy               : {metrics['accuracy']:.4f}"
        )

        print(
            f"Precision              : {metrics['precision']:.4f}"
        )

        print(
            f"Recall                 : {metrics['recall']:.4f}"
        )

        print(
            f"F1 Score               : {metrics['f1_score']:.4f}"
        )

        print(
            f"Training Time (sec)    : {metrics['training_time']}"
        )

        print(
            f"Prediction Time (sec)  : {predictions['prediction_time']}"
        )

        print(
            f"Confusion Matrix       : {metrics['confusion_matrix']}"
        )

        print("=" * 70)

        print("\nSample Predictions")

        for index, value in enumerate(
            predictions["prediction"],
            start=1,
        ):
            print(
                f"Record {index:02d} -> Prediction: {value}"
            )


def main() -> None:
    """
    Application entry point.
    """

    app = Application()

    app.execute()


if __name__ == "__main__":
    main()
