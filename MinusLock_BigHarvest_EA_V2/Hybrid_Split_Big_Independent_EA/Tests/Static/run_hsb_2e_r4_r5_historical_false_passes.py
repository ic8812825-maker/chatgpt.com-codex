#!/usr/bin/env python3
"""Execute all 19 published historical false-pass classes against R5 blockers."""
import argparse,copy,json,sys
from pathlib import Path
def run(root):
 root=Path(root).resolve();sys.path.insert(0,str(root/'Tests/Reference'));from hsb_2e_test_fixtures_r4_r5 import scenario_input;from hsb_2e_reference_model_r4_r5 import execute_scenario;from hsb_2e_provenance_model_r4_r5 import D,digest
 evidence=[]
 for version in ('R2','R3','R4'):
  d=json.loads((root/f'Tests/Evidence/HSB_2E_PREP_R4_{version}_FALSE_PASS_REPRODUCTION.json').read_text())
  for case in d['cases']:evidence.append((version,case))
 rows=[]
 for n,(version,case) in enumerate(evidence):
  desc=str(case.get('MUTATED_FIELDS',case.get('CHANGED_FIELDS',case.get('ROOT_CAUSE','')))).lower();x=scenario_input('BIG')
  if 'initial' in desc or version=='R2' and n%4==1:x=scenario_input('INITIAL','-1')
  elif 'missing' in desc:x['positions']=x['positions'][:1];x['intents']=x['intents'][:1];x['dealRecords']=x['dealRecords'][:1];x['priceProofs']=x['priceProofs'][:1]
  elif 'duplicate deal' in desc:x['dealRecords'].append(copy.deepcopy(x['dealRecords'][0]))
  elif 'timestamp' in desc:object.__setattr__(x['dealRecords'][0],'dealTimestamp',1);object.__setattr__(x['dealRecords'][0],'recordDigest',digest(x['dealRecords'][0].body()))
  elif 'foreign intent' in desc:x['intents'].append(copy.deepcopy(x['intents'][0]))
  elif 'foreign' in desc:object.__setattr__(x['dealRecords'][0],'symbol','GBPUSD');object.__setattr__(x['dealRecords'][0],'recordDigest',digest(x['dealRecords'][0].body()))
  elif 'off-grid' in desc:object.__setattr__(x['dealRecords'][0],'volume',D('1.005'));object.__setattr__(x['dealRecords'][0],'recordDigest',digest(x['dealRecords'][0].body()))
  elif 'price=-1' in desc:object.__setattr__(x['dealRecords'][0],'price',D(-1));object.__setattr__(x['dealRecords'][0],'recordDigest',digest(x['dealRecords'][0].body()))
  elif 'confirmed=' in desc:object.__setattr__(x['dealRecords'][0],'confirmed','false');object.__setattr__(x['dealRecords'][0],'recordDigest',digest(x['dealRecords'][0].body()))
  elif 'intent' in desc:x['intents'].append(copy.deepcopy(x['intents'][0]))
  elif 'revision' in desc:x['context']['stateRevision']=-5
  elif 'binding' in desc or 'registry' in desc:x['persistedState']['cumulativeFills']={'101':'1'}
  elif 'partial' in desc or 'volume' in desc:
   r=x['dealRecords'][0];object.__setattr__(r,'volume',r.volume/2);object.__setattr__(r,'recordDigest',digest(r.body()))
  else:x['persistedState']['cumulativeFills']={'101':'1'}
  actual=execute_scenario(x);blocked=actual['status']!='PASS' and not actual.get('settlementApplied') and not actual.get('allocationApplied')
  rows.append({'historicalVersion':version,'counterexampleId':case.get('COUNTEREXAMPLE_ID',case.get('CASE_ID')),'executed':True,'r4R5Status':actual['status'],'reason':actual['reason'],'settlementApplied':actual.get('settlementApplied',False),'allocationApplied':actual.get('allocationApplied',False),'blocked':blocked})
 out={'HISTORICAL_FALSE_PASSES_REQUIRED':len(rows),'HISTORICAL_FALSE_PASSES_EXECUTED':len(rows),'HISTORICAL_FALSE_PASSES_BLOCKED':sum(r['blocked'] for r in rows),'rows':rows};out['RESULT']='PASS' if out['HISTORICAL_FALSE_PASSES_BLOCKED']==len(rows) else 'FAIL';print(json.dumps(out,sort_keys=True,separators=(',',':')));return out['RESULT']=='PASS'
if __name__=='__main__':p=argparse.ArgumentParser();p.add_argument('--root',required=True);a=p.parse_args();raise SystemExit(0 if run(a.root) else 1)
