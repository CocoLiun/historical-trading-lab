"""Single-asset historical replay UI."""
import hashlib
from decimal import Decimal
import pandas as pd
import streamlit as st
from data_loader import parse_bars
from engine import Account, maximum_drawdown

st.set_page_config(page_title="Historical Trading Lab", layout="wide")
st.title("📈 Historical Trading Lab")
st.caption("历史行情回放 · 收盘后决策 · 下一交易日开盘模拟成交 · 教学用途")
st.warning("请上传真实历史日线 OHLCV CSV。不提供随机价格、实时行情或券商交易；目前仅为单资产教学模型。")
file = st.file_uploader("上传 CSV：date,open,high,low,close,volume", type="csv")
if file is None:
    st.info("数据建议使用未复权价格；当前尚未处理分红和拆股。")
    st.stop()
try:
    raw = file.getvalue()
    bars = parse_bars(raw)
except Exception as exc:
    st.error(f"数据导入失败：{exc}")
    st.stop()

fingerprint = hashlib.sha256(raw).hexdigest()
if st.session_state.get("dataset") != fingerprint:
    st.session_state.dataset = fingerprint
    st.session_state.idx = 0
    st.session_state.account = Account()
    st.session_state.equity = []
    st.session_state.notes = []
i = st.session_state.idx
account = st.session_state.account
visible = bars[:i + 1]
today = bars[i]
st.subheader(f"当前决策日：{today.day} 收盘后")
a, b, c = st.columns(3)
a.metric("现金", f"{account.cash:,.2f}")
b.metric("持仓", account.shares)
c.metric("估算总资产", f"{account.equity(today.close):,.2f}")
st.line_chart(pd.DataFrame({"date": [x.day for x in visible], "close": [float(x.close) for x in visible]}).set_index("date"))
st.caption("当前图表不会显示未来日线；订单按下一交易日开盘价加上假设滑点成交。")
with st.form("place_order"):
    side = st.selectbox("交易方向", ["buy", "sell"])
    qty = st.number_input("交易数量（不含市场整手限制）", min_value=1, value=10, step=1)
    note = st.text_input("决策理由（可选）")
    submit = st.form_submit_button("下单并推进一个交易日", disabled=i >= len(bars)-1)
    if submit:
        try:
            trade = account.execute_next_open(bars[i+1], side, int(qty), decision_date=today.day)
            st.session_state.idx += 1
            st.session_state.notes.append({"date": today.day.isoformat(), "note": note, "decision": f"{side} {qty}"})
            st.session_state.equity.append({"date": bars[i+1].day, "equity": account.equity(bars[i+1].close)})
            st.success(f"成交：{trade}")
            st.rerun()
        except ValueError as exc:
            st.error(f"订单被拒绝：{exc}（时间不会推进）")
if st.button("跳过一个交易日", disabled=i >= len(bars)-1):
    st.session_state.idx += 1
    st.session_state.equity.append({"date": bars[i+1].day, "equity": account.equity(bars[i+1].close)})
    st.rerun()
st.subheader("交易流水")
st.dataframe(pd.DataFrame(account.trades), use_container_width=True)
if st.session_state.equity:
    equity = [Decimal("100000")] + [e["equity"] for e in st.session_state.equity]
    st.metric("最大回撤", f"{maximum_drawdown(equity)*100:.2f}%")
    st.line_chart(pd.DataFrame([{"date": e["date"], "equity": float(e["equity"])} for e in st.session_state.equity]).set_index("date"))
st.subheader("决策笔记")
st.dataframe(pd.DataFrame(st.session_state.notes), use_container_width=True)
if st.button("重置模拟"):
    st.session_state.dataset = None
    st.rerun()
