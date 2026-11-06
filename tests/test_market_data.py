import pandas as pd
from market_data import history_frame_to_csv

def test_history_frame_normalizes_columns():
    frame = pd.DataFrame({
        "Open":[100.0,101.0], "High":[102.0,103.0],
        "Low":[99.0,100.0], "Close":[101.0,102.0],
        "Volume":[1000,1200]
    }, index=pd.to_datetime(["2024-01-02","2024-01-03"]))
    result = history_frame_to_csv(frame).decode()
    assert result.splitlines()[0] == "date,open,high,low,close,volume"
    assert "2024-01-02" in result

def test_history_frame_empty_rejected():
    import pytest
    with pytest.raises(ValueError):
        history_frame_to_csv(pd.DataFrame())
