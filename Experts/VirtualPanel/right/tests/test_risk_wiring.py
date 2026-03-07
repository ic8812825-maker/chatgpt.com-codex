from pathlib import Path

ROOT = Path("Experts/VirtualPanel/right")


def _read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_risk_config_fields_present():
    cfg = _read("ale/config/CALRiskConfig.mqh")

    for field in [
        "dd_max",
        "stress_limit",
        "dd_prob_limit",
        "global_margin_limit",
        "global_dd_sum_limit",
        "safe_alpha",
        "safe_beta",
        "safe_gamma",
        "safe_k",
    ]:
        assert field in cfg, f"Missing field {field} in CALRiskConfig"


def test_risk_engine_uses_configurable_thresholds():
    text = _read("ale/risk/CALRiskEngine.mqh")

    assert "SetConfig(const CALRiskConfig &cfg)" in text
    assert "m_cfg.dd_max" in text
    assert "m_cfg.stress_limit" in text
    assert "m_cfg.dd_prob_limit" in text


def test_engine_propagates_config_to_both_flows():
    text = _read("ale/core/CALEngine.mqh")

    assert "m_buy_stream.SetRiskConfig(m_cfg)" in text
    assert "m_sell_stream.SetRiskConfig(m_cfg)" in text
