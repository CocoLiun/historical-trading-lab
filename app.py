"""Single-asset historical replay UI with SQLite persistence and optional personal-use sample data."""
import hashlib
from decimal import Decimal
import pandas as pd
import streamlit as st
from data_loader import parse_bars
from engine import Account, maximum_drawdown
from market_data import download_default_spy
import storage
from i18n import translate

st.set_page_config(page_title="Historical Trading Lab", layout="wide")
language = st.sidebar.selectbox("语言 / Language", ["中文", "English"], key="language")
def t(text):
    return translate(text, language)

def display_table(records):
    frame = pd.DataFrame(records)
    if "side" in frame:
        frame["side"] = frame["side"].map(lambda value: t("买入") if value == "buy" else t("卖出"))
    if "decision" in frame:
        frame["decision"] = frame["decision"].map(lambda value: str(value).replace("buy", t("买入")).replace("sell", t("卖出")))
    return frame.rename(columns={key: t(label) for key, label in {"date":"日期", "side":"交易方向", "qty":"数量", "price":"成交价", "fee":"手续费", "note":"笔记", "decision":"决策"}.items()})

storage.initialize()
st.title("📈 历史行情交易实验室" if language == "中文" else "📈 Historical Trading Lab")
st.info(t("无需准备报表，直接下载行情就能开始。"))
st.write(t("① 选择数据 → ② 每天决定买入、卖出或跳过 → ③ 查看收益和笔记。操作后自动保存，下次选择账户即可继续。"))
st.caption(t("历史行情回放 · 收盘后决策 · 下一交易日开盘模拟成交 · 教学用途"))
st.warning(t("仅供学习。当前为单资产日线模型；未实现完整交易所规则、公司行动和订单簿撮合。"))
st.sidebar.caption(t("账户管理"))
existing_sessions = storage.list_sessions()
selected_session = st.sidebar.selectbox(t("恢复已有练习"), [t("新建 / 输入名称")] + existing_sessions)
session_name = st.sidebar.text_input(t("模拟账户名称（用于保存和恢复）"), value=selected_session if selected_session in existing_sessions else "my-practice").strip()
if not session_name.strip():
    st.stop()

saved = storage.load_session(session_name)
saved_fingerprint = saved.get("fingerprint") if saved else None

st.subheader(t("获取一份默认练习行情"))
st.caption(t("默认标的：SPY（美国上市的标普500 ETF），最近约 5 年日线。点击后从 Yahoo Finance 获取，并保存到你这台 Mac 的 SQLite；不会把行情文件提交到 GitHub。仅供个人学习，数据使用受 Yahoo 条款约束。"))
if saved_fingerprint:
    st.success(t("已有行情已就绪，可直接向下开始练习。"))
if st.button(t("下载 SPY 默认练习数据（约 5 年）"), type="primary"):
    with st.spinner(t("正在获取历史行情…")):
        try:
            downloaded = download_default_spy("5y")
            parse_bars(downloaded)
            fp = hashlib.sha256(downloaded).hexdigest()
            storage.save_dataset(fp, "SPY_5y_yahoo_personal_use.csv", downloaded)
            st.session_state[f"selected_dataset_fingerprint_{session_name}"] = fp
            st.success(t("已下载并保存到本机 SQLite。"))
        except Exception as exc:
            st.error(t("下载失败，请检查网络后重试。") + f" ({exc})")

with st.expander(t("上传自己的 CSV（可选）")):
    uploaded = st.file_uploader(t("或者上传自己的历史日线 CSV：date,open,high,low,close,volume"), type="csv")
raw = uploaded.getvalue() if uploaded else None
filename = uploaded.name if uploaded else None
if raw:
    fingerprint = hashlib.sha256(raw).hexdigest()

else:
    fingerprint = st.session_state.get(f"selected_dataset_fingerprint_{session_name}") or saved_fingerprint
    stored = storage.load_dataset(fingerprint) if fingerprint else None
    if stored:
        filename, raw = stored
if raw is not None and saved_fingerprint and fingerprint != saved_fingerprint:
    st.warning(t("此数据与当前练习不同。替换会清空该练习的进度；也可以输入新账户名称另建练习。"))
    if not st.checkbox(t("确认替换当前练习的数据并清空进度"), key=f"replace_{session_name}_{fingerprint}"):
        st.stop()
if raw is None:
    st.info(t("先点击上方按钮获取默认 SPY 行情，或者上传自己的 CSV。"))
    st.stop()
@st.cache_data(show_spinner=False)
def cached_bars(content):
    return parse_bars(content)

try:
    bars = cached_bars(raw)
except Exception as exc:
    st.error(t("数据导入失败，请检查 CSV 格式。") + f" ({exc})")
    st.stop()

storage.save_dataset(fingerprint, filename or "prices.csv", raw)

if saved and saved.get("fingerprint") == fingerprint:
    idx = min(int(saved.get("idx", 0)), len(bars)-1)
    account = Account(Decimal(saved.get("cash", "100000")), int(saved.get("shares", 0)), saved.get("trades", []))
    equity_history = saved.get("equity", [])
    notes = saved.get("notes", [])
else:
    idx, account, equity_history, notes = 0, Account(), [], []

