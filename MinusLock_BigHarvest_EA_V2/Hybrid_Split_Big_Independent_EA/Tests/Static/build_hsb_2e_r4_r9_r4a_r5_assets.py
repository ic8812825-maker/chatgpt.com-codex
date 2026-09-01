#!/usr/bin/env python3
"""Build the versioned R5 schema, Registry and 28 corrected positive bases."""
from __future__ import annotations
import copy, hashlib, json
from decimal import Decimal
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
R4_SCHEMA=ROOT/'Tests/Contracts/HSB_2E_R4_R9_R4A_R4_SCENARIO_INPUT_SCHEMA_V3.json'
R4_REGISTRY=ROOT/'Tests/Contracts/HSB_2E_R4_R9_R4_PREDICATE_REGISTRY.json'
SCHEMA=ROOT/'Tests/Contracts/HSB_2E_R4_R9_R4A_R5_SCENARIO_INPUT_SCHEMA_V3_1.json'
REGISTRY=ROOT/'Tests/Contracts/HSB_2E_R4_R9_R4A_R5_PREDICATE_REGISTRY.json'
VECTORS=ROOT/'Tests/Vectors/HSB_2E_R4_R9_R4A_R5_POSITIVE_BASES.json'
SCENARIOS=('INITIAL','BIG','SMALL','FINAL','RESTART_CONTINUATION','REPLAY_COMMITTED')
def canon(v): return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def digest(v): return hashlib.sha256(canon(v).encode()).hexdigest()
def schema():
 s=json.loads(R4_SCHEMA.read_text());s['schemaId']='HSBI_ScenarioInput_V3_1_R5';s['schemaVersion']='3.1.0';p=s['root']['properties'];p['schemaVersion']['enum']=['3.1.0']
 p['phase']={'type':'string','requiredState':'REQUIRED','required':True,'nullable':False,'unit':'NONE','enum':['PRE_COMMIT','COMMITTED','REPLAY'],'applicableScenarios':list(SCENARIOS)}
 cert=p['certificate'];cert['requiredState']='OPTIONAL_WITH_RULE';cert['required']=False;cert['applicabilityRuleId']='CERTIFICATE_BY_PHASE';cert['requiredWhen']="phase IN ['COMMITTED','REPLAY']";cert['forbiddenWhen']="phase == 'PRE_COMMIT'";cert['optionalWhen']='NEVER'
 digest_spec=copy.deepcopy(cert['properties']['digest']); revision_spec=copy.deepcopy(p['fsm']['properties']['inputRevision'])
 cert['properties']['operationIdentityDigest']=copy.deepcopy(digest_spec);cert['properties']['inputRevision']=copy.deepcopy(revision_spec);cert['properties']['outputRevision']=copy.deepcopy(revision_spec)
 far=p['persistedState']['properties']['farState'];far['properties']['active']={'type':'boolean','requiredState':'REQUIRED','required':True,'nullable':False,'unit':'NONE','applicableScenarios':list(SCENARIOS)}
 far['properties']['direction']={'type':'string','requiredState':'OPTIONAL_WITH_RULE','required':False,'nullable':False,'unit':'NONE','enum':['BUY','SELL'],'applicableScenarios':list(SCENARIOS),'applicabilityRuleId':'ACTIVE_FAR','requiredWhen':'farState.active == true','forbiddenWhen':'farState.active == false','optionalWhen':'NEVER'}
 for k in ('ticket','volume','loss'):
  far['properties'][k]['requiredState']='OPTIONAL_WITH_RULE';far['properties'][k]['required']=False;far['properties'][k]['applicabilityRuleId']='ACTIVE_FAR';far['properties'][k]['requiredWhen']='farState.active == true';far['properties'][k]['forbiddenWhen']='farState.active == false';far['properties'][k]['optionalWhen']='NEVER'
 s['phaseContract']={
  'PRE_COMMIT':{'certificate':'FORBIDDEN','executionEvidence':'FORBIDDEN','consumedRegistries':'FORBIDDEN','revisions':'REQUIRED','activeFar':'STATE_DEPENDENT','currentAndNextState':'REQUIRED'},
  'COMMITTED':{'certificate':'REQUIRED','executionEvidence':'REQUIRED','consumedRegistries':'OPTIONAL','revisions':'REQUIRED','activeFar':'STATE_DEPENDENT','currentAndNextState':'REQUIRED'},
  'REPLAY':{'certificate':'REQUIRED','executionEvidence':'REQUIRED','consumedRegistries':'REQUIRED','revisions':'REQUIRED','activeFar':'STATE_DEPENDENT','currentAndNextState':'REQUIRED'},
 }
 s['lifecycleContainer']={'requiredFields':['sequenceId','steps'],'stepRequiredFields':['operation','inputState','operationInput','declaredOutputState'],'stateRequiredFields':['fsmState','revision','cycleId','stateDigest'],'continuityRule':'next.inputState == previous.declaredOutputState','nativeModelExecution':False}
 return s
