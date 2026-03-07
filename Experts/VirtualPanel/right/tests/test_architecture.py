from pathlib import Path

ROOT = Path("Experts/VirtualPanel/right")


def _read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_separate_brains_wired_in_engine():
    text = _read("ale/core/CALEngine.mqh")

    assert "CALEngineBuy m_buy_brain" in text
    assert "CALEngineSell m_sell_brain" in text
    assert "CALEngineCommon m_common_brain" in text

    assert "m_buy_brain.OnPriceUpdate(price)" in text
    assert "m_sell_brain.OnPriceUpdate(price)" in text
    assert "m_common_brain.Aggregate(" in text


def test_ale_events_are_emitted_for_buy_sell_and_common():
    text = _read("ale/core/CALEngine.mqh")

    assert "OnStateChangeBuy" in text
    assert "OnStateChangeSell" in text
    assert "OnStateChangeCommon" in text
    assert "OnSAFETriggered" in text
    assert "OnDrawdownExceeded" in text
