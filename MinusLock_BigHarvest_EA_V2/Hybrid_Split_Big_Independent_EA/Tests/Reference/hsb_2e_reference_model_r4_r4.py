#!/usr/bin/env python3
"""Layer C: scenario, persistence, transaction barrier and restart."""
import argparse,copy,hashlib,json
from decimal import Decimal
from hsb_2e_primitive_validators_r4_r4 import D,validate_collection_type,validate_volume,on_grid
from hsb_2e_identity_model_r4_r4 import *
REQUIRED={'INITIAL':{'WINNER'},'BIG':{'BIG','SMALL'},'SMALL':{'SMALL','OLD_FAR','BIG'},'FINAL':{'FAR'}}
PARTIAL_ALLOWED={'SMALL':{'BIG'},'FINAL':{'FAR'}}
PERSIST_ORDER=['PARTIAL_EVIDENCE','DEAL_EVENT_REGISTRY','SETTLEMENT_DECISION','STATE_REVISION','FSM_COMMIT']
def canon(x):
 if isinstance(x,Decimal):return str(x)
 if isinstance(x,dict):return {k:canon(v) for k,v in sorted(x.items())}
 if isinstance(x,list):
  values=[canon(v) for v in x]
  if values and all(isinstance(v,dict) for v in values):values.sort(key=lambda v:str(v.get('dealId',v.get('intentId',v.get('positionTicket','')))))
  return values
 return x
def digest(x):return hashlib.sha256(json.dumps(canon(x),sort_keys=True,separators=(',',':')).encode()).hexdigest()
def result(inp,status,reason,phase,out,records):
 r={'status':status,'reason':reason,'phase':phase,'scenario':inp.get('scenario'),'output':canon(out),'persistenceRecords':records,'inputDigest':digest(inp)};r['outputDigest']=digest(r);return r
def empty(inp):return {'requiredRoles':sorted(REQUIRED.get(inp.get('scenario'),set())),'observedRoles':[],'missingRoles':[],'extraRoles':[],'fills':{},'acceptedDealIds':[],'consumedDealIds':[],'seenEventIds':[],'dealEventBindings':{},'confirmedVolumeByTicket':{},'remainingVolumeByTicket':{},'moneyByDeal':{},'moneyByTicket':{},'settlementApplied':False,'allocationApplied':False,'stateRevision':inp.get('context',{}).get('stateRevision'),'evidenceRevision':inp.get('persistedState',{}).get('evidenceRevision',0)}
def reject(inp,reason,out=None,status='REJECT'):return result(inp,status,reason,'VALIDATION_BLOCKED',out or empty(inp),[])
def validate_required_legs(inp):
 ps,its,ds=inp.get('positions'),inp.get('intents'),inp.get('deals')
 for v,k in ((ps,list),(its,list),(ds,list)):
  if validate_collection_type(v,k):return 'COLLECTION_SCHEMA_INVALID'
 if any(type(x)is not dict for seq in (ps,its,ds) for x in seq):return 'COLLECTION_ELEMENT_INVALID'
 req=REQUIRED.get(inp.get('scenario'))
 if req is None:return 'UNKNOWN_SCENARIO'
 roles=[p.get('role') for p in ps];tickets=[p.get('positionTicket') for p in ps];itickets=[i.get('positionTicket') for i in its];iids=[i.get('intentId') for i in its]
 if set(roles)!=req:return 'MANDATORY_LEG_MISSING' if req-set(roles) else 'EXTRA_ROLE'
 if len(roles)!=len(set(roles)):return 'ROLE_MULTIPLICITY_INVALID'
 if len(tickets)!=len(set(tickets)):return 'DUPLICATE_POSITION_TICKET'
 if len(iids)!=len(set(iids)):return 'DUPLICATE_INTENT_ID'
 if len(itickets)!=len(set(itickets)):return 'MULTIPLE_INTENTS_FOR_POSITION'
 if len(ps)!=len(its) or set(tickets)!=set(itickets):return 'ONE_POSITION_ONE_INTENT_VIOLATION'
 if any(d.get('positionTicket') not in set(tickets) for d in ds):return 'ORPHAN_DEAL'
 return None
