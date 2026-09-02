#!/usr/bin/env python3
"""Seven independent R11 predicate evaluators; no R10 validator dispatch and no metadata reads."""
import json,math,sys
from decimal import Decimal,InvalidOperation
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'Tests/Static'))
import verify_hsb_2e_r4_r9_r4a_r5 as schema_primitives
SCHEMA=json.loads((ROOT/'Tests/Contracts/HSB_2E_R4_R9_R4A_R10_SCHEMA.json').read_text())['root']
CONTRACT=json.loads((ROOT/'Tests/Contracts/HSB_2E_R4_R9_R4A_R11_FIRST_BLOCK_CONTRACT.json').read_text())['predicates']
ORDER=[x['predicateId'] for x in CONTRACT];BY_ID={x['predicateId']:x for x in CONTRACT}
def result(pid,status,paths,dependencies,check='',reason=''):
 return {'predicateId':pid,'status':status,'checkId':check,'reason':reason,'evaluatedPaths':paths,'dependencyResults':dependencies}
def fail(pid,paths,deps,reason=None):
 c=BY_ID[pid];return result(pid,'FAIL',paths,deps,c['failureCheckId'],reason or c['failureReason'])
def passed(pid,paths,deps):return result(pid,'PASS',paths,deps)
def shape(value,node,path,paths):
 paths.append(path);typ=node['type']
 if typ=='object':
  if not isinstance(value,dict):return False
  required={k for k,v in node['properties'].items() if v.get('required')}
  if not required<=set(value) or not set(value)<=set(node['properties']):return False
  return all(shape(value[k],node['properties'][k],f'{path}.{k}',paths) for k in value)
 if typ=='array':return isinstance(value,list) and all(shape(x,node['items'],f'{path}[{i}]',paths) for i,x in enumerate(value))
 if typ=='integer':ok=isinstance(value,int) and not isinstance(value,bool)
 elif typ=='number':ok=isinstance(value,(int,float)) and not isinstance(value,bool)
 elif typ=='string':ok=isinstance(value,str)
 elif typ=='boolean':ok=isinstance(value,bool)
 else:ok=False
 return ok and ('enum' not in node or value in node['enum'])
def evaluate_schema(r,deps):
 paths=[]
 if not shape(r,SCHEMA,'scenarioInput',paths):return fail('SCHEMA',paths,deps)
 return passed('SCHEMA',paths,deps)
def numeric_nodes(value,node,path,out):
 typ=node['type']
 if typ=='object':
  for k,ch in node['properties'].items():
   if k in value:numeric_nodes(value[k],ch,f'{path}.{k}',out)
 elif typ=='array':
  for i,x in enumerate(value):numeric_nodes(x,node['items'],f'{path}[{i}]',out)
 elif typ in ('integer','number') or node.get('semanticType')=='DECIMAL':out.append((path,value,typ,node.get('semanticType')))
def evaluate_numeric_finite(r,deps):
 vals=[];numeric_nodes(r,SCHEMA,'scenarioInput',vals);paths=[]
 for p,v,typ,sem in vals:
  paths.append(p)
  if isinstance(v,bool):return fail('NUMERIC_FINITE',paths,deps,'BOOLEAN_IS_NOT_NUMERIC')
  try:n=Decimal(str(v))
  except (InvalidOperation,ValueError):return fail('NUMERIC_FINITE',paths,deps,'NUMERIC_PARSE_FAILURE')
  if not n.is_finite():return fail('NUMERIC_FINITE',paths,deps,'NONFINITE_NUMERIC')
 return passed('NUMERIC_FINITE',paths,deps)
def nonempty(v):return isinstance(v,str) and bool(v.strip())
def evaluate_runtime_identity(r,deps):
 c=r['context'];paths=[f'scenarioInput.context.{k}' for k in ('accountId','cycleId','transactionId','actionId')]
 if any(not nonempty(c[k]) for k in ('accountId','cycleId','transactionId','actionId')):return fail('RUNTIME_IDENTITY',paths,deps,'EMPTY_RUNTIME_IDENTITY')
 for i,x in enumerate(r['intents']):
  paths += [f'scenarioInput.intents[{i}].transactionId',f'scenarioInput.intents[{i}].actionId']
  if x['transactionId']!=c['transactionId'] or x['actionId']!=c['actionId']:return fail('RUNTIME_IDENTITY',paths,deps)
 for group in ('deals','events'):
  for i,x in enumerate(r[group] if group in r else []):
   paths += [f'scenarioInput.{group}[{i}].accountId',f'scenarioInput.{group}[{i}].cycleId',f'scenarioInput.{group}[{i}].transactionId',f'scenarioInput.{group}[{i}].actionId']
   if any(x[k]!=c[k] for k in ('accountId','cycleId','transactionId','actionId')):return fail('RUNTIME_IDENTITY',paths,deps)
 return passed('RUNTIME_IDENTITY',paths,deps)
