#!/usr/bin/env python3
"""Build corrected R6 schema/Registry/fixtures from the preserved R5 contour."""
import copy,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'Tests/Static'))
import verify_hsb_2e_r4_r9_r4a_r5 as v5
from build_hsb_2e_r4_r9_r4a_r5_assets import recert,digest
SCHEMA=ROOT/'Tests/Contracts/HSB_2E_R4_R9_R4A_R6_SCHEMA.json';REG=ROOT/'Tests/Contracts/HSB_2E_R4_R9_R4A_R6_PREDICATE_REGISTRY.json';VEC=ROOT/'Tests/Vectors/HSB_2E_R4_R9_R4A_R6_POSITIVE_BASES.json'
def schema():
 s=json.loads((ROOT/'Tests/Contracts/HSB_2E_R4_R9_R4A_R5_SCENARIO_INPUT_SCHEMA_V3_1.json').read_text());s['schemaId']='HSBI_ScenarioInput_R6';s['schemaVersion']='3.2.0';s['root']['properties']['schemaVersion']['enum']=['3.2.0'];return s
def fix(r):
 r=copy.deepcopy(r);r['schemaVersion']='3.2.0';main=r['positions'][0]
 for d in (r['deals'] if 'deals'in r else []):d['price']=r['broker']['bid'] if main['direction']=='BUY' else r['broker']['ask']
 for e in (r['events'] if 'events'in r else []):
  d=next(x for x in r['deals'] if x['dealId']==e['dealId']);e['price']=d['price']
 r['economic']['tailCount']=1 if r['persistedState']['farState']['active'] else 0
 if r['phase']=='REPLAY':
  historical_before=r['fsm']['inputRevision'];historical_after=r['fsm']['outputRevision'];current=historical_after;r['fsm']['inputRevision']=current;r['fsm']['outputRevision']=current;r['persistedState']['stateRevision']=current
  r['persistedState']['consumedDealIds']=[d['dealId'] for d in r['deals']];r['persistedState']['seenEventIds']=[e['eventId'] for e in r['events']];r['persistedState']['dealEventBindings']=[{'dealId':e['dealId'],'eventId':e['eventId']} for e in r['events']]
  r['replayContract']={'historicalRevisionBefore':historical_before,'historicalRevisionAfter':historical_after,'currentRevisionBefore':current,'currentRevisionAfter':current,'reserveBefore':r['persistedState']['reserve'],'reserveAfter':r['persistedState']['reserve'],'farBefore':copy.deepcopy(r['persistedState']['farState']),'farAfter':copy.deepcopy(r['persistedState']['farState']),'consumedDealIdsBefore':list(r['persistedState']['consumedDealIds']),'consumedDealIdsAfter':list(r['persistedState']['consumedDealIds'])}
 recert(r);return r
def body(r,state,revision):return {'identity':{k:r['context'][k] for k in ('accountId','symbol','magic','cycleId')},'fsmState':state,'revision':revision,'positions':r['positions'],'farState':r['persistedState']['farState'],'reserve':r['persistedState']['reserve'],'consumedDealIds':list(r['persistedState']['consumedDealIds']) if 'consumedDealIds'in r['persistedState'] else [],'seenEventIds':list(r['persistedState']['seenEventIds']) if 'seenEventIds'in r['persistedState'] else [],'ledger':{'previousStateDigest':r['persistedState']['previousStateDigest'],'authoritativeLedgerRoot':r['persistedState']['authoritativeLedgerRoot'],'transactionJournalRoot':r['persistedState']['transactionJournalRoot']}}
def state(r,state_name,revision):
 b=body(r,state_name,revision);return {'stateBody':b,'stateDigest':digest(b)}
def lifecycle(seq):
 seq=copy.deepcopy(seq);steps=seq['steps']
 for step in steps:step['operationInput']=fix(step['operationInput'])
 for i in range(1,len(steps)):
  prev=steps[i-1]['operationInput'];cur=steps[i]['operationInput'];cur['context']['cycleId']=prev['context']['cycleId']
  for coll in ('positions','deals','events'):
   for x in (cur[coll] if coll in cur else []):x['cycleId']=cur['context']['cycleId']
  cur['fsm']['inputState']=prev['fsm']['outputState'];cur['fsm']['inputRevision']=prev['fsm']['outputRevision'];cur['fsm']['outputRevision']=cur['fsm']['inputRevision'] if cur['phase']=='REPLAY' else cur['fsm']['inputRevision']+1
  if cur['phase']=='REPLAY':cur['replayContract']['currentRevisionBefore']=cur['fsm']['inputRevision'];cur['replayContract']['currentRevisionAfter']=cur['fsm']['outputRevision']
  recert(cur)
 for i,step in enumerate(steps):
  r=step['operationInput'];step['inputState']=state(r,r['fsm']['inputState'],r['fsm']['inputRevision'])
  if i+1<len(steps):n=steps[i+1]['operationInput'];step['declaredOutputState']=state(n,n['fsm']['inputState'],n['fsm']['inputRevision'])
  else:step['declaredOutputState']=state(r,r['fsm']['outputState'],r['fsm']['outputRevision'])
 return seq
def main():
 s=schema();SCHEMA.write_text(json.dumps(s,indent=2,sort_keys=True)+'\n');reg=json.loads((ROOT/'Tests/Contracts/HSB_2E_R4_R9_R4A_R5_PREDICATE_REGISTRY.json').read_text());reg['schemaVersion']='3.2.0';reg['schemaRef']=str(SCHEMA.relative_to(ROOT));REG.write_text(json.dumps(reg,indent=2,sort_keys=True)+'\n')
 fs=[]
 for f in v5.fixtures():
  g=copy.deepcopy(f)
  if 'lifecycleSequence'in g:g['lifecycleSequence']=lifecycle(g['lifecycleSequence'])
  else:g['scenarioInput']=fix(g['scenarioInput'])
  fs.append(g)
 VEC.write_text(json.dumps({'schemaVersion':'3.2.0','fixtures':fs},indent=2,sort_keys=True)+'\n');print(len(fs))
if __name__=='__main__':main()
