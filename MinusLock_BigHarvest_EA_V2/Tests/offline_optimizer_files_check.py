from pathlib import Path
root = Path(__file__).resolve().parents[1]
for rel in [
    "Tools/offline_optimizer.py",
    "Tools/offline_scenarios.py",
    "Tools/score_parameters.py",
    "Tools/generate_set_files.py",
    "Optimization_Report.csv",
    "Best_Parameters.md",
    "Sets/USDJPY_M30_SAFE.set",
    "Sets/USDJPY_M30_BALANCED.set",
    "Sets/USDJPY_M30_LOWLOT_SAFE.set",
]:
    assert (root / rel).exists(), rel
assert (root / "Sets" / "USDJPY_M30_AGGRESSIVE.set").exists() or (root / "Sets" / "USDJPY_M30_AGGRESSIVE_NOT_FOUND.txt").exists()
print("OFFLINE_OPTIMIZER_FILES_CHECK PASS")
