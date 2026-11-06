from datetime import date
from decimal import Decimal
import pytest
from engine import Bar, Account, maximum_drawdown

def bar():
    return Bar(date(2020,1,2), Decimal("100"), Decimal("110"), Decimal("90"), Decimal("105"), 10000)

def test_buy_sell():
    a = Account(Decimal("1000"))
    a.execute_next_open(bar(), "buy", 5, decision_date=date(2020,1,1))
    assert a.shares == 5 and a.cash < 500
    a.execute_next_open(bar(), "sell", 5)
    assert a.shares == 0 and a.cash < 1000

def test_insufficient_cash():
    with pytest.raises(ValueError): Account(Decimal("100")).execute_next_open(bar(), "buy", 2)

def test_insufficient_shares():
    with pytest.raises(ValueError): Account().execute_next_open(bar(), "sell", 1)

def test_bad_bar():
    with pytest.raises(ValueError): Bar(date(2020,1,2), Decimal("100"), Decimal("90"), Decimal("80"), Decimal("95"), 10).validate()

@pytest.mark.parametrize("bad", ["NaN", "Infinity", "-1", "0"])
def test_bad_price(bad):
    with pytest.raises(ValueError): Bar(date(2020,1,2), Decimal(bad), Decimal("110"), Decimal("90"), Decimal("105"), 1).validate()

def test_drawdown():
    assert maximum_drawdown([100,120,90,110]) == Decimal("-0.25")

def test_future_fill_blocked():
    with pytest.raises(ValueError): Account().execute_next_open(bar(), "buy", 1, decision_date=date(2020,1,2))

def test_invalid_cost_is_atomic():
    a = Account(Decimal("1000"))
    with pytest.raises(ValueError): a.execute_next_open(bar(), "buy", 1, slippage=Decimal("NaN"))
    assert a.shares == 0 and a.cash == 1000 and not a.trades

def test_bad_initial_cash():
    with pytest.raises(ValueError): Account(Decimal("NaN"))
