#!/usr/bin/env python3
"""Independent predicates over vector input and actual output; does not import the model."""
from decimal import Decimal,InvalidOperation
import argparse,hashlib,json
D=lambda x:Decimal(str(x))
def eq(a,b,t='0.00000001'):return abs(D(a)-D(b))<=D(t)
def output(a):return a.get('output',{})
def money(i,a):
 o=output(a);return eq(o['sourceMoney'],D(o['allocatedPartialFar'])+D(o['allocatedReserve'])+D(o['allocatedOther'])+D(o['unallocatedRemainder']))
def volume(i,a):
 o=output(a);groups=[k[:-6] for k in o if k.endswith('Before') and k[:-6]+'Closed' in o and k[:-6]+'Remaining' in o];return bool(groups) and all(eq(o[g+'Before'],D(o[g+'Closed'])+D(o[g+'Remaining'])) for g in groups)
def reserve_nonnegative(i,a):return D(output(a).get('reserveAfter',0))>=0
def reserve_isolation(i,a):return D(output(a).get('closeFarBudget',0))<=max(D(0),D(output(a).get('bigNetMoney',0))+D(output(a).get('smallNetMoney',0)))
def initial_ignored(i,a):
 o=output(a);return eq(o['recoveryBudgetWithInitialProfit'],o['recoveryBudgetWithoutInitialProfit']) and any(x.get('source')=='IGNORED_INITIAL_POSITIVE_PROFIT' and not x.get('consumable') for x in a['ledgerDelta'])
def compression(i,a):return D(output(a)['newFarVolume'])<D(output(a)['oldFarVolume'])
def ownership(i,a):
 c=i.get('context',{});return all(p.get('symbol')==c.get('symbol') and p.get('magic')==c.get('magic') and p.get('cycleId')==c.get('cycleId') and p.get('ticket',0)>0 for p in i.get('positions',[]))
def unique_deals(i,a):
 keys=[(x.get('dealId'),x.get('eventId')) for x in i.get('deals',[])];return len(keys)==len(set(keys))
def unique_events(i,a):
 k=[x.get('eventId') for x in i.get('deals',[])];return len(k)==len(set(k))
def action_once(i,a):return len({x.get('actionId') for x in a.get('futureBrokerIntents',[])})<=1
def revision(i,a):return all(x.get('stateRevision')==i['context']['stateRevision'] for x in a.get('futureBrokerIntents',[]))
def persistence(i,a):return not a.get('positionDelta') or bool(a.get('persistenceRecords'))
def final_gates(i,a):return not output(a).get('finalCloseAllowed') or D(output(a)['recoveryPL'])>0 and D(output(a)['reserveCoverage'])>=0
def no_dual(i,a):return output(a).get('dualTail',False) is False
def no_intent_failure(i,a):return a['status']=='PASS' or not a.get('futureBrokerIntents') or a['reason']=='PARTIAL_FILL'
def no_duplicate_intent(i,a):
 intents=a.get('futureBrokerIntents',[]);ids=[x['intentId'] for x in intents];keys=[(x['positionTicket'],x['actionType'],x['normalizedVolume']) for x in intents];return len(ids)==len(set(ids)) and len(keys)==len(set(keys))
def deterministic(i,a):
 b={k:v for k,v in a.items() if k!='outputDigest'};return a['outputDigest']==hashlib.sha256(json.dumps(b,sort_keys=True,separators=(',',':'),default=str).encode()).hexdigest()
def big_full(i,a):return eq(output(a)['bigCloseVolume'],next(p['volume'] for p in i['positions'] if p['role']=='BIG'))
def small_full_big(i,a):return eq(output(a)['smallCloseVolume'],next(p['volume'] for p in i['positions'] if p['role']=='SMALL'))
def old_far_full(i,a):return eq(output(a)['oldFarClosedVolume'],next(p['volume'] for p in i['positions'] if p['role']=='FAR'))
def big_conservation(i,a):return eq(output(a)['bigVolumeBefore'],D(output(a)['bigVolumeClosed'])+D(output(a)['bigVolumeRemaining']))
def reserve_once(i,a):return len([x.get('allocationKey') for x in a.get('ledgerDelta',[]) if x.get('allocationKey')])==len(set(x.get('allocationKey') for x in a.get('ledgerDelta',[]) if x.get('allocationKey')))
REGISTRY={'MONEY_CONSERVATION':money,'VOLUME_CONSERVATION':volume,'RESERVE_NONNEGATIVE':reserve_nonnegative,'PARTIAL_FAR_RESERVE_ISOLATION':reserve_isolation,'INITIAL_POSITIVE_PROFIT_IGNORED':initial_ignored,'NEW_FAR_COMPRESSION':compression,'IDENTITY_OWNERSHIP':ownership,'DEAL_KEYS_UNIQUE':unique_deals,'EVENT_KEYS_UNIQUE':unique_events,'ACTION_EXACTLY_ONCE':action_once,'STATE_REVISION_MONOTONIC':revision,'PERSISTENCE_BEFORE_MUTATION':persistence,'FINAL_CLOSE_GATES':final_gates,'NO_DUAL_TAIL':no_dual,'NO_INTENT_ON_FAILURE':no_intent_failure,'NO_DUPLICATE_BROKER_INTENT':no_duplicate_intent,'DETERMINISTIC_DIGEST':deterministic,'BIG_FULL_CLOSE':big_full,'SMALL_FULL_CLOSE_ON_BIG':small_full_big,'OLD_FAR_FULL_CLOSE_ON_SMALL':old_far_full,'BIG_VOLUME_CONSERVATION_ON_SMALL':big_conservation,'RESERVE_ALLOCATION_EXACTLY_ONCE':reserve_once}
def check(name,i,a):
 if name not in REGISTRY:return None
 try:return bool(REGISTRY[name](i,a))
 except (KeyError,InvalidOperation,TypeError,StopIteration):return False
def self_test():
 cases=[eq('1','1'),not eq('1','2'),reserve_nonnegative({}, {'output':{'reserveAfter':'0'}}),no_duplicate_intent({}, {'futureBrokerIntents':[]}),check('UNKNOWN',{}, {}) is None]
 print('\n'.join(f'INV4_{n}={"PASS" if x else "FAIL"}' for n,x in enumerate(cases,1)));print(f'INVARIANTS_R4_SELF_TESTS={sum(cases)}/{len(cases)}');return all(cases)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--self-test',action='store_true');a=p.parse_args();raise SystemExit(0 if a.self_test and self_test() else 1)
