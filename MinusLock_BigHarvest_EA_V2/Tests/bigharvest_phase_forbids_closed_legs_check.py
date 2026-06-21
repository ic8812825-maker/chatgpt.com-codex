from pathlib import Path
engine = (Path(__file__).resolve().parents[1] / "Include" / "StateIntegrityEngine.mqh").read_text()
close_small = engine[engine.index("case STATE_BIG_HARVEST_CLOSE_SMALL:"):engine.index("case STATE_BIG_HARVEST_CALC_NET:")]
assert "forbidBig = true" in close_small
calc_net = engine[engine.index("case STATE_BIG_HARVEST_CALC_NET:"):engine.index("case STATE_SMALL_CLOSE_OLD_FAR:")]
assert "forbidBig = true" in calc_net
assert "forbidSmall = true" in calc_net
print("PASS bigharvest_phase_forbids_closed_legs_check")
