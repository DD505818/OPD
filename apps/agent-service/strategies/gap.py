"""GAP — session gap-fill strategy."""

from __future__ import annotations

from typing import Optional

from .common import clamp, safe_atr


class GAP:
    def __init__(self, min_gap_pct: float = 0.003, atr_period: int = 14):
        self.name = "GAP"
        self.min_gap_pct = min_gap_pct
        self.atr_period = atr_period
        self.last_session = None
        self.filled_for_session = False

    def generate_signal(self, daily_df, intraday_df) -> Optional[dict]:
        if daily_df is None or len(daily_df) < 2:
            return None
        if intraday_df is None or len(intraday_df) < 1:
            return None

        session_key = getattr(intraday_df.index[0], "date", lambda: None)()
        if session_key != self.last_session:
            self.last_session = session_key
            self.filled_for_session = False

        if self.filled_for_session:
            return None

        prior_close = float(daily_df["close"].iloc[-2])
        current_open = float(intraday_df["open"].iloc[0])
        current_bar = intraday_df.iloc[-1]
        gap_pct = (current_open - prior_close) / prior_close

        if abs(gap_pct) < self.min_gap_pct:
            return None

        atr = safe_atr(daily_df, self.atr_period)
        if atr <= 0:
            return None

        close = float(current_bar["close"])

        if gap_pct < -self.min_gap_pct and close > current_open:
            self.filled_for_session = True
            return {
                "intent_type": "directional_signal",
                "agent": self.name,
                "direction": "BUY",
                "entry": close,
                "stop": current_open - 1.5 * atr,
                "target": prior_close,
                "risk": 1.5 * atr,
                "confidence": clamp(abs(gap_pct) * 10, 0.0, 0.9),
                "reason": f"Gap down {gap_pct * 100:.2f}%; buying toward prior close.",
            }

        if gap_pct > self.min_gap_pct and close < current_open:
            self.filled_for_session = True
            return {
                "intent_type": "directional_signal",
                "agent": self.name,
                "direction": "SELL",
                "entry": close,
                "stop": current_open + 1.5 * atr,
                "target": prior_close,
                "risk": 1.5 * atr,
                "confidence": clamp(gap_pct * 10, 0.0, 0.9),
                "reason": f"Gap up {gap_pct * 100:.2f}%; selling toward prior close.",
            }

        return None

    def risk_profile(self) -> dict:
        return {
            "max_position": 1,
            "risk_per_trade": 0.005,
            "stop_multiplier": 1.5,
            "preferred_regime": ["ALL"],
            "min_gap_pct": self.min_gap_pct,
        }

    def explain(self) -> str:
        return "GAP trades meaningful session gaps back toward the prior close after confirmation of fill direction."
