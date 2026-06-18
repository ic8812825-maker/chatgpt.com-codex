from pathlib import Path
text = (Path(__file__).resolve().parents[1] / "Include" / "StateMachine.mqh").read_text()
assert "Ctx.smallScenarioRealBefore = Ctx.realCyclePL" in text
assert "Ctx.smallScenarioRealAfter = Ctx.realCyclePL" in text
assert "smallScenarioRealNet = Ctx.smallScenarioRealAfter - Ctx.smallScenarioRealBefore" in text
assert "Ctx.realCyclePL - totalReserveBefore" not in text
print("SMALL_REAL_NET_CHECK PASS")
