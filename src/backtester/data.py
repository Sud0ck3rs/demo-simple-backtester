from __future__ import annotations

from pathlib import Path
import pandas as pd


def load_ohlcv_csv(path: str | Path) -> pd.DataFrame:
    """
    Load an OHLCV CSV file.

    Supports formats like TradingView exports with:
      - time (unix seconds) OR timestamp (datetime string)
      - open, high, low, close
      - volume or Volume

    Returns a DataFrame indexed by datetime with columns:
      ['open', 'high', 'low', 'close', 'volume']
    """
    path = Path(path)
    df = pd.read_csv(path)

    # 1) Time column: 'timestamp' or 'time's
    if "timestamp" in df.columns:
        time_col = "timestamp"
    elif "time" in df.columns:
        time_col = "time"
    else:
        raise ValueError("CSV must contain a 'timestamp' or 'time' column")

    # Convert datatime
    df[time_col] = pd.to_datetime(df[time_col], unit="s")
    df = df.set_index(time_col).sort_index()
    df.index.name = "timestamp"

    # 2) Normalize volume column
    if "volume" in df.columns:
        vol_col = "volume"
    elif "Volume" in df.columns:
        vol_col = "Volume"
    else:
        raise ValueError("CSV must contain a 'volume' or 'Volume' column")

    # 3) Keep only OHLCV columns
    keep_cols = ["open", "high", "low", "close", vol_col]
    missing = [c for c in ["open", "high", "low", "close"] if c not in df.columns]
    if missing:
        raise ValueError(f"Missing OHLC columns in CSV: {missing}")

    df = df[keep_cols].copy()
    df = df.rename(columns={vol_col: "volume"})

    return df
