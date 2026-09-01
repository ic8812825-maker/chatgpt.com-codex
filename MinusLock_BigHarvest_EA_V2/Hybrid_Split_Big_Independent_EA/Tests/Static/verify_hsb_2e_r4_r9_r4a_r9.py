#!/usr/bin/env python3
"""R9 execution-record gates layered over the immutable R8 contract."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'Tests/Static'))
import verify_hsb_2e_r4_r9_r4a_r8 as v8
import verify_hsb_2e_r4_r9_r4a_r5 as v5
SCHEMA=ROOT/'Tests/Contracts/HSB_2E_R4_R9_R4A_R9_SCHEMA.json';VECTORS=ROOT/'Tests/Vectors/HSB_2E_R4_R9_R4A_R9_POSITIVE_BASES.json';NormativeError=v8.NormativeError;digest=v8.digest
def reject(c,r,p):raise NormativeError(c,r,p)
def scenario_phase(r):
 s,p=r['scenario'],r['phase']
 if s=='REPLAY_COMMITTED' and p!='REPLAY':reject('R9_SCENARIO_PHASE','REPLAY_SCENARIO_REQUIRES_REPLAY','scenarioInput.phase')
 if p=='REPLAY' and s!='REPLAY_COMMITTED':reject('R9_SCENARIO_PHASE','REPLAY_PHASE_REQUIRES_REPLAY_SCENARIO','scenarioInput.scenario')
 if p=='COMMITTED' and s=='REPLAY_COMMITTED':reject('R9_SCENARIO_PHASE','COMMITTED_REPLAY_SCENARIO_FORBIDDEN','scenarioInput')
 if p=='PRE_COMMIT' and (r.get('deals') or r.get('events') or r.get('certificate')):reject('R9_SCENARIO_PHASE','PRE_COMMIT_CURRENT_EVIDENCE_FORBIDDEN','scenarioInput')
def execution_records(r):
 if r['phase']=='PRE_COMMIT':return
 c=r['context']
 for kind in ('deals','events'):
  for n,x in enumerate(r[kind]):
   if type(x['confirmed']) is not bool:reject('R9_EXECUTION_CONFIRMATION','CONFIRMED_BOOLEAN_REQUIRED',f'{kind}[{n}].confirmed')
   if x['confirmed'] is not True:reject('R9_EXECUTION_CONFIRMATION','EXECUTION_NOT_CONFIRMED',f'{kind}[{n}].confirmed')
   if x['stateRevision']!=c['stateRevision']:reject('R9_EXECUTION_REVISION','STATE_REVISION_CONTEXT_MISMATCH',f'{kind}[{n}].stateRevision')
   if x['snapshotRevision']!=c['snapshotRevision']:reject('R9_EXECUTION_REVISION','SNAPSHOT_REVISION_CONTEXT_MISMATCH',f'{kind}[{n}].snapshotRevision')
def runtime(r):
 # Schema is evaluated against the presented R9 object; no input rewrite occurs.
 v5.node(r,json.loads(SCHEMA.read_text())['root'],'scenarioInput');scenario_phase(r);execution_records(r);return v8.runtime(r)
def expected_output(st):return v8.expected_output(st)
def lifecycle(seq):
 # R8 lifecycle calls its own runtime, therefore validate every operation through R9 first.
 for st in seq['steps']:runtime(st['operationInput'])
 return v8.lifecycle(seq)
def fixtures():return json.loads(VECTORS.read_text())['fixtures']
def execute(fs=None):return [lifecycle(f['lifecycleSequence']) if 'lifecycleSequence'in f else runtime(f['scenarioInput']) for f in (fs or fixtures())]
if __name__=='__main__':
 try:o=execute();print(f'FIXTURES={len(o)} LIFECYCLE_STEPS={sum(x.get("steps",0) for x in o)} RESULT=PASS')
 except NormativeError as e:print(f'RESULT=FAIL {e}');raise SystemExit(1)
 except Exception as e:print(f'INFRASTRUCTURE_ERROR={type(e).__name__}:{e}');raise SystemExit(2)
