"""Causal source mutations of new reference specification, not production remediation."""
import hashlib,sys
from copy import deepcopy
import HSBI_DG01_common as a
P=a.ROOT/'Tests/Reference/HSBI_DG01_ledger.py'
def fact():return dict(broker='FIXTURE',server='OFFLINE',account=1,deal=11,symbol='X',magic=7,cycle=1,role='BigCore',schema=1,currency='USD',digits=2,kind='RECONCILED',entry='OUT',policy=1,components=(6000,0,-1000,0))
def probe(cls,which):
 l=cls();p=fact();k=('FIXTURE','OFFLINE',1,11)
 if which=='AUTH':
  before=l.snapshot();q=fact();q['components']=(5000,0,0,0);s=l.fund(q,p,(5000,0,0,0,0),101,1,history='COMPLETE',costs=True,precision=True)
 else:
  assert l.fund(p,fact(),(5000,0,0,0,0),101,1,history='COMPLETE',costs=True,precision=True)=='FUNDED_IN_MEMORY'
  if which=='REV':assert l.operation(k,101,10,'reserve',0,100,'A',(1,'X',1),1)=='APPLIED_IN_MEMORY'
  before=l.snapshot()
  if which=='VECTOR':s=l.fund(fact(),fact(),(0,5000,0,0,0),101,2,history='COMPLETE',costs=True,precision=True)
  elif which=='SCOPE':s=l.operation(k,101,10,'consume',0,100,'A',(2,'X',1),1)
  elif which=='REV':s=l.operation(k,101,11,'reserve',0,100,'B',(1,'X',1),1)
  elif which=='HISTORY':s=l.operation(k,101,10,'consume',0,100,'A',(1,'X',1),1,history='INCOMPLETE')
  elif which=='ACCOUNT':q=fact();q['account']=2;s=l.fund(q,dict(q),(5000,0,0,0,0),101,1,history='COMPLETE',costs=True,precision=True)
  else:raise ValueError(which)
 return dict(Status=s,Before=repr(before),After=repr(l.snapshot()),StateUnchanged=before==l.snapshot())
def positive(cls):
 l=cls();p=fact();return l.fund(p,fact(),(5000,0,0,0,0),101,1,history='COMPLETE',costs=True,precision=True)
def main():
 started=a.now();source=P.read_text();specs=[('M-AUTH','AUTH','if presented!=authority:','if False:','CONFLICT'),('M-VECTOR','VECTOR',"return 'NO_OP' if self.sources[k]['immutable']==payload else 'CONFLICT'","return 'NO_OP'",'CONFLICT'),('M-SCOPE','SCOPE',"if context!=(record['account'],record['symbol'],record['cycle']) or allocation!=source['immutable'][2]:","if allocation!=source['immutable'][2]:",'CONFLICT'),('M-REV','REV',"if expected_revision!=source['revision']:return 'CONFLICT'","if False:return 'CONFLICT'",'CONFLICT'),('M-HISTORY','HISTORY',"if history!='COMPLETE' or k not in self.sources:return 'UNAVAILABLE'","if k not in self.sources:return 'UNAVAILABLE'",'UNAVAILABLE'),('M-ACCOUNT','ACCOUNT',"return (r['broker'],r['server'],r['account'],r['deal'])","return (r['broker'],r['server'],1,r['deal'])",'FUNDED_IN_MEMORY')]
 original={};exec(compile(source,str(P),'exec'),original);rows=[]
 for mid,which,old,new,expected in specs:
  row=dict(MutationID=mid,TestID='CAUSAL-'+mid,OriginalSourceSHA256=a.sha(P),RunnerSHA256=a.sha(__file__),ExactEdit=dict(Old=old,New=new),Input=which,Expected=expected,Environment=dict(OS=sys.platform),ExecutionTimeUTC=a.now(),ProofBoundary='New reference-model source mutation only; not native or production mutation')
  try:
   if source.count(old)!=1:raise ValueError('source edit count '+str(source.count(old)))
   mutant=source.replace(old,new);row['MutantSourceSHA256']=hashlib.sha256(mutant.encode()).hexdigest();scope={};exec(compile(mutant,mid,'exec'),scope)
   op=positive(original['Ledger']);mp=positive(scope['Ledger']);on=probe(original['Ledger'],which);mn=probe(scope['Ledger'],which)
   row.update(OriginalPositive=op,MutantPositive=mp,OriginalCausal=on,MutantCausal=mn,ExitCode=0)
   causal=op==mp=='FUNDED_IN_MEMORY' and on['Status']==expected and (on['StateUnchanged'] or expected=='FUNDED_IN_MEMORY') and mn['Status']!=expected
   row['Status']='UNSAFE_ACCEPTANCE_KILL' if causal and mn['Status'] in ('FUNDED_IN_MEMORY','APPLIED_IN_MEMORY') else 'STATUS_CONTRACT_KILL' if causal else 'MUTATION_SURVIVED'
  except Exception as e:row.update(Status='INFRASTRUCTURE_ERROR',ExitCode=None,Error=type(e).__name__+': '+str(e))
  rows.append(row)
 suite_exit=int(any(x['Status'] not in ('UNSAFE_ACCEPTANCE_KILL','STATUS_CONTRACT_KILL') for x in rows))
 for row in rows:row['ExitCode']=suite_exit;row['ExitCodeScope']='Containing mutation runner process'
 result=dict(StartedUTC=started,FinishedUTC=a.now(),Rows=rows,Killed=sum(x['Status'].endswith('_KILL') for x in rows),Survived=sum(x['Status']=='MUTATION_SURVIVED' for x in rows),InfrastructureErrors=sum(x['Status']=='INFRASTRUCTURE_ERROR' for x in rows));a.save('MUTATION_RESULTS',result);print('MUTATIONS',result['Killed'],result['Survived'],result['InfrastructureErrors']);return int(result['Survived']+result['InfrastructureErrors']>0)
if __name__=='__main__':raise SystemExit(main())
