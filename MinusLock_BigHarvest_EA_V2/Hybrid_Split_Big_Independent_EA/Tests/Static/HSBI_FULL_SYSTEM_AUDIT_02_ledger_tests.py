"""Literal expected transitions and balances, independent of production and historical evaluators."""
from copy import deepcopy
import HSBI_FULL_SYSTEM_AUDIT_02_verify as a
from HSBI_FULL_SYSTEM_AUDIT_02_ledger import Ledger

def main():
 started=a.utc();l=Ledger();key=('fixture-broker','fixture-server',1,101);rows=[]
 def snap():return deepcopy(l.__dict__)
 def check(i,call,expected,balance=None,unchanged=False):
  before=snap();actual=call();after=snap();ok=actual==expected
  if balance is not None:ok &= tuple(l.sources[key][k] for k in ('G','C','R','F'))==balance
  if unchanged:ok &= before==after
  rows.append(dict(TestID=i,Expected=expected,Actual=actual,ExpectedBalance=balance,Before=repr(before),After=repr(after),ZeroDeltaRequired=unchanged,Result='PASS' if ok else 'FAIL'))
 check('HISTORY_UNKNOWN',lambda:l.fund(key,(5000,0,0,0),(5000,),1,False),'UNAVAILABLE',unchanged=True)
 check('FUND',lambda:l.fund(key,(6000,0,-1000,0),(3000,2000),1),'FUNDED_IN_MEMORY',(5000,0,0,5000))
 check('EXACT_FUND',lambda:l.fund(key,(6000,0,-1000,0),(3000,2000),1),'NO_OP',unchanged=True)
 check('CHANGED_COMPONENTS_EQUAL_NET',lambda:l.fund(key,(5000,0,0,0),(3000,2000),2),'CONFLICT',unchanged=True)
 check('CHANGED_VECTOR_EQUAL_NET',lambda:l.fund(key,(6000,0,-1000,0),(2000,3000),2),'CONFLICT',unchanged=True)
 check('NEGATIVE_BUCKET',lambda:l.fund(('fixture-broker','fixture-server',1,102),(5000,0,0,0),(-5000,10000),2),'REJECT',unchanged=True)
 check('UNKNOWN_CURRENCY',lambda:l.fund(('fixture-broker','fixture-server',1,102),(5000,0,0,0),(5000,),2,currency='EUR'),'UNAVAILABLE',unchanged=True)
 check('UNKNOWN_PRECISION',lambda:l.fund(('fixture-broker','fixture-server',1,102),(5000,0,0,0),(5000,),2,digits=3),'UNAVAILABLE',unchanged=True)
 check('BOOL_EVENT',lambda:l.op(key,True,'consume',1,'A'),'REJECT',unchanged=True)
 check('RESERVE',lambda:l.op(key,10,'reserve',4500,'A'),'APPLIED_IN_MEMORY',(5000,0,4500,500))
 check('RESERVED_CANNOT_SPEND_FREE',lambda:l.op(key,11,'consume',1000,'B'),'REJECT',unchanged=True)
 check('FOREIGN_OWNER',lambda:l.op(key,11,'consume_reserved',1000,'B'),'REJECT',unchanged=True)
 check('RELEASE',lambda:l.op(key,11,'release',500,'A'),'APPLIED_IN_MEMORY',(5000,0,4000,1000))
 check('CONSUME_RESERVED',lambda:l.op(key,12,'consume_reserved',4000,'A'),'APPLIED_IN_MEMORY',(5000,4000,0,1000))
 check('CONSUME_FREE',lambda:l.op(key,13,'consume',1000,'A'),'APPLIED_IN_MEMORY',(5000,5000,0,0))
 check('EXACT_CONSUMPTION',lambda:l.op(key,13,'consume',1000,'A'),'NO_OP',unchanged=True)
 check('ALTERED_REPLAY',lambda:l.op(key,13,'consume',999,'A'),'CONFLICT',unchanged=True)
 check('EXHAUSTED',lambda:l.op(key,14,'consume',1,'A'),'REJECT',unchanged=True)
 check('INCOMPLETE_JOURNAL',lambda:l.op(key,14,'consume',1,'A',False),'UNAVAILABLE',unchanged=True)
 snapshot=snap();other=Ledger();actual=other.reconstruct(snapshot);rows.append(dict(TestID='RECONSTRUCTION_ONLY',Expected='ACCOUNTING_RECONSTRUCTED_ONLY',Actual=actual,Result='PASS' if actual=='ACCOUNTING_RECONSTRUCTED_ONLY' and other.__dict__==snapshot else 'FAIL',Scope='No historical reauthorization/durable authenticity'))
 actual=other.fund(key,(6000,0,-1000,0),(3000,2000),1);rows.append(dict(TestID='POST_RESTART_EXACT_FUND',Expected='NO_OP',Actual=actual,Result='PASS' if actual=='NO_OP' else 'FAIL',Scope='Complete trusted in-memory snapshot supplied; NOT real restart/crash test'))
 actual=l.fund(('fixture-broker','fixture-server',2,101),(5000,0,0,0),(5000,),2);rows.append(dict(TestID='ACCOUNT_NAMESPACE',Expected='FUNDED_IN_MEMORY',Actual=actual,Result='PASS' if actual=='FUNDED_IN_MEMORY' else 'FAIL',Scope='Independent fixture source in another account, not cross-account spending'))
 a.save('LEDGER_TESTS',dict(Command=[a.sys.executable,*a.sys.argv],StartedUtc=started,FinishedUtc=a.utc(),BaseSHA=a.BASE,Rows=rows,Pass=sum(x['Result']=='PASS' for x in rows),Fail=sum(x['Result']=='FAIL' for x in rows),SubjectSHA256=a.sha(a.ROOT/'Tests/Reference'/(a.TAG+'ledger.py')),RunnerSHA256=a.sha(__file__),Boundary='Proposed integer-minor-unit specification only. Does NOT prove production global funding, durable restart, concurrent double-spend or provider authenticity.'))
 print('LEDGER',len(rows),sum(x['Result']=='PASS' for x in rows));return int(any(x['Result']!='PASS' for x in rows))
if __name__=='__main__':raise SystemExit(main())
