#!/usr/bin/env python3
"""Independent conservation/ownership invariants; no reference-model imports."""
from decimal import Decimal,InvalidOperation
import argparse,hashlib,json
D=lambda x:Decimal(str(x))
def check(name,data):
 try:
  if name=='money_conservation':return abs(D(data['source'])-sum(D(data[k]) for k in ('partialFar','reserve','other','remainder')))<=D(data['tolerance']) and D(data['remainder'])>=0
  if name=='volume_conservation':return abs(D(data['before'])-D(data['closed'])-D(data['remaining']))<=D(data['tolerance'])
  if name=='reserve_nonnegative':return D(data['reserve'])>=0
  if name=='partial_far_reserve_isolation':return D(data['reserveUsed'])==0
  if name=='initial_profit_ignored':return D(data['budgetWithInitial'])==D(data['budgetWithoutInitial'])
  if name=='new_far_compression':return D(data['newFar'])<D(data['oldFar'])
  if name=='ownership':return all(data.get(k) not in (None,'',0) for k in ('accountLogin','symbol','magic','cycleId','ticket'))
  if name=='unique_keys':return len(data['keys'])==len(set(data['keys']))
  if name=='revision_monotonic':return int(data['after'])>=int(data['before'])
  if name=='persistence_before_mutation':return data['persisted'] is True or data['mutated'] is False
  if name=='final_close_gates':return not data['closeFar'] or (D(data['recoveryPL'])>0 and data['actualDeals'] and D(data['coverage'])>=0)
  if name=='no_dual_tail':return not data['dualTail']
  if name=='no_intent_on_failure':return data['status']=='PASS' or not data['intents']
  if name=='deterministic_digest':return data['digestA']==data['digestB']
 except (KeyError,InvalidOperation,ValueError):return False
 return False
def self_test():
 samples={'money_conservation':{'source':'10','partialFar':'4','reserve':'2','other':'1','remainder':'3','tolerance':'0.01'},'volume_conservation':{'before':'1','closed':'0.4','remaining':'0.6','tolerance':'0.0001'},'reserve_nonnegative':{'reserve':'0'},'partial_far_reserve_isolation':{'reserveUsed':'0'},'initial_profit_ignored':{'budgetWithInitial':'5','budgetWithoutInitial':'5'},'new_far_compression':{'newFar':'0.5','oldFar':'1'},'ownership':{'accountLogin':1,'symbol':'EURUSD','magic':2,'cycleId':3,'ticket':4},'unique_keys':{'keys':[1,2]},'revision_monotonic':{'before':2,'after':3},'persistence_before_mutation':{'persisted':True,'mutated':True},'final_close_gates':{'closeFar':True,'recoveryPL':'1','actualDeals':True,'coverage':'0'},'no_dual_tail':{'dualTail':False},'no_intent_on_failure':{'status':'REJECT','intents':[]},'deterministic_digest':{'digestA':'x','digestB':'x'}}
 ok={k:check(k,v) for k,v in samples.items()};print('\n'.join(f'INV_{k}={"PASS" if v else "FAIL"}' for k,v in ok.items()));print(f'INVARIANT_SELF_TESTS={sum(ok.values())}/{len(ok)}');return all(ok.values())
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--self-test',action='store_true');a=p.parse_args();raise SystemExit(0 if a.self_test and self_test() else 1)
