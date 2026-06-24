from pathlib import Path
root = Path(__file__).resolve().parents[1]
report = (root / "Best_Parameters.md").read_text()
for category in ["SAFE", "BALANCED", "AGGRESSIVE", "LOWLOT_SAFE"]:
    marker = f"### {category}"
    section = report.split(marker, 1)[1].split("### ", 1)[0]
    set_path = root / "Sets" / f"USDJPY_M30_{category}.set"
    if set_path.exists():
        assert "Verdict=ACCEPT" in section, category
        assert "IsSelectableForSetFile=YES" in section, category
    else:
        assert f"{category}_NOT_FOUND" in section, category
print("OFFLINE_SET_ACCEPT_ONLY_CHECK PASS")
