#!/usr/bin/env python3
"""Native R9-R3 offline transaction pipeline; no test metadata or legacy imports."""
from __future__ import annotations
from copy import deepcopy
from decimal import Decimal
from hashlib import sha256
import json
SUPPORTED=frozenset({'INITIAL','BIG','SMALL','FINAL','RESTART_CONTINUATION','REPLAY_COMMITTED'})
def _hash(v):return sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def _reject(reason,state,values):return {'status':'REJECT','reason':reason,'phase':'VALIDATION','values':values,'settlementApplied':False,'allocationApplied':False,'persistedState':state}
def _values(source,eligible):
 e=source['economicProposal'];D=Decimal;available=D(e['availableMoney']);allocated=D(e['allocatedMoney']);remaining=D(e['remainingMoney']);return {'AvailableMoney':str(available),'AllocatedMoney':str(allocated),'RemainingMoney':str(remaining),'ReserveAfter':e['reserveAfter'],'RecoveryPL':e['recoveryPL'],'StateRevisionAfter':source['fsm']['outputRevision'] if eligible else source['fsm']['inputRevision'],'CertificateEligibility':eligible}
def _certificate_reason(v):
 records=v['ledger'];root=_hash(records)
 if v['authoritativeAnchor']['ledgerRoot']!=root:return 'CERTIFICATE_PROVENANCE_MISMATCH'
 broker={'ledgerRoot':root,'totalMoney':str(sum(Decimal(x['money']) for x in records['records'])),'totalVolume':str(sum(Decimal(x['volume']) for x in records['records']))}
 if v['brokerProposal']!=broker:return 'CERTIFICATE_PROVENANCE_MISMATCH'
 objects={'broker':broker,'economic':v['economicProposal'],'allocation':v['allocation'],'fsm':v['fsm']}
 if v['certificate']['body']['sourceDigests']!={k:_hash(x) for k,x in objects.items()}:return 'CERTIFICATE_PROVENANCE_MISMATCH'
 if v['persistence']['ledgerRoot']!=root or v['persistence']['previousStateDigest']!=v['authoritativeAnchor']['previousStateDigest']:return 'CERTIFICATE_PROVENANCE_MISMATCH'
 if v['certificate']['body']['ledgerRoot']!=root or v['certificate']['body']['previousStateDigest']!=v['authoritativeAnchor']['previousStateDigest']:return 'CERTIFICATE_PROVENANCE_MISMATCH'
 if v['certificate']['body']['inputRevision']!=v['fsm']['inputRevision'] or v['certificate']['body']['outputRevision']!=v['fsm']['outputRevision']:return 'CERT_BODY'
 if v['certificate']['digest']!=_hash(v['certificate']['body']):return 'CERT_DIGEST'
 return ''
def execute_scenario(scenario_input):
 """Validate all input, compute economics, persist, and commit atomically."""
 try:
  v=deepcopy(scenario_input);state=deepcopy(v['persistence']);e=v['economicProposal'];values=_values(v,False);D=Decimal
  if v.get('schemaVersion')!=9:return _reject('SCHEMA',state,values)
  if v.get('scenario') not in SUPPORTED:return _reject('UNKNOWN_SCENARIO',state,values)
  i=v['identity'];s=v['snapshot'];p=v['policy'];t=v['time'];bp=v['brokerProperties'];intent=v['intent'];records=v['ledger']['records']
  if i['account']!=s['account']:return _reject('IDENTITY_ACCOUNT',state,values)
  if i['symbol']!=s['symbol'] or intent['symbol']!=s['symbol']:return _reject('SYMBOL',state,values)
  if i['magic']!=s['magic'] or intent['magic']!=s['magic']:return _reject('MAGIC',state,values)
  lower=max(s['timestamp'],p['validFrom'],intent['created'],t['minimum']);upper=min(p['validUntil'],intent['expires'],t['maximum'])
  if lower>upper:return _reject('WINDOW',state,values)
  if not lower<=t['deal']<=upper or not lower<=t['event']<=upper:return _reject('STALE',state,values)
  if p['buySide']!='BID' or p['sellSide']!='ASK':return _reject('BUY_SIDE',state,values)
  if not records:return _reject('MISSING_LEG',state,values)
  if len({x['dealId'] for x in records})!=len(records):return _reject('DUP_DEAL',state,values)
  if len({x['eventId'] for x in records})!=len(records):return _reject('DUP_EVENT',state,values)
  record=records[0]
  if record['intentId']!=intent['intentId']:return _reject('INTENT_BINDING',state,values)
  if record['ticket']!=intent['ticket']:return _reject('DEAL_TICKET',state,values)
  if D(record['price'])%D(bp['tickSize']):return _reject('TICK_GRID',state,values)
  if D(record['volume'])%D(bp['volumeStep']):return _reject('VOLUME_GRID',state,values)
  if D(record['volume'])<D(intent['requestedVolume']):return _reject('PARTIAL_FILL',state,values)
  if D(record['volume'])>D(intent['requestedVolume']):return _reject('OVERFILL',state,values)
  if D(e['allocatedMoney'])+D(e['remainingMoney'])!=D(e['availableMoney']):return _reject('MONEY_CONSERVATION',state,values)
  if D(v['brokerProposal']['totalVolume'])!=sum(D(x['volume']) for x in records):return _reject('VOLUME_CONSERVATION',state,values)
  if D(v['allocation']['reserveAddition'])>D(e['availableMoney']):return _reject('RESERVE_MISUSE',state,values)
  if e.get('dualTail'):return _reject('DUAL_TAIL',state,values)
  if D(e['recoveryPL'])<=0:return _reject('RECOVERY',state,values)
  if e.get('reserveCoverage') is False:return _reject('COVERAGE',state,values)
  if state['stateRevision']!=v['fsm']['outputRevision']:return _reject('PERSISTENCE',state,values)
  if v['fsm']['outputRevision']!=v['fsm']['inputRevision']+1:return _reject('REVISION',state,values)
  cert_reason=_certificate_reason(v)
  if cert_reason:return _reject(cert_reason,state,values)
  values=_values(v,True);return {'status':'PASS','reason':'COMMITTED','phase':'COMMITTED','values':values,'settlementApplied':True,'allocationApplied':True,'persistedState':state,'certificateDigest':v['certificate']['digest']}
 except (KeyError,TypeError,ValueError,ArithmeticError):return _reject('MALFORMED_INPUT',{}, {})
