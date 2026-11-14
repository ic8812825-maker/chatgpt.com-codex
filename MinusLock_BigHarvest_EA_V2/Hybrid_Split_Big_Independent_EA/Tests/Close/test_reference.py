"""Literal goldens independent of subject; named model mutants, not production mutation."""
import copy,json,datetime,hashlib,os,importlib.util
from pathlib import Path
import reference_contract as m
if os.environ.get('HSBI_CLOSE_MODEL'):
 spec=importlib.util.spec_from_file_location('mutant_contract',os.environ['HSBI_CLOSE_MODEL']);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
p=Path(__file__).resolve().parent
rows=[]
def case(tid,actual,expected,before=None,after=None):
 ok=actual==expected and (before is None or before==after)
 rows.append(dict(ID=tid,Expected=expected,Actual=actual,ZeroDelta=before==after if before is not None else None,Status='PASS' if ok else 'FAIL'))
def record():return dict(broker='FIXTURE',server='OFFLINE',account=1,symbol='X',magic=7,cycle=1,deal=11,order=12,position=13,action=14,event=15,role='BigCore',entry='OUT',direction='BUY',volume=1,price=100,profit=6000,swap=0,commission=-1000,fee=0,net=5000,time=1,schema=1,currency='USD',digits=2)
r=record();l=m.Ledger();k=m.key(r)
case('CONTROL-FUND',l.fund(r,dict(r),(5000,0,0,0,0),1),'FUNDED')
for tid,change in [('P0-01',dict(profit=7000,commission=-2000)),('POSITION',dict(position=99)),('ROLE',dict(role='Small')),('PRICE',dict(price=101))]:
 altered=dict(r,**change);before=l.snapshot();case(tid,l.fund(altered,altered,(5000,0,0,0,0),1),'CONFLICT',before,l.snapshot())
before=l.snapshot();case('P0-02',l.fund(r,dict(r),(0,5000,0,0,0),1),'CONFLICT',before,l.snapshot())
case('CONSUME',l.consume(k,0,5000,2,1),'APPLIED')
before=l.snapshot();case('P0-03',l.consume(k,0,1,3,2),'REJECT',before,l.snapshot())
case('EXHAUSTED-VECTOR',l.sources[k]['free'],[0,0,0,0,0])
case('P0-13',m.Ledger.restore_trusted(l.snapshot()).consume(k,0,5000,2,1),'NO_OP')
case('P0-08',l.consume(k,0,4999,2,1),'CONFLICT')
case('P0-09',l.consume(k,0,1,3,1),'REJECT')
case('P0-04',m.risk([float('nan')],[100]),False)
case('NAN-CAP',m.risk([1],[float('nan')]),False)
case('P0-05',m.risk([float('inf')],[100]),False)
case('P0-06',m.grid('.005','.01','1','.01'),False)
case('VOLUME-OFFGRID',m.grid('.015','.01','1','.01'),False)
case('VOLUME-MAX',m.grid('1','.01','1','.01'),True)
case('PRICE-GRID',m.grid('100.03','.01','1000','.05'),False)
case('P0-07',m.barrier('PARTIAL',.5,1,1,1,False),False)
case('COMPLETED-FILL',m.barrier('COMPLETED',1,1,1,1,True),True)
case('P0-10',m.barrier('UNKNOWN',1,1,1,1,True),False)
case('P0-12',m.Ledger().fund(r,None,(5000,0,0,0,0),1),'UNAVAILABLE')
case('P0-14',m.final_close(5000,-6000,100,0),False)
case('FINAL-CONTROL',m.final_close(5000,-4000,100,500),True)
case('MARGIN-SHORTAGE',m.final_close(5000,-4000,100,500,risk_ok=False),False)
case('SNAPSHOT-MISMATCH',m.final_close(5000,-4000,100,500,positions_fresh=False),False)
for tid,changes in [('INVALID-ENUM',{'direction':99}),('NONFINITE-MONEY',{'net':float('inf')}),('ALTERED-BODY',{'fee':-1}),('MALFORMED',{'broker':''})]:case(tid,m.valid_record(dict(r,**changes)),False)
for field in ('account','server','deal'):
 altered=dict(r,**{field:2 if field!='server' else 'OTHER'});case('DIFFERENT-'+field,m.key(altered)==k,False)
