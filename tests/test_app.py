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
