from __future__ import annotations

from pathlib import Path
import pandas as pd


def load_ohlcv_csv(path: str | Path) -> pd.DataFrame:
    """
    Charge un CSV OHLCV.
    Gère notamment un format type TradingView avec :
      - time (unix seconds)
      - open, high, low, close
      - Volume (V majuscule)

    Retourne un DataFrame avec index datetime et colonnes :
      ['open', 'high', 'low', 'close', 'volume']
    """
    path = Path(path)
    df = pd.read_csv(path)

    # 1) Gestion du temps : 'timestamp' ou 'time'
    if "timestamp" in df.columns:
        time_col = "timestamp"
    elif "time" in df.columns:
        time_col = "time"
    else:
        raise ValueError("CSV must contain a 'timestamp' or 'time' column")

    # Convertit en datetime (on suppose des secondes)
    df[time_col] = pd.to_datetime(df[time_col], unit="s")
    df = df.set_index(time_col).sort_index()
    df.index.name = "timestamp"

    # 2) Normalisation des colonnes de volume
    if "volume" in df.columns:
        vol_col = "volume"
    elif "Volume" in df.columns:
        vol_col = "Volume"
    else:
        raise ValueError("CSV must contain a 'volume' or 'Volume' column")

    # 3) Ne garder que les colonnes utiles
    keep_cols = ["open", "high", "low", "close", vol_col]
    missing = [c for c in ["open", "high", "low", "close"] if c not in df.columns]
    if missing:
        raise ValueError(f"Missing OHLC columns in CSV: {missing}")

    df = df[keep_cols].copy()
    df = df.rename(columns={vol_col: "volume"})

    return df
