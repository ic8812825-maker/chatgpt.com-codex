#!/usr/bin/env python3
"""Fail-closed broker-evidence trust chain (offline, Decimal-only)."""
import argparse,copy,hashlib,json,math
from decimal import Decimal,InvalidOperation
D=lambda x:Decimal(str(x))
REQUIRED={'INITIAL':{'WINNER'},'BIG':{'BIG','SMALL'},'SMALL':{'SMALL','OLD_FAR','BIG'},'FINAL':{'FAR'}}
MUTATION_GUARDS={
 "DEAL_ID_KEY":True,
 "EVENT_ID_UNIQUE":True,
 "DEAL_REUSE":True,
 "NEW_EVENT_OLD_DEAL":True,
 "NEW_DEAL_OLD_EVENT":True,
 "BINDING":True,
 "TIMESTAMP_LOWER":True,
 "TIMESTAMP_UPPER":True,
 "INTENT_ACTION":True,
 "INTENT_TRANSACTION":True,
 "INTENT_CYCLE":True,
 "INTENT_SCOPE":True,
 "POSITION_SCOPE":True,
 "POSITION_REVISION":True,
 "MISSING_BIG":True,
 "MISSING_SMALL":True,
 "MISSING_OLD_FAR":True,
 "EXTRA_ROLE":True,
 "DUPLICATE_TICKET":True,
 "DUPLICATE_INTENT":True,
 "ORPHAN_POSITION":True,
 "ORPHAN_INTENT":True,
 "ORPHAN_DEAL":True,
 "POSITION_VOLUME_BINDING":True,
 "PARTIAL_REQUIRED":True,
 "POSITION_FRESHNESS":True,
 "PERSISTENCE_ORDER":True,
 "RESTART_DEALS":True,
 "RESTART_EVENTS":True,
 "STATE_REVISION":True,
 "RAW_EXCEPTION":True,
 "CANONICAL_STATUS":True,
 "MANIFEST":True,
 "EVIDENCE_DELETE":True,
 "EVIDENCE_ADD":True,
 "SEAL_DUPLICATE":True,
 "EVIDENCE_CHANGE":True,
}
PERSIST=['FILL_EVIDENCE','DEAL_EVENT_REGISTRY','SETTLEMENT_DECISION','STATE_REVISION','FSM_COMMIT']
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':'),default=str).encode()).hexdigest()
def canon(x):
 if isinstance(x,Decimal):return str(x)
 if isinstance(x,dict):return {k:canon(v) for k,v in x.items()}
 if isinstance(x,list):return [canon(v) for v in x]
 return x
def finite(x):
 try:return D(x).is_finite()
 except (InvalidOperation,TypeError,ValueError):return False
def fail(inp,reason,detail=None):
 out=base_output(inp);out.update(detail or {});return finish(inp,'REJECT',reason,'VALIDATION_BLOCKED',out,[])
def finish(inp,status,reason,phase,out,persist):
 r={'status':status,'reason':reason,'phase':phase,'scenario':inp.get('scenario'),'output':out,'persistenceRecords':persist,'inputDigest':digest(inp)};r['outputDigest']=digest(r);return canon(r)
def base_output(inp):return {'requiredRoles':sorted(REQUIRED.get(inp.get('scenario'),set())),'observedRoles':[],'missingRoles':[],'extraRoles':[],'fills':{},'consumedDealIds':[],'seenEventIds':[],'dealEventBindings':{},'moneyByTicket':{},'settlementApplied':False,'allocationApplied':False,'stateRevision':inp.get('context',{}).get('stateRevision')}
def schema(inp):
 c=inp.get('context');ps=inp.get('positions');its=inp.get('intents');ds=inp.get('deals')
 if not isinstance(c,dict):return 'CONTEXT_SCHEMA_INVALID'
 if not isinstance(ps,list):return 'POSITIONS_SCHEMA_INVALID'
 if not isinstance(its,list):return 'INTENTS_SCHEMA_INVALID'
 if not isinstance(ds,list):return 'DEALS_SCHEMA_INVALID'
 if any(x is None or not isinstance(x,dict) for seq in (ps,its,ds) for x in seq):return 'NULL_OR_MALFORMED_ELEMENT'
 req=('accountLogin','symbol','magic','cycleId','stateRevision','snapshotId','snapshotVersion','snapshotTimestamp','minimumTimestamp','transactionId','actionId','allowedUpperBound','volumeStep')
 if any(k not in c or c[k] in ('',None) for k in req):return 'CONTEXT_MISSING'
 if not all(finite(c[k]) for k in ('stateRevision','snapshotVersion','snapshotTimestamp','minimumTimestamp','allowedUpperBound','volumeStep')):return 'CONTEXT_NUMERIC_INVALID'
 return None
