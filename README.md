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

## Persistence
- SQLite stores named practice sessions, trades, notes, equity history and uploaded CSV datasets.
- Default DB: `data/historical_trading_lab.sqlite3`; override with `HTL_DB_PATH`.
- Local SQLite survives app restarts. Back up the DB file; do not commit private data.
- **Important cloud caveat:** Streamlit Community Cloud's local filesystem is not durable storage. SQLite on its ephemeral runtime disk is not a reliable cross-restart cloud database. For persistent hosted use, configure a managed database/object store (e.g. Supabase) in a later deployment step. Do not assume cloud data survives a reboot.

## Data
Upload user-supplied historical OHLCV CSV with columns `date,open,high,low,close,volume`. No random data is generated. Data is not bundled for licensing reasons.

## Model and limitations
- Single-asset daily replay: after day T close, orders fill at next bar open with assumed fixed slippage and fees.
- Past-only chart, cash/holdings, buy/sell, decision notes and drawdown.
- Index itself is not tradeable; use actual ETF prices for execution.
- Not an order-book matching engine.
- Not yet implemented: exchange calendars, A-share T+1, lot sizes, price limits, suspensions, dividends, splits, delistings, tax, FX, volume constraints, mutual-fund NAV settlement, time-stamped historical fundamentals/news, benchmarks and strategy comparisons.
- Without corporate actions this is unsuitable for accurate long-run total-return studies.

Educational simulation only. No brokerage connection or investment advice.

## License
MIT source code; third-party data may have separate terms.
