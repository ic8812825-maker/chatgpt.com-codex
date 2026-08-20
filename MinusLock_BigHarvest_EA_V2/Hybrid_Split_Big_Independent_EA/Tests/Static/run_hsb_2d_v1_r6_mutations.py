#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,json,shutil,subprocess,sys,tempfile
from collections import Counter
from pathlib import Path

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def snapshot(root):return {p.relative_to(root).as_posix():sha(p) for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
def rehash(manifest,rel,root):
 lines=manifest.read_text(encoding='utf-8').splitlines();found=False
 for i,line in enumerate(lines):
  if line.endswith('  '+rel):lines[i]=sha(root/rel)+'  '+rel;found=True
 if not found:raise RuntimeError('manifest target absent: '+rel)
 manifest.write_text('\n'.join(lines)+'\n',encoding='utf-8')
def mutate_manifest(m,p):
 lines=p.read_text(encoding='utf-8').splitlines();data=[i for i,x in enumerate(lines) if x and not x.startswith('#')]
 if m['id']=='M051':lines.pop(data[0])
 elif m['id']=='M052' or m['id']=='M055':lines.append(m['new'].rstrip())
 elif m['id']=='M053':lines.insert(data[0]+1,lines[data[0]])
 elif m['id']=='M054':i=data[0];lines[i]=('0' if lines[i][0]!='0' else '1')+lines[i][1:]
 p.write_text('\n'.join(lines)+'\n',encoding='utf-8')
def apply(m,root):
 p=root/m['target'];
 if not p.is_file():raise FileNotFoundError(m['target'])
 if m['mutation_type']=='manifest':mutate_manifest(m,p);return
 if m.get('id') in ('M103','M120','M121','M122','M123'):
  lines=p.read_text(encoding='utf-8').splitlines();data=[i for i,x in enumerate(lines) if x.strip()]
  if m['id'] in ('M103','M120'):lines.pop(data[0])
  elif m['id']=='M121':lines.append('0'*64+'  extra.file')
  elif m['id']=='M122':lines.insert(data[0]+1,lines[data[0]])
  else:i=data[0];lines[i]=('0' if lines[i][0]!='0' else '1')+lines[i][1:]
  p.write_text('\n'.join(lines)+'\n',encoding='utf-8');return
 s=p.read_text(encoding='utf-8-sig');n=s.count(m['old'])
 if m.get('replacements'):
  for old,new in m['replacements']:
   if s.count(old)!=1:raise RuntimeError(f'replacement_count={s.count(old)}')
   s=s.replace(old,new,1)
 elif n!=1:raise RuntimeError(f'replacement_count={n}')
 else:s=s.replace(m['old'],m['new'],1)
 p.write_text(s,encoding='utf-8')
 if m['mutation_type']=='semantic':rehash(root/'Reports/HSB_2D_V1_R6_FILE_MANIFEST_SHA256.txt',m['target'],root)
def parse(stdout):
 failed=[];statuses={}
 for line in stdout.splitlines():
  parts=line.split('|',2)
  if len(parts)>=2 and parts[0].startswith('S'):statuses[parts[0]]=parts[1];failed += [parts[0]] if parts[1]=='FAIL' else []
 return failed,statuses
def classify(applied,unexpected,crashed,returncode,failed,expected,mutation_type,manifest_status):
 if not applied:return "MUTATION_NOT_APPLIED"
 if unexpected:return "UNEXPECTED_FILES_CHANGED"
 if crashed:return "INFRASTRUCTURE_FAILURE"
 if returncode==0:return "SURVIVED"
 if failed==["S045"] and "S045" not in expected:return "INVALID_MANIFEST_ONLY_DETECTION"
 if not all(x in failed for x in expected):return "WRONG_FAILURE"
 if mutation_type=="semantic" and manifest_status!="PASS":return "INVALID_MANIFEST_FAILURE"
 return "CAUGHT"
def selftests(catalog):
 ids=[m['id'] for m in catalog];cases={}
 with tempfile.TemporaryDirectory(prefix='hsbi-mr-') as td:
  r=Path(td);missing={'target':'absent','mutation_type':'semantic'}
  try:apply(missing,r);cases['MR001']=False
  except FileNotFoundError:cases['MR001']=True
  (r/'x').write_text('a',encoding='utf-8');bad={'target':'x','mutation_type':'semantic','old':'z','new':'q'}
  try:apply(bad,r);cases['MR002']=False
  except RuntimeError:cases['MR002']=True
  cases['MR003']=classify(True,['extra'],False,1,['S028'],['S028'],'semantic','PASS')=='UNEXPECTED_FILES_CHANGED'
  cp=subprocess.run([sys.executable,'-c','import sys;sys.exit(3)']);cases['MR004']=classify(True,[],cp.returncode not in (0,1),cp.returncode,[],['S028'],'semantic','PASS')=='INFRASTRUCTURE_FAILURE'
  cases['MR005']=classify(True,[],False,0,[],['S028'],'semantic','PASS')=='SURVIVED'
  cases['MR006']=classify(True,[],False,1,['S045'],['S028'],'semantic','FAIL')=='INVALID_MANIFEST_ONLY_DETECTION'
  cases['MR007']=classify(True,[],False,1,['S040'],['S028'],'semantic','PASS')=='WRONG_FAILURE'
 with tempfile.TemporaryDirectory(prefix='hsbi-mr-clean-') as td2:q=Path(td2)
 cases['MR008']=not q.exists();cases['MR009']=len(ids)==len(set(ids));cases['MR010']=set(ids)==set(f'M{i:03}' for i in range(1,166))
 return [{'id':k,'status':'PASS' if v else 'FAIL'} for k,v in cases.items()]
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--root',required=True);ap.add_argument('--catalog',default='Tests/Static/hsb_2d_v1_r6_mutations.json');ap.add_argument('--output-json');ap.add_argument('--output-text');ap.add_argument('--publish-evidence',action='store_true');a=ap.parse_args();root=Path(a.root).resolve();catalog=json.loads((root/a.catalog).read_text(encoding='utf-8'))
 publish_json=root/'Tests/Evidence/HSB_2D_V1_R6_MUTATION_RESULTS.json';publish_text=root/'Tests/Evidence/HSB_2D_V1_R6_MUTATION_RESULTS.txt';outj=Path(a.output_json).resolve() if a.output_json else (publish_json if a.publish_evidence else None);outt=Path(a.output_text).resolve() if a.output_text else (publish_text if a.publish_evidence else None)
 required_mutations=[m for m in catalog if m.get('required') is True];required={m['id'] for m in required_mutations};ids=[m['id'] for m in catalog];infra=[]
 if len(ids)!=len(set(ids)):infra.append('duplicate_catalog_id')
 if not required<=set(ids):infra.append('required_missing')
 verifier=root/'Tests/Static/verify_hsb_2d_v1_r6.py';clean=subprocess.run([sys.executable,str(verifier),'--root',str(root)],text=True,capture_output=True)
 if clean.returncode:print(clean.stdout,end='');print('MUTATION_SUITE_ALLOWED=NO');return 2
 production_before=snapshot(root);results=[]
 if set(ids)!=set(f'M{i:03}' for i in range(1,len(ids)+1)):infra.append('catalog_id_gap')
 if len(required_mutations)!=len(catalog):infra.append('optional_mutation')
 for m in required_mutations:
  rec={'id':m['id'],'name':m['name'],'target':m['target'],'target_found':(root/m['target']).is_file(),'expected_failed_checks':m['expected_check_ids'],'applied':False,'changed_files':[],'unexpected_changed_files':[],'manifest_rehashed':m['manifest_strategy']=='rehash_mutated_file','verifier_started':False,'verifier_crashed':False}
  temp_path=None
  try:
   with tempfile.TemporaryDirectory(prefix='hsbi-r2-') as td:
    temp_path=Path(td);copy=temp_path/root.name;shutil.copytree(root,copy,symlinks=True,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
    rec['clean_fixture_before_mutation']=clean.returncode==0 and snapshot(copy)==production_before
    before=snapshot(copy);target_before=sha(copy/m['target']);apply(m,copy);after=snapshot(copy);rec['target_hash_changed']=sha(copy/m['target'])!=target_before;rec['expected_mutated_fragment_present']=m.get('new','') in (copy/m['target']).read_text(encoding='utf-8-sig') if not m.get('old','').startswith('__') else True;changed=sorted(k for k in set(before)|set(after) if before.get(k)!=after.get(k));allowed={m['target']};
    if m['mutation_type']=='semantic':allowed.add('Reports/HSB_2D_V1_R6_FILE_MANIFEST_SHA256.txt')
    rec['changed_files']=changed;rec['unexpected_changed_files']=sorted(set(changed)-allowed);rec['applied']=m['target'] in changed
    cp=subprocess.run([sys.executable,str(copy/'Tests/Static/verify_hsb_2d_v1_r6.py'),'--root',str(copy),'--fixture-mode'],text=True,capture_output=True);rec['verifier_started']=True;rec['verifier_exit_code']=cp.returncode;rec['verifier_crashed']=cp.returncode not in (0,1);failed,status=parse(cp.stdout);rec['actual_failed_checks']=failed;rec['manifest_check_status']=status.get('S045','MISSING');rec['stdout_sha256']=hashlib.sha256(cp.stdout.encode()).hexdigest();rec['stderr_sha256']=hashlib.sha256(cp.stderr.encode()).hexdigest();expected=all(x in failed for x in m['expected_check_ids']);manifest_only=failed==['S045'] and 'S045' not in m['expected_check_ids'];rec['primary_failure_check']=failed[0] if failed else '';rec['secondary_failure_checks']=failed[1:];rec['manifest_only_failure']=manifest_only
    result=classify(rec['applied'],rec['unexpected_changed_files'],rec['verifier_crashed'],cp.returncode,failed,m['expected_check_ids'],m['mutation_type'],rec['manifest_check_status'])
    if not rec.get('clean_fixture_before_mutation') or not rec.get('target_hash_changed') or not rec.get('expected_mutated_fragment_present'):result='INFRASTRUCTURE_FAILURE'
    rec['result']=result;rec['stdout']=cp.stdout;rec['stderr']=cp.stderr
  except Exception as e:rec.update(result='INFRASTRUCTURE_FAILURE',error=f'{type(e).__name__}:{e}',verifier_exit_code=None,actual_failed_checks=[])
  finally:rec['temporary_copy_removed']=temp_path is None or not temp_path.exists()
  results.append(rec)
 post_unchanged=snapshot(root)==production_before
 for rec in results:rec['production_worktree_unchanged']=post_unchanged
 selfcheck=selftests(catalog);counts=Counter(x['result'] for x in results)
 executed={x['id'] for x in results};caught={x['id'] for x in results if x['result']=='CAUGHT'}
 summary={'CATALOG_ENTRIES':len(catalog),'REQUIRED_ENTRIES':len(required_mutations),'EXECUTED_ENTRIES':len(executed),'CAUGHT_ENTRIES':len(caught),'CATALOG_MISSING_IDS':0 if set(ids)==set(f'M{i:03}' for i in range(1,len(ids)+1)) else 1,'CATALOG_DUPLICATE_IDS':len(ids)-len(set(ids)),'OPTIONAL_MUTATIONS':len(catalog)-len(required_mutations),'MUTATIONS_REQUIRED':len(required_mutations),'MUTATIONS_EXECUTED':len(results),'MUTATIONS_CAUGHT':counts['CAUGHT'],'MUTATIONS_SURVIVED':counts['SURVIVED'],'MUTATIONS_INVALID':sum(v for k,v in counts.items() if k.startswith('INVALID')),'MUTATIONS_NOT_APPLIED':counts['MUTATION_NOT_APPLIED'],'WRONG_FAILURES':counts['WRONG_FAILURE'],'INFRASTRUCTURE_FAILURES':counts['INFRASTRUCTURE_FAILURE'],'PRODUCTION_FILES_CHANGED_BY_MUTATIONS':0 if post_unchanged else 1,'REQUIRED_ID_SET':','.join(sorted(required)),'EXECUTED_ID_SET':','.join(sorted(executed)),'CAUGHT_ID_SET':','.join(sorted(caught)),'M151':'CAUGHT' if next(x for x in results if x['id']=='M151')['result']=='CAUGHT' else 'FAIL','M152_M165':'CAUGHT' if all(next(x for x in results if x['id']==f'M{i:03}')['result']=='CAUGHT' for i in range(152,166)) else 'FAIL'}
 ok=not infra and all(x['status']=='PASS' for x in selfcheck) and executed==required and caught==required and post_unchanged
 payload={'schema':'HSB.2D-V1-R6/mutations/1','catalog_sha256':sha(root/a.catalog),'results':results,'runner_self_tests':selfcheck,'summary':summary,'result':'PASS' if ok else 'FAIL'};
 if outj:outj.parent.mkdir(parents=True,exist_ok=True);outj.write_text(json.dumps(payload,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8')
 lines=[]
 for x in results:lines.append(f"{x['id']}|TARGET={x['target']}|TARGET_FOUND={'YES' if x.get('target_found') else 'NO'}|MUTATION_APPLIED={'YES' if x.get('applied') else 'NO'}|TARGET_HASH_CHANGED={'YES' if x.get('target_hash_changed') else 'NO'}|EXPECTED={','.join(x['expected_failed_checks'])}|ACTUAL={','.join(x.get('actual_failed_checks',[]))}|EXIT={x.get('verifier_exit_code')}|MANIFEST={x.get('manifest_check_status')}|VERIFIER_CRASHED={'YES' if x.get('verifier_crashed') else 'NO'}|RESULT={x['result']}")
 lines+=['HSB_2D_V1_R6_MUTATION_SUMMARY']+[f'{k}={v}' for k,v in summary.items()]+[f'RUNNER_SELF_TESTS={sum(x["status"]=="PASS" for x in selfcheck)}/10',f"RESULT={'PASS' if ok else 'FAIL'}"]
 text='\n'.join(lines)+'\n';
 if outt:outt.write_text(text,encoding='utf-8')
 sys.stdout.write(text);return 0 if ok else 1
if __name__=='__main__':raise SystemExit(main())
