# 📈 Historical Trading Lab / 历史行情交易实验室

**在不知道未来行情的前提下，使用真实历史数据练习投资决策。**

## Run locally
Python 3.10+:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
python -m pytest -q
```

## Default practice data
The app offers a one-click download of approximately five years of daily SPY ETF OHLCV history through yfinance/Yahoo Finance. It is fetched on demand and saved to the user's local SQLite database; **no market-data file is committed to this repository or redistributed**. Yahoo Finance data is for personal use subject to Yahoo's terms; yfinance is unofficial and not affiliated with Yahoo. See https://ranaroussi.github.io/yfinance/ and Yahoo's terms. The download can fail due to provider/network/rate limits.

SPY is an ETF tracking the S&P 500, not the index itself. This convenience sample is not an official exchange feed and does not include a complete corporate-action accounting model. Use it for learning the UI and basic replay only.

## Persistence
- SQLite stores named practice sessions, trades, notes, equity history and downloaded/uploaded CSV datasets.
- Default DB: `data/historical_trading_lab.sqlite3`; override with `HTL_DB_PATH`.
- Local SQLite survives app restarts. Back up the DB file; do not commit private data.
- Cloud Tunnel exposes the local app; data stays on the Mac.
- Do not assume a hosted ephemeral disk is durable storage.

## Data
CSV columns: `date,open,high,low,close,volume`. The app does not fabricate prices.

## Model and limitations
- Single-asset daily replay: after day T close, orders fill at next bar open with assumed fixed slippage and fees.
- Past-only chart, cash/holdings, buy/sell, decision notes and drawdown.
- Not an order-book matching engine.
- Not yet implemented: exchange calendars, A-share T+1, lot sizes, price limits, suspensions, dividends, splits, delistings, tax, FX, volume constraints, mutual-fund NAV settlement, time-stamped historical fundamentals/news, benchmarks and strategy comparisons.
- Without corporate actions this is unsuitable for accurate long-run total-return studies.

Educational simulation only. No brokerage connection or investment advice.

## License
MIT source code; third-party data may have separate terms.
