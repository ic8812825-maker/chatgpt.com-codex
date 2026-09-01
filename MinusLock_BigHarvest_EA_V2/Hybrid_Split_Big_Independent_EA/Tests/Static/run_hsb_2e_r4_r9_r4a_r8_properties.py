#!/usr/bin/env python3
import copy,hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'Tests/Static'))
import verify_hsb_2e_r4_r9_r4a_r8 as v
import accept_hsb_2e_r4_r9_r4a_r8 as a
def sha(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def main():
 fs=v.fixtures();before=sha(fs);v.execute(copy.deepcopy(fs));immutable=before==sha(fs)
 life=next(x['lifecycleSequence'] for x in fs if 'lifecycleSequence'in x and len(x['lifecycleSequence']['steps'])>2);step=life['steps'][0];e1=v.expected_output(step);changed=copy.deepcopy(life);changed['steps'][-1]['operationInput']['context']['actionId']='FUTURE-ONLY';e2=v.expected_output(changed['steps'][0]);causal=e1==e2
 erased=copy.deepcopy(fs)
 for f in erased:f['testContract']={}
 same=(a.run(erased,skip_scope=True)['result']==a.run(fs,skip_scope=True)['result'])
 dup=copy.deepcopy(fs)
 groups={}
 for i,f in enumerate(dup):groups.setdefault(f.get('scenarioInput',{}).get('scenario','LIFECYCLE'),[]).append(i)
 for ix in groups.values():
  src=copy.deepcopy(dup[ix[0]])
  for j in ix[1:]:meta=dup[j]['testContract'];dup[j]=copy.deepcopy(src);dup[j]['testContract']=meta
 duplicate_caught=any(x['check']=='RUNTIME_DERIVED_COVERAGE' for x in a.run(dup,skip_scope=True)['findings'])
 out={'INPUT_IMMUTABLE':immutable,'FUTURE_STEP_INDEPENDENCE':causal,'METADATA_ERASURE_INVARIANT':same,'RUNTIME_DUPLICATES_CAUGHT':duplicate_caught};out['result']='PASS' if all(out.values()) else 'FAIL';print(json.dumps(out,sort_keys=True));return 0 if out['result']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
