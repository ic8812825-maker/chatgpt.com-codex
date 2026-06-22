from pathlib import Path
root = Path(__file__).resolve().parents[1]
state = (root / 'Include' / 'StateMachine.mqh').read_text()
recon = (root / 'Include' / 'ReconciliationEngine.mqh').read_text()
assert 'bool TryRecoverPromotedBigAsFar(string reason)' in state
assert 'PROMOTED_BIG_AS_FAR_RECOVERED' in state
assert 'State = STATE_FAR_ACTIVE' in state
assert 'TryRecoverPromotedBigAsFar("RecoverState")' in state
assert 'TryRecoverPromotedBigAsFar("RunReconciliation")' in recon
print('recover_promoted_big_as_far_check PASS')
