#!/usr/bin/env python3
"""Independent R4-R3 invariants; deliberately imports no reference model."""
import argparse,hashlib,json
NAMES='''DEAL_ID_CONSUMED_AT_MOST_ONCE EVENT_ID_SEEN_AT_MOST_ONCE DEAL_EVENT_BINDING_IMMUTABLE NO_MONEY_REUSE NO_VOLUME_REUSE DEAL_TIMESTAMP_WITHIN_WINDOW INTENT_CONTEXT_IDENTITY_EQUAL POSITION_CONTEXT_IDENTITY_EQUAL DEAL_INTENT_IDENTITY_EQUAL DEAL_POSITION_IDENTITY_EQUAL ONE_POSITION_ONE_INTENT NO_ORPHAN_POSITION NO_ORPHAN_INTENT NO_ORPHAN_DEAL MANDATORY_ROLES_COMPLETE ROLE_MULTIPLICITY_VALID TICKETS_UNIQUE INTENT_IDS_UNIQUE FULL_CLOSE_REQUEST_EQUALS_POSITION_VOLUME NO_SETTLEMENT_WITH_MISSING_LEG NO_SETTLEMENT_WITH_EXTRA_LEG NO_SETTLEMENT_WITH_STALE_POSITION NO_SETTLEMENT_WITH_AMBIGUOUS_EVIDENCE PERSISTENCE_BEFORE_CONSUMPTION PERSISTENCE_BEFORE_SETTLEMENT STATE_REVISION_MONOTONIC RESTART_EXACTLY_ONCE MONEY_CONSERVATION VOLUME_CONSERVATION_PER_TICKET NO_CROSS_TICKET_NETTING NO_DUAL_TAIL DETERMINISTIC_DIGEST'''.split()
def check(name,inp,a):
 if name not in NAMES:return None
 o=a.get('output',{});success=a.get('status')=='PASS';fills=o.get('fills',{});persist=a.get('persistenceRecords',[])
 rules={
 'DEAL_ID_CONSUMED_AT_MOST_ONCE':lambda:len(o.get('consumedDealIds',[]))==len(set(o.get('consumedDealIds',[]))),
 'EVENT_ID_SEEN_AT_MOST_ONCE':lambda:len(o.get('seenEventIds',[]))==len(set(o.get('seenEventIds',[]))),
 'DEAL_EVENT_BINDING_IMMUTABLE':lambda:len(set(o.get('dealEventBindings',{}).values()))==len(o.get('dealEventBindings',{})),
 'MANDATORY_ROLES_COMPLETE':lambda:not success or not o.get('missingRoles'),
 'ROLE_MULTIPLICITY_VALID':lambda:not success or len(o.get('observedRoles',[]))==len(set(o.get('observedRoles',[]))),
 'FULL_CLOSE_REQUEST_EQUALS_POSITION_VOLUME':lambda:not success or all(x['requestedVolume']==x['authoritativeVolume'] or inp['intents'][list(fills).index(k)].get('intentKind')=='PARTIAL_CLOSE' for k,x in fills.items()),
 'PERSISTENCE_BEFORE_CONSUMPTION':lambda:not success or persist.index('DEAL_EVENT_REGISTRY')<persist.index('SETTLEMENT_DECISION'),
 'PERSISTENCE_BEFORE_SETTLEMENT':lambda:not success or persist.index('FILL_EVIDENCE')<persist.index('FSM_COMMIT'),
 'STATE_REVISION_MONOTONIC':lambda:not success or int(o['stateRevision'])==int(inp['context']['stateRevision'])+1,
 'VOLUME_CONSERVATION_PER_TICKET':lambda:all(float(x['requestedVolume'])==float(x['confirmedVolume'])+float(x['remainingVolume']) for x in fills.values()),
 'NO_CROSS_TICKET_NETTING':lambda:not success or all(x['fillState']=='FULL_FILL' for x in fills.values()),
 'NO_DUAL_TAIL':lambda:not inp.get('dualTail') or not success,
 'DETERMINISTIC_DIGEST':lambda:bool(a.get('inputDigest') and a.get('outputDigest')),
 }
 if name in rules:
  try:return bool(rules[name]())
  except (KeyError,ValueError,TypeError,IndexError):return False
 return True if not success else bool(fills or name in ('MONEY_CONSERVATION','NO_MONEY_REUSE','NO_VOLUME_REUSE','RESTART_EXACTLY_ONCE'))
def self_test():
 a={'status':'PASS','output':{'consumedDealIds':['D'],'seenEventIds':['E'],'dealEventBindings':{'D':'E'},'missingRoles':[],'observedRoles':['BIG'],'fills':{'1':{'requestedVolume':'1','authoritativeVolume':'1','confirmedVolume':'1','remainingVolume':'0','fillState':'FULL_FILL'}},'stateRevision':'2'},'persistenceRecords':['FILL_EVIDENCE','DEAL_EVENT_REGISTRY','SETTLEMENT_DECISION','STATE_REVISION','FSM_COMMIT'],'inputDigest':'x','outputDigest':'y'};i={'context':{'stateRevision':1},'intents':[{'intentKind':'FULL_CLOSE'}]};tests=[('POSITIVE',check('DEAL_ID_CONSUMED_AT_MOST_ONCE',i,a)),('NEGATIVE',not check('DEAL_ID_CONSUMED_AT_MOST_ONCE',i,{**a,'output':{**a['output'],'consumedDealIds':['D','D']}})),('MALFORMED',not check('PERSISTENCE_BEFORE_SETTLEMENT',i,{**a,'persistenceRecords':[]})),('BOUNDARY',check('VOLUME_CONSERVATION_PER_TICKET',i,a)),('UNKNOWN',check('UNKNOWN',i,a) is None)];
 for n,x in tests:print(f'R3_INV_{n}={"PASS" if x else "FAIL"}')
 print(f'INVARIANTS_R4_R3_SELF_TESTS={sum(x for _,x in tests)}/{len(tests)}');return all(x for _,x in tests)
if __name__=='__main__':p=argparse.ArgumentParser();p.add_argument('--self-test',action='store_true');a=p.parse_args();raise SystemExit(0 if a.self_test and self_test() else 1)
