# Simple Trading Strategy Backtester

A minimal yet clean Python backtesting engine for OHLCV data.

This project is designed to:
- Showcase a clear and extensible architecture for backtesting
- Provide a simple example strategy (SMA crossover)
- Compute basic performance metrics and plot the equity curve

It is a good portfolio project for Python / trading / quant roles.

---

## Features

- Load OHLCV data from CSV (TradingView-style exports supported)
- SMA crossover strategy (long-only, 1 position at a time)
- Capital-based position sizing (percentage of equity per trade)
- Equity curve computation
- Basic metrics:
  - Total return
  - Max drawdown
  - Winrate
  - Number of trades
  - Average win / loss
  - Simple daily Sharpe ratio (rf = 0)
- Simple CLI entry point (`main.py`) with an equity curve plot

---

## Project Structure

```bash
simple-backtester/
  ├─ src/
  │   └─ backtester/
  │        ├─ __init__.py
  │        ├─ data.py          # Data loading / normalization
  │        ├─ strategy_base.py # Strategy interface
  │        ├─ sma_strategy.py  # SMA crossover implementation
  │        ├─ engine.py        # Backtest engine
  │        └─ metrics.py       # Performance metrics
  ├─ data/
  │   └─ sample_data.csv       # Example OHLCV dataset
  ├─ tests/
  │   └─ test_engine.py        # (optional) Unit tests
  ├─ main.py                   # Simple CLI entry point
  ├─ requirements.txt
  ├─ README.md
  └─ .gitignore
```

---

## Installation

```bash
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>

# Create and activate a virtual env (recommended)
python -m venv .venv
source .venv/bin/activate  # on Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## Data format

The backtester expects an OHLCV CSV file with at least:

- Either:
  - `time` (unix seconds), or
  - `timestamp` (datetime string)
- Columns:
  - `open`
  - `high`
  - `low`
  - `close`
  - `volume`

Example (TradingView-style):

```c
time,open,high,low,close,Volume
1763627400,199.5,201.2,198.8,200.1,12345
1763628300,200.1,202.0,199.7,201.4,9876
```

The loader will:

- Convert the time column to a pandas `DatetimeIndex`
- Normalize the volume column to `volume`
- Keep only `open, high, low, close, volume`

Place your file in the `data/` folder and update the path in `main.py` if needed.

---

## Usage

From the project root:

```bash
python3 main.py
```

This will:

1. Load `data/BITGET_SOLUSDT.P, 15_3b650.csv`
2. Run the SMA crossover strategy with
    - short_window = 20
    - long_window = 50
3. Print backtest metrics in the console
4. Display an equity curve plot

---

## Customization

### Change strategy parameters

In `main.py`:

```python
strategy = SmaCrossStrategy(short_window=10, long_window=30)
```

### Change risk per trade / capital

In `main.py`:

```python
engine = BacktestEngine(
    initial_capital=20_000,
    risk_per_trade=0.05,  # 5% of capital per trade
)
```

### Implement a new strategy

Create a new file `src/backtester/my_strategy.py`:

```python
import pandas as pd
from .strategy_base import Strategy

class MyStrategy(Strategy):
    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        # Your custom logic here
        signal = ...
        signal.name = "signal"
        return signal
```

Then import and use it in `main.py`.