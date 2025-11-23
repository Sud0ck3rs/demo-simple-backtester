from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt

from src.backtester.data import load_ohlcv_csv
from src.backtester.engine import BacktestEngine
from src.backtester.sma_strategy import SmaCrossStrategy
from src.backtester.metrics import compute_basic_metrics


def main():
    data_path = Path("data/BITGET_SOLUSDT.P, 15_3b650.csv")  # Path to your CSV files
    df = load_ohlcv_csv(data_path)

    # Define strategy and engine
    strategy = SmaCrossStrategy(short_window=20, long_window=50)
    engine = BacktestEngine(initial_capital=10_000, risk_per_trade=0.1)

    # Run backtest
    result = engine.run(df, strategy)
    equity = result["equity_curve"]
    trades = result["trades"]

    # Compute metrics
    metrics = compute_basic_metrics(equity, trades)

    print("=== Résultats du backtest ===")
    for k, v in metrics.items():
        print(f"{k}: {v}")

    # Plot equity curve
    plt.figure()
    equity.plot()
    plt.title("Equity curve")
    plt.xlabel("Date")
    plt.ylabel("Capital")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