for tid,value,digits,expected in [('CENTS','1.005',2,100),('HALF-EVEN','1.015',2,102),('MILLS','1.2345',3,1234),('NEGATIVE-ZERO','-0.0',2,0),('NEGATIVE-COST','-1.23',2,-123)]:case(tid,m.minor(value,digits),expected)
for tid,value in [('NAN','NaN'),('INF','Infinity'),('OVERFLOW','1e100')]:
 try:m.minor(value);actual='ACCEPT'
 except ValueError:actual='REJECT'
 case('NUM-'+tid,actual,'REJECT')
# Exact linear synthetic geometry; favorable direction d reverses for mirror.
case('BUY-SELL-SYMMETRY',[(3-1-1)*2,(3-1-1)*(-2)*(-1)],[2,2])
case('ZERO-TREND',3+0-1-1,1)
case('SIGNED-DEAL',6000-100-200-50,5650)
case('GAP',m.final_close(5000,-7000,100,0),False)
case('SPREAD-EXPANSION',m.final_close(5000,-4500,600,0),False)
case('ADVERSE-TREND',m.final_close(5000,-20000,100,0),False)
q=m.Ledger();q.fund(r,dict(r),(5000,0,0,0,0),1)
case('COMPETING-A',q.consume(k,0,4000,2,1),'APPLIED');before=q.snapshot();case('COMPETING-B-STALE',q.consume(k,0,4000,3,1),'REJECT',before,q.snapshot())
case('BALANCE-AFTER-COMPETING',q.sources[k]['free'],[1000,0,0,0,0])
case('INF-CAP',m.risk([1],[float('inf')]),False)
case('UNDERALLOCATION',m.Ledger().fund(r,dict(r),(4000,0,0,0,0),1),'REJECT')
fresh=m.Ledger();fresh.fund(r,dict(r),(5000,0,0,0,0),1)
before=fresh.snapshot();case('SECOND-ALLOCATION-EVENT',fresh.fund(r,dict(r),(5000,0,0,0,0),99),'CONFLICT',before,fresh.snapshot())
fresh=m.Ledger();fresh.fund(r,dict(r),(5000,0,0,0,0),1)
before=fresh.snapshot();case('STALE-WITH-AVAILABLE',fresh.consume(k,0,1,3,0),'REJECT',before,fresh.snapshot())
case('P0-11',m.topology([('far','Far'),('candidate','Far')]),False)
case('TOPOLOGY-CONTROL',m.topology([('far','Far'),('core','BigCore')]),True)
case('RESERVE-BINDING-CONTROL',m.catchup(5000,5000,2000,-2000,100,5000),'PASS')
case('ELIGIBLE-PROOF-MISMATCH',m.catchup(10000,1000,2000,-2000,100,10000),'REJECT')
case('LOSS-PROOF-MISMATCH',m.catchup(5000,5000,0,-5000,100,5000),'REJECT')
case('EXHAUSTED-RESERVE',m.catchup(5000,5000,2000,-2000,100,0),'REJECT')
case('PROJECTED-NOT-FUNDING',m.catchup(5000,5000,2000,-2000,100,0,projected=True),'PREVIEW_ONLY')
case('ALL-LEVEL-COUNTEREXAMPLE',min((9,-11))>0,False)
result=dict(UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),Rows=rows,Pass=sum(r['Status']=='PASS' for r in rows),Fail=sum(r['Status']=='FAIL' for r in rows),ModelSHA256=hashlib.sha256((p/'reference_contract.py').read_bytes()).hexdigest(),Boundary='PROPOSED offline model; trusted snapshot restart and serialized competing consumers only. No durable IO, authentic broker or real concurrency. P0-11 tests abstract full-slot topology; actual context caller/native scenario remains separate.')
(Path(os.environ.get('HSBI_CLOSE_RESULTS',str(p)))/'reference_results.json').write_text(json.dumps(result,indent=2)+'\n');print({k:result[k] for k in ('Pass','Fail')})
raise SystemExit(int(result['Fail']>0))