def load_r4():
 out=[]
 for p in sorted((ROOT/'Tests/Vectors').glob('HSB_2E_R4_R9_R4A_R4_POSITIVE_BASES_V3_*.json')): out+=json.loads(p.read_text())['fixtures']
 return out
def recert(r):
 if r['phase']=='PRE_COMMIT': r.pop('certificate',None);return
 bp,e,a,p,f=r['brokerProposal'],r['economic'],r['allocationPolicy'],r['persistedState'],r['fsm']
 body={'broker':bp,'economic':e,'allocation':a,'persisted':p,'fsm':f,'output':f['outputState'],'identity':r['context']}
 c={'version':5,'body':digest(body),'previousStateDigest':p['previousStateDigest'],'authoritativeLedgerRoot':p['authoritativeLedgerRoot'],'transactionJournalRoot':p['transactionJournalRoot'],'claimedBrokerDigest':digest(bp),'claimedEconomicDigest':digest(e),'claimedAllocationDigest':digest(a),'claimedPersistenceDigest':digest(p),'claimedFsmDigest':digest(f),'claimedOutputStateDigest':digest(f['outputState']),'operationIdentityDigest':digest(r['context']),'inputRevision':f['inputRevision'],'outputRevision':f['outputRevision']}
 c['digest']=digest(c);r['certificate']=c
def sync_event(r):
 for d in r['deals']:
  for e in r['events']:
   if e['dealId']==d['dealId']:
    for k in ('intentId','positionTicket','accountId','symbol','magic','cycleId','transactionId','actionId','role','direction','volume','price','commission','swap','fee','timestamp','stateRevision','snapshotRevision','confirmed'):e[k]=d[k]
def transform(item,variant):
 r=copy.deepcopy(item['scenarioInput']);r['schemaVersion']='3.1.0';scenario=r['scenario'];r['phase']='REPLAY' if scenario=='REPLAY_COMMITTED' else ('PRE_COMMIT' if scenario=='INITIAL' and variant==1 else 'COMMITTED')
 # Four computed boundary forms per group.
 if variant==2:
  vol='0.01';r['broker']['volumeMin']=vol;r['positions'][0]['volume']=vol;r['positions'][0]['authoritativeVolume']=vol;r['intents'][0]['requestedVolume']=vol;r['deals'][0]['volume']=vol;r['deals'][0]['commission']='-2';r['deals'][0]['swap']='-1';r['deals'][0]['fee']='-0.5'
 if variant==3:
  r['broker']['tickSize']='0.0005';r['broker']['point']='0.0001';base=Decimal(r['broker']['bid']);aligned=(base/Decimal('0.0005')).quantize(Decimal('1'))*Decimal('0.0005');price=f'{aligned:.4f}';r['broker']['bid']=price;r['broker']['ask']=f'{aligned+Decimal("0.0005"):.4f}';r['positions'][0]['openPrice']=price;r['deals'][0]['price']=price
  total=Decimal(r['intents'][0]['requestedVolume']);first=Decimal('0.05');second=total-first;r['deals'][0]['volume']=f'{first:.2f}';d2=copy.deepcopy(r['deals'][0]);d2['dealId']+='-B';d2['eventId']+='-B';d2['volume']=f'{second:.2f}';d2['commission']='-0.75';r['deals'].append(d2);e2=copy.deepcopy(r['events'][0]);e2['dealId']=d2['dealId'];e2['eventId']=d2['eventId'];r['events'].append(e2)
 if variant==4:
  r['economic']['recoveryPL']='0.01';r['persistedState']['recoveryPL']='0.01';r['deals'][0]['commission']='-3';r['deals'][0]['swap']='-0.25';r['deals'][0]['fee']='-0.10'
 if r['phase']=='PRE_COMMIT':r['deals']=[];r['events']=[];r['persistedState']['consumedDealIds']=[];r['persistedState']['seenEventIds']=[];r['persistedState']['dealEventBindings']=[]
 active=scenario in ('BIG','SMALL','RESTART_CONTINUATION')
 if active:
  main=r['positions'][0];far=copy.deepcopy(main);far['ticket']=main['ticket']+'-FAR';far['role']='FAR';far['direction']='SELL' if main['direction']=='BUY' else 'BUY';far['volume']='0.05';far['authoritativeVolume']='0.05';r['positions'].append(far);r['persistedState']['farState']={'active':True,'ticket':far['ticket'],'volume':far['volume'],'loss':r['economic']['farActualLoss'],'direction':far['direction']}
 else:r['persistedState']['farState']={'active':False}
 r['persistedState']['cumulativeFills']=[{'ticket':r['positions'][0]['ticket'],'volume':r['intents'][0]['requestedVolume']}]
 r['persistedState']['moneyByDeal']=[{'key':d['dealId'],'value':str(abs(Decimal(d['commission'])+Decimal(d['swap'])+Decimal(d['fee'])))} for d in r['deals']]
 sync_event(r);recert(r);return r
