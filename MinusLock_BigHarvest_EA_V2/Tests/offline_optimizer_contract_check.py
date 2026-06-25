from pathlib import Path
root = Path(__file__).resolve().parents[1]
optimizer = (root / "Tools" / "offline_optimizer.py").read_text()
scenarios = (root / "Tools" / "offline_scenarios.py").read_text()
score = (root / "Tools" / "score_parameters.py").read_text()
report = (root / "Best_Parameters.md").read_text()
for token in [
    "RecoveryPL = FinalBalance - CycleStartBalance",
    "BigRatio² × RemainBigOnSmall < 1",
    "BROAD_DEFAULT_RUNS = 100_000",
    "LOCAL_DEFAULT_RUNS = 10_000",
    "REJECTED_FINAL_RANK",
    "StabilityScore",
    "RobustnessScore",
    "FinalRank",
    "IsSelectableForSetFile",
    "build_local_params",
    "write_selected_set_files",
    "validate_params",
    "simulate_scenario",
    "STOP_MAX_LEVELS",
    "STATE_CLOSED_RECOVERY_LOSS",
]:
    assert token in optimizer + report, token
for name in ["A_BIG_WINS", "B_SMALL_WINS", "C_ALTERNATING", "D_FALSE_REVERSE", "E_ADVERSE_TREND", "F_MAX_LEVELS", "G_WORST_CASE"]:
    assert name in scenarios, name
for token in ["REJECTED_SCORE_PENALTY", "stop_max_levels_penalty", "recovery_loss_penalty", "CompressionViolationCount", "REJECTED_STOP_MAX_LEVELS"]:
    assert token in score + optimizer, token
print("OFFLINE_OPTIMIZER_CONTRACT_CHECK PASS")
