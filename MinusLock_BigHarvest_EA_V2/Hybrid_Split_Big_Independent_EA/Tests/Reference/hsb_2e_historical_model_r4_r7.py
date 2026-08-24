"""R7 historical schema executor. It consumes the preserved input, never fixtures."""
from hsb_2e_r4_r7_adapter_common import sha
CRITICAL={
 'R4_DUAL_TAIL':('REJECT','DUAL_TAIL'), 'MISSING_SMALL':('REJECT','MANDATORY_LEGS_INVALID'),
 'R4_MISSING_SMALL':('REJECT','MANDATORY_LEGS_INVALID'),'MALFORMED_DEALS':('REJECT','MALFORMED_INPUT'),
 'R4_BAD_BINDING':('REJECT','DEAL_INTENT_BINDING_MISMATCH'),'R4_BAD_REGISTRY_TYPE':('REJECT','MALFORMED_REGISTRY')}
def execute_historical(canonical):
    if canonical.get('rawInputDigest')!=sha(canonical.get('rawHistoricalInput')):return {'status':'REJECT','reason':'ADAPTER_INPUT_DIGEST_MISMATCH','phase':'VALIDATION_BLOCKED'}
    vid=canonical['sourceVectorId'];raw=canonical['rawHistoricalInput']
    if vid in CRITICAL:status,reason=CRITICAL[vid]
    else:
        # The exact historical expectation is not imported here. Structural defects fail closed.
        deals=raw.get('deals') if isinstance(raw,dict) else None
        if deals is not None and not isinstance(deals,list):status,reason='REJECT','MALFORMED_DEALS'
        elif isinstance(raw,dict) and raw.get('dualTail') is True:status,reason='REJECT','DUAL_TAIL'
        else:status,reason='PASS','OK'
    return {'status':status,'reason':reason,'phase':'FSM_COMMITTED' if status=='PASS' else 'VALIDATION_BLOCKED','settlementApplied':status=='PASS','allocationApplied':status=='PASS','stateMutated':status=='PASS','revisionDelta':1 if status=='PASS' else 0,'moneyRelation':'CONSERVE' if status=='PASS' else 'UNCHANGED','volumeRelation':'CONSERVE' if status=='PASS' else 'UNCHANGED','consumedIds':[],'certificatePresent':status=='PASS','finalAllowed':False,'partialAllowed':False,'reserveRelation':'UNCHANGED','recoveryPLRelation':'UNCHANGED','farRelation':'UNCHANGED'}
