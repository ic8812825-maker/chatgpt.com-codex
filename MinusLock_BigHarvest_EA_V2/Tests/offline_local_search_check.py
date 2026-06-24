from pathlib import Path
root = Path(__file__).resolve().parents[1]
optimizer = (root / "Tools" / "offline_optimizer.py").read_text()
for token in ["--local-runs", "default=10000", "LEADER_ZONE_PARAMS", "BigRatio=1.15", "SmallRatio=0.35", "CloseBigOnSmall=0.35", "CloseFarShare=0.25"]:
    assert token in optimizer, token
for token in ["1.12", "1.13", "1.14", "1.15", "1.16", "1.17", "1.18", "0.30", "0.40"]:
    assert token in optimizer, token
print("OFFLINE_LOCAL_SEARCH_CHECK PASS")
