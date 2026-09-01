#!/usr/bin/env python3
"""Fail-closed R5 schema, phase, certificate, Far and lifecycle validator."""
from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal,InvalidOperation
import hashlib,json
from pathlib import Path
from typing import Any
ROOT=Path(__file__).resolve().parents[2]
SCHEMA=ROOT/'Tests/Contracts/HSB_2E_R4_R9_R4A_R5_SCENARIO_INPUT_SCHEMA_V3_1.json';VECTORS=ROOT/'Tests/Vectors/HSB_2E_R4_R9_R4A_R5_POSITIVE_BASES.json'
@dataclass(frozen=True)
class NormativeError(Exception):
 checkId:str;reason:str;inputPath:str
 def __str__(self):return f'{self.checkId}:{self.reason}:{self.inputPath}'
def reject(c,r,p):raise NormativeError(c,r,p)
def canon(v):return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def digest(v):return hashlib.sha256(canon(v).encode()).hexdigest()
def dec(v,p):
 if not isinstance(v,str):reject('R5_TYPE','DECIMAL_STRING_REQUIRED',p)
 try:d=Decimal(v)
 except InvalidOperation:reject('R5_NUMERIC','INVALID_DECIMAL',p)
 if not d.is_finite():reject('R5_NUMERIC','NONFINITE_DECIMAL',p)
 return d
def node(v,s,p):
 if v is None:reject('R5_SCHEMA','NULL_FORBIDDEN',p)
 t=s['type']
 if t=='object':
  if not isinstance(v,dict):reject('R5_TYPE','OBJECT_REQUIRED',p)
  props=s['properties'];unknown=set(v)-set(props)
  if unknown:reject('R5_SCHEMA','UNKNOWN_FIELD',p+'.'+sorted(unknown)[0])
  for k,x in props.items():
   if x.get('required',False) and k not in v:reject('R5_SCHEMA','MISSING_REQUIRED',p+'.'+k)
   if k in v:node(v[k],x,p+'.'+k)
 elif t=='array':
  if not isinstance(v,list):reject('R5_TYPE','ARRAY_REQUIRED',p)
  for i,x in enumerate(v):node(x,s['items'],f'{p}[{i}]')
 elif t=='string':
  if not isinstance(v,str):reject('R5_TYPE','STRING_REQUIRED',p)
  if s.get('semanticType')=='DECIMAL':
   d=dec(v,p)
   if 'minimum'in s and d<Decimal(str(s['minimum'])):reject('R5_RANGE','BELOW_MINIMUM',p)
  else:
   if 'minimum'in s and len(v)<int(s['minimum']):reject('R5_RANGE','STRING_TOO_SHORT',p)
   if 'maximum'in s and len(v)>int(s['maximum']):reject('R5_RANGE','STRING_TOO_LONG',p)
  if 'enum'in s and v not in s['enum']:reject('R5_ENUM','INVALID_ENUM',p)
 elif t=='integer':
  if isinstance(v,bool) or not isinstance(v,int):reject('R5_TYPE','EXACT_INTEGER_REQUIRED',p)
  if 'minimum'in s and v<int(s['minimum']):reject('R5_RANGE','BELOW_MINIMUM',p)
 elif t=='boolean':
  if not isinstance(v,bool):reject('R5_TYPE','BOOLEAN_REQUIRED',p)
 else:reject('R5_SCHEMA','UNKNOWN_TYPE',p)
def multiple(v,g):return g>0 and v%g==0
def certificate(r):
 phase=r['phase'];c=r.get('certificate')
 if phase=='PRE_COMMIT':
  if c is not None:reject('CERTIFICATE_STRUCTURE','CERTIFICATE_FORBIDDEN_PRE_COMMIT','scenarioInput.certificate')
  return {'structure':'NOT_APPLICABLE','internalIntegrity':'NOT_APPLICABLE','sourceBinding':'NOT_APPLICABLE'}
 if c is None:reject('CERTIFICATE_STRUCTURE','CERTIFICATE_REQUIRED','scenarioInput.certificate')
 for k,v in c.items():
  if k not in ('version','inputRevision','outputRevision') and (not isinstance(v,str) or len(v)!=64 or any(ch not in '0123456789abcdef' for ch in v)):reject('CERTIFICATE_STRUCTURE','INVALID_SHA256','scenarioInput.certificate.'+k)
 own=dict(c);own.pop('digest')
 if c['digest']!=digest(own):reject('CERTIFICATE_INTERNAL_INTEGRITY','CERTIFICATE_DIGEST_MISMATCH','scenarioInput.certificate.digest')
 body={'broker':r['brokerProposal'],'economic':r['economic'],'allocation':r['allocationPolicy'],'persisted':r['persistedState'],'fsm':r['fsm'],'output':r['fsm']['outputState'],'identity':r['context']}
 expected={'body':digest(body),'previousStateDigest':r['persistedState']['previousStateDigest'],'authoritativeLedgerRoot':r['persistedState']['authoritativeLedgerRoot'],'transactionJournalRoot':r['persistedState']['transactionJournalRoot'],'claimedBrokerDigest':digest(r['brokerProposal']),'claimedEconomicDigest':digest(r['economic']),'claimedAllocationDigest':digest(r['allocationPolicy']),'claimedPersistenceDigest':digest(r['persistedState']),'claimedFsmDigest':digest(r['fsm']),'claimedOutputStateDigest':digest(r['fsm']['outputState']),'operationIdentityDigest':digest(r['context']),'inputRevision':r['fsm']['inputRevision'],'outputRevision':r['fsm']['outputRevision']}
 for k,v in expected.items():
  if c[k]!=v:reject('CERTIFICATE_SOURCE_BINDING','CERTIFICATE_SOURCE_MISMATCH','scenarioInput.certificate.'+k)
 return {'structure':'PASS','internalIntegrity':'PASS','sourceBinding':'PASS'}
