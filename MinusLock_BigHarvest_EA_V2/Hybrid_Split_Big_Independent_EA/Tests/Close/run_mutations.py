"""Execute the same literal suite against one-guard model mutants. No production changes."""
import subprocess,sys,os,tempfile,json
from pathlib import Path
p=Path(__file__).resolve().parent;source=(p/'reference_contract.py').read_text();rows=[]
mutations=[
 ('NO_FINITE_RISK','all(math.isfinite(v) for v in values+limits)','True'),
 ('NET_ONLY_REPLAY',"self.events[event]==body", "True"),
 ('NO_VECTOR_CONSERVATION',"sum(vector)!=r['net']",'False'),
 ('NO_SOURCE_REUSE_GUARD',"if k in self.sources:return 'CONFLICT'", "if False:return 'CONFLICT'"),
 ('NO_REVISION',"revision!=s['revision']",'False'),
 ('NO_AVAILABILITY',"amount>s['free'][bucket]",'False'),
 ('NO_FINAL_COST',"realized+unrealized-remaining>=threshold",'realized+unrealized>=threshold'),
 ('UNKNOWN_COMPLETES',"outcome=='COMPLETED'", "outcome in ('COMPLETED','UNKNOWN')")]
for name,old,new in mutations:
 assert old in source,name
 with tempfile.TemporaryDirectory(prefix='mutant-',dir=p) as d:
  d=Path(d);f=d/'model.py';f.write_text(source.replace(old,new,1));env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',HSBI_CLOSE_MODEL=str(f),HSBI_CLOSE_RESULTS=str(d))
  r=subprocess.run([sys.executable,str(p/'test_reference.py')],env=env,text=True,capture_output=True)
  path=d/'reference_results.json'
  result=json.loads(path.read_text()) if path.exists() else None
  failed=[x['ID'] for x in result['Rows'] if x['Status']=='FAIL'] if result else []
  status='KILLED' if failed else 'SURVIVED' if r.returncode==0 else 'INFRASTRUCTURE_ERROR'
  rows.append(dict(ID=name,Before=old,After=new,Status=status,FailingCases=failed,ExitCode=r.returncode,Output=r.stdout+r.stderr))
result=dict(Rows=rows,Killed=sum(r['Status']=='KILLED' for r in rows),Survived=sum(r['Status']=='SURVIVED' for r in rows),InfrastructureErrors=sum(r['Status']=='INFRASTRUCTURE_ERROR' for r in rows),Boundary='Actual source mutations of proposed Python model; neither MQL5 mutation nor proof of absence of defects.')
(p/'mutation_results.json').write_text(json.dumps(result,indent=2)+'\n');print(result)
raise SystemExit(int(result['Survived']+result['InfrastructureErrors']>0))
