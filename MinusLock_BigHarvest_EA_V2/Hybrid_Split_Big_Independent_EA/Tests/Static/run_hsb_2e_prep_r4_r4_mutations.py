#!/usr/bin/env python3
"""Run unique semantic and evidence mutations in disposable fixtures."""
import argparse,hashlib,json,shutil,subprocess,sys,tempfile
from pathlib import Path

def digest(data): return hashlib.sha256(data).hexdigest()

def main():
 p=argparse.ArgumentParser();p.add_argument('--root',required=True);p.add_argument('--evidence-dir');a=p.parse_args()
 root=Path(a.root).resolve();catalog=json.loads((root/'Tests/Static/hsb_2e_prep_r4_r4_mutations.json').read_text())['mutations']
 ids=[x['MUTATION_ID'] for x in catalog]
 specs=[(x['TARGET_FILE'],x.get('OPERATION','REPLACE'),x.get('BEFORE',''),x.get('AFTER',''),x['SEMANTIC_PURPOSE']) for x in catalog]
 duplicates=len(ids)-len(set(ids))+len(specs)-len(set(specs));rows=[]
 with tempfile.TemporaryDirectory(prefix='r4-r4-mut-') as td:
  fixture=Path(td)/'project';shutil.copytree(root,fixture,ignore=shutil.ignore_patterns('.git','__pycache__','*.pyc'))
  for mutation in catalog:
   target=fixture/mutation['TARGET_FILE'];operation=mutation.get('OPERATION','REPLACE');original=target.read_bytes() if target.exists() else b'';applied=False
   if operation=='REPLACE' and target.exists():
    source=target.read_text();applied=source.count(mutation['BEFORE'])==1
    if applied: target.write_text(source.replace(mutation['BEFORE'],mutation['AFTER'],1))
   elif operation=='DELETE' and target.exists(): target.unlink();applied=True
   elif operation=='ADD' and not target.exists(): target.write_text(mutation['AFTER']);applied=True
   elif operation=='DUPLICATE_LINE' and target.exists():
    lines=target.read_text().splitlines(True);applied=bool(lines)
    if applied: target.write_text(lines[0]+''.join(lines))
   changed=(not target.exists()) or target.read_bytes()!=original
   for cache in fixture.glob('Tests/**/__pycache__'): shutil.rmtree(cache,ignore_errors=True)
   command=[sys.executable,str(fixture/'Tests/Static/verify_hsb_2e_prep_r4_r4.py'),'--root',str(fixture),'--fixture-mode']
   if mutation.get('TYPE','SEMANTIC')=='SEMANTIC': command.append('--skip-integrity')
   try: completed=subprocess.run(command,capture_output=True,text=True,timeout=30);failed=[line.split('|',1)[0] for line in completed.stdout.splitlines() if '|FAIL' in line];normal='RESULT=FAIL' in completed.stdout
   except (OSError,subprocess.TimeoutExpired): completed=None;failed=[];normal=False
   observed=any(x==mutation['EXPECTED_CHECK_ID'] or x.startswith(mutation['EXPECTED_CHECK_ID']) for x in failed)
   result='INVALID' if not applied or not changed else 'INFRASTRUCTURE_FAILURE' if completed is None else 'SURVIVED' if completed.returncode==0 else 'INFRASTRUCTURE_FAILURE' if not normal else 'WRONG_FAILURE' if not observed else 'CAUGHT'
   rows.append({**mutation,'BEFORE_HASH':digest(original),'AFTER_HASH':digest(target.read_bytes()) if target.exists() else None,'APPLIED':applied,'FULL_VERIFIER_EXIT':None if completed is None else completed.returncode,'ACTUAL_FAILED_CHECK_IDS':failed,'RESULT':result})
   if target.exists(): target.unlink()
   if original: target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(original)
 counts={key:sum(row['RESULT']==key for row in rows) for key in ('CAUGHT','SURVIVED','INVALID','WRONG_FAILURE','INFRASTRUCTURE_FAILURE')}
 summary={'MUTATION_IDS':len(ids),'UNIQUE_TRANSFORMS':len(set(specs)),'UNIQUE_TARGET_TRANSFORM_PAIRS':len({x[:4] for x in specs}),'DUPLICATE_MUTATIONS':duplicates,'NOT_APPLIED':sum(not x['APPLIED'] for x in rows),'MUTATIONS_EXECUTED':len(rows),'MUTATIONS_CAUGHT':counts['CAUGHT'],'SURVIVED':counts['SURVIVED'],'INVALID':counts['INVALID'],'WRONG_FAILURES':counts['WRONG_FAILURE'],'INFRASTRUCTURE_FAILURES':counts['INFRASTRUCTURE_FAILURE'],'results':rows}
 summary['RESULT']='PASS' if not duplicates and counts['CAUGHT']==len(rows) else 'FAIL'
 output='\n'.join(f'{key}={value}' for key,value in summary.items() if key!='results')+'\n'+'\n'.join(f'{x["MUTATION_ID"]}|{x["RESULT"]}|{",".join(x["ACTUAL_FAILED_CHECK_IDS"])}' for x in rows)+'\n';print(output,end='')
 if a.evidence_dir:
  directory=Path(a.evidence_dir);directory.mkdir(exist_ok=True)
  (directory/'HSB_2E_PREP_R4_R4_MUTATION_RESULTS.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
  (directory/'HSB_2E_PREP_R4_R4_MUTATION_RESULTS.txt').write_text(output)
  (directory/'HSB_2E_PREP_R4_R4_MUTATION_UNIQUENESS_AUDIT.json').write_text(json.dumps({k:v for k,v in summary.items() if k!='results'},indent=2,sort_keys=True)+'\n')
 return 0 if summary['RESULT']=='PASS' else 1
if __name__=='__main__': raise SystemExit(main())
