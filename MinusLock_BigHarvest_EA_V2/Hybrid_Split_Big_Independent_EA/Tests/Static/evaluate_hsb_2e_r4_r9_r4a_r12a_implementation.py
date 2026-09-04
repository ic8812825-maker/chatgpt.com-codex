#!/usr/bin/env python3
"""R12A-FIX-01 evaluator for predicates 8--14; does not alter frozen R12 artifacts."""
from decimal import Decimal, InvalidOperation
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'Tests/Static'))
from verify_hsb_2e_r4_r9_r4a_r12a_normative_contract import root as canonical_ledger_root

FAIL={
 'POSITION_VALIDATION':'R9_POSITION_VALIDATION','INTENT_VALIDATION':'R9_INTENT_VALIDATION',
 'DEAL_EVENT_UNIQUENESS':'R9_DEAL_EVENT_UNIQUENESS','DEAL_POSITION_INTENT_BINDING':'R9_DEAL_POSITION_INTENT_BINDING',
 'PERSISTED_LEDGER_REVALIDATION':'R9_PERSISTED_LEDGER_REVALIDATION','BATCH_ATOMICITY':'R9_BATCH_ATOMICITY',
 'PER_TICKET_FILL':'R9_PER_TICKET_FILL'}
def result(pid,status,paths,reason=''):
 return {'predicateId':pid,'status':status,'checkId':FAIL[pid] if status=='FAIL' else '', 'reason':reason,'evaluatedPaths':paths}
def fail(pid,paths,reason): return result(pid,'FAIL',paths,reason)
def passed(pid,paths): return result(pid,'PASS',paths)
def decimal(v):
 try: return Decimal(str(v))
 except (InvalidOperation,ValueError): raise ValueError('INVALID_DECIMAL')
def grid(value, minimum, step):
 v,m,s=decimal(value),decimal(minimum),decimal(step)
 return s>0 and (v-m) % s == 0

def evaluate_position_validation(r):
 p='POSITION_VALIDATION'; paths=['positions[*].ticket','positions[*].direction','positions[*].role','positions[*].volume','positions[*].openPrice','broker.volumeMin','broker.volumeMax','broker.volumeStep','broker.tickSize']
 b=r['broker']; seen=set()
 for x in r['positions']:
  if not isinstance(x['ticket'],str) or not x['ticket'] or x['ticket'] in seen:return fail(p,paths,'INVALID_OR_DUPLICATE_TICKET')
  seen.add(x['ticket'])
  if x['direction'] not in ('BUY','SELL') or x['role'] not in ('NEAR','BIG','FAR'):return fail(p,paths,'INVALID_DIRECTION_OR_ROLE')
  try:
   volume=decimal(x['volume'])
   price=decimal(x['openPrice'])
  except ValueError:return fail(p,paths,'INVALID_POSITION_DECIMAL')
  if not (decimal(b['volumeMin'])<=volume<=decimal(b['volumeMax']) and volume>0 and grid(volume,b['volumeMin'],b['volumeStep'])):return fail(p,paths,'INVALID_VOLUME_GRID')
  if not (price>0 and grid(price,0,b['tickSize'])):return fail(p,paths,'INVALID_PRICE_GRID')
 return passed(p,paths)

def evaluate_intent_validation(r):
 p='INTENT_VALIDATION';paths=['intents[*].intentId','intents[*].direction','intents[*].requestedVolume','intents[*].createdTimestamp','intents[*].expiresTimestamp','broker.volumeMin','broker.volumeMax','broker.volumeStep']; seen=set();b=r['broker']
 for x in r['intents']:
  if not isinstance(x['intentId'],str) or not x['intentId'] or x['intentId'] in seen:return fail(p,paths,'INVALID_OR_DUPLICATE_INTENT')
  seen.add(x['intentId'])
  if x['direction'] not in ('BUY','SELL') or x['expiresTimestamp']<x['createdTimestamp']:return fail(p,paths,'INVALID_INTENT_DIRECTION_OR_TIME')
  v=decimal(x['requestedVolume'])
  if not (decimal(b['volumeMin'])<=v<=decimal(b['volumeMax']) and grid(v,b['volumeMin'],b['volumeStep'])):return fail(p,paths,'INVALID_REQUESTED_VOLUME_GRID')
 return passed(p,paths)

def evaluate_deal_event_uniqueness(r):
 p='DEAL_EVENT_UNIQUENESS';paths=['deals[*].dealId','deals[*].eventId','events[*].eventId','events[*].dealId'];ds=r.get('deals',[]);es=r.get('events',[])
 did=[x['dealId'] for x in ds]; eid=[x['eventId'] for x in es]; links=[x['eventId'] for x in ds]
 if len(did)!=len(set(did)) or len(eid)!=len(set(eid)) or len(links)!=len(set(links)):return fail(p,paths,'DUPLICATE_DEAL_OR_EVENT_LINK')
 event_to_deal={x['eventId']:x['dealId'] for x in es}
 if set(links)!=set(event_to_deal) or any(event_to_deal[x['eventId']]!=x['dealId'] for x in ds):return fail(p,paths,'NOT_ONE_TO_ONE_DEAL_EVENT')
 return passed(p,paths)

