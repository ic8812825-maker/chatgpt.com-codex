"""Literal expected statuses/balances, no subject call computes expected."""
from copy import deepcopy
import sys,platform,json,hashlib
import HSBI_DG01_common as a
from HSBI_DG01_ledger import Ledger,key,I64_MAX,U64_MAX

TRACE=[]
class TracedLedger(Ledger):
 def fund(self,*args,**kwargs):
  TRACE.append(dict(API='fund',Args=deepcopy(args),Kwargs=deepcopy(kwargs)));return super().fund(*args,**kwargs)
 def operation(self,*args,**kwargs):
  TRACE.append(dict(API='operation',Args=deepcopy(args),Kwargs=deepcopy(kwargs)));return super().operation(*args,**kwargs)

def fact():return dict(broker='FIXTURE',server='OFFLINE',account=1,deal=11,symbol='X',magic=7,cycle=1,role='BigCore',schema=1,currency='USD',digits=2,kind='RECONCILED',entry='OUT',policy=1,components=(6000,0,-1000,0))
def main():
 start=a.now();rows=[];l=TracedLedger();r=fact();authority=fact();k=key(r)
 def case(tid,fn,expected,balance=None,zero=False,inputs=None):
  before=l.snapshot();input_before=deepcopy(inputs);TRACE.clear()
  try:actual=fn();error=None
  except Exception as e:actual='INFRASTRUCTURE_ERROR';error=type(e).__name__+': '+str(e)
  after=l.snapshot();actualbal=None
  if k in l.sources:
   b=l.sources[k]['buckets'][0];actualbal=(b['G'],b['C'],sum(b['reservations'].values()),b['F'])
  revision=l.sources[k]['revision'] if k in l.sources else None
  literal_revision={'L05-NEW-SOURCE':1,'L11-RESERVE':2,'L15-RELEASE':3,'L16-CONSUME-RESERVED':4,'L19-CONSUME-FREE':5,'L33-MAX-SOURCE':1,'L34-TINY-DEBIT-1':2,'L35-TINY-DEBIT-2-OUT-OF-ID-ORDER':3}.get(tid)
  ok=(literal_revision is None or revision==literal_revision) and actual==expected and (balance is None or actualbal==balance) and (not zero or before==after) and input_before==inputs
  rows.append(dict(TestID=tid,SubjectSHA256=a.sha(a.ROOT/'Tests/Reference/HSBI_DG01_ledger.py'),RunnerSHA256=a.sha(__file__),Input=repr(TRACE[-1]) if TRACE else repr(inputs),Expected=dict(Status=expected,Balance=balance,Revision=literal_revision,ZeroDelta=zero),Actual=dict(Status=actual,Balance=actualbal,Revision=revision,StateUnchanged=before==after,InputUnchanged=input_before==inputs),Status='INFRASTRUCTURE_ERROR' if error else 'PASS' if ok else 'FAIL',Error=error,ExitCode=None if error else 0,Environment=dict(OS=sys.platform,Python=platform.python_version()),ExecutionTimeUTC=a.now(),ProofBoundary='Proposed in-memory per-source/per-bucket fixture; no provider authenticity, durable storage or real concurrency'))
 def fund(p=r,auth=authority,g=(5000,0,0,0,0),alloc=101,event=1,**kw):return l.fund(p,auth,g,alloc,event,**dict(dict(history='COMPLETE',costs=True,precision=True),**kw))
 def op(event,action,amount,owner='A',revision=None,ctx=(1,'X',1),alloc=101,bucket=0,**kw):return l.operation(k,alloc,event,action,bucket,amount,owner,ctx,l.sources[k]['revision'] if revision is None else revision,**kw)
 case('L01-HISTORY-MISSING',lambda:fund(auth=None),'UNAVAILABLE',zero=True,inputs=(r,authority))
 case('L02-HISTORY-INCOMPLETE',lambda:fund(history='INCOMPLETE'),'UNAVAILABLE',zero=True)
 case('L03-COSTS-INCOMPLETE',lambda:fund(costs=False),'UNAVAILABLE',zero=True)
 case('L04-PRECISION-UNKNOWN',lambda:fund(precision=False),'UNAVAILABLE',zero=True)
 case('L05-NEW-SOURCE',lambda:fund(),'FUNDED_IN_MEMORY',(5000,0,0,5000),inputs=(r,authority))
 case('L05A-UNKNOWN-DEFAULTS',lambda:l.fund(r,authority,(5000,0,0,0,0),101,1),'UNAVAILABLE',zero=True)
 case('L05B-BOOL-CONTEXT',lambda:op(4,'consume',1,ctx=(True,'X',True)),'REJECT',zero=True)
 case('L05C-BOOL-KEY',lambda:l.operation(('FIXTURE','OFFLINE',True,11),101,4,'consume',0,1,'A',(1,'X',1),1),'REJECT',zero=True)
 case('L06-EXACT-FUND',lambda:fund(),'NO_OP',zero=True)
 changed=fact();changed['components']=(5000,0,0,0)
 case('L07-ALTERED-EQUAL-NET',lambda:fund(p=changed,auth=changed),'CONFLICT',zero=True,inputs=changed)
 case('L08-AUTHORITY-MISMATCH',lambda:fund(p=changed),'CONFLICT',zero=True)
 case('L09-SECOND-ALLOCATION',lambda:fund(alloc=999,event=2),'CONFLICT',zero=True)
 case('L10-IMMUTABLE-VECTOR',lambda:fund(g=(0,5000,0,0,0)),'CONFLICT',zero=True)
 case('L11-RESERVE',lambda:op(10,'reserve',4500),'APPLIED_IN_MEMORY',(5000,0,4500,500))
 case('L12-RESERVED-NOT-FREE',lambda:op(11,'consume',1000,owner='B'),'REJECT',zero=True)
 case('L13-FOREIGN-RESERVATION-OWNER',lambda:op(11,'consume_reserved',1000,owner='B'),'REJECT',zero=True)
 case('L14-STALE-COMPETING-CONSUMER',lambda:op(11,'reserve',100,owner='B',revision=1),'CONFLICT',zero=True)
 case('L15-RELEASE',lambda:op(11,'release',500),'APPLIED_IN_MEMORY',(5000,0,4000,1000))
 case('L16-CONSUME-RESERVED',lambda:op(12,'consume_reserved',4000),'APPLIED_IN_MEMORY',(5000,4000,0,1000))
 case('L17-FOREIGN-ALLOCATION',lambda:op(13,'consume',100,alloc=999),'CONFLICT',zero=True)
 for i,context in enumerate([(2,'X',1),(1,'Y',1),(1,'X',2)]):case('L18-SCOPE-'+str(i),lambda c=context:op(13,'consume',1,ctx=c),'CONFLICT',zero=True)
 case('L19-CONSUME-FREE',lambda:op(13,'consume',1000),'APPLIED_IN_MEMORY',(5000,5000,0,0))
 case('L20-EXACT-AFTER-EXHAUSTION',lambda:op(13,'consume',1000,revision=1),'NO_OP',zero=True)
 case('L21-ALTERED-REPLAY',lambda:op(13,'consume',999),'CONFLICT',zero=True)
 case('L22-EXHAUSTED',lambda:op(14,'consume',1),'REJECT',zero=True)
 case('L23-INCOMPLETE-JOURNAL',lambda:op(14,'consume',1,history='INCOMPLETE'),'UNAVAILABLE',zero=True)
 l=TracedLedger.from_trusted_snapshot(l.snapshot())
 case('L24-RESTART-REPLAY',lambda:op(13,'consume',1000,revision=1),'NO_OP',zero=True)
 case('L25-RESTART-FUND',lambda:fund(),'NO_OP',zero=True)
 second=fact();second['deal']=12
 case('L25A-SECOND-SOURCE',lambda:l.fund(second,dict(second),(5000,0,0,0,0),102,2,history='COMPLETE',costs=True,precision=True),'FUNDED_IN_MEMORY')
 case('L25B-FUND-EVENT-COLLISION',lambda:fund(event=2),'CONFLICT',zero=True)
 for i,value in enumerate([True,False,0,-1,1.5,'1',None,U64_MAX+1]):case('L26-EVENT-'+str(i),lambda e=value:op(e,'consume',1),'REJECT',zero=True)
 for i,value in enumerate([0,-1,True,float('nan'),float('inf'),I64_MAX+1]):case('L27-AMOUNT-'+str(i),lambda n=value:op(20,'consume',n),'REJECT',zero=True)
 future=fact();future['schema']=2
 case('L28-SCHEMA-UNKNOWN',lambda:fund(p=future,auth=future),'UNAVAILABLE',zero=True)
 unknown=fact();unknown['currency']='EUR';case('L29-CURRENCY',lambda:fund(p=unknown,auth=unknown),'UNAVAILABLE',zero=True)
 unknown=fact();unknown['digits']=3;case('L30-PRECISION',lambda:fund(p=unknown,auth=unknown),'UNAVAILABLE',zero=True)
 projected=fact();projected['kind']='PROJECTED';case('L31-PROJECTED',lambda:fund(p=projected,auth=projected),'UNAVAILABLE',zero=True)
 case('L32-NET-OVERFLOW',lambda:fund(p=dict(fact(),deal=20,components=(I64_MAX,0,1,0)),auth=dict(fact(),deal=20,components=(I64_MAX,0,1,0)),g=(I64_MAX,0,0,0,0),event=2),'REJECT',zero=True)
 # Isolated exact signed64 boundary source, each literal decrement remains representable.
 l=TracedLedger();r=dict(fact(),components=(I64_MAX,0,0,0));authority=dict(fact(),components=(I64_MAX,0,0,0));k=key(r)
 case('L33-MAX-SOURCE',lambda:l.fund(r,authority,(I64_MAX,0,0,0,0),101,1,history='COMPLETE',costs=True,precision=True),'FUNDED_IN_MEMORY',(9223372036854775807,0,0,9223372036854775807))
 case('L34-TINY-DEBIT-1',lambda:op(100,'consume',1),'APPLIED_IN_MEMORY',(9223372036854775807,1,0,9223372036854775806))
 case('L35-TINY-DEBIT-2-OUT-OF-ID-ORDER',lambda:op(99,'consume',1),'APPLIED_IN_MEMORY',(9223372036854775807,2,0,9223372036854775805))
 case('L36-OLD-REVISION',lambda:op(98,'consume',1,revision=1),'CONFLICT',zero=True)
 l.sources[k]['revision']=U64_MAX
 case('L37-REVISION-OVERFLOW',lambda:op(98,'consume',1,revision=U64_MAX),'REJECT',zero=True)
 # Funding event IDs are account-namespaced; shape/broker-source contexts still independently bound.
 l=TracedLedger();r=fact();authority=fact();k=key(r)
 case('L38-BOOL-ALLOCATION',lambda:l.fund(r,authority,(5000,0,0,0,0),True,1),'REJECT',zero=True)
 case('L39-MISSING-FIELD',lambda:l.fund({},authority,(5000,0,0,0,0),101,1),'REJECT',zero=True)
 case('L40-SMALL-NOT-BIG',lambda:l.fund(dict(fact(),role='Small'),dict(fact(),role='Small'),(5000,0,0,0,0),101,1),'REJECT',zero=True)
 case('L40A-OPENING-NO-GRANT',lambda:fund(p=dict(fact(),entry='IN'),auth=dict(fact(),entry='IN')),'REJECT',zero=True)
 case('L40B-MIXED-ENTRY',lambda:fund(p=dict(fact(),entry='INOUT'),auth=dict(fact(),entry='INOUT')),'UNAVAILABLE',zero=True)
 case('L40C-UNKNOWN-POLICY',lambda:fund(p=dict(fact(),policy=2),auth=dict(fact(),policy=2)),'UNAVAILABLE',zero=True)
 # Three exact presentation-only checks remain separate from ledger transitions.
 formatrows=[]
 for z in a.load('FORMATTING_RESULTS')['Rows']:
  src=(a.ROOT/z['Source']).read_text();out=(a.ROOT/z['Output']).read_text();formatrows.append(dict(TestID='FORMAT-'+z['Source'].split('_02_')[1].split('_RU')[0],Expected='EXACT_NEWLINE_TRANSFORM',Actual='EXACT_NEWLINE_TRANSFORM' if out==src.replace('\\n','\n') else 'DIFFERENT',Status='PASS' if out==src.replace('\\n','\n') else 'FAIL',SourceSHA256=a.sha(a.ROOT/z['Source']),OutputSHA256=a.sha(a.ROOT/z['Output'])))
 suite_exit=int(any(x['Status']!='PASS' for x in rows+formatrows))
 for row in rows:row['ExitCode']=suite_exit;row['ExitCodeScope']='Containing runner process; callable has no separate OS exit'
 result=dict(BaseSHA=a.BASE,StartedUTC=start,FinishedUTC=a.now(),Command=[sys.executable,*sys.argv],RunnerSHA256=a.sha(__file__),Rows=rows,Pass=sum(x['Status']=='PASS' for x in rows),Fail=sum(x['Status']=='FAIL' for x in rows),InfrastructureErrors=sum(x['Status']=='INFRASTRUCTURE_ERROR' for x in rows),FormattingRows=formatrows,FormattingPass=sum(x['Status']=='PASS' for x in formatrows),ProofBoundary='Ledger and formatting counted separately. Restart is trusted snapshot simulation, competing consumers serialized revision test, NOT actual concurrency/durability; incomplete facts never fixture broker evidence.')
 a.save('TEST_RESULTS',result);print('REFERENCE',len(rows),result['Pass'],result['Fail'],'INFRA',result['InfrastructureErrors'],'FORMAT',result['FormattingPass']);return int(result['Fail']+result['InfrastructureErrors']+sum(x['Status']!='PASS' for x in formatrows)>0)
if __name__=='__main__':raise SystemExit(main())
