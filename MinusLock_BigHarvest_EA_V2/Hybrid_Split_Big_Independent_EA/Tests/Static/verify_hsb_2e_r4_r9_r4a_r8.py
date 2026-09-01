#!/usr/bin/env python3
"""R8 fail-closed pipeline. Presented inputs are validated without mutation or resealing."""
import copy,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'Tests/Static'))
import verify_hsb_2e_r4_r9_r4a_r5 as v5
import verify_hsb_2e_r4_r9_r4a_r6 as v6
import verify_hsb_2e_r4_r9_r4a_r7 as v7
from build_hsb_2e_r4_r9_r4a_r5_assets import digest
from build_hsb_2e_r4_r9_r4a_r7_assets import state_body
SCHEMA=ROOT/'Tests/Contracts/HSB_2E_R4_R9_R4A_R8_SCHEMA.json';VECTORS=ROOT/'Tests/Vectors/HSB_2E_R4_R9_R4A_R8_POSITIVE_BASES.json'
NormativeError=v5.NormativeError
def reject(c,r,p):raise NormativeError(c,r,p)
def unique(rows,key,check,path):
 vals=[x[key] for x in rows]
 if len(vals)!=len(set(vals)):reject(check,'DUPLICATE_IDENTIFIER',path)
def references(r):
 ps={p['ticket']:p for p in r['positions']};ins={i['intentId']:i for i in r['intents']};ds={d['dealId']:d for d in r.get('deals',[])}
 unique(r['positions'],'ticket','R8_COLLECTION','positions');unique(r['intents'],'intentId','R8_COLLECTION','intents');unique(r.get('deals',[]),'dealId','R8_COLLECTION','deals');unique(r.get('events',[]),'eventId','R8_COLLECTION','events')
 for n,i in enumerate(r['intents']):
  if i['positionTicket'] not in ps:reject('R8_REFERENCE','INTENT_POSITION_NOT_FOUND',f'intents[{n}].positionTicket')
 for n,d in enumerate(r.get('deals',[])):
  if d['intentId'] not in ins:reject('R8_REFERENCE','DEAL_INTENT_NOT_FOUND',f'deals[{n}].intentId')
  if d['positionTicket'] not in ps:reject('R8_REFERENCE','DEAL_POSITION_NOT_FOUND',f'deals[{n}].positionTicket')
  if ins[d['intentId']]['positionTicket']!=d['positionTicket']:reject('R8_REFERENCE','DEAL_INTENT_POSITION_MISMATCH',f'deals[{n}]')
 for n,e in enumerate(r.get('events',[])):
  if e['dealId'] not in ds:reject('R8_REFERENCE','EVENT_DEAL_NOT_FOUND',f'events[{n}].dealId')
 return ps,ins,ds
def identity(r,ps,ins,ds):
 c=r['context']; owner=('accountId','symbol','magic','cycleId')
 for n,p in enumerate(r['positions']):
  if any(p[k]!=c[k] for k in owner):reject('R8_IDENTITY','POSITION_CONTEXT_MISMATCH',f'positions[{n}]')
 for n,i in enumerate(r['intents']):
  p=ps[i['positionTicket']]
  if i['transactionId']!=c['transactionId'] or i['actionId']!=c['actionId'] or any(i[k]!=p[k] for k in ('role','direction') if k!='direction'):
   reject('R8_IDENTITY','INTENT_BINDING_MISMATCH',f'intents[{n}]')
 for n,d in enumerate(r.get('deals',[])):
  i=ins[d['intentId']];p=ps[d['positionTicket']]
  if any(d[k]!=c[k] for k in owner+('transactionId','actionId')):reject('R8_IDENTITY','DEAL_CONTEXT_MISMATCH',f'deals[{n}]')
  if d['role']!=i['role'] or d['role']!=p['role']:reject('R8_IDENTITY','DEAL_ROLE_MISMATCH',f'deals[{n}]')
 for n,e in enumerate(r.get('events',[])):
  d=ds[e['dealId']]
  keys=('eventId','intentId','positionTicket','accountId','symbol','magic','cycleId','transactionId','actionId','role','direction','volume','price','commission','swap','fee','timestamp','stateRevision','snapshotRevision','confirmed')
  if any(e[k]!=d[k] for k in keys):reject('R8_IDENTITY','EVENT_DEAL_MISMATCH',f'events[{n}]')
def phase_revision(r):
 phase=r['phase'];deals=r.get('deals',[]);events=r.get('events',[]);cert=r.get('certificate')
 if phase=='PRE_COMMIT':
  if deals or events or cert is not None:reject('R8_PHASE','CURRENT_EXECUTION_EVIDENCE_FORBIDDEN', 'phase')
 elif phase=='COMMITTED':
  if not deals or not events or cert is None:reject('R8_PHASE','COMMIT_EVIDENCE_REQUIRED','phase')
  if r['fsm']['outputRevision']!=r['fsm']['inputRevision']+1:reject('R8_REVISION','COMMIT_INCREMENT_REQUIRED','fsm.outputRevision')
 else:
  q=r['replayContract'];h=q['historicalRevisionAfter']
  if r['fsm']['inputRevision']!=h or r['fsm']['outputRevision']!=h or r['persistedState']['stateRevision']!=h or q['currentRevisionBefore']!=h or q['currentRevisionAfter']!=h:reject('R8_REVISION','REPLAY_CURRENT_NOT_HISTORICAL_OUTPUT','replayContract')
