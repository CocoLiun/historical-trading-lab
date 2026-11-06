import pytest
from data_loader import parse_bars

HEAD = b"date,open,high,low,close,volume\n"
FIRST = b"2020-01-02,100,110,90,105,1000\n"
SECOND = b"2020-01-03,105,120,100,115,1500\n"

def test_valid_data():
    bars = parse_bars(HEAD + SECOND + FIRST)
    assert len(bars) == 2 and bars[0].day < bars[1].day

@pytest.mark.parametrize("invalid", [
    HEAD + FIRST + FIRST,
    HEAD + FIRST + b"2020-01-03,NaN,120,100,115,1500\n",
    HEAD + FIRST + b"2020-01-03,105,120,100,115,1.5\n",
    HEAD + FIRST + b"2020-01-03,105,120,100,115,-1\n",
    HEAD + FIRST + b"2020-01-03,105,120,100,115,\n",
])
def test_invalid_data(invalid):
    with pytest.raises(ValueError):
        parse_bars(invalid)
