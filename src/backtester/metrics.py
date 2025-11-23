from __future__ import annotations

from typing import List
import numpy as np
import pandas as pd

from .engine import Trade


def compute_basic_metrics(equity_curve: pd.Series, trades: List[Trade]) -> dict:
    """
    Compute basic performance metrics for the backtest.

    Metrics:
      - total_return
      - max_drawdown
      - winrate
      - number of trades
      - average win / loss
      - simple Sharpe ratio (daily approx)
    """
    returns = equity_curve.pct_change().dropna()

    total_return = equity_curve.iloc[-1] / equity_curve.iloc[0] - 1

    # Max drawdown
    rolling_max = equity_curve.cummax()
    drawdown = equity_curve / rolling_max - 1
    max_drawdown = drawdown.min()

    # Winrate, avg win/loss
    if trades:
        wins = [t for t in trades if t.pnl > 0]
        winrate = len(wins) / len(trades)
        avg_win = np.mean([t.pnl for t in wins]) if wins else 0.0
        losses = [t for t in trades if t.pnl <= 0]
        avg_loss = np.mean([t.pnl for t in losses]) if losses else 0.0
    else:
        winrate = 0.0
        avg_win = 0.0
        avg_loss = 0.0

    # Naive daily Sharpe (rf = 0)
    sharpe = 0.0
    if not returns.empty and returns.std() != 0:
        sharpe = (returns.mean() / returns.std()) * (252 ** 0.5)

    return {
        "total_return": float(total_return),
        "max_drawdown": float(max_drawdown),
        "winrate": float(winrate),
        "nb_trades": len(trades),
        "avg_win": float(avg_win),
        "avg_loss": float(avg_loss),
        "sharpe": float(sharpe),
    }
