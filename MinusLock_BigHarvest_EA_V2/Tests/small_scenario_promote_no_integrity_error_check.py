from pathlib import Path
state = (Path(__file__).resolve().parents[1] / 'Include' / 'StateMachine.mqh').read_text()
body = state.split('void ProcessSmallBuildNewFar()', 1)[1].split('void ProcessSmallCheckReserve()', 1)[0]
assert 'PromoteRemainingBigToNewFar()' in body
assert 'SetState(STATE_SMALL_CHECK_RESERVE' in body
assert 'STATE_INTEGRITY_ERROR' not in body
print('small_scenario_promote_no_integrity_error_check PASS')
