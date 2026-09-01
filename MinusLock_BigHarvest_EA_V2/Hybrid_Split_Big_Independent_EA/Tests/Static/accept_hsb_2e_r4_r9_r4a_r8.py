#!/usr/bin/env python3
"""R8 read-only acceptance with an independent, non-empty required-case catalog."""
import argparse,copy,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'Tests/Static'))
import verify_hsb_2e_r4_r9_r4a_r8 as v
import run_hsb_2e_r4_r9_r4a_r8_regressions as regress
import accept_hsb_2e_r4_r9_r4a_r7 as coverage7
CAT=ROOT/'Tests/Contracts/HSB_2E_R4_R9_R4A_R8_REQUIRED_CASES.json';PROTECTED=ROOT/'Tests/Contracts/HSB_2E_R4_R9_R4A_R8_PROTECTED_FILES.json';OUT=ROOT/'Tests/Evidence/R4A_R8/acceptance_result.json';BASE='4a4bd1fd4d41d0b8394e48d34dfb28316351c04d'
def fresh_result(fs=None):return regress.run(fs)
def assess(fresh,fs=None,skip_scope=False):
 findings=[];cat=json.loads(CAT.read_text());expected=cat['expectedCaseIds'];rows=fresh.get('cases',[]);executed=[x.get('caseId') for x in rows]
 if not expected:findings.append({'check':'REQUIRED_CATALOG_EMPTY'})
 if len(expected)!=len(set(expected)):findings.append({'check':'REQUIRED_CATALOG_DUPLICATE'})
 if set(expected)!=set(executed) or len(executed)!=len(expected):findings.append({'check':'REQUIRED_CASE_SET','missing':sorted(set(expected)-set(executed)),'unexpected':sorted(set(executed)-set(expected))})
 if len(executed)!=len(set(executed)):findings.append({'check':'EXECUTED_CASE_DUPLICATE'})
 if fresh.get('required')!=len(expected) or fresh.get('executed')!=len(rows):findings.append({'check':'RUNNER_SUMMARY_NOT_AUTHORITATIVE'})
 bad=[x['caseId'] for x in rows if x.get('result')!='PASS']
 if bad:findings.append({'check':'REGRESSION_OUTCOME','failed':bad})
 obligations=cat['historicalObligations'];covered={x['executedCaseId'] for x in obligations if x['executedCaseId'] in executed}
 if len(obligations)!=86 or any(x['executedCaseId'] not in executed for x in obligations):findings.append({'check':'HISTORICAL_OBLIGATION_LOSS'})
 cf,_=coverage7.coverage(copy.deepcopy(fs or v.fixtures()))
 if cf:findings.append({'check':'RUNTIME_DERIVED_COVERAGE','details':cf})
 try:v.execute(copy.deepcopy(fs or v.fixtures()))
 except v.NormativeError as e:findings.append({'check':'POSITIVE_FIXTURES','detail':str(e)})
 except Exception as e:raise RuntimeError(f'fixture infrastructure: {e}') from e
 if PROTECTED.exists():
  reg=json.loads(PROTECTED.read_text())['files'];badfiles=[]
  for x in reg:
   p=ROOT/x['path']
   if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=x['sha256']:badfiles.append(x['path'])
  if badfiles:findings.append({'check':'PROTECTED_FILES','paths':badfiles})
 if not skip_scope:
  changed=subprocess.run(['git','diff','--name-only',f'{BASE}..HEAD'],cwd=ROOT,text=True,check=True,stdout=subprocess.PIPE).stdout.splitlines();prefix='MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/';badpaths=[x for x in changed if not x.startswith(prefix) or x.endswith(('.mq5','.mqh'))]
  if badpaths:findings.append({'check':'SCOPE','paths':badpaths})
 return {'expectedCaseIds':expected,'executedCaseIds':executed,'missingCaseIds':sorted(set(expected)-set(executed)),'historicalObligations':len(obligations),'coveredObligationTargets':len(covered),'findings':findings,'result':'PASS' if not findings else 'FAIL'}
def run(fs=None,runner=None,skip_scope=False):return assess((runner or fresh_result)(fs),fs,skip_scope)
def main():
 p=argparse.ArgumentParser();p.add_argument('--publish-evidence',action='store_true');a=p.parse_args()
 try:o=run()
 except Exception as e:print(f'INFRASTRUCTURE_ERROR={type(e).__name__}:{e}');return 2
 if a.publish_evidence:OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(o,indent=2,sort_keys=True)+'\n')
 print(f"RESULT={o['result']} EXPECTED={len(o['expectedCaseIds'])} EXECUTED={len(o['executedCaseIds'])} MISSING={len(o['missingCaseIds'])} FINDINGS={len(o['findings'])}");return 0 if o['result']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
