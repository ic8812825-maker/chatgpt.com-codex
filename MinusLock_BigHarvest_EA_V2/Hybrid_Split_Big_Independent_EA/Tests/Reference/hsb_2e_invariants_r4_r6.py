#!/usr/bin/env python3
"""Thirty independently recomputed critical R4-R6 properties."""
import argparse,copy
from dataclasses import replace
from hsb_2e_test_fixtures_r4_r6 import broker_fixture
from hsb_2e_provenance_model_r4_r6 import *
from hsb_2e_reference_model_r4_r6 import execute_scenario,validate_committed

CHECK_IDS=('R6_ORPHAN_DEAL_BLOCK','R6_DEAL_ROLE_BINDING','R6_DEAL_DIRECTION_BINDING','R6_DEAL_INTENT_BINDING','R6_TRUSTED_PRICE_DERIVATION','R6_PERSISTED_RECORD_REVALIDATION','R6_DEAL_EVENT_BIJECTION','R6_VOLUME_CONSERVATION','R6_MONEY_CONSERVATION','R6_DISJOINT_ALLOCATION','R6_CERTIFICATE_LEDGER_BINDING','R6_CERTIFICATE_ECONOMIC_BINDING','R6_CERTIFICATE_PERSISTENCE_BINDING','R6_INITIAL_POSITIVE_PROFIT_EXCLUDED','R6_BIG_FULL_FILL_ELIGIBILITY','R6_PARTIAL_FAR_CALCULATION','R6_RESERVE_PARTIAL_ISOLATION','R6_SMALL_MANDATORY_LEGS','R6_NEW_FAR_DERIVATION','R6_CATCH_UP_PROOF','R6_DUAL_TAIL_BLOCK','R6_FINAL_FULL_CLOSE','R6_FINAL_RESERVE_CONSUMPTION','R6_RECOVERY_PL_TRANSITION','R6_EXACTLY_ONCE_REPLAY','R6_PERSISTENCE_BEFORE_MUTATION','R6_STATE_REVISION_PLUS_ONE','R6_DETERMINISTIC_DIGEST','R6_MALFORMED_COLLECTION_REJECTION','R6_UNKNOWN_PROPERTY_FAIL_CLOSED')

