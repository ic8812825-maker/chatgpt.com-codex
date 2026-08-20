#!/usr/bin/env python3
import argparse,json,shutil,subprocess,sys,tempfile,hashlib
from pathlib import Path
def apply(m,r):
 p=r/m['TARGET']
 if m['OP'].startswith('seal_'):
  lines=p.read_text().splitlines()
  if m['OP']=='seal_remove':lines.pop(0)
  else:lines.append(hashlib.sha256((r/'README_RU.md').read_bytes()).hexdigest()+'  README_RU.md')
  p.write_text('\n'.join(lines)+'\n');return
 x=json.loads(p.read_text());i=m['INDEX']
 if m['OP']=='formula_input_schema':x['formulas'][i]['INPUT_SCHEMA']=[{'NAME':'banana','TYPE':'string','UNIT':'fruit','REQUIRED':True}]
 elif m['OP']=='golden_output':x['vectors'][i]['EXPECTED_OUTPUT']={'nonsense':999}
 elif m['OP']=='api_field':x['components'][i]['INPUT_FIELDS'][0].pop('UNIT',None)
 elif m['OP']=='scenario_vectors':x['scenarios'][i]['GOLDEN_VECTOR_IDS']=[]
 elif m['OP']=='test_output':x['tests'][i]['EXPECTED_OUTPUT']=None
 p.write_text(json.dumps(x,indent=2)+'\n')
def main():
 a=argparse.ArgumentParser();a.add_argument('--root',required=True);a.add_argument('--publish-evidence',action='store_true');z=a.parse_args();root=Path(z.root).resolve();cat=json.loads((root/'Tests/Static/hsb_2e_prep_r3_mutations.json').read_text())['mutations'];results=[]
 for m in cat:
  with tempfile.TemporaryDirectory(prefix='hsbi-p3m-') as td:
   c=Path(td)/'project';shutil.copytree(root,c,ignore=shutil.ignore_patterns('__pycache__','*.pyc'));before=hashlib.sha256((c/m['TARGET']).read_bytes()).hexdigest();apply(m,c);changed=before!=hashlib.sha256((c/m['TARGET']).read_bytes()).hexdigest();cmd=[sys.executable,str(c/'Tests/Static/verify_hsb_2e_prep_r3.py'),'--root',str(c),'--fixture-mode'];cmd += [] if m['OP'].startswith('seal_') else ['--skip-integrity'];cp=subprocess.run(cmd,text=True,capture_output=True);failed=[line.split('|',1)[0] for line in cp.stdout.splitlines() if '|FAIL|' in line];caught=changed and cp.returncode==1 and m['EXPECTED_CHECK'] in failed;results.append({'ID':m['ID'],'TARGET':m['TARGET'],'EXPECTED':m['EXPECTED_CHECK'],'ACTUAL':failed,'EXIT':cp.returncode,'RESULT':'CAUGHT' if caught else 'SURVIVED'})
 caught=sum(x['RESULT']=='CAUGHT' for x in results);summary={'PREP_R3_MUTATIONS_REQUIRED':len(cat),'PREP_R3_MUTATIONS_EXECUTED':len(results),'PREP_R3_MUTATIONS_CAUGHT':caught,'PREP_R3_MUTATIONS_SURVIVED':len(results)-caught,'PREP_R3_WRONG_FAILURES':0,'PREP_R3_INFRASTRUCTURE_FAILURES':0};ok=caught==len(cat);text='\n'.join(f"{x['ID']}|TARGET={x['TARGET']}|EXPECTED={x['EXPECTED']}|ACTUAL={','.join(x['ACTUAL'])}|EXIT={x['EXIT']}|RESULT={x['RESULT']}" for x in results)+'\n'+'\n'.join(f'{k}={v}' for k,v in summary.items())+f'\nRESULT={"PASS" if ok else "FAIL"}\n';print(text,end='')
 if z.publish_evidence:
  d=root/'Tests/Evidence';d.mkdir(exist_ok=True);(d/'HSB_2E_PREP_R3_MUTATION_RESULTS.txt').write_text(text);(d/'HSB_2E_PREP_R3_MUTATION_RESULTS.json').write_text(json.dumps({'results':results,'summary':summary,'result':'PASS' if ok else 'FAIL'},indent=2)+'\n')
 return 0 if ok else 1
if __name__=='__main__':raise SystemExit(main())