def validate_collections(inp):
 ps,its,ds=inp['positions'],inp['intents'],inp['deals'];scenario=inp['scenario'];required=REQUIRED.get(scenario)
 if required is None:return 'UNKNOWN_SCENARIO'
 roles=[p.get('role') for p in ps];observed=set(roles);missing=required-observed;extra=observed-required
 if missing:return 'MANDATORY_LEG_MISSING'
 if extra:return 'EXTRA_ROLE'
 if any(roles.count(r)!=1 for r in required):return 'ROLE_MULTIPLICITY_INVALID'
 tickets=[p.get('positionTicket') for p in ps]
 if None in tickets or len(tickets)!=len(set(tickets)):return 'DUPLICATE_TICKET'
 ids=[i.get('intentId') for i in its]
 if None in ids or len(ids)!=len(set(ids)):return 'DUPLICATE_INTENT_ID'
 pt={p.get('positionTicket') for p in ps};it={i.get('positionTicket') for i in its}
 if pt-it:return 'ORPHAN_POSITION'
 if it-pt:return 'ORPHAN_INTENT'
 if any(d.get('positionTicket') not in pt for d in ds):return 'ORPHAN_DEAL'
 return None
def identity(inp,p,i):
 c=inp['context'];scope=('accountLogin','symbol','magic','cycleId')
 if any(p.get(k)!=c.get(k) for k in scope) or p.get('positionRevision')!=c['stateRevision'] or p.get('snapshotId')!=c['snapshotId'] or p.get('snapshotVersion')!=c['snapshotVersion']:return 'POSITION_OWNERSHIP_MISMATCH'
 if any(i.get(k)!=c.get(k) for k in scope+('transactionId','actionId')) or i.get('stateRevision')!=c['stateRevision'] or i.get('snapshotId')!=c['snapshotId'] or i.get('snapshotVersion')!=c['snapshotVersion']:return 'INTENT_IDENTITY_MISMATCH'
 if i.get('positionTicket')!=p.get('positionTicket') or i.get('positionRole')!=p.get('role') or i.get('direction')!=p.get('direction'):return 'INTENT_POSITION_BINDING_MISMATCH'
 if not finite(p.get('positionVolume')) or not finite(i.get('requestedVolume')):return 'VOLUME_INVALID'
 pv,rv=D(p['positionVolume']),D(i['requestedVolume'])
 if i.get('intentKind')=='FULL_CLOSE' and rv!=pv:return 'FULL_CLOSE_VOLUME_MISMATCH'
 if i.get('intentKind')=='PARTIAL_CLOSE':
  if p['role'] in REQUIRED[inp['scenario']] and p['role']!='BIG':return 'PARTIAL_CLOSE_NOT_ALLOWED'
  if not (D(0)<rv<pv):return 'PARTIAL_CLOSE_VOLUME_INVALID'
 elif i.get('intentKind')!='FULL_CLOSE':return 'INTENT_KIND_INVALID'
 return None
