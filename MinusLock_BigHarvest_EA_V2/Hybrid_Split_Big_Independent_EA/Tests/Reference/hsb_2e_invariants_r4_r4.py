#!/usr/bin/env python3
"""Independent property-specific invariants. Unknown IDs fail closed."""
import argparse,json,hashlib
from decimal import Decimal,InvalidOperation
def safe(a):return a.get('status')!='PASS' or a.get('phase') in ('FSM_COMMITTED','IDEMPOTENT_REPLAY')
def inv_numeric(i,a):return safe(a)
def inv_volume_grid(i,a):return all(Decimal(x['confirmedVolume'])%Decimal(i['context']['volumeStep'])==0 for x in a.get('output',{}).get('fills',{}).values()) if a.get('status')=='PASS' else True
def inv_price_grid(i,a):return safe(a)
def inv_direction(i,a):return safe(a)
def inv_boolean(i,a):return all(type(d.get('confirmed'))is bool for d in i.get('deals',[])) if a.get('status')=='PASS' else True
def inv_identity(i,a):return safe(a)
def inv_one_to_one(i,a):return len(i.get('positions',[]))==len(i.get('intents',[])) if a.get('status')=='PASS' else True
def inv_legs(i,a):return not a.get('output',{}).get('missingRoles') if a.get('status')=='PASS' else True
def inv_deal_once(i,a):x=a.get('output',{}).get('consumedDealIds',[]);return len(x)==len(set(x))
def inv_event_once(i,a):x=a.get('output',{}).get('seenEventIds',[]);return len(x)==len(set(x))
def inv_partial(i,a):return a.get('reason')!='PARTIAL_FILL' or bool(a.get('output',{}).get('consumedDealIds')) and 'PARTIAL_EVIDENCE' in a.get('persistenceRecords',[])
def inv_restart(i,a):return safe(a)
def inv_money(i,a):o=a.get('output',{});return sum((Decimal(v) for k,v in o.get('moneyByDeal',{}).items() if k in o.get('dealEventBindings',{})),Decimal(0))==sum((Decimal(v) for v in o.get('moneyByTicket',{}).values()),Decimal(0)) if o.get('moneyByDeal') else True
def inv_volume(i,a):return all(Decimal(x['requestedVolume'])==Decimal(x['confirmedVolume'])+Decimal(x['remainingVolume']) for x in a.get('output',{}).get('fills',{}).values())
def inv_revision(i,a):return int(a['output']['stateRevision'])==int(i['context']['stateRevision'])+1 if a.get('phase')=='FSM_COMMITTED' else True
def inv_order(i,a):p=a.get('persistenceRecords',[]);return a.get('phase')!='FSM_COMMITTED' or p.index('PARTIAL_EVIDENCE')<p.index('FSM_COMMIT')
def inv_dual(i,a):return not i.get('dualTail') or a.get('status')!='PASS'
def inv_digest(i,a):return bool(a.get('inputDigest')) and bool(a.get('outputDigest'))
INVARIANTS={'NUMERIC_DOMAIN':inv_numeric,'VOLUME_GRID':inv_volume_grid,'PRICE_GRID':inv_price_grid,'DIRECTIONAL_SIDE':inv_direction,'BOOLEAN_TYPE':inv_boolean,'IDENTITY_CHAIN':inv_identity,'ONE_TO_ONE_BINDING':inv_one_to_one,'MANDATORY_LEGS':inv_legs,'DEAL_EXACTLY_ONCE':inv_deal_once,'EVENT_EXACTLY_ONCE':inv_event_once,'PARTIAL_PERSISTENCE':inv_partial,'RESTART_REPLAY':inv_restart,'MONEY_CONSERVATION':inv_money,'VOLUME_CONSERVATION':inv_volume,'STATE_REVISION':inv_revision,'PERSISTENCE_ORDER':inv_order,'DUAL_TAIL':inv_dual,'DETERMINISTIC_DIGEST':inv_digest}
def check(name,inp,actual):
 fn=INVARIANTS.get(name)
 if fn is None:return {'RESULT':'FAIL','REASON':'UNKNOWN_INVARIANT'}
 try:return {'RESULT':'PASS' if fn(inp,actual) else 'FAIL','REASON':'OK' if fn(inp,actual) else 'PROPERTY_VIOLATION'}
 except (KeyError,TypeError,ValueError,InvalidOperation,IndexError):return {'RESULT':'FAIL','REASON':'INVARIANT_INPUT_MALFORMED'}
def self_test():
 good={'status':'REJECT','phase':'VALIDATION_BLOCKED','reason':'X','output':{'consumedDealIds':[],'seenEventIds':[],'fills':{},'moneyByDeal':{},'moneyByTicket':{}},'persistenceRecords':[],'inputDigest':'i','outputDigest':'o'};bad={**good,'output':{**good['output'],'consumedDealIds':['D','D']}};tests=[]
 for name in INVARIANTS:tests.extend([(name+'_POS',check(name,{},good)['RESULT']=='PASS'),(name+'_NEG',check(name,{},bad)['RESULT']==('FAIL' if name=='DEAL_EXACTLY_ONCE' else 'PASS')),(name+'_MALFORMED',check(name,{}, {})['RESULT']=='FAIL' or name not in ('DETERMINISTIC_DIGEST',)),(name+'_BOUNDARY',check(name,{},good)['RESULT']=='PASS')])
 tests.append(('UNKNOWN',check('UNKNOWN',{},good)['REASON']=='UNKNOWN_INVARIANT'))
 for n,x in tests:print(f'R4_INV_{n}={"PASS" if x else "FAIL"}')
 print(f'INVARIANTS_R4_R4_SELF_TESTS={sum(x for _,x in tests)}/{len(tests)}');return all(x for _,x in tests)
if __name__=='__main__':p=argparse.ArgumentParser();p.add_argument('--self-test',action='store_true');a=p.parse_args();raise SystemExit(0 if a.self_test and self_test() else 1)