def evaluate_symbol_magic_ownership(r,deps):
 c=r['context'];paths=['scenarioInput.context.symbol','scenarioInput.context.magic']
 for group in ('positions','deals','events'):
  for i,x in enumerate(r[group] if group in r else []):
   paths += [f'scenarioInput.{group}[{i}].symbol',f'scenarioInput.{group}[{i}].magic']
   if x['symbol']!=c['symbol'] or x['magic']!=c['magic']:return fail('SYMBOL_MAGIC_OWNERSHIP',paths,deps)
 return passed('SYMBOL_MAGIC_OWNERSHIP',paths,deps)
def evaluate_broker_properties(r,deps):
 b=r['broker'];positive=('point','tickSize','tickValue','contractSize','volumeMin','volumeMax','volumeStep');paths=[f'scenarioInput.broker.{k}' for k in ('digits',)+positive+('bid','ask','maximumDeviation')]
 if b['digits']<0 or b['maximumDeviation']<0:return fail('BROKER_PROPERTIES',paths,deps)
 if any(Decimal(str(b[k]))<=0 for k in positive):return fail('BROKER_PROPERTIES',paths,deps,'BROKER_VALUE_NOT_POSITIVE')
 if Decimal(str(b['volumeMin']))>Decimal(str(b['volumeMax'])) or Decimal(str(b['bid']))>Decimal(str(b['ask'])):return fail('BROKER_PROPERTIES',paths,deps,'BROKER_RANGE_INVALID')
 return passed('BROKER_PROPERTIES',paths,deps)
def evaluate_snapshot_context(r,deps):
 s,c=r['snapshot'],r['context'];paths=['scenarioInput.snapshot.symbol','scenarioInput.snapshot.magic','scenarioInput.snapshot.revision','scenarioInput.context.symbol','scenarioInput.context.magic','scenarioInput.context.snapshotRevision']
 if s['symbol']!=c['symbol'] or s['magic']!=c['magic'] or s['revision']!=c['snapshotRevision']:return fail('SNAPSHOT_CONTEXT',paths,deps)
 return passed('SNAPSHOT_CONTEXT',paths,deps)
def evaluate_temporal_window(r,deps):
 s=r['snapshot']['timestamp'];p=r['temporalPolicy'];paths=['scenarioInput.snapshot.timestamp','scenarioInput.temporalPolicy.validFrom','scenarioInput.temporalPolicy.validUntil','scenarioInput.temporalPolicy.minimumTimestamp','scenarioInput.temporalPolicy.allowedUpperBound']
 intents={x['intentId']:x for x in r['intents']}
 for i,x in enumerate(r['intents']):
  paths += [f'scenarioInput.intents[{i}].createdTimestamp',f'scenarioInput.intents[{i}].expiresTimestamp']
  if max(s,p['validFrom'],x['createdTimestamp'],p['minimumTimestamp'])>min(p['validUntil'],x['expiresTimestamp'],p['allowedUpperBound']):return fail('TEMPORAL_WINDOW',paths,deps,'CONTRADICTORY_TEMPORAL_WINDOW')
 for i,d in enumerate(r['deals'] if 'deals'in r else []):
  paths.append(f'scenarioInput.deals[{i}].timestamp')
  if d['intentId'] not in intents:return fail('TEMPORAL_WINDOW',paths,deps,'TEMPORAL_INTENT_NOT_FOUND')
  x=intents[d['intentId']];lo=max(s,p['validFrom'],x['createdTimestamp'],p['minimumTimestamp']);hi=min(p['validUntil'],x['expiresTimestamp'],p['allowedUpperBound'])
  if not lo<=d['timestamp']<=hi:return fail('TEMPORAL_WINDOW',paths,deps,'TIMESTAMP_OUTSIDE_WINDOW')
 return passed('TEMPORAL_WINDOW',paths,deps)
EVALUATORS={'SCHEMA':evaluate_schema,'NUMERIC_FINITE':evaluate_numeric_finite,'RUNTIME_IDENTITY':evaluate_runtime_identity,'SYMBOL_MAGIC_OWNERSHIP':evaluate_symbol_magic_ownership,'BROKER_PROPERTIES':evaluate_broker_properties,'SNAPSHOT_CONTEXT':evaluate_snapshot_context,'TEMPORAL_WINDOW':evaluate_temporal_window}
def trace(r):
 rows=[];by={}
 for pid in ORDER:
  prereq=BY_ID[pid]['prerequisitePredicates'];deps={x:by[x]['status'] for x in prereq}
  if any(by[x]['status']!='PASS' for x in prereq):row=result(pid,'BLOCKED_BY_PREREQUISITE',[],deps,'','PREREQUISITE_NOT_PASSED')
  else:row=EVALUATORS[pid](r,deps)
  rows.append(row);by[pid]=row
 first=next((x for x in rows if x['status']=='FAIL'),None)
 return {'predicates':rows,'firstNormativeFailure':first['predicateId'] if first else None}