def evaluate_deal_position_intent_binding(r):
 p='DEAL_POSITION_INTENT_BINDING';paths=['deals[*].positionTicket','deals[*].intentId','intents[*].positionTicket','positions[*].ticket'];ps={x['ticket'] for x in r['positions']};ins={x['intentId']:x for x in r['intents']}
 for x in r.get('deals',[]):
  if x['positionTicket'] not in ps or x['intentId'] not in ins or ins[x['intentId']]['positionTicket']!=x['positionTicket']:return fail(p,paths,'INVALID_DEAL_POSITION_INTENT_BINDING')
 return passed(p,paths)

def evaluate_persisted_ledger_revalidation(r):
 p='PERSISTED_LEDGER_REVALIDATION';paths=['persistedState.consumedDealIds','persistedState.authoritativeLedgerRoot','deals[*]']; state=r['persistedState']; deals=r.get('deals',[]); ids=state['consumedDealIds']
 if len(ids)!=len(set(ids)) or any(not isinstance(x,str) or not x for x in ids):return fail(p,paths,'INVALID_CONSUMED_DEAL_IDS')
 if set(ids)!={x['dealId'] for x in deals}:return fail(p,paths,'LEDGER_MEMBERSHIP_MISMATCH')
 try: expected=canonical_ledger_root(deals)
 except (KeyError,ValueError,InvalidOperation):return fail(p,paths,'INVALID_CANONICAL_LEDGER')
 if state['authoritativeLedgerRoot']!=expected:return fail(p,paths,'AUTHORITATIVE_LEDGER_ROOT_MISMATCH')
 return passed(p,paths)

def evaluate_batch_atomicity(r):
 p='BATCH_ATOMICITY';paths=['phase','context.transactionId','context.actionId','deals[*].transactionId','deals[*].actionId','events[*].transactionId','events[*].actionId','deals[*].confirmed','events[*].confirmed','intents[*].intentId','deals[*].intentId'];phase=r['phase']; ds=r.get('deals',[]);es=r.get('events',[])
 if phase=='PRE_COMMIT':
  return result(p,'NOT_APPLICABLE',paths,'PRE_COMMIT_WITHOUT_SETTLED_RECORDS') if not ds and not es else fail(p,paths,'PRE_COMMIT_HAS_SETTLED_RECORDS')
 if phase=='PARTIAL' or phase=='REPLAY':return fail(p,paths,'PARTIAL_OR_REPLAY_BATCH')
 if phase in ('ROLLED_BACK','FAILED'):return passed(p,paths) if not ds and not es else fail(p,paths,'UNSETTLED_PHASE_HAS_RECORDS')
 if phase not in ('COMMITTING','COMMITTED'):return fail(p,paths,'UNKNOWN_BATCH_PHASE')
 c=r['context']; identity=(c['transactionId'],c['actionId'])
 records=ds+es
 if any((x['transactionId'],x['actionId'])!=identity for x in records):return fail(p,paths,'BATCH_IDENTITY_MISMATCH')
 if any(not x['confirmed'] for x in records):return fail(p,paths,'UNCONFIRMED_BATCH')
 if {x['intentId'] for x in r['intents']}!={x['intentId'] for x in ds}:return fail(p,paths,'INTENT_DEAL_SET_MISMATCH')
 return passed(p,paths)

def evaluate_per_ticket_fill(r):
 p='PER_TICKET_FILL';paths=['intents[*].requestedVolume','intents[*].positionTicket','deals[*].volume','deals[*].intentId','deals[*].positionTicket','broker.volumeMin','broker.volumeStep'];ints={x['intentId']:x for x in r['intents']};seen_deals=set();seen_events=set();totals={k:Decimal(0) for k in ints};b=r['broker']
 for x in r.get('deals',[]):
  if x['dealId'] in seen_deals or x['eventId'] in seen_events:return fail(p,paths,'DUPLICATE_FILL')
  seen_deals.add(x['dealId']);seen_events.add(x['eventId'])
  if x['intentId'] not in ints or ints[x['intentId']]['positionTicket']!=x['positionTicket']:return fail(p,paths,'WRONG_INTENT_OR_TICKET_FILL')
  v=decimal(x['volume'])
  if not (v>0 and grid(v,b['volumeMin'],b['volumeStep'])):return fail(p,paths,'OFF_GRID_OR_NONPOSITIVE_FILL')
  totals[x['intentId']]+=v
 for iid,x in ints.items():
  if totals[iid]>decimal(x['requestedVolume']):return fail(p,paths,'OVERFILL')
 return passed(p,paths)

EVALUATORS={'POSITION_VALIDATION':evaluate_position_validation,'INTENT_VALIDATION':evaluate_intent_validation,'DEAL_EVENT_UNIQUENESS':evaluate_deal_event_uniqueness,'DEAL_POSITION_INTENT_BINDING':evaluate_deal_position_intent_binding,'PERSISTED_LEDGER_REVALIDATION':evaluate_persisted_ledger_revalidation,'BATCH_ATOMICITY':evaluate_batch_atomicity,'PER_TICKET_FILL':evaluate_per_ticket_fill}
