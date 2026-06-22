from pathlib import Path
engine = (Path(__file__).resolve().parents[1] / 'Include' / 'PositionResolutionEngine.mqh').read_text()
assert 'POSITION_RESOLUTION_BY_TIME' in engine
assert 'positionTime >= openStartTime' in engine
assert 'positionTime <= maxOpenTime' in engine
assert 'PositionResolutionDirectionMatches(candidate.direction, direction)' in engine
assert 'PositionResolutionLotMatches(candidate.lot, expectedLot)' in engine
print('position_resolution_time_window_check PASS')
