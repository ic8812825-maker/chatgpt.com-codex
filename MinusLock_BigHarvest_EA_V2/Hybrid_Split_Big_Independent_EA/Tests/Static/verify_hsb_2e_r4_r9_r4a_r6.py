#!/usr/bin/env python3
"""R6 validation restoring temporal/identity/Far/replay/lifecycle constraints."""
import copy,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'Tests/Static'))
import verify_hsb_2e_r4_r9_r4a_r5 as v5
from build_hsb_2e_r4_r9_r4a_r5_assets import recert,digest
from build_hsb_2e_r4_r9_r4a_r6_assets import body
VECTORS=ROOT/'Tests/Vectors/HSB_2E_R4_R9_R4A_R6_POSITIVE_BASES.json';NormativeError=v5.NormativeError
def reject(c,r,p):raise NormativeError(c,r,p)
def base(r):
 x=copy.deepcopy(r);x['schemaVersion']='3.1.0';x.pop('replayContract',None)
 if x['phase']=='REPLAY':x['fsm']['outputRevision']=x['fsm']['inputRevision']+1;recert(x)
 return v5.runtime(x)
def temporal(r):
 policy=r['temporalPolicy'];snap=r['snapshot']['timestamp']
 if policy['validFrom']>policy['validUntil'] or policy['minimumTimestamp']>policy['allowedUpperBound']:reject('R6_TEMPORAL','CONTRADICTORY_WINDOW','scenarioInput.temporalPolicy')
 intents={i['intentId']:i for i in r['intents']}
 for d in (r['deals'] if 'deals'in r else []):
  i=intents[d['intentId']];lower=max(snap,policy['validFrom'],i['createdTimestamp'],policy['minimumTimestamp']);upper=min(policy['validUntil'],i['expiresTimestamp'],policy['allowedUpperBound'])
  if lower>upper:reject('R6_TEMPORAL','EMPTY_EFFECTIVE_WINDOW','scenarioInput.intents')
  if not lower<=d['timestamp']<=upper:reject('R6_TEMPORAL','DEAL_OUTSIDE_WINDOW','scenarioInput.deals.timestamp')
  e=next((e for e in r['events'] if e['dealId']==d['dealId']),None)
  if e is None or not lower<=e['timestamp']<=upper:reject('R6_TEMPORAL','EVENT_OUTSIDE_WINDOW','scenarioInput.events.timestamp')
def identity_direction(r):
 c=r['context'];positions={p['ticket']:p for p in r['positions']};intents={i['intentId']:i for i in r['intents']}
 for i in r['intents']:
  if i['transactionId']!=c['transactionId'] or i['actionId']!=c['actionId'] or i['positionTicket'] not in positions:reject('R6_IDENTITY','INTENT_CONTEXT_BINDING','scenarioInput.intents')
  p=positions[i['positionTicket']]
  if i['role']!=p['role'] or i['direction']==p['direction'] or i['stateRevision']!=c['stateRevision'] or i['snapshotRevision']!=c['snapshotRevision']:reject('R6_DIRECTION','CLOSE_DIRECTION_OR_REVISION_MISMATCH','scenarioInput.intents')
 for d in (r['deals'] if 'deals'in r else []):
  i=intents[d['intentId']];p=positions[d['positionTicket']]
  if any(d[k]!=c[k] for k in ('accountId','symbol','magic','cycleId','transactionId','actionId')):reject('R6_IDENTITY','DEAL_CONTEXT_MISMATCH','scenarioInput.deals')
  if d['positionTicket']!=i['positionTicket'] or d['role']!=i['role'] or d['direction']!=i['direction'] or d['direction']==p['direction']:reject('R6_DIRECTION','DEAL_INTENT_POSITION_DIRECTION','scenarioInput.deals')
  quote=r['broker']['bid'] if p['direction']=='BUY' else r['broker']['ask']
  if d['price']!=quote:reject('R6_DIRECTION','WRONG_QUOTE_CLOSE_SIDE','scenarioInput.deals.price')
def far_tail(r):
 owned=[p for p in r['positions'] if p['accountId']==r['context']['accountId'] and p['symbol']==r['context']['symbol'] and p['magic']==r['context']['magic'] and p['cycleId']==r['context']['cycleId']];tails=[p for p in owned if p['role']=='FAR'];f=r['persistedState']['farState']
 if len(tails)>1:reject('R6_FAR','MULTIPLE_ACTIVE_FAR','scenarioInput.positions')
 expected_tail=1 if f['active'] else 0
 if r['economic']['tailCount']!=expected_tail:reject('R6_DUAL_TAIL','TAIL_COUNT_MISMATCH','scenarioInput.economic.tailCount')
 if len(tails)>1 or r['economic']['tailCount']>1:reject('R6_DUAL_TAIL','DUAL_TAIL','scenarioInput.positions')
 if f['active'] and len(tails)!=1:reject('R6_FAR','FAR_ACTIVE_STATE_MISMATCH','scenarioInput.persistedState.farState')
 if not f['active'] and tails and r['fsm']['outputState']!='COMMITTED':reject('R6_FAR','INACTIVE_FAR_WITHOUT_CLOSING_TRANSITION','scenarioInput.persistedState.farState')
