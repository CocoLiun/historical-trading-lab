from storage import initialize, save_dataset, load_dataset, save_session, load_session, list_sessions

def test_dataset_roundtrip(tmp_path, monkeypatch):
    monkeypatch.setenv("HTL_DB_PATH", str(tmp_path / "test.sqlite"))
    initialize()
    save_dataset("abc", "prices.csv", b"date,close\n")
    assert load_dataset("abc") == ("prices.csv", b"date,close\n")

def test_session_roundtrip(tmp_path, monkeypatch):
    monkeypatch.setenv("HTL_DB_PATH", str(tmp_path / "test.sqlite"))
    initialize()
    state = {"idx": 3, "cash": "1000", "trades": []}
    save_session("practice", state)
    assert load_session("practice") == state
    assert "practice" in list_sessions()
