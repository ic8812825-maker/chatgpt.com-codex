from pathlib import Path
state=(Path(__file__).resolve().parents[1]/"Include"/"StateMachine.mqh").read_text()
assert "_Symbol" in state and "MagicNumber" in state and "Ctx.cycleId" in state
for token in ["Ctx.bigCoreIdentifier", "Ctx.bigTrendIdentifier", "Ctx.smallBaseIdentifier", "Ctx.reverseSmallIdentifier", "Ctx.farIdentifier"]:
    assert token in state, token
print("PASS symbol magic cycle isolation event key contains split identifiers")
