"""
Model abstraction layer.
"""

from __future__ import annotations

from sklearn.ensemble import RandomForestClassifier


class ModelFactory:
    """
    Factory responsible for creating
    ML algorithm instances.
    """

    @staticmethod
    def create():
        """
        Returns configured model.
        """

        return RandomForestClassifier(
            n_estimators=200,
            random_state=42,
        )
