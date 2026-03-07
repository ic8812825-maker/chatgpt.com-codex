from pathlib import Path

ROOT = Path("Experts/VirtualPanel/right")


def _read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_dual_flow_streams_wired_in_engine():
    text = _read("ale/core/CALEngine.mqh")

    assert "CBuyEngine m_buy_stream" in text
    assert "CSellEngine m_sell_stream" in text

    assert "m_buy_stream.Init(ALE_FLOW_BUY)" in text
    assert "m_sell_stream.Init(ALE_FLOW_SELL)" in text

    assert "m_buy_stream.Process(price)" in text
    assert "m_sell_stream.Process(price)" in text


def test_ale_events_are_emitted_for_both_streams():
    text = _read("ale/core/CALEngine.mqh")

    assert "OnStateChangeBuy" in text
    assert "OnStateChangeSell" in text
    assert "OnSAFETriggered" in text
    assert "OnDrawdownExceeded" in text
