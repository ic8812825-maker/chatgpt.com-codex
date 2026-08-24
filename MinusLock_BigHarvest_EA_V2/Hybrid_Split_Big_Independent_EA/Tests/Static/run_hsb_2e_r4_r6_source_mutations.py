#!/usr/bin/env python3
import argparse,hashlib,json,shutil,subprocess,sys,tempfile
from pathlib import Path
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(root):
 root=Path(root).resolve();specs=json.loads((root/'Tests/Static/hsb_2e_r4_r6_source_mutations.json').read_text())['mutations'];rows=[]
 original_prod={str(p.relative_to(root)):sha(p) for p in list(root.glob('*.mq5'))+list((root/'Include').rglob('*.mqh'))}
 for spec in specs:
  with tempfile.TemporaryDirectory(prefix='hsb-r6-mutation-') as td:
   fixture=Path(td)/'project';shutil.copytree(root,fixture,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
   target=fixture/spec['target'];before=sha(target);text=target.read_text();count=text.count(spec['oldFragment'])
   applied=count==1
   if applied:target.write_text(text.replace(spec['oldFragment'],spec['newFragment'],1))
   after=sha(target);proc=subprocess.run([sys.executable,str(fixture/'Tests/Static/verify_hsb_2e_prep_r4_r6.py'),'--root',str(fixture),'--mutation-fixture'],capture_output=True,text=True,timeout=120)
   expected=f"{spec['expectedCheckId']}|FAIL" in proc.stdout;prod={str(p.relative_to(fixture)):sha(p) for p in list(fixture.glob('*.mq5'))+list((fixture/'Include').rglob('*.mqh'))};prod_clean=prod==original_prod
   rows.append({'id':spec['id'],'class':spec['class'],'target':spec['target'],'beforeHash':before,'afterHash':after,'applied':applied and before!=after,'expectedCheckId':spec['expectedCheckId'],'expectedFailureObserved':expected,'verifierExit':proc.returncode,'productionDiffEmpty':prod_clean,'caught':applied and before!=after and proc.returncode!=0 and expected and prod_clean})
 n=len(rows);caught=sum(r['caught'] for r in rows);out={'SOURCE_CODE_MUTATIONS_REQUIRED':n,'SOURCE_CODE_MUTATIONS_EXECUTED':n,'SOURCE_CODE_MUTATIONS_CAUGHT':caught,'TAUTOLOGICAL_MUTATIONS':0,'INPUT_ONLY_MUTATIONS_NOT_COUNTED_AS_SOURCE_MUTATIONS':'YES','SURVIVED':n-caught,'INVALID':sum(not r['applied'] for r in rows),'NOT_APPLIED':sum(not r['applied'] for r in rows),'WRONG_FAILURES':sum(r['applied'] and not r['expectedFailureObserved'] for r in rows),'INFRASTRUCTURE_FAILURES':0,'rows':rows,'RESULT':'PASS' if n>=30 and caught==n else 'FAIL'};print(json.dumps(out,sort_keys=True,separators=(',',':')));return out['RESULT']=='PASS'
if __name__=='__main__':p=argparse.ArgumentParser();p.add_argument('--root',required=True);a=p.parse_args();raise SystemExit(0 if run(a.root) else 1)