def settle(inp):
 inp=copy.deepcopy(inp);err=schema(inp)
 if err:return fail(inp,err)
 err=validate_collections(inp)
 if err:return fail(inp,err)
 c=inp['context'];out=base_output(inp);out['observedRoles']=sorted(p['role'] for p in inp['positions']);out['missingRoles']=sorted(REQUIRED[inp['scenario']]-set(out['observedRoles']));out['extraRoles']=sorted(set(out['observedRoles'])-REQUIRED[inp['scenario']])
 intents={i['positionTicket']:i for i in inp['intents']};positions={p['positionTicket']:p for p in inp['positions']}
 for ticket,p in positions.items():
  err=identity(inp,p,intents[ticket])
  if err:return fail(inp,err,out)
 seen_deals=set(inp.get('consumedDealIds',[]));seen_events=set(inp.get('seenEventIds',[]));d2e=dict(inp.get('dealEventBindings',{}));e2d={v:k for k,v in d2e.items()};valid={t:[] for t in positions}
 for d in inp['deals']:
  did,eid=d.get('dealId'),d.get('eventId')
  if not did:return fail(inp,'DEAL_ID_MISSING',out)
  if not eid:return fail(inp,'EVENT_ID_MISSING',out)
  if did in seen_deals:return fail(inp,'DEAL_ALREADY_CONSUMED',out)
  if eid in seen_events:return fail(inp,'EVENT_ALREADY_SEEN',out)
  if did in d2e and d2e[did]!=eid or eid in e2d and e2d[eid]!=did:return fail(inp,'DEAL_EVENT_BINDING_CONFLICT',out)
  seen_deals.add(did);seen_events.add(eid);d2e[did]=eid;e2d[eid]=did
  p=positions[d['positionTicket']];i=intents[d['positionTicket']]
  for k in ('accountLogin','symbol','magic','cycleId','transactionId','actionId','stateRevision','direction'):
   expected=(p if k=='direction' else c).get(k)
   if d.get(k)!=expected:return fail(inp,'DEAL_IDENTITY_MISMATCH',out)
  if not all(finite(d.get(k)) for k in ('volume','price','profit','commission','swap','fee','timestamp')):return fail(inp,'DEAL_NUMERIC_INVALID',out)
  if not d.get('confirmed') or D(d['volume'])<=0:return fail(inp,'DEAL_INVALID',out)
  if D(d['timestamp'])<max(D(c['minimumTimestamp']),D(i['createdTimestamp'])):return fail(inp,'STALE_DEAL',out)
  if D(d['timestamp'])>min(D(c['allowedUpperBound']),D(i['expiresTimestamp'])):return fail(inp,'FUTURE_DEAL',out)
  valid[d['positionTicket']].append(d)
 for t,p in positions.items():
  i=intents[t];confirmed=sum((D(d['volume']) for d in valid[t]),D(0));requested=D(i['requestedVolume']);remaining=max(D(0),requested-confirmed);state='FULL_FILL' if confirmed==requested else 'PARTIAL_FILL' if confirmed<requested else 'OVERFILL'
  out['fills'][str(t)]={'fillState':state,'requestedVolume':requested,'authoritativeVolume':D(p['positionVolume']),'confirmedVolume':confirmed,'remainingVolume':remaining};out['moneyByTicket'][str(t)]=sum((D(d['profit'])+D(d['commission'])+D(d['swap'])+D(d['fee']) for d in valid[t]),D(0))
  if state!='FULL_FILL':return finish(inp,'UNAVAILABLE' if state=='PARTIAL_FILL' else 'CONFLICT',state,'RECONCILIATION_BLOCKED',out,['FILL_EVIDENCE'])
 out['consumedDealIds']=sorted(seen_deals);out['seenEventIds']=sorted(seen_events);out['dealEventBindings']=dict(sorted(d2e.items()));out['settlementApplied']=True;out['allocationApplied']=True;out['stateRevision']=D(c['stateRevision'])+1
 return finish(inp,'PASS','OK','FSM_COMMITTED',out,PERSIST)
def self_test():
 from pathlib import Path
 vectors=json.loads((Path(__file__).parents[1]/'Vectors/HSB_2E_R4_R3_VECTORS.json').read_text())['vectors'];ids=('VALID_BIG','DUP_DEAL','STALE_DEAL','MISSING_SMALL','VOLUME_LOW','MALFORMED_POSITIONS');checks=[]
 for i in ids:
  v=next(x for x in vectors if x['VECTOR_ID']==i);checks.append((i,settle(v['INPUT'])==v['EXPECTED_RESULT']))
 for i,ok in checks:print(f'R3_MODEL_{i}={"PASS" if ok else "FAIL"}')
 print(f'REFERENCE_MODEL_R4_R3_SELF_TESTS={sum(x[1] for x in checks)}/{len(checks)}');return all(x[1] for x in checks)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--self-test',action='store_true');a=p.parse_args();raise SystemExit(0 if a.self_test and self_test() else 1)
