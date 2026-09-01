#!/usr/bin/env python3
"""Build R7 inputs without changing historical R4-R6 artifacts."""
import copy,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'Tests/Static'))
import verify_hsb_2e_r4_r9_r4a_r6 as v6
from build_hsb_2e_r4_r9_r4a_r5_assets import digest
SCHEMA=ROOT/'Tests/Contracts/HSB_2E_R4_R9_R4A_R7_SCHEMA.json';VEC=ROOT/'Tests/Vectors/HSB_2E_R4_R9_R4A_R7_POSITIVE_BASES.json'
def cert(s):
 body={'broker':s['brokerProposal'],'economic':s['economic'],'allocation':s['allocationPolicy'],'persisted':s['persistedState'],'fsm':s['fsm'],'output':s['fsm']['outputState'],'identity':s['context']}
 c={'version':7,'body':digest(body),'previousStateDigest':s['persistedState']['previousStateDigest'],'authoritativeLedgerRoot':s['persistedState']['authoritativeLedgerRoot'],'transactionJournalRoot':s['persistedState']['transactionJournalRoot'],'claimedBrokerDigest':digest(s['brokerProposal']),'claimedEconomicDigest':digest(s['economic']),'claimedAllocationDigest':digest(s['allocationPolicy']),'claimedPersistenceDigest':digest(s['persistedState']),'claimedFsmDigest':digest(s['fsm']),'claimedOutputStateDigest':digest(s['fsm']['outputState']),'operationIdentityDigest':digest(s['context']),'inputRevision':s['fsm']['inputRevision'],'outputRevision':s['fsm']['outputRevision']};c['digest']=digest(c);return c
def state_body(r,fsm,rev):return {'identity':{k:r['context'][k] for k in ('accountId','symbol','magic','cycleId')},'fsmState':fsm,'revision':rev,'positions':copy.deepcopy(r['positions']),'farState':copy.deepcopy(r['persistedState']['farState']),'reserve':r['persistedState']['reserve'],'consumedDealIds':copy.deepcopy(r['persistedState'].get('consumedDealIds',[])),'seenEventIds':copy.deepcopy(r['persistedState'].get('seenEventIds',[])),'ledger':{k:r['persistedState'][k] for k in ('previousStateDigest','authoritativeLedgerRoot','transactionJournalRoot')}}
def state(r,fsm,rev):b=state_body(r,fsm,rev);return {'stateBody':b,'stateDigest':digest(b)}
def infer(x,required=True):
 base={'required':required,'nullable':False,'requiredState':'REQUIRED' if required else 'OPTIONAL_WITH_RULE','unit':'NONE','applicableScenarios':['REPLAY_COMMITTED']}
 if isinstance(x,dict):base.update({'type':'object','additionalProperties':False,'properties':{k:infer(v) for k,v in x.items()}})
 elif isinstance(x,list):base.update({'type':'array','items':infer(x[0]) if x else {'type':'string','required':True,'nullable':False,'requiredState':'REQUIRED','unit':'NONE','applicableScenarios':['REPLAY_COMMITTED']}})
 elif isinstance(x,bool):base['type']='boolean'
 elif isinstance(x,int):base['type']='integer'
 else:base['type']='string'
 return base
def replay(r):
 q=r['replayContract'];hb,ha=q['historicalRevisionBefore'],q['historicalRevisionAfter'];historical=copy.deepcopy(r);historical.pop('replayContract',None);historical['fsm']['inputRevision']=hb;historical['fsm']['outputRevision']=ha
 q['ledgerBefore']={k:r['persistedState'][k] for k in ('previousStateDigest','authoritativeLedgerRoot','transactionJournalRoot')};q['ledgerAfter']=copy.deepcopy(q['ledgerBefore'])
 r['replayContract']['historicalSourceObjects']={'brokerProposal':historical['brokerProposal'],'economic':historical['economic'],'allocationPolicy':historical['allocationPolicy'],'persistedState':historical['persistedState'],'fsm':historical['fsm'],'context':historical['context']}
 r['certificate']=cert(historical);return r
