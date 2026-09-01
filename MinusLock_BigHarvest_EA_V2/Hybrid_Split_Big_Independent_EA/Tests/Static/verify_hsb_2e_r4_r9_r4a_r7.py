#!/usr/bin/env python3
"""Direct R7 validation: presented input is never rewritten, removed or resealed."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'Tests/Static'))
import verify_hsb_2e_r4_r9_r4a_r5 as v5
import verify_hsb_2e_r4_r9_r4a_r6 as v6
from build_hsb_2e_r4_r9_r4a_r5_assets import digest
from build_hsb_2e_r4_r9_r4a_r7_assets import state_body
SCHEMA=ROOT/'Tests/Contracts/HSB_2E_R4_R9_R4A_R7_SCHEMA.json';VECTORS=ROOT/'Tests/Vectors/HSB_2E_R4_R9_R4A_R7_POSITIVE_BASES.json';NormativeError=v5.NormativeError
def reject(c,r,p):raise NormativeError(c,r,p)
def certificate_for_sources(c,s):
 for k,x in c.items():
  if k not in ('version','inputRevision','outputRevision') and (not isinstance(x,str) or len(x)!=64 or any(z not in '0123456789abcdef' for z in x)):reject('R7_CERTIFICATE_STRUCTURE','INVALID_SHA256','certificate.'+k)
 own=dict(c);own.pop('digest')
 if c['digest']!=digest(own):reject('R7_CERTIFICATE_INTEGRITY','CERTIFICATE_DIGEST_MISMATCH','certificate.digest')
 body={'broker':s['brokerProposal'],'economic':s['economic'],'allocation':s['allocationPolicy'],'persisted':s['persistedState'],'fsm':s['fsm'],'output':s['fsm']['outputState'],'identity':s['context']}
 exp={'body':digest(body),'previousStateDigest':s['persistedState']['previousStateDigest'],'authoritativeLedgerRoot':s['persistedState']['authoritativeLedgerRoot'],'transactionJournalRoot':s['persistedState']['transactionJournalRoot'],'claimedBrokerDigest':digest(s['brokerProposal']),'claimedEconomicDigest':digest(s['economic']),'claimedAllocationDigest':digest(s['allocationPolicy']),'claimedPersistenceDigest':digest(s['persistedState']),'claimedFsmDigest':digest(s['fsm']),'claimedOutputStateDigest':digest(s['fsm']['outputState']),'operationIdentityDigest':digest(s['context']),'inputRevision':s['fsm']['inputRevision'],'outputRevision':s['fsm']['outputRevision']}
 for k,x in exp.items():
  if c[k]!=x:reject('R7_CERTIFICATE_BINDING','CERTIFICATE_SOURCE_MISMATCH','certificate.'+k)
def replay(r):
 q=r['replayContract'];s=q['historicalSourceObjects'];certificate_for_sources(r['certificate'],s)
 if q['historicalRevisionAfter']!=q['historicalRevisionBefore']+1 or s['fsm']['inputRevision']!=q['historicalRevisionBefore'] or s['fsm']['outputRevision']!=q['historicalRevisionAfter']:reject('R7_REPLAY','HISTORICAL_REVISION_MISMATCH','replayContract')
 p=r['persistedState'];current=p['stateRevision']
 if r['fsm']['inputRevision']!=current or r['fsm']['outputRevision']!=current or q['currentRevisionBefore']!=current or q['currentRevisionAfter']!=current:reject('R7_REPLAY','CURRENT_REVISION_MUTATION','replayContract')
 if q['reserveBefore']!=p['reserve'] or q['reserveAfter']!=p['reserve'] or q['farBefore']!=p['farState'] or q['farAfter']!=p['farState']:reject('R7_REPLAY','AUTHORITATIVE_STATE_BINDING_MISMATCH','replayContract')
 ledger={k:p[k] for k in ('previousStateDigest','authoritativeLedgerRoot','transactionJournalRoot')}
 if q['ledgerBefore']!=ledger or q['ledgerAfter']!=ledger:reject('R7_REPLAY','LEDGER_MUTATION','replayContract')
 if q['consumedDealIdsBefore']!=p['consumedDealIds'] or q['consumedDealIdsAfter']!=p['consumedDealIds']:reject('R7_REPLAY','REGISTRY_MUTATION','replayContract')
 deals={d['dealId'] for d in r['deals']};events={e['eventId'] for e in r['events']}
 if not deals<=set(p['consumedDealIds']) or not events<=set(p['seenEventIds']):reject('R7_REPLAY','REPLAY_IDS_NOT_CONSUMED','persistedState')
 bindings={(x['dealId'],x['eventId']) for x in p['dealEventBindings']}
 if not {(e['dealId'],e['eventId']) for e in r['events']}<=bindings:reject('R7_REPLAY','REPLAY_BINDING_MISSING','persistedState.dealEventBindings')
def runtime(r):
 schema=json.loads(SCHEMA.read_text());v5.node(r,schema['root'],'scenarioInput')
 v6.temporal(r);v6.identity_direction(r);v6.far_tail(r)
 tick=v5.dec(r['broker']['tickSize'],'broker.tickSize');step=v5.dec(r['broker']['volumeStep'],'broker.volumeStep')
 for p in r['positions']:
  if not v5.multiple(v5.dec(p['volume'],'position.volume'),step) or not v5.multiple(v5.dec(p['openPrice'],'position.openPrice'),tick):reject('R5_GRID','POSITION_OFF_GRID','scenarioInput.positions')
 for d in (r['deals'] if 'deals'in r else []):
  if not v5.multiple(v5.dec(d['volume'],'deal.volume'),step) or not v5.multiple(v5.dec(d['price'],'deal.price'),tick):reject('R5_GRID','DEAL_OFF_GRID','scenarioInput.deals')
 deals=r['deals'] if 'deals'in r else [];events=r['events'] if 'events'in r else []
 if len({d['dealId'] for d in deals})!=len(deals):reject('R5_DEAL','DUPLICATE_DEAL','scenarioInput.deals')
 if len({e['eventId'] for e in events})!=len(events):reject('R5_EVENT','DUPLICATE_EVENT','scenarioInput.events')
 if r['phase']!='PRE_COMMIT':
  requested=sum((v5.dec(i['requestedVolume'],'intent.volume') for i in r['intents']),v5.Decimal(0));filled=sum((v5.dec(d['volume'],'deal.volume') for d in deals),v5.Decimal(0))
  if requested!=filled:reject('R5_VOLUME','VOLUME_CONSERVATION_MISMATCH','scenarioInput.deals')
 e,a=r['economic'],r['allocationPolicy']
 if v5.dec(e['availableMoney'],'economic.available')!=v5.dec(a['allocatedMoney'],'allocation.allocated')+v5.dec(a['remainingMoney'],'allocation.remaining'):reject('R5_MONEY','MONEY_CONSERVATION_MISMATCH','scenarioInput.allocationPolicy')
 if v5.dec(e['partialFarVolume'],'economic.partial')>0 and v5.dec(e['reserveConsumption'],'economic.reserve')>0:reject('R5_RESERVE','RESERVE_PARTIAL_FAR_FORBIDDEN','scenarioInput.economic.reserveConsumption')
 if r['phase']=='REPLAY':replay(r)
 else:v5.certificate(r)
 return {'result':'PASS'}
OPS={'INITIAL':'INITIAL','BIG':'BIG','SMALL':'SMALL','FINAL':'FINAL','RESTART':'RESTART_CONTINUATION','REPLAY':'REPLAY_COMMITTED'};STATES={'INITIAL','BIG','SMALL','FINAL','COMMITTED'}
def valid_state(s,p):
 if set(s)!={'stateBody','stateDigest'}:reject('R7_LIFECYCLE','STATE_SHAPE_MISMATCH',p)
 if s['stateBody']['fsmState'] not in STATES:reject('R7_LIFECYCLE','UNKNOWN_FSM_STATE',p)
 if s['stateDigest']!=digest(s['stateBody']):reject('R7_LIFECYCLE','STATE_DIGEST_MISMATCH',p)
def lifecycle(seq):
 steps=seq['steps']
 if len(steps)<2:reject('R7_LIFECYCLE','SEQUENCE_TOO_SHORT','steps')
 for i,st in enumerate(steps):
  if set(st)!={'operation','inputState','operationInput','declaredOutputState'}:reject('R7_LIFECYCLE','STEP_SHAPE_MISMATCH',f'steps[{i}]')
  if st['operation'] not in OPS:reject('R7_LIFECYCLE','UNKNOWN_OPERATION',f'steps[{i}].operation')
  r=st['operationInput']
  if r['scenario']!=OPS[st['operation']]:reject('R7_LIFECYCLE','OPERATION_SCENARIO_MISMATCH',f'steps[{i}]')
  runtime(r);valid_state(st['inputState'],f'steps[{i}].inputState');valid_state(st['declaredOutputState'],f'steps[{i}].declaredOutputState')
  if st['inputState']['stateBody']!=state_body(r,r['fsm']['inputState'],r['fsm']['inputRevision']):reject('R7_LIFECYCLE','INPUT_BINDING_MISMATCH',f'steps[{i}]')
  outrev=r['fsm']['inputRevision'] if st['operation']=='REPLAY' else r['fsm']['inputRevision']+1
  expected_out=state_body(r,r['fsm']['outputState'],outrev)
  if i+1<len(steps) and steps[i+1]['operation']=='REPLAY':
   nxt=steps[i+1]['operationInput'];expected_out['consumedDealIds']=sorted(set(expected_out['consumedDealIds'])|{d['dealId'] for d in nxt['deals']});expected_out['seenEventIds']=sorted(set(expected_out['seenEventIds'])|{e['eventId'] for e in nxt['events']})
  if st['declaredOutputState']['stateBody']!=expected_out:reject('R7_LIFECYCLE','OUTPUT_BINDING_MISMATCH',f'steps[{i}]')
  if i and st['inputState']!=steps[i-1]['declaredOutputState']:reject('R7_LIFECYCLE','CHAIN_DISCONTINUITY',f'steps[{i}]')
  if st['operation']=='REPLAY' and st['declaredOutputState']!=st['inputState']:reject('R7_LIFECYCLE','REPLAY_STATE_MUTATION',f'steps[{i}]')
 return {'steps':len(steps),'declaredChainValidated':True,'executedByNativeModel':False}
def fixtures():return json.loads(VECTORS.read_text())['fixtures']
def execute(fs=None):return [lifecycle(f['lifecycleSequence']) if 'lifecycleSequence'in f else runtime(f['scenarioInput']) for f in (fs or fixtures())]
if __name__=='__main__':
 try:o=execute();print(f'FIXTURES={len(o)} LIFECYCLE_STEPS={sum(x.get("steps",0) for x in o)} RESULT=PASS')
 except NormativeError as e:print(f'RESULT=FAIL {e}');raise SystemExit(1)
 except Exception as e:print(f'INFRASTRUCTURE_ERROR={type(e).__name__}:{e}');raise SystemExit(2)
