from pathlib import Path
root=Path(__file__).resolve().parents[1]
config=(root/'Include'/'Config.mqh').read_text()
state=(root/'Include'/'StateMachine.mqh').read_text()
money=(root/'Include'/'BrokerMoneyModel.mqh').read_text()
assert 'CommissionPerLotPerSide' in config
assert 'CommissionPerLotRoundTurn' in config
assert 'CommissionFixedPerDeal' in config
assert 'CommissionPercent' in config
assert 'result.estimatedCommission = money.closeCommission' in state
assert 'result.projectedNet = money.netMoney;' in state
assert 'CalcProjectedCloseNetMoneyWithAccrued' in state
assert 'COMMISSION_MODE_CONFLICT' in money
assert 'grossAbs*CommissionPercent' not in money
assert 'COMMISSION_PERCENT_MARGIN' in money
assert 'profit + swapPart - result.estimatedCommission - SafetyBufferMoney' not in state
print('PASS: Far projection uses the unified commission and account-currency money model.')
