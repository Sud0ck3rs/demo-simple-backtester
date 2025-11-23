from __future__ import annotations

from abc import ABC, abstractmethod
import pandas as pd


class Strategy(ABC):
    """
    Base interface for a trading strategy.

    A strategy receives a price DataFrame and returns signals:
      1  -> long
      0  -> flat
     -1  -> short (not used in v1)
    """

    @abstractmethod
    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        """
        Generate a signal Series aligned with `data` index.

        Returns:
            pd.Series: values in {1, 0, -1}
        """
        ...
