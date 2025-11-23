from __future__ import annotations

from abc import ABC, abstractmethod
import pandas as pd


class Strategy(ABC):
    """
    Interface de base pour une stratégie.
    """

    @abstractmethod
    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        """
        Retourne une Series alignée au DataFrame data,
        avec :
          1  -> signal long
          0  -> neutral (pas de position)
         -1  -> signal short (pas géré en V1)
        """
        ...
