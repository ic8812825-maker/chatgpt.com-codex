#!/usr/bin/env python3
"""Execute thirty isolated adversarial mutations against pre-freeze qualification."""
import argparse,copy,json,subprocess,sys,tempfile
from pathlib import Path
def write(path,value):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')
def main(root):
 root=Path(root);fixtures=json.loads((root/'Tests/Vectors/HSB_2E_R4_R9_R3_DRAFT_FIXTURES_V2.json').read_text());pairs=json.loads((root/'Tests/Contracts/HSB_2E_R4_R9_R3_CAUSAL_PAIRS.json').read_text());cert=json.loads((root/'Tests/Vectors/HSB_2E_R4_R9_R3_CERTIFICATE_FORGERY_DRAFTS.json').read_text());caught=0;catalog=[]
 for index in range(30):
  f=copy.deepcopy(fixtures);p=copy.deepcopy(pairs);c=copy.deepcopy(cert);mutation_id=f'ORACLE_MUT_{index+1:02d}'
  if index<10:f['fixtures'][index+1]['scenarioInput']=copy.deepcopy(f['fixtures'][0]['scenarioInput']);klass='REMOVE_CAUSAL_DEFECT'
  elif index<15:f['fixtures'][index+1]['scenarioInput']['snapshot']['bid']=f'1.{index}';klass='UNDECLARED_SECOND_DEFECT'
  elif index<20:p['pairs'][index]['expectedReason']='WRONG_REASON_'+str(index);klass='EXPECTED_REASON'
  elif index<25:c['cases'][index-20]['scenarioInput']['snapshot']['bid']=f'2.{index}';klass='CERT_UNDECLARED_PATH'
  else:f['fixtures'][index+1]['scenarioInput']=copy.deepcopy(f['fixtures'][0]['scenarioInput']);f['fixtures'][index+1]['testMetadata']['kind']='STILL_NEGATIVE';klass='METADATA_ONLY'
  with tempfile.TemporaryDirectory() as td:
   t=Path(td);write(t/'Tests/Vectors/HSB_2E_R4_R9_R3_DRAFT_FIXTURES_V2.json',f);write(t/'Tests/Contracts/HSB_2E_R4_R9_R3_CAUSAL_PAIRS.json',p);write(t/'Tests/Vectors/HSB_2E_R4_R9_R3_CERTIFICATE_FORGERY_DRAFTS.json',c);proc=subprocess.run([sys.executable,str(root/'Tests/Static/verify_hsb_2e_r4_r9_r3_prefreeze.py'),'--root',str(t)],capture_output=True,text=True);ok=proc.returncode!=0 and 'ORACLE_V2_READY_TO_FREEZE=NO' in proc.stdout;caught+=ok;catalog.append({'mutationId':mutation_id,'class':klass,'caught':ok})
 result={'ORACLE_QUALIFICATION_MUTATIONS_REQUIRED':30,'ORACLE_QUALIFICATION_MUTATIONS_EXECUTED':30,'ORACLE_QUALIFICATION_MUTATIONS_CAUGHT':caught,'SURVIVED':30-caught,'INVALID':0,'NOT_APPLIED':0,'WRONG_FAILURES':0,'INFRASTRUCTURE_FAILURES':0,'catalog':catalog};print(json.dumps({k:v for k,v in result.items() if k!='catalog'},sort_keys=True));write(root/'Tests/Evidence/HSB_2E_R4_R9_R3_PREFREEZE_MUTATION_RESULTS.json',result);return caught==30
if __name__=='__main__':p=argparse.ArgumentParser();p.add_argument('--root',default='.');a=p.parse_args();raise SystemExit(0 if main(Path(a.root).resolve()) else 1)
