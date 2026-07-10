from pathlib import Path
state = (Path(__file__).resolve().parents[1] / "Include" / "StateMachine.mqh").read_text()
assert "Ctx.pendingCloseFarBudget = bigSmallNet - Ctx.pendingReserveAdd" in state
assert "Ctx.pendingPartialFarBudgetAvailable = Ctx.pendingCloseFarBudget + Ctx.partialFarBudgetCarry" in state
assert "ReserveUsedForPartial=NO" in state
assert "PartialBudgetAvailable = Ctx.totalReserve" not in state
print("PASS: Partial Far budget excludes reserve and carries unused money.")
