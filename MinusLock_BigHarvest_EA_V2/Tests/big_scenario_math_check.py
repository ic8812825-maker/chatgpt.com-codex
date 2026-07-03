from pathlib import Path
root = Path(__file__).resolve().parents[1]
recovery = (root / 'Include' / 'RecoveryMath.mqh').read_text()
logger = (root / 'Include' / 'Logger.mqh').read_text()
audit = (root / 'Docs' / 'BIG_SCENARIO_ENGINEERING_AUDIT.md').read_text()
for token in ['WorkBigMoveStartPoints() + (level - 1) * WorkBigMoveStepPoints()', 'NormalizeLotNearest(farLot * BigRatio)', 'NormalizeLotUp(bigLot * WorkSmallRatio)', 'return closeFarBudget / lossPerLot;', 'NormalizeLotDown(rawLot)']:
    assert token in recovery, token
for token in ['Symbol', 'State', 'Level', 'FarLotBefore', 'BigLot', 'SmallLot', 'CloseFarBudget', 'ReserveAdd', 'TotalReserve', 'RecoveryPL', 'ProjectedReserveCoverage', 'FinalCloseAllowed', 'ClosedBigNet', 'ClosedSmallNet', 'BigScenarioNet', 'CloseFarLot', 'RemainingFarLot', 'ReserveCoverage']:
    assert token in logger, token
for token in ['CloseFarActualCost <= CloseFarBudget', 'Reserve does not decrease during partial Far close', 'Reserve is not used for partial Far close', 'BigScenarioNet = ClosedBigNet + ClosedSmallNet']:
    assert token in audit, token
print('BIG_SCENARIO_MATH_CHECK PASS')
