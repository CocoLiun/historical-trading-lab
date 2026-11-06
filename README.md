# 📈 Historical Trading Lab / 历史行情交易实验室

**在不知道未来行情的前提下，使用真实历史数据练习投资决策。**

## Run
Python 3.10+:
```bash
pip install -r requirements.txt
streamlit run app.py
python -m pytest -q
```

Import user-supplied historical OHLCV CSV with columns `date,open,high,low,close,volume`. Data is not bundled for licensing reasons.

## Model
- Single-asset daily replay: after day T close, a simulated market order fills at the next bar open, with fixed proportional slippage and fees.
- Past-only close-price chart, cash/holdings, buy/sell, insufficient-funds rejection, decision notes and drawdown.
- Historical prices come from **uploaded observed data**, not generated random prices.
- An index itself is not tradeable: use actual ETF historical **unadjusted** prices for ETF execution, not the index's historical level.
- The fixed slippage model is *not* a real exchange order-book matching engine.
- Data provenance is user-managed; record source, ticker, exchange, currency, timezone, retrieval date, raw/adjusted policy, license.

## Limitations
Not yet implemented: exchange calendar, A-share T+1 sellability and board lots, price limits, suspensions, dividends, splits, delistings, tax, FX, volume constraints, mutual-fund NAV settlement, time-stamped historical fundamental/news publication, database persistence or benchmark returns. Streamlit session state is temporary. Without corporate actions the engine is unsuitable for accurate long-run total-return studies.

## Roadmap
1. P0 reliable data: provenance manifests, validated raw OHLCV, corporate actions, immutable snapshots.
2. P0 market rules: A-share, US/ETF, mutual-fund-specific settlement, order states, schedules, cost models.
3. P1 deterministic replay: versioned sessions, export, persistence, configurable starting cash.
4. P1 benchmarks, DCA, rebalancing, comparable cash flows and risk metrics.
5. P2 point-in-time financial and news data; guided lessons and explained replay.
6. P2 FastAPI, Vue 3 / TypeScript, PostgreSQL, Docker and e2e tests.

Educational simulation only. No brokerage connection or investment advice.

## License
MIT source code, third-party market data may carry separate terms.