def phase(r):
 p=r['phase'];sc=r['scenario']
 if sc=='REPLAY_COMMITTED' and p!='REPLAY':reject('R5_PHASE','REPLAY_PHASE_REQUIRED','scenarioInput.phase')
 if p=='REPLAY' and sc!='REPLAY_COMMITTED':reject('R5_PHASE','REPLAY_SCENARIO_REQUIRED','scenarioInput.scenario')
 if p=='PRE_COMMIT':
  if r['deals'] or r['events'] or r['persistedState']['consumedDealIds'] or r['persistedState']['seenEventIds']:reject('R5_PHASE','PRE_COMMIT_EVIDENCE_FORBIDDEN','scenarioInput.phase')
 else:
  if not r['deals'] or not r['events']:reject('R5_PHASE','COMMITTED_EVIDENCE_REQUIRED','scenarioInput.deals')
  if p=='REPLAY' and (not r['persistedState']['consumedDealIds'] or not r['persistedState']['seenEventIds']):reject('R5_PHASE','REPLAY_REGISTRY_REQUIRED','scenarioInput.persistedState')
def far(r):
 f=r['persistedState']['farState'];active=f['active'];allowed=r['scenario'] in ('BIG','SMALL','RESTART_CONTINUATION')
 if active!=allowed:reject('R5_FAR','FAR_APPLICABILITY_MISMATCH','scenarioInput.persistedState.farState.active')
 optional={'ticket','volume','loss','direction'}
 if not active:
  if set(f)&optional:reject('R5_FAR','INACTIVE_FAR_FIELDS_FORBIDDEN','scenarioInput.persistedState.farState')
  return
 if not optional<=set(f):reject('R5_FAR','ACTIVE_FAR_FIELDS_REQUIRED','scenarioInput.persistedState.farState')
 matches=[p for p in r['positions'] if p['ticket']==f['ticket'] and p['cycleId']==r['context']['cycleId'] and p['accountId']==r['context']['accountId'] and p['symbol']==r['context']['symbol'] and p['magic']==r['context']['magic']]
 if len(matches)!=1:reject('R5_FAR','ACTIVE_FAR_NOT_UNIQUE_OWNED','scenarioInput.persistedState.farState.ticket')
 p=matches[0]
 if p['role']!='FAR' or p['volume']!=f['volume'] or p['direction']!=f['direction']:reject('R5_FAR','ACTIVE_FAR_ROLE_VOLUME_DIRECTION_MISMATCH','scenarioInput.persistedState.farState')