def lifecycle(seq):
 seq=copy.deepcopy(seq);steps=seq['steps']
 for st in steps:
  r=st['operationInput'];r['schemaVersion']='3.3.0'
  if r['phase']=='REPLAY':replay(r)
 for i,st in enumerate(steps):
  r=st['operationInput'];st['inputState']=state(r,r['fsm']['inputState'],r['fsm']['inputRevision'])
  replay_ids=None
  if i+1<len(steps) and steps[i+1]['operation']=='REPLAY':
   nxt=steps[i+1]['operationInput'];replay_ids=({d['dealId'] for d in nxt['deals']},{e['eventId'] for e in nxt['events']})
  outrev=r['fsm']['inputRevision'] if st['operation']=='REPLAY' else r['fsm']['inputRevision']+1;outbody=state_body(r,r['fsm']['outputState'],outrev)
  if replay_ids:outbody['consumedDealIds']=sorted(set(outbody['consumedDealIds'])|replay_ids[0]);outbody['seenEventIds']=sorted(set(outbody['seenEventIds'])|replay_ids[1])
  st['declaredOutputState']={'stateBody':outbody,'stateDigest':digest(outbody)}
  if i+1<len(steps):
   n=steps[i+1]['operationInput'];b=st['declaredOutputState']['stateBody'];n['context'].update(b['identity']);n['fsm']['inputState']=b['fsmState'];n['fsm']['inputRevision']=b['revision'];n['fsm']['outputRevision']=b['revision'] if steps[i+1]['operation']=='REPLAY' else b['revision']+1;n['positions']=copy.deepcopy(b['positions']);n['persistedState']['farState']=copy.deepcopy(b['farState']);n['persistedState']['reserve']=b['reserve'];n['persistedState']['previousStateDigest']=b['ledger']['previousStateDigest'];n['persistedState']['authoritativeLedgerRoot']=b['ledger']['authoritativeLedgerRoot'];n['persistedState']['transactionJournalRoot']=b['ledger']['transactionJournalRoot']
   n['persistedState']['stateRevision']=n['fsm']['inputRevision']
   if 'consumedDealIds'in n['persistedState']:n['persistedState']['consumedDealIds']=copy.deepcopy(b['consumedDealIds']);n['persistedState']['seenEventIds']=copy.deepcopy(b['seenEventIds'])
   main=next((p for p in n['positions'] if p['role']!='FAR'),n['positions'][0])
   n['economic']['tailCount']=1 if n['persistedState']['farState']['active'] else 0
   for it in n['intents']:it['positionTicket']=main['ticket'];it['role']=main['role'];it['direction']='SELL' if main['direction']=='BUY' else 'BUY'
   for d in (n['deals'] if 'deals'in n else []):d['positionTicket']=main['ticket'];d['role']=main['role'];d['direction']=n['intents'][0]['direction'];d['price']=n['broker']['bid'] if main['direction']=='BUY' else n['broker']['ask']
   for e in (n['events'] if 'events'in n else []):
    d=next(d for d in n['deals'] if d['dealId']==e['dealId']);e.update({k:d[k] for k in ('positionTicket','role','direction','price')})
   if n['phase']=='REPLAY':n['replayContract']['currentRevisionBefore']=b['revision'];n['replayContract']['currentRevisionAfter']=b['revision'];n['replayContract']['consumedDealIdsBefore']=copy.deepcopy(n['persistedState']['consumedDealIds']);n['replayContract']['consumedDealIdsAfter']=copy.deepcopy(n['persistedState']['consumedDealIds']);replay(n)
   else:n['certificate']=cert(n)
 return seq
def main():
 fs=copy.deepcopy(v6.fixtures())
 for f in fs:
  if 'lifecycleSequence'in f:f['lifecycleSequence']=lifecycle(f['lifecycleSequence'])
  else:
   r=f['scenarioInput'];r['schemaVersion']='3.3.0'
   if r['phase']=='REPLAY':
    if not any(x.startswith('HISTORY-') for x in r['persistedState']['consumedDealIds']):r['persistedState']['consumedDealIds'].append('HISTORY-DEAL');r['persistedState']['seenEventIds'].append('HISTORY-EVENT');r['persistedState']['dealEventBindings'].append({'dealId':'HISTORY-DEAL','eventId':'HISTORY-EVENT'});r['replayContract']['consumedDealIdsBefore']=copy.deepcopy(r['persistedState']['consumedDealIds']);r['replayContract']['consumedDealIdsAfter']=copy.deepcopy(r['persistedState']['consumedDealIds'])
    replay(r)
 s=json.loads((ROOT/'Tests/Contracts/HSB_2E_R4_R9_R4A_R6_SCHEMA.json').read_text());s['schemaId']='HSBI_ScenarioInput_R7';s['schemaVersion']='3.3.0';s['root']['properties']['schemaVersion']['enum']=['3.3.0'];sample=next(f['scenarioInput']['replayContract'] for f in fs if 'scenarioInput'in f and f['scenarioInput']['phase']=='REPLAY');s['root']['properties']['replayContract']=infer(sample,False);s['root']['properties']['replayContract']['requiredWhen']="phase == 'REPLAY'";s['root']['properties']['replayContract']['forbiddenWhen']="phase != 'REPLAY'";SCHEMA.write_text(json.dumps(s,indent=2,sort_keys=True)+'\n')
 VEC.write_text(json.dumps({'schemaVersion':'3.3.0','fixtures':fs},indent=2,sort_keys=True)+'\n');print(len(fs))
if __name__=='__main__':main()
