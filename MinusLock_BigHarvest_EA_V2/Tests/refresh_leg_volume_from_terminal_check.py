from pathlib import Path
root = Path(__file__).resolve().parents[1]
pos = (root / "Include" / "PositionUtils.mqh").read_text()
state = (root / "Include" / "StateMachine.mqh").read_text()
assert "bool RefreshLegVolumeFromTerminal" in pos
for token in ["ActualVolume", "NormalizedVolume", "targetLot = normalizedVolume", "RefreshFarVolumeFromTerminal", "RefreshBigVolumeFromTerminal", "RefreshSmallVolumeFromTerminal"]:
    assert token in pos + state
assert "RefreshFarVolumeFromTerminal(\"BIG_HARVEST_CLOSE_FAR partial close\")" in state
print("REFRESH_LEG_VOLUME_FROM_TERMINAL_CHECK PASS")
