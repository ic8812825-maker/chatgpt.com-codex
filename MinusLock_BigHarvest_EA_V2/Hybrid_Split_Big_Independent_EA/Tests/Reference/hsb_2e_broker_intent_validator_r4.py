#!/usr/bin/env python3
from decimal import Decimal,InvalidOperation
import argparse,hashlib,json
ACTIONS={'OPEN_POSITION','CLOSE_POSITION_FULL','CLOSE_POSITION_PARTIAL'}
def validate(intents,positions,failed=False):
 errors=[];ids=set();closes=set();pos={p['ticket']:p for p in positions}
 if failed and intents:errors.append('INTENT_AFTER_FAILURE')
 for n,x in enumerate(intents):
  if x.get('actionType') not in ACTIONS:errors.append('UNKNOWN_ACTION_TYPE')
  if x.get('intentId') in ids:errors.append('DUPLICATE_BROKER_INTENT')
  ids.add(x.get('intentId'));ticket=x.get('positionTicket');p=pos.get(ticket)
  if x.get('actionType','').startswith('CLOSE') and not p:errors.append('UNKNOWN_POSITION_TICKET')
  key=(ticket,x.get('actionType'),x.get('normalizedVolume'))
  if key in closes:errors.append('DUPLICATE_BROKER_INTENT')
  closes.add(key)
  if p:
   if any(x.get(k)!=p.get(k) for k in ('symbol','magic','cycleId')):errors.append('OWNERSHIP')
   if x.get('direction') not in ('BUY','SELL'):errors.append('INVALID_DIRECTION')
   side='BID' if x.get('direction')=='BUY' else 'ASK'
   if x.get('expectedPriceSide')!=side:errors.append('INVALID_PRICE_SIDE')
   try:
    if Decimal(x['normalizedVolume'])>Decimal(p['volume']) or Decimal(x['normalizedVolume'])<=0:errors.append('INVALID_VOLUME')
   except (InvalidOperation,KeyError):errors.append('INVALID_VOLUME')
  if not x.get('actionId') or x.get('stateRevision',-1)<0:errors.append('TRANSACTION_CONTEXT')
  if n and x.get('parentIntentId') not in ('',intents[n-1].get('intentId')):errors.append('PARENT_BINDING')
 return {'result':'PASS' if not errors else 'FAIL','errors':sorted(set(errors))}
def self_test():
 p=[{'ticket':1,'symbol':'X','magic':2,'cycleId':'C','volume':'1'}];base={'intentId':'I','symbol':'X','magic':2,'cycleId':'C','actionType':'CLOSE_POSITION_FULL','positionTicket':1,'direction':'BUY','normalizedVolume':'1','expectedPriceSide':'BID','actionId':'A','stateRevision':1,'parentIntentId':''}
 checks=[validate([base],p)['result']=='PASS','UNKNOWN_POSITION_TICKET' in validate([{**base,'positionTicket':9}],p)['errors'],'DUPLICATE_BROKER_INTENT' in validate([base,base],p)['errors']]
 print('\n'.join(f'BI4_{i}={"PASS" if x else "FAIL"}' for i,x in enumerate(checks,1)));print(f'BROKER_INTENT_R4_SELF_TESTS={sum(checks)}/{len(checks)}');return all(checks)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--self-test',action='store_true');a=p.parse_args();raise SystemExit(0 if a.self_test and self_test() else 1)