def aggregate_fill_per_ticket(inp,ps,its,state):
 c=inp['context'];out=empty(inp);out['observedRoles']=sorted(p['role'] for p in ps);out['consumedDealIds']=list(state['consumedDealIds']);out['seenEventIds']=list(state['seenEventIds']);out['dealEventBindings']=dict(state['dealEventBindings']);out['confirmedVolumeByTicket']=dict(state.get('cumulativeFills',{}));out['moneyByDeal']=dict(state.get('moneyByDeal',{}));out['moneyByTicket']=dict(state.get('moneyByTicket',{}));positions={p['positionTicket']:p for p in ps};intents={i['positionTicket']:i for i in its}
 for d in inp['deals']:
  did,eid=d.get('dealId'),d.get('eventId')
  if did in out['consumedDealIds']:return None,'DEAL_ALREADY_CONSUMED',out
  if eid in out['seenEventIds']:return None,'EVENT_ALREADY_SEEN',out
  p=positions.get(d.get('positionTicket'));i=intents.get(d.get('positionTicket'))
  if p is None:return None,'ORPHAN_DEAL',out
  e=validate_deal(d,p,i,c)
  if e:return None,e,out
  expected=expected_close_side(p['direction'],c)
  if D(d['price'])!=D(expected) and inp.get('executionPriceWindowProven') is not True:return None,'EXECUTION_PRICE_WINDOW_UNPROVEN',out
  out['acceptedDealIds'].append(did);out['consumedDealIds'].append(did);out['seenEventIds'].append(eid);out['dealEventBindings'][did]=eid
  t=str(p['positionTicket']);out['confirmedVolumeByTicket'][t]=D(out['confirmedVolumeByTicket'].get(t,'0'))+D(d['volume']);money=D(d['profit'])+D(d['commission'])+D(d['swap'])+D(d['fee']);out['moneyByDeal'][did]=money;out['moneyByTicket'][t]=D(out['moneyByTicket'].get(t,'0'))+money
 for p in ps:
  t=str(p['positionTicket']);i=intents[p['positionTicket']];confirmed=D(out['confirmedVolumeByTicket'].get(t,'0'));requested=D(i['requestedVolume']);remaining=max(D(0),requested-confirmed);fill='FULL_FILL' if confirmed==requested else 'PARTIAL_FILL' if confirmed<requested else 'OVERFILL';out['confirmedVolumeByTicket'][t]=confirmed;out['remainingVolumeByTicket'][t]=remaining;out['fills'][t]={'fillState':fill,'requestedVolume':requested,'authoritativeVolume':D(p['positionVolume']),'confirmedVolume':confirmed,'remainingVolume':remaining}
 return out,None,out
def build_settlement_proposal(inp):
 c=inp.get('context');e=validate_context(c)
 if e:return reject(inp,e)
 state=inp.get('persistedState',{'consumedDealIds':[],'seenEventIds':[],'dealEventBindings':{},'cumulativeFills':{},'moneyByDeal':{},'moneyByTicket':{},'evidenceRevision':0,'settlementCommitted':False})
 e=validate_registry(state)
 if e:return reject(inp,e)
 if type(state.get('cumulativeFills',{}))is not dict or type(state.get('moneyByDeal',{}))is not dict or type(state.get('moneyByTicket',{}))is not dict:return reject(inp,'PERSISTED_REGISTRY_SCHEMA_INVALID')
 e=validate_required_legs(inp)
 if e:return reject(inp,e)
 if inp.get('dualTail') is True:return reject(inp,'DUAL_TAIL')
 ps,its=inp['positions'],inp['intents'];imap={i['positionTicket']:i for i in its}
 for p in ps:
  e=validate_position(p,c)
  if e:return reject(inp,e)
  i=imap[p['positionTicket']];e=validate_intent(i,p,c)
  if e:return reject(inp,e)
  if i['intentKind']=='PARTIAL_CLOSE' and p['role'] not in PARTIAL_ALLOWED.get(inp['scenario'],set()):return reject(inp,'PARTIAL_CLOSE_NOT_ALLOWED')
 if state.get('settlementCommitted') is True:return result(inp,'PASS','ALREADY_COMMITTED','IDEMPOTENT_REPLAY',empty(inp),[])
 out,e,_=aggregate_fill_per_ticket(inp,ps,its,state)
 if e:return reject(inp,e,out,'CONFLICT' if e in ('DEAL_ALREADY_CONSUMED','EVENT_ALREADY_SEEN') else 'REJECT')
 states=[x['fillState'] for x in out['fills'].values()]
 out['evidenceRevision']=int(state.get('evidenceRevision',0))+1
 if any(x=='OVERFILL' for x in states):return result(inp,'CONFLICT','OVERFILL','RECONCILIATION_BLOCKED',out,['PARTIAL_EVIDENCE','DEAL_EVENT_REGISTRY'])
 if any(x!='FULL_FILL' for x in states):return result(inp,'UNAVAILABLE','PARTIAL_FILL','WAITING_FOR_FULL_FILL',out,['PARTIAL_EVIDENCE','DEAL_EVENT_REGISTRY'])
 return result(inp,'PASS','PROPOSAL_READY','SETTLEMENT_PROPOSED',out,['PARTIAL_EVIDENCE','DEAL_EVENT_REGISTRY'])