def persist():
    storage.save_session(session_name.strip(), {
        "market": market, "fingerprint": fingerprint, "idx": st.session_state.idx,
        "cash": str(st.session_state.account.cash), "shares": st.session_state.account.shares,
        "trades": st.session_state.account.trades, "equity": st.session_state.equity,
        "notes": st.session_state.notes
    })

if st.session_state.get("active_session") != session_name.strip() or st.session_state.get("active_fingerprint") != fingerprint:
    st.session_state.active_session = session_name.strip()
    st.session_state.active_fingerprint = fingerprint
    st.session_state.idx = idx
    st.session_state.account = account
    st.session_state.equity = equity_history
    st.session_state.notes = notes

market = st.selectbox(t("交易模式"), ["generic", "a_share"], index=1 if saved and saved.get("market") == "a_share" else 0,
    format_func=lambda x: t("通用模式") if x == "generic" else t("A 股基础规则（买入100股整数倍、T+1）"))
st.caption(t("A 股基础模式未模拟板块涨跌停、历史制度变化和公司行动；切换模式会在下次保存时记录。"))
i = st.session_state.idx
account = st.session_state.account
today = bars[i]
st.subheader(t("第 2 步 · 看行情，做决策"))
st.write(f"{today.day} · " + t("收盘后决策"))
st.progress((i + 1) / len(bars), text=f"{i + 1} / {len(bars)}")
a,b,c = st.columns(3)
a.metric(t("现金"), f"{account.cash:,.2f}")
b.metric(t("持仓"), account.shares)
c.metric(t("估算总资产"), f"{account.equity(today.close):,.2f}")
st.line_chart(pd.DataFrame({"date":[x.day for x in bars[:i+1]],t("收盘价"):[float(x.close) for x in bars[:i+1]]}).set_index("date"))
st.caption(t("只展示当前模拟日及之前行情；下单按下一交易日开盘价加假设滑点成交。"))
with st.form("place_order"):
    side = st.selectbox(t("交易方向"), ["buy","sell"], format_func=lambda value: t("买入") if value == "buy" else t("卖出"))
    qty = st.number_input(t("数量（尚未应用各市场整手限制）"), min_value=1, value=10, step=1)
    note = st.text_input(t("决策理由（可选）"))
    submit = st.form_submit_button(t("下单并推进一个交易日"), disabled=i >= len(bars)-1)
    if submit:
        try:
            trade = account.execute_next_open(bars[i+1], side, int(qty), decision_date=today.day, market=market)
            st.session_state.idx += 1
            st.session_state.notes.append({"date":today.day.isoformat(),"note":note,"decision":f"{side} {qty}"})
            st.session_state.equity.append({"date":bars[i+1].day.isoformat(),"equity":str(account.equity(bars[i+1].close))})
            persist()
            st.success(t("订单已成交"))
            st.rerun()
        except ValueError as exc:
            st.error(t("订单被拒绝，时间不会推进：") + t(str(exc)))
if st.button(t("跳过一个交易日"), disabled=i >= len(bars)-1):
    st.session_state.idx += 1
    st.session_state.equity.append({"date":bars[i+1].day.isoformat(),"equity":str(account.equity(bars[i+1].close))})
    persist()
    st.rerun()
st.subheader(t("第 3 步 · 查看收益与复盘"))
if i >= len(bars)-1:
    st.info(t("已到最后一个交易日，可查看复盘或重置练习。"))
initial_equity = Decimal("100000")
current_equity = account.equity(today.close)
benchmark_equity = initial_equity * today.close / bars[0].close
r1, r2, r3 = st.columns(3)
r1.metric(t("累计收益"), f"{(current_equity / initial_equity - 1) * 100:.2f}%")
r2.metric(t("买入持有基准（不计费用，可分股）"), f"{(benchmark_equity / initial_equity - 1) * 100:.2f}%")
r3.metric(t("相对基准收益（百分点）"), f"{(current_equity - benchmark_equity) / initial_equity * 100:.2f}")
st.subheader(t("交易流水"))
st.dataframe(display_table(account.trades), use_container_width=True)
if st.session_state.equity:
    values = [Decimal("100000")] + [Decimal(x["equity"]) for x in st.session_state.equity]
    st.metric(t("最大回撤"), f"{maximum_drawdown(values)*100:.2f}%")
    close_by_date = {bar.day.isoformat(): bar.close for bar in bars[:i+1]}
    comparison = [{"date": bars[0].day.isoformat(), t("账户"): float(initial_equity), t("买入持有"): float(initial_equity)}]
    comparison += [{"date": x["date"], t("账户"): float(x["equity"]), t("买入持有"): float(initial_equity * close_by_date[x["date"]] / bars[0].close)} for x in st.session_state.equity]
    st.line_chart(pd.DataFrame(comparison).set_index("date"))
    daily = pd.DataFrame(comparison).set_index("date")
    daily[t("每日盈亏")] = daily[t("账户")].diff().fillna(0)
    st.dataframe(daily, use_container_width=True)
st.subheader(t("决策笔记"))
st.dataframe(display_table(st.session_state.notes), use_container_width=True)
if st.button(t("重置当前模拟账户")):
    st.session_state.idx = 0
    st.session_state.account = Account()
    st.session_state.equity = []
    st.session_state.notes = []
    persist()
    st.rerun()
