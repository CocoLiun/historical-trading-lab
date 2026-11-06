"""Deterministic daily historical paper-trading core."""
from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal

@dataclass(frozen=True)
class Bar:
    day: date
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: int

    def validate(self):
        prices = (self.open, self.high, self.low, self.close)
        if any(not p.is_finite() or p <= 0 for p in prices):
            raise ValueError("Invalid price")
        if isinstance(self.volume, bool) or not isinstance(self.volume, int) or self.volume < 0:
            raise ValueError("Invalid volume")
        if self.high < max(self.open, self.close, self.low) or self.low > min(self.open, self.close, self.high):
            raise ValueError("Inconsistent OHLC")

@dataclass
class Account:
    cash: Decimal = Decimal("100000")
    shares: int = 0
    trades: list = field(default_factory=list)

    def __post_init__(self):
        if not self.cash.is_finite() or self.cash < 0 or self.shares < 0:
            raise ValueError("Invalid initial account")

    def equity(self, close: Decimal):
        return self.cash + self.shares * close

    def execute_next_open(self, bar: Bar, side: str, qty: int, fee_rate=Decimal("0.0003"), slippage=Decimal("0.0005"), decision_date=None):
        bar.validate()
        if decision_date is not None and bar.day <= decision_date:
            raise ValueError("Execution must follow decision date")
        if side not in ("buy", "sell") or type(qty) is not int or qty <= 0:
            raise ValueError("Invalid order")
        fee_rate, slippage = Decimal(str(fee_rate)), Decimal(str(slippage))
        if not fee_rate.is_finite() or not slippage.is_finite() or fee_rate < 0 or not (0 <= slippage < 1):
            raise ValueError("Invalid transaction cost")
        if side == "sell" and qty > self.shares:
            raise ValueError("Insufficient shares")
        price = bar.open * (1 + slippage if side == "buy" else 1 - slippage)
        notional = price * qty
        fee = notional * fee_rate
        if side == "buy":
            if notional + fee > self.cash:
                raise ValueError("Insufficient cash")
            self.cash -= notional + fee
            self.shares += qty
        else:
            self.cash += notional - fee
            self.shares -= qty
        trade = {"date": bar.day.isoformat(), "side": side, "qty": qty, "price": str(price), "fee": str(fee)}
        self.trades.append(trade)
        return trade

def maximum_drawdown(values):
    peak = None
    worst = Decimal("0")
    for v in values:
        v = Decimal(str(v))
        if not v.is_finite() or v < 0:
            raise ValueError("Invalid equity")
        peak = v if peak is None else max(peak, v)
        if peak > 0:
            worst = min(worst, v / peak - 1)
    return worst
