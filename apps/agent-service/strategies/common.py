"""Shared helpers for ΩMEGA PRIME Δ strategy agents.

These helpers are intentionally lightweight and deterministic. They do not execute
orders and do not connect to brokers.
"""

from __future__ import annotations

from typing import Iterable

import numpy as np


def safe_atr(df, period: int = 14, fallback_pct: float = 0.005) -> float:
    """Return ATR with NaN/short-history protection.

    Expected columns: high, low, close.
    """
    if df is None or len(df) < 2:
        return 0.0

    high = df["high"]
    low = df["low"]
    close = df["close"]

    tr1 = high - low
    tr2 = np.abs(high - close.shift())
    tr3 = np.abs(low - close.shift())
    tr = np.maximum(np.maximum(tr1, tr2), tr3)

    atr = tr.rolling(period).mean().iloc[-1]
    if np.isnan(atr) or atr <= 0:
        last_close = float(close.iloc[-1])
        return max(last_close * fallback_pct, 1e-9)
    return float(atr)


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return float(max(low, min(high, value)))


def last_close(df) -> float:
    if df is None or len(df) == 0:
        return 0.0
    return float(df["close"].iloc[-1])


def mean(values: Iterable[float]) -> float:
    arr = np.asarray(list(values), dtype=float)
    return float(np.mean(arr)) if len(arr) else 0.0
