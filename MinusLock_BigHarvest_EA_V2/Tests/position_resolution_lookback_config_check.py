from pathlib import Path
root = Path(__file__).resolve().parents[1]
config = (root / 'Include' / 'Config.mqh').read_text()
engine = (root / 'Include' / 'PositionResolutionEngine.mqh').read_text()
assert 'input int    PositionResolutionLookbackSeconds = 10;' in config
assert 'PositionResolutionLookbackSeconds' in engine
assert 'openStartTime + PositionResolutionLookbackSeconds' in engine
print('position_resolution_lookback_config_check PASS')
