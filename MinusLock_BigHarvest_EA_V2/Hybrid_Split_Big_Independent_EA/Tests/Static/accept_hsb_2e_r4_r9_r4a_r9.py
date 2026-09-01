#!/usr/bin/env python3
"""R9 acceptance independently derives every outcome from the normative case contract."""
import argparse,copy,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'Tests/Static'))
import verify_hsb_2e_r4_r9_r4a_r9 as v
import run_hsb_2e_r4_r9_r4a_r9_regressions as regress
import accept_hsb_2e_r4_r9_r4a_r7 as coverage7
CAT=ROOT/'Tests/Contracts/HSB_2E_R4_R9_R4A_R9_CASE_CONTRACT.json';PROTECTED=ROOT/'Tests/Contracts/HSB_2E_R4_R9_R4A_R9_PROTECTED_FILES.json';OUT=ROOT/'Tests/Evidence/R4A_R9/acceptance_result.json';BASE='db47f2c091ac900323b14452b321e8e7581a30cc'
def fresh_result(fs=None):return regress.run(fs)
def assess(fresh,fs=None,skip_scope=False):
 findings=[];cat=json.loads(CAT.read_text());contracts=cat['cases'];expected={x['caseId']:x for x in contracts};rows=fresh.get('cases')
 if not isinstance(rows,list):return {'result':'FAIL','findings':[{'check':'OUTCOME_ROWS_MISSING'}]}
 ids=[x.get('caseId') for x in rows]
 if not expected or len(expected)!=len(contracts):findings.append({'check':'CONTRACT_EMPTY_OR_DUPLICATE'})
 if set(ids)!=set(expected) or len(ids)!=len(expected):findings.append({'check':'CASE_SET','missing':sorted(set(expected)-set(ids)),'unexpected':sorted(set(ids)-set(expected))})
 if len(ids)!=len(set(ids)):findings.append({'check':'DUPLICATE_CASE_ID'})
 required={'caseId','actualClass','actualCheckId','actualReason','executionStatus'}
 for row in rows:
  cid=row.get('caseId')
  if not required<=set(row):findings.append({'check':'ACTUAL_FIELDS_MISSING','caseId':cid});continue
  if row['actualClass'] not in cat['outcomeEnums'] or row['executionStatus']!='EXECUTED':findings.append({'check':'ACTUAL_ENUM_OR_EXECUTION','caseId':cid});continue
  if cid not in expected:continue
  exp=expected[cid];actual=(row['actualClass'],row['actualCheckId'],row['actualReason']);wanted=(exp['expectedClass'],exp['expectedCheckId'],exp['expectedReason'])
  derived='PASS' if actual==wanted else 'FAIL'
  if actual!=wanted:findings.append({'check':'OUTCOME_MISMATCH','caseId':cid,'expected':wanted,'actual':actual})
  if 'result' in row and row['result']!=derived:findings.append({'check':'CONTRADICTORY_DIAGNOSTIC_RESULT','caseId':cid})
 if fresh.get('required')!=len(expected) or fresh.get('executed')!=len(rows):findings.append({'check':'SUMMARY_MISMATCH'})
 obligations=cat['historicalObligations']
 if len(obligations)!=86 or any(x['caseId'] not in ids for x in obligations):findings.append({'check':'HISTORICAL_VARIANT_MISSING'})
 cf,_=coverage7.coverage(copy.deepcopy(fs or v.fixtures()))
 if cf:findings.append({'check':'RUNTIME_DERIVED_COVERAGE','details':cf})
 try:v.execute(copy.deepcopy(fs or v.fixtures()))
 except v.NormativeError as e:findings.append({'check':'POSITIVE_FIXTURE','detail':str(e)})
 reg=json.loads(PROTECTED.read_text())['files'];badfiles=[x['path'] for x in reg if not (ROOT/x['path']).is_file() or hashlib.sha256((ROOT/x['path']).read_bytes()).hexdigest()!=x['sha256']]
 if badfiles:findings.append({'check':'PROTECTED_FILES','paths':badfiles})
 if not skip_scope:
  changed=subprocess.run(['git','diff','--name-only',f'{BASE}..HEAD'],cwd=ROOT,text=True,check=True,stdout=subprocess.PIPE).stdout.splitlines();prefix='MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/';bad=[x for x in changed if not x.startswith(prefix) or x.endswith(('.mq5','.mqh'))]
  if bad:findings.append({'check':'SCOPE','paths':bad})
 return {'expected':len(expected),'executed':len(rows),'historicalVariants':len(obligations),'findings':findings,'result':'PASS' if not findings else 'FAIL'}
def run(fs=None,runner=None,skip_scope=False):return assess((runner or fresh_result)(fs),fs,skip_scope)
def main():
 p=argparse.ArgumentParser();p.add_argument('--publish-evidence',action='store_true');a=p.parse_args()
 try:o=run()
 except Exception as e:print(f'INFRASTRUCTURE_ERROR={type(e).__name__}:{e}');return 2
 if a.publish_evidence:OUT.write_text(json.dumps(o,indent=2,sort_keys=True)+'\n')
 print(f"RESULT={o['result']} EXPECTED={o['expected']} EXECUTED={o['executed']} FINDINGS={len(o['findings'])}");return 0 if o['result']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
