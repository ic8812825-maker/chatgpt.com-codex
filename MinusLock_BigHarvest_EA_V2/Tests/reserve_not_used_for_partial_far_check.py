from pathlib import Path
root = Path(__file__).resolve().parents[1]
state = (root / 'Include' / 'StateMachine.mqh').read_text()
close_far = state[state.index('void ProcessBigHarvestCloseFar()'):state.index('void ProcessBigHarvestCheckFinal()')]
partial_branch = close_far.split('datetime partialCloseStartTime = TimeCurrent();', 1)[1]
check_final = state[state.index('void ProcessBigHarvestCheckFinal()'):state.index('void ProcessSmallCloseSmall()')]
assert 'ApplyReserveCredit' not in close_far
assert 'ApplyReserveDebit' not in partial_branch
assert 'Ctx.totalReserve' not in partial_branch
assert 'Ctx.pendingCloseFarLot' in close_far
assert 'ReserveUsedForPartial=NO' in close_far
assert 'ApplyReserveCredit(RESERVE_EVENT_BIG_HARVEST_ADD, Ctx.pendingReserveAdd);' in check_final
assert 'ProjectedRecoveryPLAfterFinalClose' in check_final
assert check_final.index('ApplyReserveCredit') < check_final.index('ProjectedRecoveryPLAfterFinalClose')
print('RESERVE_NOT_USED_FOR_PARTIAL_FAR_CHECK PASS')
