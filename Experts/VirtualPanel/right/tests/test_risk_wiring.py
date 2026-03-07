from pathlib import Path

ROOT = Path("Experts/VirtualPanel/right")


def _read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_risk_config_fields_present():
    cfg = _read("ale/config/CALRiskConfig.mqh")

    for field in [
        "MAX_DRAWDOWN",
        "STRESS_LIMIT",
        "DD_PROB_LIMIT",
        "GLOBAL_MARGIN_LIMIT",
        "GLOBAL_DD_SUM_LIMIT",
        "SAFE_ALPHA",
        "SAFE_BETA",
        "SAFE_GAMMA",
        "SAFE_K",
        "MAX_POSITIONS",
        "MIN_LOT",
        "ENABLE_STRICT_RUNTIME_CHECKS",
    ]:
        assert field in cfg, f"Missing field {field} in CALRiskConfig"


def test_risk_engine_uses_configurable_thresholds():
    text = _read("ale/risk/CALRiskEngine.mqh")

    assert "SetConfig(const CALRiskConfig &cfg)" in text
    assert "m_cfg.MAX_DRAWDOWN" in text
    assert "m_cfg.STRESS_LIMIT" in text
    assert "m_cfg.DD_PROB_LIMIT" in text


def test_engine_propagates_config_to_both_flows():
    text = _read("ale/core/CALEngine.mqh")

    assert "m_buy_stream.SetRiskConfig(m_cfg)" in text
    assert "m_sell_stream.SetRiskConfig(m_cfg)" in text
