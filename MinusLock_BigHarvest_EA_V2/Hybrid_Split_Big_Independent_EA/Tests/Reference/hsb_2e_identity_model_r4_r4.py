#!/usr/bin/env python3
"""Layer B: identity, evidence and persisted-registry validation."""
import argparse
from hsb_2e_primitive_validators_r4_r4 import *
def validate_context(c):
 if type(c) is not dict:return 'CONTEXT_SCHEMA_INVALID'
 for k in ('cycleId','actionId','transactionId','snapshotId'):
  if validate_identifier(c.get(k)):return f'{k.upper()}_INVALID'
 if validate_revision(c.get('stateRevision')):return 'STATE_REVISION_INVALID'
 if validate_revision(c.get('snapshotVersion'),True):return 'SNAPSHOT_VERSION_INVALID'
 if validate_price(c.get('bid'),c.get('tickSize')) or validate_price(c.get('ask'),c.get('tickSize')):return 'BID_ASK_INVALID'
 if D(c['ask'])<D(c['bid']):return 'BID_ASK_INVALID'
 if validate_revision(c.get('digits')):return 'DIGITS_INVALID'
 return None
def validate_registry(state):
 if type(state) is not dict:return 'PERSISTED_REGISTRY_SCHEMA_INVALID'
 cd,se,b=state.get('consumedDealIds'),state.get('seenEventIds'),state.get('dealEventBindings')
 if type(cd) is not list or type(se) is not list or type(b) is not dict or not all(type(x)is str for x in cd+se) or not all(type(k)is str and type(v)is str for k,v in b.items()):return 'PERSISTED_REGISTRY_SCHEMA_INVALID'
 if len(cd)!=len(set(cd)) or len(se)!=len(set(se)):return 'PERSISTED_REGISTRY_DUPLICATE'
 if len(set(b.values()))!=len(b):return 'PERSISTED_BINDING_NOT_BIJECTIVE'
 if set(b)!=set(cd) or set(b.values())!=set(se):return 'PERSISTED_BINDING_LEDGER_MISMATCH'
 return None
def validate_position(p,c):
 if type(p)is not dict:return 'POSITION_SCHEMA_INVALID'
 if validate_identifier(p.get('role')) or validate_revision(p.get('positionRevision')):return 'POSITION_IDENTITY_INVALID'
 for k in ('accountLogin','symbol','magic','cycleId'):
  if p.get(k)!=c.get(k):return 'POSITION_OWNERSHIP_MISMATCH'
 if p.get('positionRevision')!=c['stateRevision'] or p.get('snapshotId')!=c['snapshotId'] or p.get('snapshotVersion')!=c['snapshotVersion']:return 'POSITION_OWNERSHIP_MISMATCH'
 return validate_volume(p.get('positionVolume'),c['volumeStep'],c['volumeMin'],c['volumeMax']) and 'POSITION_VOLUME_INVALID'
def validate_intent(i,p,c):
 if type(i)is not dict:return 'INTENT_SCHEMA_INVALID'
 for k in ('intentId','cycleId','transactionId','actionId','snapshotId'):
  if validate_identifier(i.get(k)):return 'INTENT_IDENTITY_INVALID'
 for k in ('accountLogin','symbol','magic','cycleId','transactionId','actionId','stateRevision','snapshotId','snapshotVersion'):
  if i.get(k)!=c.get(k):return 'INTENT_IDENTITY_MISMATCH'
 if i.get('positionTicket')!=p.get('positionTicket') or i.get('positionRole')!=p.get('role') or i.get('direction')!=p.get('direction'):return 'INTENT_POSITION_BINDING_MISMATCH'
 e=validate_volume(i.get('requestedVolume'),c['volumeStep'],c['volumeMin'],c['volumeMax'])
 if e:return 'REQUESTED_VOLUME_INVALID' if e!='VOLUME_OFF_GRID' else e
 if i.get('intentKind')=='FULL_CLOSE' and D(i['requestedVolume'])!=D(p['positionVolume']):return 'FULL_CLOSE_VOLUME_MISMATCH'
 if i.get('intentKind')=='PARTIAL_CLOSE' and not (D(0)<D(i['requestedVolume'])<D(p['positionVolume']) and on_grid(D(p['positionVolume'])-D(i['requestedVolume']),c['volumeStep'])):return 'PARTIAL_CLOSE_VOLUME_INVALID'
 if i.get('intentKind') not in ('FULL_CLOSE','PARTIAL_CLOSE'):return 'INTENT_KIND_INVALID'
 return None
