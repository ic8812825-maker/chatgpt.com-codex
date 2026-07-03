from pathlib import Path
root = Path(__file__).resolve().parents[1]
pos = (root / 'Include' / 'PositionUtils.mqh').read_text()
trade = (root / 'Include' / 'TradeEngine.mqh').read_text()
state = (root / 'Include' / 'StateMachine.mqh').read_text()
logger = (root / 'Include' / 'Logger.mqh').read_text()
assert 'PositionGetString(POSITION_SYMBOL) != _Symbol' in pos
assert '(ulong)PositionGetInteger(POSITION_MAGIC) != MagicNumber' in pos
assert 'IsManagedPositionForCurrentSymbol()' in trade
assert 'HistoryDealGetString(dealTicket, DEAL_SYMBOL) != _Symbol' in state
assert '(ulong)HistoryDealGetInteger(dealTicket, DEAL_MAGIC) != MagicNumber' in state
assert 'CycleMathCsvFileName()' in logger
print('BIG_SCENARIO_MULTISYMBOL_GUARD_CHECK PASS')
