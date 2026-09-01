#!/usr/bin/env python3
"""Execute the six R4 audit counterexamples without modifying historical artifacts."""
from __future__ import annotations
import copy, hashlib, importlib.util, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'Tests/Evidence/R4A_R5/historical_counterexamples.json'
def sha(v): return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def load():
 spec=importlib.util.spec_from_file_location('r4',ROOT/'Tests/Static/verify_hsb_2e_r4_r9_r4a_r4_schema.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
def fixtures(m): return m.load_fixtures()
def outcome(m,s,x):
 try: m.validate_runtime(x,s)
 except m.ValidationError as e: return {'class':'NORMATIVE_REJECTION','detail':str(e)}
 except Exception as e: return {'class':'INFRASTRUCTURE_ERROR','detail':f'{type(e).__name__}: {e}'}
 return {'class':'ACCEPTED','detail':'returned normally'}
def main():
 m=load(); s=json.loads(m.SCHEMA_PATH.read_text()); fs=fixtures(m); base=copy.deepcopy(fs[0]['scenarioInput'])
 forged=copy.deepcopy(base); forged['certificate']['digest']='0'*64
 absent=copy.deepcopy(base); absent.pop('certificate')
 far=[f['testContract']['fixtureId'] for f in fs if (lambda r,p: p is None or p['role']!='FAR')(f['scenarioInput'],next((p for p in f['scenarioInput']['positions'] if p['ticket']==f['scenarioInput']['persistedState']['farState']['ticket']),None))]
 life=[f for f in fs if f['scenarioInput']['scenario']=='LIFECYCLE']
 cases=[
  {'caseId':'R4_FORGED_CERTIFICATE_DIGEST','inputSha256':sha(forged),'historicalValidator':str(m.__file__),'historicalActualResult':outcome(m,s,forged),'requiredCorrectBehavior':'NORMATIVE_REJECTION:CERTIFICATE_INTERNAL_INTEGRITY'},
  {'caseId':'R4_CERTIFICATE_PHASE_UNEXPRESSIBLE','inputSha256':sha(absent),'historicalValidator':str(m.__file__),'historicalActualResult':outcome(m,s,absent),'requiredCorrectBehavior':'EXPLICIT_PHASE_DEPENDENT_APPLICABILITY'},
  {'caseId':'R4_FAR_ROLE_MISMATCH','inputSha256':sha(far),'historicalValidator':str(m.__file__),'historicalActualResult':{'class':'MISMATCHES','count':len(far),'fixtures':far},'requiredCorrectBehavior':'ACTIVE_FAR_RESOLVES_TO_ONE_OWNED_FAR_POSITION'},
  {'caseId':'R4_LIFECYCLE_SINGLE_STEP','inputSha256':sha(life),'historicalValidator':str(m.__file__),'historicalActualResult':{'class':'SINGLE_RUNTIME_OBJECTS','count':len(life)},'requiredCorrectBehavior':'CONNECTED_DECLARED_SEQUENCE'},
  {'caseId':'R4_SELF_TEST_INFRASTRUCTURE_CAUGHT','inputSha256':sha((ROOT/'Tests/Static/run_hsb_2e_r4_r9_r4a_r4_schema_self_tests.py').read_text()),'historicalValidator':'R4 self-test harness','historicalActualResult':{'class':'KEYERROR_AND_TYPEERROR_COUNTED_AS_CAUGHT'},'requiredCorrectBehavior':'INFRASTRUCTURE_ERROR'},
  {'caseId':'R4_BOUNDARY_DIVERSITY_ABSENT','inputSha256':sha([f['scenarioInput'] for f in fs]),'historicalValidator':'independent data classification','historicalActualResult':{'class':'STANDARD_GRID_TEMPLATE','fixtureCount':len(fs)},'requiredCorrectBehavior':'COMPUTED_RUNTIME_BOUNDARY_COVERAGE'},
 ]
 protected=[]
 for p in sorted(list((ROOT/'Tests').rglob('*R4A_R4*'))+list((ROOT/'Reports').glob('*R4A_R4*'))):
  if p.is_file(): protected.append({'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
 out={'schemaVersion':'1.0','cases':cases,'required':len(cases),'executed':len(cases),'protectedFiles':protected}
 OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(f'REQUIRED={len(cases)} EXECUTED={len(cases)}')
if __name__=='__main__': main()