def replay(r):
 if r['phase']!='REPLAY':return
 q=r.get('replayContract')
 if q is None:reject('R6_REPLAY','REPLAY_CONTRACT_REQUIRED','scenarioInput.replayContract')
 if r['fsm']['inputRevision']!=r['fsm']['outputRevision'] or q['currentRevisionBefore']!=q['currentRevisionAfter'] or q['currentRevisionBefore']!=r['fsm']['inputRevision']:reject('R6_REPLAY','REPLAY_REVISION_MUTATION','scenarioInput.fsm')
 if q['reserveBefore']!=q['reserveAfter'] or q['farBefore']!=q['farAfter'] or q['consumedDealIdsBefore']!=q['consumedDealIdsAfter']:reject('R6_REPLAY','REPLAY_STATE_MUTATION','scenarioInput.replayContract')
 dealids={d['dealId'] for d in r['deals']};eventids={e['eventId'] for e in r['events']};p=r['persistedState']
 if set(p['consumedDealIds'])!=dealids or set(p['seenEventIds'])!=eventids or {(x['dealId'],x['eventId']) for x in p['dealEventBindings']}!={(e['dealId'],e['eventId']) for e in r['events']}:reject('R6_REPLAY','REPLAY_REGISTRY_BINDING_MISMATCH','scenarioInput.persistedState')
def runtime(r):base(r);temporal(r);identity_direction(r);far_tail(r);replay(r);return {'result':'PASS'}
OPS={'INITIAL':'INITIAL','BIG':'BIG','SMALL':'SMALL','FINAL':'FINAL','RESTART':'RESTART_CONTINUATION','REPLAY':'REPLAY_COMMITTED'}
def valid_state(s,p):
 if set(s)!={'stateBody','stateDigest'}:reject('R6_LIFECYCLE','STATE_SHAPE_MISMATCH',p)
 if s['stateDigest']!=digest(s['stateBody']):reject('R6_LIFECYCLE','STATE_DIGEST_MISMATCH',p+'.stateDigest')
def lifecycle(seq):
 steps=seq['steps']
 for i,st in enumerate(steps):
  if st['operation'] not in OPS:reject('R6_LIFECYCLE','UNKNOWN_OPERATION',f'steps[{i}].operation')
  r=st['operationInput']
  if r['scenario']!=OPS[st['operation']]:reject('R6_LIFECYCLE','OPERATION_SCENARIO_MISMATCH',f'steps[{i}].operation')
  runtime(r);valid_state(st['inputState'],f'steps[{i}].inputState');valid_state(st['declaredOutputState'],f'steps[{i}].declaredOutputState')
  expected=body(r,r['fsm']['inputState'],r['fsm']['inputRevision'])
  if st['inputState']['stateBody']!=expected:reject('R6_LIFECYCLE','INPUT_STATE_BODY_MISMATCH',f'steps[{i}].inputState')
  if i and st['inputState']!=steps[i-1]['declaredOutputState']:reject('R6_LIFECYCLE','CHAIN_DISCONTINUITY',f'steps[{i}].inputState')
  if st['operation']=='REPLAY' and st['declaredOutputState']!=st['inputState']:reject('R6_LIFECYCLE','REPLAY_STATE_MUTATION',f'steps[{i}].declaredOutputState')
 return {'steps':len(steps),'declaredChainValidated':True,'executedByNativeModel':False}
def fixtures():return json.loads(VECTORS.read_text())['fixtures']
def execute(fs=None):
 out=[]
 for f in fs or fixtures():out.append(lifecycle(f['lifecycleSequence']) if 'lifecycleSequence'in f else runtime(f['scenarioInput']))
 return out
if __name__=='__main__':
 try:o=execute();print(f'FIXTURES={len(o)} LIFECYCLE_STEPS={sum(x.get("steps",0) for x in o)} RESULT=PASS')
 except NormativeError as e:print(f'RESULT=FAIL {e}');raise SystemExit(1)
 except Exception as e:print(f'INFRASTRUCTURE_ERROR={type(e).__name__}:{e}');raise SystemExit(2)
