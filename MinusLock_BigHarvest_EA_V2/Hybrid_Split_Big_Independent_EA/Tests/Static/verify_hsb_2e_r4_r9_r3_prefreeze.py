#!/usr/bin/env python3
"""Independent pre-freeze causal and metadata qualification (no model imports)."""
import argparse,copy,hashlib,json
from decimal import Decimal
from pathlib import Path
def h(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def diff(a,b,p=''):
 if type(a)!=type(b):return [p]
 if isinstance(a,dict):return sum((diff(a.get(k),b.get(k),p+'.'+k if p else k) for k in sorted(set(a)|set(b))),[])
 if isinstance(a,list):
  if len(a)!=len(b):return [p]
  return sum((diff(x,y,f'{p}.{i}') for i,(x,y) in enumerate(zip(a,b))),[])
 return [] if a==b else [p]
def reason(v):
 D=Decimal;i=v['identity'];s=v['snapshot'];t=v['time'];p=v['policy'];bp=v['brokerProperties'];records=v['ledger']['records']
 if v.get('schemaVersion')!=9:return 'SCHEMA'
 if i['account']!=s['account']:return 'IDENTITY_ACCOUNT'
 if i['symbol']!=s['symbol']:return 'SYMBOL'
 if i['magic']!=s['magic']:return 'MAGIC'
 if max(s['timestamp'],p['validFrom'],v['intent']['created'],t['minimum'])>min(p['validUntil'],v['intent']['expires'],t['maximum']):return 'WINDOW'
 if not max(s['timestamp'],p['validFrom'],v['intent']['created'],t['minimum'])<=t['deal']<=min(p['validUntil'],v['intent']['expires'],t['maximum']):return 'STALE'
 if p['buySide']!='BID':return 'BUY_SIDE'
 if not records:return 'MISSING_LEG'
 if len({x['dealId'] for x in records})!=len(records):return 'DUP_DEAL'
 if len({x['eventId'] for x in records})!=len(records):return 'DUP_EVENT'
 r=records[0]
 if r['intentId']!=v['intent']['intentId']:return 'INTENT_BINDING'
 if r['ticket']!=v['intent']['ticket']:return 'DEAL_TICKET'
 if D(r['price'])%D(bp['tickSize']):return 'TICK_GRID'
 if D(r['volume'])%D(bp['volumeStep']):return 'VOLUME_GRID'
 if D(r['volume'])<D(v['intent']['requestedVolume']):return 'PARTIAL_FILL'
 if D(r['volume'])>D(v['intent']['requestedVolume']):return 'OVERFILL'
 if D(v['economicProposal']['allocatedMoney'])+D(v['economicProposal']['remainingMoney'])!=D(v['economicProposal']['availableMoney']):return 'MONEY_CONSERVATION'
 if D(v['brokerProposal']['totalVolume'])!=sum(D(x['volume']) for x in records):return 'VOLUME_CONSERVATION'
 if D(v['allocation']['reserveAddition'])>D(v['economicProposal']['availableMoney']):return 'RESERVE_MISUSE'
 if v['economicProposal'].get('dualTail'):return 'DUAL_TAIL'
 if D(v['economicProposal']['recoveryPL'])<=0:return 'RECOVERY'
 if v['economicProposal'].get('reserveCoverage') is False:return 'COVERAGE'
 if v['persistence']['stateRevision']!=v['fsm']['outputRevision']:return 'PERSISTENCE'
 if v['fsm']['outputRevision']!=v['fsm']['inputRevision']+1:return 'REVISION'
 if v['certificate']['body']['outputRevision']!=v['fsm']['outputRevision']:return 'CERT_BODY'
 if v['certificate']['digest']!=h(v['certificate']['body']):return 'CERT_DIGEST'
 return 'VALID'
def main(root):
 root=Path(root);data=json.loads((root/'Tests/Vectors/HSB_2E_R4_R9_R3_DRAFT_FIXTURES_V2.json').read_text());pairs=json.loads((root/'Tests/Contracts/HSB_2E_R4_R9_R3_CAUSAL_PAIRS.json').read_text())['pairs'];by={x['testMetadata']['fixtureId']:x for x in data['fixtures']};base=by['VALID_BASE']['scenarioInput'];qualified=1;metadata_changes=0;bad=[]
 for pair in pairs:
  row=by[pair['negativeFixtureId']];actual=diff(base,row['scenarioInput']);decl=pair['allowedChangedPaths'];det=reason(row['scenarioInput']);ok=actual==decl and bool(actual) and det==pair['expectedReason'];qualified+=ok
  altered=copy.deepcopy(row);altered['testMetadata']={'fixtureId':'RENAMED','kind':'OTHER','tags':[],'description':'changed'};metadata_changes+=reason(altered['scenarioInput'])!=det
  if not ok:bad.append((pair['negativeFixtureId'],actual,decl,det,pair['expectedReason']))
 cert=json.loads((root/'Tests/Vectors/HSB_2E_R4_R9_R3_CERTIFICATE_FORGERY_DRAFTS.json').read_text());cert_ok=all(sorted(diff(cert['validBase'],x['scenarioInput']))==sorted(x['allowedChangedPaths']) and x['authoritativeAnchor']==cert['validBase']['authoritativeAnchor'] for x in cert['cases'])
 ok=qualified==len(data['fixtures']) and not bad and metadata_changes==0 and cert_ok
 for key in ('ORACLE_V2_PREFREEZE_CHECKS','ORACLE_V2_FIXTURE_QUALIFICATION','ORACLE_V2_CAUSALITY','ORACLE_V2_METADATA_INDEPENDENCE','ORACLE_V2_CERTIFICATE_FORGERY_COMPLETENESS'):print(key+'='+('PASS' if ok else 'FAIL'))
 print('NATIVE_FIXTURES_V2_REQUIRED='+str(len(data['fixtures'])));print('NATIVE_FIXTURES_V2_QUALIFIED='+str(qualified));print('METADATA_ONLY_NEGATIVES=0' if not bad else 'METADATA_ONLY_NEGATIVES='+str(len(bad)));print('MODEL_RESULT_CHANGED_BY_METADATA='+str(metadata_changes));print('ORACLE_V2_READY_TO_FREEZE='+('YES' if ok else 'NO'));print('FAILURES='+json.dumps(bad[:5]));return ok
if __name__=='__main__':p=argparse.ArgumentParser();p.add_argument('--root',default='.');a=p.parse_args();raise SystemExit(0 if main(Path(a.root).resolve()) else 1)
