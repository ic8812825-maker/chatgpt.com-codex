#!/usr/bin/env python3
"""Computed acceptance for R5. Exit: 0 pass, 1 normative finding, 2 infrastructure."""
from __future__ import annotations
from collections import defaultdict
import hashlib,json,subprocess
from pathlib import Path
import verify_hsb_2e_r4_r9_r4a_r5 as v
ROOT=v.ROOT;BASE='634f250beac05baed4d9ee42f851d2d13dd63208';OUT=ROOT/'Tests/Evidence/R4A_R5/acceptance_result.json'
def git(*a):return subprocess.run(('git',*a),cwd=ROOT,check=True,text=True,stdout=subprocess.PIPE).stdout.strip()
def main():
 try:
  findings=[];fixtures=v.fixtures();results=[]
  for f in fixtures:
   try:res=v.lifecycle(f['lifecycleSequence']) if 'lifecycleSequence'in f else v.runtime(f['scenarioInput']);results.append(res)
   except v.NormativeError as e:findings.append({'check':'FIXTURE_VALIDATION','fixture':f['testContract']['fixtureId'],'detail':str(e)})
  if len(fixtures)!=28:findings.append({'check':'FIXTURE_COUNT','actual':len(fixtures)})
  groups=defaultdict(list);far_mismatch=0;phase_coverage=set();coverage=[];lifecycle_steps=0
  for f in fixtures:
   tc=f['testContract'];groups[tc['scenario']].append(f)
   if 'lifecycleSequence'in f:
    lifecycle_steps+=len(f['lifecycleSequence']['steps']);continue
   r=f['scenarioInput'];phase_coverage.add(r['phase']);far=r['persistedState']['farState']
   if far['active']:
    matches=[p for p in r['positions'] if p['ticket']==far['ticket'] and p['role']=='FAR' and p['volume']==far['volume'] and p['direction']==far['direction']]
    far_mismatch+=len(matches)!=1
   costs=[str(d['commission'])+','+str(d['swap'])+','+str(d['fee']) for d in r['deals']]
   coverage.append({'fixtureId':tc['fixtureId'],'scenario':r['scenario'],'phase':r['phase'],'boundaryProperty':tc['boundaryProperty'],'actualBoundaryValues':{'tickSize':r['broker']['tickSize'],'volumeStep':r['broker']['volumeStep'],'volumes':[p['volume'] for p in r['positions']]},'recordCounts':{k:len(r[k]) for k in ('positions','intents','deals','events')},'positionRoles':[p['role'] for p in r['positions']],'costCase':costs,'persistenceCase':'ACCUMULATED' if r['persistedState']['consumedDealIds'] else 'FRESH'})
  if far_mismatch:findings.append({'check':'FAR_ROLE_CONSISTENCY','mismatches':far_mismatch})
  if phase_coverage!={'PRE_COMMIT','COMMITTED','REPLAY'}:findings.append({'check':'PHASE_COVERAGE','actual':sorted(phase_coverage)})
  if any(len(x)!=4 for x in groups.values()) or len(groups)!=7:findings.append({'check':'GROUP_DISTRIBUTION','actual':{k:len(z) for k,z in groups.items()}})
  for name,items in groups.items():
   boundaries={x['testContract'].get('boundaryProperty') for x in items}
   if len(boundaries)!=4:findings.append({'check':'DIVERSITY','scenario':name,'boundaryProperties':sorted(str(x) for x in boundaries)})
  if lifecycle_steps<8:findings.append({'check':'LIFECYCLE_STEPS','actual':lifecycle_steps})
  regress=json.loads((ROOT/'Tests/Evidence/R4A_R5/regression_results.json').read_text())
  if regress['wrongFailures'] or regress['unexpectedInfrastructureErrors'] or regress['required']!=regress['executed']:findings.append({'check':'REGRESSION','summary':regress})
  required_cert={'CERT_ZERO_DIGEST','CERT_BODY_CHANGED','CERT_CLAIM_RESEALED','CERT_OTHER_OPERATION','CERT_MISSING_COMMITTED','VALID_PRECOMMIT_NO_CERT','CERT_PROVIDED_PRECOMMIT'}
  passed={x['caseId'] for x in regress['cases'] if x['result']=='PASS'}
  if not required_cert<=passed:findings.append({'check':'CERTIFICATE_PROBES','missing':sorted(required_cert-passed)})
  protected=json.loads((ROOT/'Tests/Evidence/R4A_R5/historical_counterexamples.json').read_text())['protectedFiles'];mismatches=[]
  for x in protected:
   p=ROOT/x['path'];actual=hashlib.sha256(p.read_bytes()).hexdigest()
   if actual!=x['sha256']:mismatches.append(x['path'])
  if mismatches:findings.append({'check':'PROTECTED_FILES','mismatches':mismatches})
  changed=git('diff','--name-only',f'{BASE}..HEAD').splitlines();prefix='MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/';external=[x for x in changed if not x.startswith(prefix)];production=[x for x in changed if x.endswith('.mq5') or ('/Include/'in x and x.endswith('.mqh'))];native=[x for x in changed if 'hsb_2e_reference_model_r4_r9_r3.py'in x or 'run_hsb_2e_r4_r9_r3_'in x]
  if external or production or native:findings.append({'check':'SCOPE','external':external,'production':production,'native':native})
  out={'requiredChecks':8,'executedChecks':8,'findings':findings,'fixtureCount':len(fixtures),'lifecycleSteps':lifecycle_steps,'phaseCoverage':sorted(phase_coverage),'farRoleMismatches':far_mismatch,'coverageTable':coverage,'regression':{'required':regress['required'],'executed':regress['executed'],'normativeRejections':regress['normativeRejections'],'wrongFailures':regress['wrongFailures'],'unexpectedInfrastructureErrors':regress['unexpectedInfrastructureErrors']},'protectedFilesRequired':len(protected),'protectedFileMismatches':len(mismatches),'scopeViolations':len(external),'productionDiffPaths':production,'nativeModelChanged':bool(native),'lifecycleDeclaredChainValidated':not any(x['check'].startswith('LIFECYCLE') for x in findings),'lifecycleExecutedByNativeModel':False,'fullEconomicCorrectness':'NOT_PROVEN','result':'PASS' if not findings else 'FAIL'}
  OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(f"RESULT={out['result']} FINDINGS={len(findings)} FIXTURES={len(fixtures)} LIFECYCLE_STEPS={lifecycle_steps}");return 0 if not findings else 1
 except Exception as e:
  print(f'INFRASTRUCTURE_ERROR={type(e).__name__}:{e}');return 2
if __name__=='__main__':raise SystemExit(main())