def admit_transaction_barrier(inp,proposal):return proposal['status']=='PASS' and proposal['phase']=='SETTLEMENT_PROPOSED' and all(x['fillState']=='FULL_FILL' for x in proposal['output']['fills'].values())
def commit_state_transition(inp,proposal):
 if not admit_transaction_barrier(inp,proposal):return proposal
 out=copy.deepcopy(proposal['output']);out['settlementApplied']=True;out['allocationApplied']=True;out['stateRevision']=int(inp['context']['stateRevision'])+1;out['settlementCommitted']=True
 return result(inp,'PASS','OK','FSM_COMMITTED',out,PERSIST_ORDER)
def execute_scenario(inp):
 try:return commit_state_transition(inp,build_settlement_proposal(copy.deepcopy(inp)))
 except (KeyError,TypeError,ValueError,ArithmeticError) as e:return reject(inp,'MALFORMED_INPUT_'+type(e).__name__.upper())
def persisted_from_partial(r):
 o=r['output'];state={'consumedDealIds':o['consumedDealIds'],'seenEventIds':o['seenEventIds'],'dealEventBindings':o['dealEventBindings'],'cumulativeFills':o['confirmedVolumeByTicket'],'moneyByDeal':o['moneyByDeal'],'moneyByTicket':o['moneyByTicket'],'evidenceRevision':o['evidenceRevision'],'settlementCommitted':o.get('settlementCommitted',False)};state['digest']=digest({k:v for k,v in state.items() if k!='digest'});return state
def restart_reconcile(persistedState,brokerSnapshot,newDeals):
 if type(persistedState)is not dict or persistedState.get('digest')!=digest({k:v for k,v in persistedState.items() if k!='digest'}):return reject(brokerSnapshot,'PERSISTED_STATE_DIGEST_INVALID')
 inp=copy.deepcopy(brokerSnapshot);inp['persistedState']={k:v for k,v in persistedState.items() if k!='digest'};inp['deals']=copy.deepcopy(newDeals);return execute_scenario(inp)
def self_test():
 from pathlib import Path
 v=json.loads((Path(__file__).parents[1]/'Vectors/HSB_2E_R4_R4_VECTORS.json').read_text())['vectors'];ids=['R4_VALID_BIG','R4_ZERO_POSITION','R4_OFFGRID_VOLUME','R4_NEG_PRICE','R4_STRING_BOOL','R4_MULTI_INTENT','R4_NEG_REVISION','R4_PARTIAL']
 checks=[(i,execute_scenario(next(x for x in v if x['VECTOR_ID']==i)['INPUT'])==next(x for x in v if x['VECTOR_ID']==i)['EXPECTED_RESULT']) for i in ids]
 for i,x in checks:print(f'R4_MODEL_{i}={"PASS" if x else "FAIL"}')
 print(f'REFERENCE_MODEL_R4_R4_SELF_TESTS={sum(x for _,x in checks)}/{len(checks)}');return all(x for _,x in checks)
if __name__=='__main__':p=argparse.ArgumentParser();p.add_argument('--self-test',action='store_true');a=p.parse_args();raise SystemExit(0 if a.self_test and self_test() else 1)