def far(r,ps):
 f=r['persistedState']['farState'];owned=[p for p in r['positions'] if p['accountId']==r['context']['accountId'] and p['symbol']==r['context']['symbol'] and p['magic']==r['context']['magic'] and p['cycleId']==r['context']['cycleId']];fars=[p for p in owned if p['role']=='FAR']
 if len(fars)>1:reject('R8_FAR','MULTIPLE_ACTIVE_FAR','positions')
 if f['active']:
  if f['ticket'] not in ps:reject('R8_FAR','ACTIVE_FAR_TICKET_NOT_FOUND','persistedState.farState.ticket')
  p=ps[f['ticket']]
  if p not in fars:reject('R8_FAR','ACTIVE_FAR_POSITION_MISMATCH','persistedState.farState')
  if p['direction']!=f['direction'] or p['volume']!=f['volume']:reject('R8_FAR','ACTIVE_FAR_VALUE_MISMATCH','persistedState.farState')
def runtime(r):
 # No copy, normalization, deletion, defaulting or certificate reconstruction occurs here.
 schema=json.loads(SCHEMA.read_text());v5.node(r,schema['root'],'scenarioInput')
 ps,ins,ds=references(r);identity(r,ps,ins,ds);phase_revision(r);far(r,ps)
 # Retained R5-R7 primitives execute only after safe reference resolution.
 v6.temporal(r);v6.identity_direction(r);v6.far_tail(r)
 v7.runtime(r)
 return {'result':'PASS'}
OPS=v7.OPS;STATES=v7.STATES
def valid_state(s,p):return v7.valid_state(s,p)
def expected_output(st):
 r=st['operationInput'];rev=r['fsm']['inputRevision'] if st['operation']=='REPLAY' else r['fsm']['inputRevision']+1
 b=state_body(r,r['fsm']['outputState'],rev)
 if st['operation']!='REPLAY' and r.get('deals'):
  b['consumedDealIds']=sorted(set(b['consumedDealIds'])|{d['dealId'] for d in r['deals']})
  b['seenEventIds']=sorted(set(b['seenEventIds'])|{e['eventId'] for e in r['events']})
 return b
def lifecycle(seq):
 if set(seq)!={'sequenceId','steps'}:reject('R8_LIFECYCLE','SEQUENCE_SHAPE_MISMATCH','lifecycleSequence')
 steps=seq['steps']
 if len(steps)<2:reject('R8_LIFECYCLE','SEQUENCE_TOO_SHORT','steps')
 for i,st in enumerate(steps):
  if set(st)!={'operation','inputState','operationInput','declaredOutputState'}:reject('R8_LIFECYCLE','STEP_SHAPE_MISMATCH',f'steps[{i}]')
  if st['operation'] not in OPS:reject('R8_LIFECYCLE','UNKNOWN_OPERATION',f'steps[{i}].operation')
  r=st['operationInput'];runtime(r)
  if r['scenario']!=OPS[st['operation']]:reject('R8_LIFECYCLE','OPERATION_SCENARIO_MISMATCH',f'steps[{i}]')
  valid_state(st['inputState'],f'steps[{i}].inputState');valid_state(st['declaredOutputState'],f'steps[{i}].declaredOutputState')
  if st['inputState']['stateBody']!=state_body(r,r['fsm']['inputState'],r['fsm']['inputRevision']):reject('R8_LIFECYCLE','INPUT_BINDING_MISMATCH',f'steps[{i}]')
  if st['declaredOutputState']['stateBody']!=expected_output(st):reject('R8_LIFECYCLE','OUTPUT_BINDING_MISMATCH',f'steps[{i}]')
  if i and st['inputState']!=steps[i-1]['declaredOutputState']:reject('R8_LIFECYCLE','CHAIN_DISCONTINUITY',f'steps[{i}]')
  if st['operation']=='REPLAY' and st['declaredOutputState']!=st['inputState']:reject('R8_LIFECYCLE','REPLAY_STATE_MUTATION',f'steps[{i}]')
 return {'steps':len(steps),'declaredChainValidated':True,'executedByNativeModel':False}
def fixtures():return json.loads(VECTORS.read_text())['fixtures']
def execute(fs=None):return [lifecycle(f['lifecycleSequence']) if 'lifecycleSequence'in f else runtime(f['scenarioInput']) for f in (fs or fixtures())]
if __name__=='__main__':
 try:o=execute();print(f'FIXTURES={len(o)} LIFECYCLE_STEPS={sum(x.get("steps",0) for x in o)} RESULT=PASS')
 except NormativeError as e:print(f'RESULT=FAIL {e}');raise SystemExit(1)
 except Exception as e:print(f'INFRASTRUCTURE_ERROR={type(e).__name__}:{e}');raise SystemExit(2)
