"""Personal-learning convenience downloader; fetched data is stored locally, not bundled."""
from io import StringIO
import pandas as pd

def history_frame_to_csv(frame):
    if frame is None or frame.empty:
        raise ValueError("数据源没有返回行情，请稍后重试")
    required = {"Open", "High", "Low", "Close", "Volume"}
    if not required.issubset(set(frame.columns)):
        raise ValueError("数据源返回的字段不完整")
    out = frame.reset_index()
    date_col = "Date" if "Date" in out.columns else "Datetime" if "Datetime" in out.columns else out.columns[0]
    out = out.rename(columns={date_col:"date", "Open":"open", "High":"high", "Low":"low", "Close":"close", "Volume":"volume"})
    out = out[["date","open","high","low","close","volume"]].dropna()
    out["date"] = pd.to_datetime(out["date"]).dt.strftime("%Y-%m-%d")
    out["volume"] = pd.to_numeric(out["volume"], errors="raise").astype("int64")
    return out.to_csv(index=False).encode("utf-8")

def download_default_spy(period="5y"):
    try:
        import yfinance as yf
        frame = yf.Ticker("SPY").history(period=period, interval="1d", auto_adjust=False, actions=False)
    except Exception as exc:
        raise RuntimeError(f"下载失败：{exc}") from exc
    return history_frame_to_csv(frame)