def state(r,label=None):
 return {'fsmState':label or r['fsm']['inputState'],'revision':r['fsm']['inputRevision'],'cycleId':r['context']['cycleId'],'stateDigest':digest({'state':label or r['fsm']['inputState'],'revision':r['fsm']['inputRevision'],'cycleId':r['context']['cycleId']})}
def lifecycle(sequence_id,runtimes,ops):
 steps=[];current=state(runtimes[0])
 for i,(r,op) in enumerate(zip(runtimes,ops)):
  r=copy.deepcopy(r);r['context']['cycleId']=current['cycleId'];r['fsm']['inputState']=current['fsmState'];r['fsm']['inputRevision']=current['revision'];r['fsm']['outputRevision']=current['revision']+1;recert(r)
  out={'fsmState':r['fsm']['outputState'],'revision':r['fsm']['outputRevision'],'cycleId':current['cycleId'],'stateDigest':digest({'state':r['fsm']['outputState'],'revision':r['fsm']['outputRevision'],'cycleId':current['cycleId']})}
  steps.append({'operation':op,'inputState':current,'operationInput':r,'declaredOutputState':out});current=copy.deepcopy(out)
 return {'lifecycleSequence':{'sequenceId':sequence_id,'steps':steps},'testContract':{'fixtureId':sequence_id,'classification':'POSITIVE_BASE','scenario':'LIFECYCLE','expectedApplicability':{'DECLARED_CHAIN':True}}}
def main():
 s=schema();SCHEMA.write_text(json.dumps(s,indent=2,sort_keys=True)+'\n')
 reg=json.loads(R4_REGISTRY.read_text());reg['schemaVersion']='3.1.0';reg['schemaRef']=str(SCHEMA.relative_to(ROOT));
 for e in reg['predicates']:
  if 'scenarioInput.phase' not in e['exactInputPaths'] and e['predicateId'] in ('SCHEMA','CERTIFICATE_STRUCTURE','CERTIFICATE_PROVENANCE','CERTIFICATE_DIGEST','REPLAY_EXACTLY_ONCE'):e['exactInputPaths'].append('scenarioInput.phase')
 REGISTRY.write_text(json.dumps(reg,indent=2,sort_keys=True)+'\n')
 old=load_r4();by={(x['scenarioInput']['scenario'],int(x['testContract']['fixtureId'].rsplit('-',1)[1])):x for x in old if x['scenarioInput']['scenario']!='LIFECYCLE'}
 fixtures=[];runtime={}
 for sc in SCENARIOS:
  for v in range(1,5):
   r=transform(by[(sc,v)],v);runtime[(sc,v)]=r;fixtures.append({'scenarioInput':r,'testContract':{'fixtureId':f'R5-{sc}-{v}','classification':'POSITIVE_BASE','scenario':sc,'boundaryProperty':('PRE_COMMIT_PHASE' if r['phase']=='PRE_COMMIT' else ['STANDARD_BUY','MIN_VOLUME_COSTS','NONTRIVIAL_TICK_MULTI_FILL','POSITIVE_RECOVERY_EDGE'][v-1])}})
 fixtures += [
  lifecycle('R5-LIFECYCLE-1',[runtime[('INITIAL',2)],runtime[('BIG',2)],runtime[('FINAL',2)]],['INITIAL','BIG','FINAL']),
  lifecycle('R5-LIFECYCLE-2',[runtime[('INITIAL',3)],runtime[('SMALL',3)],runtime[('FINAL',3)]],['INITIAL','SMALL','FINAL']),
  lifecycle('R5-LIFECYCLE-3',[runtime[('INITIAL',4)],runtime[('RESTART_CONTINUATION',4)],runtime[('FINAL',4)]],['INITIAL','RESTART','FINAL']),
  lifecycle('R5-LIFECYCLE-4',[runtime[('FINAL',1)],runtime[('REPLAY_COMMITTED',1)]],['FINAL','REPLAY']),]
 VECTORS.write_text(json.dumps({'schemaVersion':'3.1.0','fixtures':fixtures},indent=2,sort_keys=True)+'\n');print(len(fixtures),sum(len(x['lifecycleSequence']['steps']) for x in fixtures if 'lifecycleSequence'in x))
if __name__=='__main__':main()
