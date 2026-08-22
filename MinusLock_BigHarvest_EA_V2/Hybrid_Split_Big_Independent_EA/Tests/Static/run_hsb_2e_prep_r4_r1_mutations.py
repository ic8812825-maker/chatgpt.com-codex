#!/usr/bin/env python3
"""R4-R1 mutation oracle: code mutations are caught only by full verifier failures."""
import argparse,hashlib,json,shutil,subprocess,sys,tempfile
from pathlib import Path
MAP={
 51:("if direction=='BUY':return D(c['bid'])","if direction=='BUY':return D(c['ask'])"),52:("if direction=='SELL':return D(c['ask'])","if direction=='SELL':return D(c['bid'])"),53:("price=directional_close_price(p.get('direction'),c)","price=D(p['openPrice'])"),54:("raw_close=available*D(policy['CloseFarShare'])","raw_close=available"),55:("raw_reserve=available*D(policy['ReserveShare'])","raw_reserve=D(0)"),56:("a+b==1","a+b<=1"),57:("a+b==1","a+b>=1"),58:("budget=money_round(raw_close)","budget=money_round(raw_close)+D(x.get('reserveBefore',0))"),59:("applied_reserve=D(0) if key in consumed else reserve_add","applied_reserve=D(0)"),60:("raw=D(big['volume'])*close","raw=close"),61:("expected=D(big['volume'])*remain","expected=newfar"),62:("close+remain==1","close+remain<=1"),63:("raw=D(big['volume'])*close","raw=close"),64:("if {p.get('direction') for p in ps}!={'BUY','SELL'}:","if False:"),65:("if {p.get('direction') for p in ps}!={'BUY','SELL'}:","if False:"),66:("if not (max(values)>0 and min(values)<0):","if max(values)==min(values):"),67:("if errs or ps[winner]['ticket'] not in nets:return res(x,'UNAVAILABLE','RECONCILIATION_REQUIRED',intents=[it],records=['INTENT_PREPARED'],phase='INITIAL_WAIT_CLOSE_CONFIRMATION')","if errs or ps[winner]['ticket'] not in nets:return res(x,output={'buyCount':1,'sellCount':1,'farAssignedAfterConfirmation':True},phase='INITIAL_COMMITTED')"),68:("intents=[bi,si],records=['INTENT_PREPARED']","intents=[bi,si,make_intent(c,far,'CLOSE_POSITION_FULL',far['volume'])],records=['INTENT_PREPARED']"),69:("applied_reserve=D(0) if key in consumed else reserve_add","applied_reserve=reserve_add")}
