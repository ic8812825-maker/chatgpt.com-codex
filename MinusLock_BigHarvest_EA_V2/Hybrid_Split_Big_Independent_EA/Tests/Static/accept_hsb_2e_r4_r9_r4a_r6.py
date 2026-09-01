#!/usr/bin/env python3
"""Read-only R6 acceptance; current regressions are executed, never loaded from evidence."""
import argparse,copy,hashlib,json,subprocess
from collections import defaultdict
from pathlib import Path
import verify_hsb_2e_r4_r9_r4a_r6 as v
import run_hsb_2e_r4_r9_r4a_r6_regressions as regress
ROOT=v.ROOT;BASE='c118d2e3d810d0708c3960f0ab78fbd891964eed';OUT=ROOT/'Tests/Evidence/R4A_R6/acceptance_result.json'
SERVICE={'fixtureId','description','tags','boundaryProperty','transactionId','actionId','intentId','dealId','eventId','ticket','proposalId','timestamp','createdTimestamp','expiresTimestamp','stateDigest','digest'}
def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':'))
def normalized(x):
 if isinstance(x,dict):return {k:normalized(z) for k,z in x.items() if k not in SERVICE and not k.endswith('Digest')}
 if isinstance(x,list):return [normalized(z) for z in x]
 return x
def coverage(fs):
 groups=defaultdict(list);exact=set();semantic=set();findings=[];table=[]
 for f in fs:
  if 'lifecycleSequence'in f:
   seq=f['lifecycleSequence'];key='LIFECYCLE';runtime=seq;props={'operations':[s['operation'] for s in seq['steps']],'stepCount':len(seq['steps'])}
  else:
   r=f['scenarioInput'];key=r['scenario'];runtime=r;deals=r['deals'] if 'deals'in r else [];props={'directions':sorted({p['direction'] for p in r['positions']}),'minimumVolume':any(p['volume']==r['broker']['volumeMin'] for p in r['positions']),'nontrivialTick':r['broker']['tickSize']!=r['broker']['point'],'nonzeroCosts':any(any(z not in ('0','0.0','0.00') for z in (d['commission'],d['swap'],d['fee'])) for d in deals),'multiFill':len(deals)>1,'phase':r['phase'],'persistedEvidence':bool(r['persistedState'].get('consumedDealIds',[]))}
  raw=hashlib.sha256(canon(runtime).encode()).hexdigest();sem=hashlib.sha256(canon(normalized(runtime)).encode()).hexdigest();groups[key].append(props)
  if raw in exact:findings.append({'check':'EXACT_RUNTIME_DUPLICATE','group':key})
  exact.add(raw)
  if sem in semantic:findings.append({'check':'SEMANTIC_RUNTIME_DUPLICATE','group':key})
  semantic.add(sem);table.append({'scenario':key,'derivedProperties':props,'runtimeSha256':raw,'semanticShapeSha256':sem})
 if len(groups)!=7 or any(len(x)!=4 for x in groups.values()):findings.append({'check':'GROUP_DISTRIBUTION','groups':{k:len(x) for k,x in groups.items()}})
 for k,rows in groups.items():
  if k=='LIFECYCLE':
   if len({tuple(x['operations']) for x in rows})<4:findings.append({'check':'LIFECYCLE_DIVERSITY'})
  else:
   aggregate={p for p in ('minimumVolume','nontrivialTick','nonzeroCosts','multiFill') if any(x[p] for x in rows)}
   directions={d for x in rows for d in x['directions']}
   if aggregate!={'minimumVolume','nontrivialTick','nonzeroCosts','multiFill'} or directions!={'BUY','SELL'}:findings.append({'check':'RUNTIME_BOUNDARY_COVERAGE','group':k,'properties':sorted(aggregate),'directions':sorted(directions)})
 return findings,table
def git(*a):return subprocess.run(('git',*a),cwd=ROOT,check=True,text=True,stdout=subprocess.PIPE).stdout.strip()
def run(fs=None):
 fs=copy.deepcopy(fs or v.fixtures());findings=[]
 try:v.execute(fs)
 except v.NormativeError as e:findings.append({'check':'FIXTURE_VALIDATION','detail':str(e)})
 fresh=regress.run(fs);required={x['caseId'] for x in fresh['cases']}
 if fresh['required']!=fresh['executed'] or fresh['wrongFailures'] or fresh['unexpectedInfrastructureErrors'] or len(required)!=fresh['required']:findings.append({'check':'FRESH_REGRESSIONS','summary':fresh})
 cf,table=coverage(fs);findings+=cf
 protected=json.loads((ROOT/'Tests/Contracts/HSB_2E_R4_R9_R4A_R6_PROTECTED_FILES.json').read_text())['files'];m=[]
 for x in protected:
  if hashlib.sha256((ROOT/x['path']).read_bytes()).hexdigest()!=x['sha256']:m.append(x['path'])
 if m:findings.append({'check':'PROTECTED_FILES','mismatches':m})
 changed=git('diff','--name-only',f'{BASE}..HEAD').splitlines();prefix='MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/';external=[x for x in changed if not x.startswith(prefix)];production=[x for x in changed if x.endswith(('.mq5','.mqh'))];native=[x for x in changed if 'hsb_2e_reference_model_r4_r9_r3.py'in x or 'run_hsb_2e_r4_r9_r3_'in x]
 if external or production or native:findings.append({'check':'SCOPE','external':external,'production':production,'native':native})
 return {'findings':findings,'freshRegression':{'required':fresh['required'],'executed':fresh['executed'],'wrongFailures':fresh['wrongFailures'],'unexpectedInfrastructureErrors':fresh['unexpectedInfrastructureErrors']},'coverageTable':table,'protectedFiles':len(protected),'protectedMismatches':len(m),'scopeViolations':len(external),'productionDiffPaths':production,'nativeModelChanged':bool(native),'result':'PASS' if not findings else 'FAIL'}
def main():
 p=argparse.ArgumentParser();p.add_argument('--publish-evidence',action='store_true');a=p.parse_args()
 try:o=run()
 except Exception as e:print(f'INFRASTRUCTURE_ERROR={type(e).__name__}:{e}');return 2
 if a.publish_evidence:OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(o,indent=2,sort_keys=True)+'\n')
 print(f"RESULT={o['result']} FINDINGS={len(o['findings'])} FRESH_REGRESSIONS={o['freshRegression']['executed']}");return 0 if o['result']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
