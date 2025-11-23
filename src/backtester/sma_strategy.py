from __future__ import annotations

import pandas as pd

from .strategy_base import Strategy


class SmaCrossStrategy(Strategy):
    """
    Stratégie simple :
    - SMA courte > SMA longue -> long
    - Sinon -> flat
    """

    def __init__(self, short_window: int = 20, long_window: int = 50):
        if short_window >= long_window:
            raise ValueError("short_window must be < long_window")
        self.short_window = short_window
        self.long_window = long_window

    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        close = data["close"]
        sma_short = close.rolling(self.short_window).mean()
        sma_long = close.rolling(self.long_window).mean()

        signal = (sma_short > sma_long).astype(int)  # 1 = long, 0 = flat
        signal.name = "signal"
        return signal