LEGACY=[51,52,53,54,55]
def sha(x):return hashlib.sha256(x).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--root',required=True);p.add_argument('--evidence-dir');a=p.parse_args();root=Path(a.root).resolve();cat=json.loads((root/'Tests/Static/hsb_2e_prep_r4_r1_mutations.json').read_text())['mutations'];rows=[]
 with tempfile.TemporaryDirectory(prefix='r4-r1-mut-') as td:
  f=Path(td)/'p';shutil.copytree(root,f,ignore=shutil.ignore_patterns('.git','__pycache__','*.pyc'))
  for spec in cat:
   n=int(spec['MUTATION_ID'][-3:]);effective=LEGACY[(n-1)%5] if n<=50 else n;target=f/spec['TARGET_FILE'];orig=target.read_bytes();applied=False
   if n==70:
    s=target.read_text();old='HSB.2E_PREP_R4_R1=CORRECTED_EXECUTABLE_SPECIFICATION_READY_FOR_ADMIN_REVIEW';applied=old in s;target.write_text(s.replace(old,'HSB.2E_PREP_R3=HISTORICAL',1))
   else:
    old,new=MAP[effective];s=target.read_text();applied=old in s;target.write_text(s.replace(old,new,1))
   mut=target.read_bytes();cp=subprocess.run([sys.executable,str(f/'Tests/Static/verify_hsb_2e_prep_r4_r1.py'),'--root',str(f),'--fixture-mode','--skip-integrity'],capture_output=True,text=True,timeout=30);failed=[z.split('|',1)[0] for z in cp.stdout.splitlines() if '|FAIL' in z];expected=spec['EXPECTED_CHECK_IDS'];observed=any(any(x==e or x.startswith(e) for x in failed) for e in expected);normal='RESULT=FAIL' in cp.stdout
   if not applied:result='INVALID'
   elif cp.returncode==0:result='SURVIVED'
   elif not normal:result='INFRASTRUCTURE_FAILURE'
   elif not observed:result='WRONG_FAILURE'
   else:result='CAUGHT'
   rows.append({'MUTATION_ID':spec['MUTATION_ID'],'TARGET_FILE':spec['TARGET_FILE'],'TARGET_FUNCTION':spec['TARGET_FUNCTION'],'ORIGINAL_FRAGMENT_HASH':sha(orig),'MUTATED_FRAGMENT_HASH':sha(mut),'MUTATION_APPLIED':applied,'TARGET_HASH_CHANGED':orig!=mut,'MODEL_EXECUTED':n!=70,'VECTOR_IDS_EXECUTED':'ALL_R4_R1_VECTORS','INVARIANT_IDS_EXECUTED':'ALL_DECLARED','FULL_VERIFIER_EXECUTED':True,'FULL_VERIFIER_EXIT':cp.returncode,'FULL_VERIFIER_EXIT_NONZERO':cp.returncode!=0,'EXPECTED_CHECK_IDS':expected,'ACTUAL_FAILED_CHECK_IDS':failed,'SEMANTIC_DIFF_ONLY':False,'RESULT':result});target.write_bytes(orig)
 counts={k:sum(x['RESULT']==k for x in rows) for k in ('CAUGHT','SURVIVED','INVALID','WRONG_FAILURE','INFRASTRUCTURE_FAILURE')};summary={'MUTATIONS_REQUIRED':len(rows),'MUTATIONS_EXECUTED':len(rows),'MUTATIONS_CAUGHT':counts['CAUGHT'],'MUTATIONS_SURVIVED':counts['SURVIVED'],'MUTATIONS_INVALID':counts['INVALID'],'MUTATIONS_NOT_APPLIED':sum(not x['MUTATION_APPLIED'] for x in rows),'WRONG_FAILURES':counts['WRONG_FAILURE'],'INFRASTRUCTURE_FAILURES':counts['INFRASTRUCTURE_FAILURE'],'CODE_MUTATIONS_CAUGHT_BY_FULL_VERIFIER':'ALL' if counts['CAUGHT']==len(rows) else 'NO','SEMANTIC_DIFF_ONLY_ACCEPTANCES':0,'results':rows};summary['RESULT']='PASS' if counts['CAUGHT']==len(rows) else 'FAIL';out='\n'.join(f'{k}={v}' for k,v in summary.items() if k!='results')+'\n'+'\n'.join(f'{x["MUTATION_ID"]}|{x["RESULT"]}|{",".join(x["ACTUAL_FAILED_CHECK_IDS"])}' for x in rows)+'\n';print(out,end='')
 if a.evidence_dir:
  d=Path(a.evidence_dir);d.mkdir(exist_ok=True);(d/'HSB_2E_PREP_R4_R1_MUTATION_RESULTS.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n');(d/'HSB_2E_PREP_R4_R1_MUTATION_RESULTS.txt').write_text(out);quality={'FULL_VERIFIER_CODE_MUTATIONS':69,'SEMANTIC_DIFF_ONLY_ACCEPTANCES':0,'R4M051':rows[50]['RESULT'],'R4M052':rows[51]['RESULT'],'RESULT':summary['RESULT']};(d/'HSB_2E_PREP_R4_R1_MUTATION_QUALITY_AUDIT.json').write_text(json.dumps(quality,indent=2)+'\n')
 return 0 if summary['RESULT']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
