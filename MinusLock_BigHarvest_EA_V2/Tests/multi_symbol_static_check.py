from pathlib import Path
root = Path(__file__).resolve().parents[1]
config = (root / 'Include' / 'Config.mqh').read_text()
pos = (root / 'Include' / 'PositionUtils.mqh').read_text()
risk = (root / 'Include' / 'RiskManager.mqh').read_text()
state = (root / 'Include' / 'StateMachine.mqh').read_text()
logger = (root / 'Include' / 'Logger.mqh').read_text()
trade = (root / 'Include' / 'TradeEngine.mqh').read_text()
recon = (root / 'Include' / 'ReconciliationEngine.mqh').read_text()
sets = ''.join(p.read_text() for p in (root / 'Sets').glob('*.set'))
manual = (root / 'Docs' / 'MANUAL.md').read_text()
test_plan = (root / 'Docs' / 'TEST_PLAN.md').read_text()

for token in ['input double MaxAccountMarginPercent', 'input int    MaxActiveSymbols']:
    assert token in config, token
assert 'PositionGetString(POSITION_SYMBOL) == _Symbol' in pos
assert '(ulong)PositionGetInteger(POSITION_MAGIC) == MagicNumber' in pos
assert 'int CountActiveManagedSymbols()' in pos
assert 'CurrentSymbolHasManagedPositions()' in pos
assert 'MaxAccountMarginPercent' in risk and 'MaxActiveSymbols' in risk
assert 'activeSymbols >= MaxActiveSymbols' in risk
assert 'MinusLock_%s_%I64u_%s' in state
assert 'CycleMathCsvFileName()' in logger and 'MinusLock_CycleMath_%s.csv' in logger
assert 'SymbolLogPrefix()' in logger and '[BigHarvest][%s]' in logger
assert 'IsManagedPositionForCurrentSymbol()' in trade
assert 'DEAL_SYMBOL' in recon and 'DEAL_MAGIC' in recon
assert 'MaxAccountMarginPercent=60' in sets and 'MaxActiveSymbols=10' in sets
assert 'Multi-Symbol / Multi-Currency operation' in manual
assert 'Multi-Symbol / Multi-Currency isolation' in test_plan
print('MULTI_SYMBOL_STATIC_CHECK PASS')
