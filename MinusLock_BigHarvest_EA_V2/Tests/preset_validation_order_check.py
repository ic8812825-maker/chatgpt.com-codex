from pathlib import Path
main = (Path(__file__).resolve().parents[1] / "MinusLock_BigHarvest_EA.mq5").read_text()
oninit = main.split("int OnInit()", 1)[1]
assert oninit.index("ConfigureWorkingParameters();") < oninit.index("ValidateInputs()") < oninit.index("ValidateWorkingParameters()")
assert "ValidateRiskCompression(BigRatio, WorkRemainBigOnSmall" in main
assert "ValidateRiskCompression(BigRatio, RemainBigOnSmall" not in main
print("PRESET_VALIDATION_ORDER_CHECK PASS")