def validate_deal(d,p,i,c):
 if type(d)is not dict:return 'DEAL_SCHEMA_INVALID'
 for k in ('dealId','eventId','orderId'):
  if validate_identifier(d.get(k)):return f'{k.upper()}_INVALID'
 if validate_boolean(d.get('confirmed')):return 'DEAL_CONFIRMED_TYPE_INVALID'
 if d['confirmed'] is not True:return 'DEAL_UNCONFIRMED'
 if validate_volume(d.get('volume'),c['volumeStep'],c['volumeMin'],c['volumeMax']):return 'DEAL_VOLUME_INVALID'
 if validate_price(d.get('price'),c['tickSize']):return 'DEAL_PRICE_INVALID'
 for k in ('profit','commission','swap','fee'):
  if decimal_value(d.get(k)) is None:return 'DEAL_MONEY_INVALID'
 for k in ('accountLogin','symbol','magic','cycleId','transactionId','actionId','stateRevision'):
  if d.get(k)!=c.get(k):return 'DEAL_IDENTITY_MISMATCH'
 if d.get('positionTicket')!=p.get('positionTicket') or d.get('direction')!=p.get('direction'):return 'DEAL_POSITION_BINDING_MISMATCH'
 if validate_timestamp(d.get('timestamp')):return 'DEAL_TIMESTAMP_INVALID'
 if D(d['timestamp'])<max(D(c['minimumTimestamp']),D(i['createdTimestamp'])):return 'STALE_DEAL'
 if D(d['timestamp'])>min(D(c['allowedUpperBound']),D(i['expiresTimestamp'])):return 'FUTURE_DEAL'
 return None
def expected_close_side(direction,c):return c['bid'] if direction=='BUY' else c['ask'] if direction=='SELL' else None
def self_test():
 c={'cycleId':'C','actionId':'A','transactionId':'T','snapshotId':'S','stateRevision':0,'snapshotVersion':1,'bid':'1.1','ask':'1.2','tickSize':'.1','digits':1,'accountLogin':1,'symbol':'X','magic':2,'volumeStep':'.1','volumeMin':'.1','volumeMax':'10'}
 t={'CONTEXT_POS':validate_context(c)is None,'CONTEXT_NEG':validate_context({**c,'stateRevision':-1})is not None,'REG_POS':validate_registry({'consumedDealIds':['D'],'seenEventIds':['E'],'dealEventBindings':{'D':'E'}})is None,'REG_BAD_TYPE':validate_registry({'consumedDealIds':'D','seenEventIds':{},'dealEventBindings':[]})=='PERSISTED_REGISTRY_SCHEMA_INVALID','REG_BAD_BIND':validate_registry({'consumedDealIds':['D1','D2'],'seenEventIds':['E'],'dealEventBindings':{'D1':'E','D2':'E'}})=='PERSISTED_BINDING_NOT_BIJECTIVE'}
 for k,v in t.items():print(f'R4_IDENTITY_{k}={"PASS" if v else "FAIL"}')
 print(f'IDENTITY_R4_R4_SELF_TESTS={sum(t.values())}/{len(t)}');return all(t.values())
if __name__=='__main__':p=argparse.ArgumentParser();p.add_argument('--self-test',action='store_true');a=p.parse_args();raise SystemExit(0 if a.self_test and self_test() else 1)
