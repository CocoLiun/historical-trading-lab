from pathlib import Path
from streamlit.testing.v1 import AppTest
from storage import initialize, save_dataset, save_session, load_session
import hashlib


def test_restore_skip_reset(tmp_path, monkeypatch):
    monkeypatch.setenv("HTL_DB_PATH", str(tmp_path / "app.sqlite"))
    initialize()
    raw = b"date,open,high,low,close,volume\n2020-01-02,100,110,90,105,1000\n2020-01-03,105,120,100,115,1500\n"
    fingerprint = hashlib.sha256(raw).hexdigest()
    save_dataset(fingerprint, "prices.csv", raw)
    save_session("my-practice", {"fingerprint": fingerprint, "idx": 0})
    app = AppTest.from_file(str(Path(__file__).parents[1] / "app.py")).run()
    assert not app.exception
    next(b for b in app.button if b.label == "跳过一个交易日").click().run()
    assert not app.exception
    assert load_session("my-practice")["idx"] == 1
    assert all(b.disabled for b in app.button if b.label in ("下单并推进一个交易日", "跳过一个交易日"))
    restored = AppTest.from_file(str(Path(__file__).parents[1] / "app.py")).run()
    assert restored.session_state["idx"] == 1
    next(b for b in restored.button if b.label == "重置当前模拟账户").click().run()
    assert not restored.exception
    assert load_session("my-practice")["idx"] == 0


def test_first_run_download_language_and_buy(tmp_path, monkeypatch):
    import market_data
    monkeypatch.setenv("HTL_DB_PATH", str(tmp_path / "first.sqlite"))
    raw = b"date,open,high,low,close,volume\n2020-01-02,100,110,90,105,1000\n2020-01-03,105,120,100,115,1500\n"
    monkeypatch.setattr(market_data, "download_default_spy", lambda period: raw)
    app = AppTest.from_file(str(Path(__file__).parents[1] / "app.py")).run()
    assert not app.exception
    assert any("无需准备报表" in x.value for x in app.info)
    next(b for b in app.button if "下载 SPY" in b.label).click().run()
    assert not app.exception
    assert app.session_state["idx"] == 0
    app.selectbox(key="language").select("English").run()
    assert not app.exception
    assert app.session_state["idx"] == 0
    side = next(x for x in app.selectbox if x.label == "Order side")
    assert side.options == ["Buy", "Sell"]
    next(b for b in app.button if b.label == "Place order and advance one day").click().run()
    assert not app.exception
    assert load_session("my-practice")["shares"] == 10
    app.selectbox(key="language").select("中文").run()
    assert not app.exception
    assert app.session_state["account"].shares == 10


def test_download_failure_keeps_start_visible(tmp_path, monkeypatch):
    import market_data
    monkeypatch.setenv("HTL_DB_PATH", str(tmp_path / "failure.sqlite"))
    def fail(period):
        raise RuntimeError("offline")
    monkeypatch.setattr(market_data, "download_default_spy", fail)
    app = AppTest.from_file(str(Path(__file__).parents[1] / "app.py")).run()
    next(b for b in app.button if "下载 SPY" in b.label).click().run()
    assert not app.exception
    assert any("检查网络" in x.value for x in app.error)
    assert any("下载 SPY" in b.label for b in app.button)
