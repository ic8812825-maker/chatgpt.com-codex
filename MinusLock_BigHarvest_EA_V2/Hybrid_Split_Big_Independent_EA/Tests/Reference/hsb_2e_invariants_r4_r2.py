#!/usr/bin/env python3
import argparse
from decimal import Decimal
D=lambda x:Decimal(str(x))
def fill(o,ticket=None):
 f=o['fills'];return f[str(ticket)] if ticket is not None else next(iter(f.values()))
def check(name,inp,actual):
 o=actual.get('output',{})
 try:
  rules={'NO_FALSE_FULL_CLOSE':lambda:actual['status']!='PASS' or all(x['fillState']=='FULL_FILL' for x in o['fills'].values()),'NO_SETTLEMENT_BEFORE_FULL_FILL':lambda:not o.get('settlementApplied') or all(x['fillState']=='FULL_FILL' for x in o['fills'].values()),'NO_ALLOCATION_BEFORE_FULL_FILL':lambda:not o.get('allocationApplied') or all(x['fillState']=='FULL_FILL' for x in o['fills'].values()),'NO_DUPLICATE_DEAL_CONSUMPTION':lambda:len(o.get('consumedDealIds',[]))==len(set(o.get('consumedDealIds',[]))),'NO_CROSS_TICKET_VOLUME_NETTING':lambda:all(D(x['confirmedVolume'])<=D(x['requestedVolume']) or x['fillState']=='OVERFILL' for x in o['fills'].values()),'NO_DUAL_TAIL':lambda:inp.get('dualTail') is not True or actual['status']!='PASS','MONEY_CONSERVATION':lambda:actual['status']!='PASS' or D(o['totalMoney'])==sum((D(x['money']) for x in o['fills'].values()),D(0)),'VOLUME_CONSERVATION':lambda:all(D(x['requestedVolume'])==D(x['confirmedVolume'])+D(x['remainingVolume'])-D(x['overfillVolume']) for x in o['fills'].values()),'RESTART_FILL_CONSERVATION':lambda:actual['phase']!='RESTART_FULL_FILL_RECOVERED' or all(x['fillState']=='FULL_FILL' for x in o['fills'].values()),'PERSISTENCE_BEFORE_MUTATION':lambda:not o.get('settlementApplied') or 'SETTLEMENT_PERSISTED' in actual['persistenceRecords'],'STATE_REVISION_MONOTONIC':lambda:not o.get('settlementApplied') or D(o['stateRevision'])==D(inp['context']['stateRevision'])+1}
  return None if name not in rules else bool(rules[name]())
 except (KeyError,TypeError):return False
def self_test():
 a={'status':'UNAVAILABLE','phase':'WAITING_FOR_FULL_FILL','output':{'fills':{'1':{'fillState':'PARTIAL_FILL','requestedVolume':'1','confirmedVolume':'.4','remainingVolume':'.6','overfillVolume':'0','consumedDealIds':['D'],'money':'1'}},'settlementApplied':False,'allocationApplied':False,'consumedDealIds':['D']},'persistenceRecords':['CUMULATIVE_FILL_PERSISTED']};checks=[check('NO_SETTLEMENT_BEFORE_FULL_FILL',{},a),check('VOLUME_CONSERVATION',{},a),check('UNKNOWN',{},a) is None];print('\n'.join(f'R4R2_INV_{i}={"PASS" if x else "FAIL"}' for i,x in enumerate(checks,1)));print(f'INVARIANTS_R4_R2_SELF_TESTS={sum(checks)}/{len(checks)}');return all(checks)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--self-test',action='store_true');a=p.parse_args();raise SystemExit(0 if a.self_test and self_test() else 1)
