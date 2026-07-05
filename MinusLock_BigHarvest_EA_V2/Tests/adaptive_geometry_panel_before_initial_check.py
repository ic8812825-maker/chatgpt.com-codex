from pathlib import Path
root = Path(__file__).resolve().parents[1]
main = (root / 'MinusLock_BigHarvest_EA.mq5').read_text()
on_tick = main.split('void OnTick()', 1)[1]
assert on_tick.index('UpdateGeometryPanel();') < on_tick.index('if(State == STATE_IDLE && managedPositions == 0)')
assert 'BIG_MOVE_LEVELS_WAITING_ATR' in main
print('ADAPTIVE_GEOMETRY_PANEL_BEFORE_INITIAL_CHECK PASS')
