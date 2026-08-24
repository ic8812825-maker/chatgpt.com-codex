"""Exact, case-ID-addressed R5 false-pass fixture migration to canonical R6."""
import copy
from dataclasses import replace
from hsb_2e_test_fixtures_r4_r6 import broker_fixture
from hsb_2e_provenance_model_r4_r6 import *
from hsb_2e_reference_model_r4_r6 import HSBI_SettlementCommitCertificate

def adapt(case):
    cid=case['CASE_ID'];exact=case['exactInput']
    scenario=exact.get('scenario','BIG');x=broker_fixture(scenario)
    if cid=='FP-R6-001':
        p=x['positions'][0];r=x['dealRecords'][0];orphan=replace(r,dealId='ORPHAN',eventId='ORPHAN-E',positionTicket=999,positionRole='UNKNOWN',intentId='MISSING',recordDigest='').sealed();x['dealRecords'].append(orphan)
    elif cid=='FP-R6-002':x['dealRecords'][0]=replace(x['dealRecords'][0],positionRole='FAR',recordDigest='').sealed()
    elif cid=='FP-R6-003':x['dealRecords'][0]=replace(x['dealRecords'][0],price=D('99999'),recordDigest='').sealed()
    elif cid=='FP-R6-004':
        first=replace(x['dealRecords'][0],volume=D('.5'),recordDigest='').sealed();bad=replace(first,recordDigest='CORRUPTED');state=copy.deepcopy(x['persistedState']);state['acceptedDealRecords']=[bad];state.update(derive([bad],x['positions']));x['persistedState']=state;x['dealRecords']=[replace(first,dealId='SECOND',eventId='SECOND-E',recordDigest='').sealed()]
    elif cid=='FP-R6-005':
        x['dealRecords']=[];fake=HSBI_SettlementCommitCertificate(1,'FAKE','I','O',2,3,scenario,(),(),(),(),'B','F','BP','EP','A','P',D(0),D(0),'FSM',1900,2200).sealed();x['persistedState']['commitCertificate']=fake
    elif cid=='FP-R6-006':x['economicPolicy']=replace(x['economicPolicy'],closeFarShare=D(1),reserveShare=D(1),policyDigest='').sealed()
    # 007-010 are valid canonical executions; independent comparators inspect corrected economics.
    return {'adapterResult':'ADAPTED','caseId':cid,'exactInputSHA256':case['EXACT_INPUT_SHA256'],'canonicalInput':x,'requiredR6CheckId':case['EXPECTED_R6_CHECK_ID'],'fieldSource':'exactInput + normative R6 contract'}
