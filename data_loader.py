"""Strict user-supplied OHLCV CSV parser."""
import io
from decimal import Decimal, InvalidOperation
import pandas as pd
from engine import Bar

FIELDS = {"date", "open", "high", "low", "close", "volume"}

def parse_bars(data: bytes):
    if not data:
        raise ValueError("Empty CSV")
    frame = pd.read_csv(io.BytesIO(data), dtype=str, keep_default_na=False)
    if not FIELDS.issubset(frame.columns):
        raise ValueError("Missing columns: " + str(FIELDS - set(frame.columns)))
    if len(frame) < 2:
        raise ValueError("At least two days required")
    if any(frame[c].eq("").any() for c in FIELDS):
        raise ValueError("Empty data cell")
    dates = pd.to_datetime(frame["date"], format="%Y-%m-%d", errors="raise").dt.date
    if dates.duplicated().any():
        raise ValueError("Duplicate trading date")
    bars = []
    try:
        for i, row in frame.iterrows():
            volume = row["volume"].strip()
            if not volume.isdecimal():
                raise ValueError("Invalid volume")
            bar = Bar(dates.iloc[i], *(Decimal(row[c]) for c in ("open", "high", "low", "close")), int(volume))
            bar.validate()
            bars.append(bar)
    except InvalidOperation as exc:
        raise ValueError("Invalid numeric price") from exc
    return sorted(bars, key=lambda x: x.day)
