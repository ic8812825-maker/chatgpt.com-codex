#!/usr/bin/env python3
"""R10 binds the already verified historical commit sources to current replay state."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'Tests/Static'))
import verify_hsb_2e_r4_r9_r4a_r9 as v9
import verify_hsb_2e_r4_r9_r4a_r7 as v7
import verify_hsb_2e_r4_r9_r4a_r5 as v5
SCHEMA=ROOT/'Tests/Contracts/HSB_2E_R4_R9_R4A_R10_SCHEMA.json';VECTORS=ROOT/'Tests/Vectors/HSB_2E_R4_R9_R4A_R10_POSITIVE_BASES.json';BINDING=ROOT/'Tests/Contracts/HSB_2E_R4_R9_R4A_R10_REPLAY_BINDING.json';NormativeError=v9.NormativeError;digest=v9.digest
def reject(c,r,p):raise NormativeError(c,r,p)
def replay_binding(r):
 q=r['replayContract'];h=q['historicalSourceObjects'];hc=h['context'];cc=r['context']
 # The presented certificate is checked, never reconstructed.
 v7.certificate_for_sources(r['certificate'],h)
 for k in ('accountId','symbol','magic','cycleId','transactionId','actionId'):
  if hc[k]!=cc[k]:reject('R10_REPLAY_SOURCE_BINDING','HISTORICAL_CURRENT_IDENTITY_MISMATCH',f'replayContract.historicalSourceObjects.context.{k}')
 if h['fsm']['inputRevision']!=q['historicalRevisionBefore'] or h['fsm']['outputRevision']!=q['historicalRevisionAfter']:reject('R10_REPLAY_REVISION_BINDING','HISTORICAL_REVISION_DOMAIN_MISMATCH','replayContract')
 if h['fsm']['outputRevision']!=r['persistedState']['stateRevision']:reject('R10_REPLAY_REVISION_BINDING','HISTORICAL_OUTPUT_CURRENT_REVISION_MISMATCH','persistedState.stateRevision')
 if h['persistedState']!=r['persistedState']:reject('R10_REPLAY_STATE_BINDING','HISTORICAL_OUTPUT_PERSISTED_STATE_MISMATCH','persistedState')
def runtime(r):
 v5.node(r,json.loads(SCHEMA.read_text())['root'],'scenarioInput')
 if r['phase']=='REPLAY':replay_binding(r)
 return v9.runtime(r)
def expected_output(st):return v9.expected_output(st)
def lifecycle(seq):
 for st in seq['steps']:runtime(st['operationInput'])
 return v9.lifecycle(seq)
def fixtures():return json.loads(VECTORS.read_text())['fixtures']
def execute(fs=None):return [lifecycle(f['lifecycleSequence']) if 'lifecycleSequence'in f else runtime(f['scenarioInput']) for f in (fs or fixtures())]
if __name__=='__main__':
 try:o=execute();print(f'FIXTURES={len(o)} LIFECYCLE_STEPS={sum(x.get("steps",0) for x in o)} RESULT=PASS')
 except NormativeError as e:print(f'RESULT=FAIL {e}');raise SystemExit(1)
 except Exception as e:print(f'INFRASTRUCTURE_ERROR={type(e).__name__}:{e}');raise SystemExit(2)