def internal(r):
 c,b=r['context'],r['broker'];phase(r);tick,step=dec(b['tickSize'],'broker.tickSize'),dec(b['volumeStep'],'broker.volumeStep')
 if dec(b['ask'],'broker.ask')<dec(b['bid'],'broker.bid'):reject('R5_BROKER','ASK_BELOW_BID','scenarioInput.broker.ask')
 ids=set()
 tickets={p['ticket']:p for p in r['positions']}
 if len(tickets)!=len(r['positions']):reject('R5_POSITION','DUPLICATE_TICKET','scenarioInput.positions')
 for p in r['positions']:
  if any(p[k]!=c[k] for k in ('accountId','symbol','magic','cycleId')):reject('R5_OWNERSHIP','POSITION_OWNERSHIP_MISMATCH','scenarioInput.positions')
  if not multiple(dec(p['volume'],'position.volume'),step) or not multiple(dec(p['openPrice'],'position.openPrice'),tick):reject('R5_GRID','POSITION_OFF_GRID','scenarioInput.positions')
 intents={i['intentId']:i for i in r['intents']}
 for d in r['deals']:
  if d['dealId'] in ids:reject('R5_DEAL','DUPLICATE_DEAL','scenarioInput.deals')
  ids.add(d['dealId'])
  if d['positionTicket'] not in tickets or d['intentId'] not in intents:reject('R5_BINDING','ORPHAN_DEAL','scenarioInput.deals')
  if not multiple(dec(d['volume'],'deal.volume'),step) or not multiple(dec(d['price'],'deal.price'),tick):reject('R5_GRID','DEAL_OFF_GRID','scenarioInput.deals')
 eventids=set()
 for e in r['events']:
  if e['eventId'] in eventids:reject('R5_EVENT','DUPLICATE_EVENT','scenarioInput.events')
  eventids.add(e['eventId'])
  match=[d for d in r['deals'] if d['dealId']==e['dealId']]
  if len(match)!=1 or any(e[k]!=match[0][k] for k in ('intentId','positionTicket','accountId','symbol','magic','cycleId','transactionId','actionId','role','direction','volume','price')):reject('R5_EVENT','EVENT_DEAL_BINDING_MISMATCH','scenarioInput.events')
 if r['phase']!='PRE_COMMIT':
  requested=sum((dec(i['requestedVolume'],'intent.volume') for i in r['intents']),Decimal(0));filled=sum((dec(d['volume'],'deal.volume') for d in r['deals']),Decimal(0))
  if requested!=filled:reject('R5_VOLUME','VOLUME_CONSERVATION_MISMATCH','scenarioInput.deals')
 e,a=r['economic'],r['allocationPolicy']
 if dec(e['availableMoney'],'economic.available')!=dec(a['allocatedMoney'],'allocation.allocated')+dec(a['remainingMoney'],'allocation.remaining'):reject('R5_MONEY','MONEY_CONSERVATION_MISMATCH','scenarioInput.allocationPolicy')
 if dec(e['partialFarVolume'],'economic.partialFarVolume')>0 and dec(e['reserveConsumption'],'economic.reserveConsumption')>0:reject('R5_RESERVE','RESERVE_PARTIAL_FAR_FORBIDDEN','scenarioInput.economic.reserveConsumption')
 if r['fsm']['outputRevision']!=r['fsm']['inputRevision']+1:reject('R5_FSM','REVISION_MISMATCH','scenarioInput.fsm.outputRevision')
 far(r);return certificate(r)
def runtime(r):
 s=json.loads(SCHEMA.read_text());node(r,s['root'],'scenarioInput');return internal(r)
def lifecycle(seq):
 steps=seq['steps'];
 if len(steps)<2:reject('R5_LIFECYCLE','SEQUENCE_TOO_SHORT','lifecycleSequence.steps')
 for i,step in enumerate(steps):
  if set(step)!={'operation','inputState','operationInput','declaredOutputState'}:reject('R5_LIFECYCLE','STEP_SHAPE_MISMATCH',f'lifecycleSequence.steps[{i}]')
  runtime(step['operationInput']);inp,out=step['inputState'],step['declaredOutputState'];r=step['operationInput']
  if inp['fsmState']!=r['fsm']['inputState'] or inp['revision']!=r['fsm']['inputRevision'] or inp['cycleId']!=r['context']['cycleId']:reject('R5_LIFECYCLE','INPUT_STATE_BINDING_MISMATCH',f'lifecycleSequence.steps[{i}].inputState')
  if out['fsmState']!=r['fsm']['outputState'] or out['revision']!=r['fsm']['outputRevision'] or out['cycleId']!=r['context']['cycleId']:reject('R5_LIFECYCLE','OUTPUT_STATE_BINDING_MISMATCH',f'lifecycleSequence.steps[{i}].declaredOutputState')
  if i and inp!=steps[i-1]['declaredOutputState']:reject('R5_LIFECYCLE','CHAIN_DISCONTINUITY',f'lifecycleSequence.steps[{i}].inputState')
 return {'declaredChainValidated':True,'executedByNativeModel':False,'steps':len(steps)}
def fixtures():return json.loads(VECTORS.read_text())['fixtures']
def execute():
 results=[]
 for f in fixtures():results.append(lifecycle(f['lifecycleSequence']) if 'lifecycleSequence'in f else runtime(f['scenarioInput']))
 return results
if __name__=='__main__':
 try:r=execute();print(f'FIXTURES={len(r)} LIFECYCLE_STEPS={sum(x.get("steps",0) for x in r)} RESULT=PASS')
 except NormativeError as e:print(f'RESULT=FAIL {e}');raise SystemExit(1)
 except Exception as e:print(f'INFRASTRUCTURE_ERROR={type(e).__name__}:{e}');raise SystemExit(2)