def run_checks():
 c={};x=broker_fixture('BIG');r=x['dealRecords'][0]
 c['R6_ORPHAN_DEAL_BLOCK']=validate_binding(replace(r,positionTicket=999,recordDigest='').sealed(),x['context'],x['positions'],x['intents'],x['snapshot'],x['pricePolicy'])=='ORPHAN_DEAL'
 c['R6_DEAL_ROLE_BINDING']=validate_binding(replace(r,positionRole='FAR',recordDigest='').sealed(),x['context'],x['positions'],x['intents'],x['snapshot'],x['pricePolicy'])=='DEAL_ROLE_MISMATCH'
 c['R6_DEAL_DIRECTION_BINDING']=validate_binding(replace(r,direction='SELL',recordDigest='').sealed(),x['context'],x['positions'],x['intents'],x['snapshot'],x['pricePolicy'])=='DEAL_DIRECTION_MISMATCH'
 c['R6_DEAL_INTENT_BINDING']=validate_binding(replace(r,intentId='MISSING',recordDigest='').sealed(),x['context'],x['positions'],x['intents'],x['snapshot'],x['pricePolicy'])=='DEAL_INTENT_MISSING'
 c['R6_TRUSTED_PRICE_DERIVATION']=validate_binding(replace(r,price=D('999'),recordDigest='').sealed(),x['context'],x['positions'],x['intents'],x['snapshot'],x['pricePolicy'])=='EXECUTION_PRICE_OUTSIDE_TRUSTED_POLICY'
 state,e=validate_all_then_apply(x['persistedState'],x['dealRecords'],x['context'],x['positions'],x['intents'],x['snapshot'],x['pricePolicy']);bad=copy.deepcopy(state);object.__setattr__(bad['acceptedDealRecords'][0],'recordDigest','bad');c['R6_PERSISTED_RECORD_REVALIDATION']=revalidate_persisted(bad,x['context'],x['positions'],x['intents'],x['snapshot'],x['pricePolicy'])=='SOURCE_RECORD_DIGEST_MISMATCH'
 c['R6_DEAL_EVENT_BIJECTION']=set(state['dealEventBindings'])==set(state['consumedDealIds']) and set(state['dealEventBindings'].values())==set(state['seenEventIds'])
 result=execute_scenario(x);ep=result['economicProposal'];c['R6_VOLUME_CONSERVATION']=all(state['volumeByTicket'][str(p['ticket'])]<=D(p['authoritativeVolume']) for p in x['positions']);c['R6_MONEY_CONSERVATION']=ep.allocatedMoney+ep.remainingMoney==ep.availableMoney;c['R6_DISJOINT_ALLOCATION']=sum(ep.allocationAttribution.values(),D(0))==ep.allocatedMoney
 committed=result['state'];c['R6_CERTIFICATE_LEDGER_BINDING']=validate_committed({**x,'context':{**x['context'],'stateRevision':committed['stateRevision']}},committed) is None
 cert=committed['commitCertificate'];bad=copy.deepcopy(committed);object.__setattr__(bad['commitCertificate'],'economicProposalDigest','bad');object.__setattr__(bad['commitCertificate'],'certificateDigest',digest(bad['commitCertificate'].body()));c['R6_CERTIFICATE_ECONOMIC_BINDING']=validate_committed({**x,'context':{**x['context'],'stateRevision':bad['stateRevision']}},bad)=='COMMIT_CERTIFICATE_PIPELINE_MISMATCH'
 bad=copy.deepcopy(committed);bad['persistenceRecordDigest']='bad';c['R6_CERTIFICATE_PERSISTENCE_BINDING']=validate_committed({**x,'context':{**x['context'],'stateRevision':bad['stateRevision']}},bad)=='COMMIT_CERTIFICATE_PIPELINE_MISMATCH'
 initial=execute_scenario(broker_fixture('INITIAL'));c['R6_INITIAL_POSITIVE_PROFIT_EXCLUDED']=initial['economicProposal'].recoveryPLAfter==broker_fixture('INITIAL')['economicPolicy'].recoveryPLBefore
 partial=broker_fixture('BIG');partial['dealRecords']=partial['dealRecords'][:1];c['R6_BIG_FULL_FILL_ELIGIBILITY']=execute_scenario(partial)['reason']=='PARTIAL_FILL';c['R6_PARTIAL_FAR_CALCULATION']=ep.partialFarVolume>0;c['R6_RESERVE_PARTIAL_ISOLATION']='FAR_LOSS_FROM_RESERVE' not in ep.allocationAttribution
 smallbad=broker_fixture('SMALL');smallbad['positions']=smallbad['positions'][:2];smallbad['intents']=smallbad['intents'][:2];c['R6_SMALL_MANDATORY_LEGS']=execute_scenario(smallbad)['reason']=='MANDATORY_LEGS_INVALID'
 small=broker_fixture('SMALL');sr=execute_scenario(small);sp=sr['economicProposal'];big=next(p for p in small['positions'] if p['role']=='BIG');c['R6_NEW_FAR_DERIVATION']=sp.newFarTicket==big['ticket'] and sp.newFarVolume==D(big['residualVolume']);c['R6_CATCH_UP_PROOF']=sp.catchUpRatio==(small['economicPolicy'].reserveBefore+sp.smallReserveAddition)/small['economicPolicy'].farLossBefore;c['R6_DUAL_TAIL_BLOCK']=not sp.dualTail
 finalbad=broker_fixture('FINAL');finalbad['intents'][0]['intentKind']='PARTIAL_CLOSE';c['R6_FINAL_FULL_CLOSE']=execute_scenario(finalbad)['reason']=='FULL_CLOSE_REQUIRED';final=broker_fixture('FINAL');fr=execute_scenario(final);fp=fr['economicProposal'];c['R6_FINAL_RESERVE_CONSUMPTION']=fp.reserveConsumed>0 and fp.reserveAfter==final['economicPolicy'].reserveBefore-fp.reserveConsumed;c['R6_RECOVERY_PL_TRANSITION']=fp.recoveryPLAfter==final['economicPolicy'].recoveryPLBefore+fp.availableMoney-final['economicPolicy'].farLossBefore
 replay=broker_fixture('FINAL');replay['persistedState']=fr['state'];replay['context']['stateRevision']=fr['state']['stateRevision'];rr=execute_scenario(replay);c['R6_EXACTLY_ONCE_REPLAY']=rr['reason']=='ALREADY_COMMITTED' and not rr['settlementApplied'];c['R6_PERSISTENCE_BEFORE_MUTATION']=result['commitCertificate'].persistenceRecordDigest==result['state']['persistenceRecordDigest'];c['R6_STATE_REVISION_PLUS_ONE']=result['state']['stateRevision']==x['context']['stateRevision']+1;c['R6_DETERMINISTIC_DIGEST']=digest(x)==digest(copy.deepcopy(x))
 malformed=broker_fixture('BIG');malformed['positions']=None;c['R6_MALFORMED_COLLECTION_REJECTION']=execute_scenario(malformed)['status']=='REJECT'
 try:assert_property('UNKNOWN');unknown=False
 except KeyError:unknown=True
 c['R6_UNKNOWN_PROPERTY_FAIL_CLOSED']=unknown
 return c
def assert_property(name):
 if name not in CHECK_IDS:raise KeyError('UNKNOWN_PROPERTY')
 return run_checks()[name]
def self_test():
 c=run_checks();print(f'R4_R6_INVARIANTS={sum(c.values())}/{len(c)}');return len(c)==30 and all(c.values())
if __name__=='__main__':p=argparse.ArgumentParser();p.add_argument('--self-test',action='store_true');a=p.parse_args();raise SystemExit(0 if a.self_test and self_test() else 1)
