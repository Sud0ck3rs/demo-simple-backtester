from __future__ import annotations

from dataclasses import dataclass
from typing import List

import pandas as pd

from .strategy_base import Strategy


@dataclass
class Trade:
    """
    Represents a completed trade.
    """
    entry_time: pd.Timestamp
    exit_time: pd.Timestamp
    entry_price: float
    exit_price: float
    qty: float
    pnl: float


class BacktestEngine:
    """
    Simple backtest engine for long-only strategies.

    Assumptions:
      - At most one position at a time
      - Long only
      - Position size = risk_per_trade * current capital
      - No fees, no slippage in v1
    """
    def __init__(
        self,
        initial_capital: float = 10_000.0,
        risk_per_trade: float = 0.1,  # 10% du capital par trade
    ):
        self.initial_capital = initial_capital
        self.risk_per_trade = risk_per_trade

    def run(
        self,
        data: pd.DataFrame,
        strategy: Strategy,
    ) -> dict:
        """
        Run the backtest.

        Args:
            data (pd.DataFrame): OHLCV data.
            strategy (Strategy): strategy instance.

        Returns:
            dict: {
                "equity_curve": pd.Series,
                "trades": list[Trade],
                "final_capital": float,
            }
        """
        df = data.copy()
        signals = strategy.generate_signals(df)
        df["signal"] = signals

        capital = self.initial_capital
        position = 0.0  # quantity in asset (e.g. BTC)
        entry_price = None
        entry_time = None

        equity_curve = []
        trades: List[Trade] = []

        for timestamp, row in df.iterrows():
            price = row["close"]
            signal = row["signal"]

            # Mark-to-market equity update
            equity = capital + position * price
            equity_curve.append((timestamp, equity))

            # Trading logic: simple long / flat switch
            if position == 0 and signal == 1:
                # Open a long position
                amount_to_invest = capital * self.risk_per_trade
                qty = amount_to_invest / price
                position = qty
                capital -= amount_to_invest
                entry_price = price
                entry_time = timestamp

            elif position > 0 and signal == 0:
                # Close the existing position
                exit_price = price
                pnl = position * (exit_price - entry_price)
                capital += position * exit_price
                trades.append(
                    Trade(
                        entry_time=entry_time,
                        exit_time=timestamp,
                        entry_price=float(entry_price),
                        exit_price=float(exit_price),
                        qty=float(position),
                        pnl=float(pnl),
                    )
                )
                position = 0.0
                entry_price = None
                entry_time = None

        # If a position is still open at the end, close it at the last price
        if position > 0:
            last_ts = df.index[-1]
            last_price = df["close"].iloc[-1]
            exit_price = last_price
            pnl = position * (exit_price - entry_price)
            capital += position * exit_price
            trades.append(
                Trade(
                    entry_time=entry_time,
                    exit_time=last_ts,
                    entry_price=float(entry_price),
                    exit_price=float(exit_price),
                    qty=float(position),
                    pnl=float(pnl),
                )
            )
            equity_curve.append((last_ts, capital))

        equity_series = pd.Series(
            [e for _, e in equity_curve],
            index=[t for t, _ in equity_curve],
            name="equity",
        )

        return {
            "equity_curve": equity_series,
            "trades": trades,
            "final_capital": capital,
        }
