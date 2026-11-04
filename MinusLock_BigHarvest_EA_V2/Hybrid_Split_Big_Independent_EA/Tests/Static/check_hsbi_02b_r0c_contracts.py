#!/usr/bin/env python3
"""R0C literal outcomes and independent wire encoder. Never imports an old oracle."""
import argparse
import copy
from datetime import datetime,timezone
from decimal import Decimal
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'Tests/Reference'))
import hsbi_02b_r0c_independent_oracle as oracle
B=('FinalReserve','PartialFar','Transition','Carry','ResidualHeld')
IDS=('Broker','Server','Account','Symbol','Magic','Deal','Order','Position','Cycle','Plan','StateRevision','AllocationEvent','PolicyVersion','SnapshotID')


def wire(x):
    if isinstance(x,Decimal):
        if not x.is_finite():return str(x)  # evidence only; invalid DTO never sealed
        s=format(x,'f');return '0' if x==0 else s.rstrip('0').rstrip('.') if '.' in s else s
    if isinstance(x,dict):return {k:wire(v) for k,v in sorted(x.items())}
    if isinstance(x,(tuple,list)):return [wire(v) for v in x]
    return x


def encode(x):return json.dumps(wire(x),sort_keys=True,separators=(',',':'),ensure_ascii=False)
def fingerprint(x):return hashlib.sha256(encode(x).encode()).hexdigest()


def fixture():
    ids=dict(zip(IDS,('B1','S1',1,'EURUSD',7,11,12,13,1,1,1,31,1,1)))
    source=('B1','S1',1,11);g=dict(zip(B,map(Decimal,('50','0','0','0','0'))));z=dict.fromkeys(B,Decimal(0))
    r=dict(identity=copy.deepcopy(ids),closingConfirmed=True,role='BigCore',profit=Decimal(55),swap=Decimal(0),commission=Decimal(-5),fee=Decimal(0),rawNet=Decimal(50),currency='USD',digits=2,receipt=dict(currency='USD',digits=2,raw=Decimal(50),posted=Decimal(50)))
    alloc=dict(allocation='A1',source=source,grant=copy.deepcopy(g),policyVersion=1,event=31)
    s=dict(allocation='A1',source=source,currency='USD',digits=2,net=Decimal(50),unallocated=Decimal(0),grant=copy.deepcopy(g),remaining=copy.deepcopy(g),consumed=z.copy(),reserved=z.copy(),phase='COMMITTED',revision=1)
    snap=dict(id=1,validUntil=110,clockDomain='FIXTURE_MONOTONIC',timeUnit='tick',marketFingerprint='independent-market-fixture-1')
    a=dict(identity=copy.deepcopy(ids),complete=True,journalComplete=True,history={source:r},historyObservedAt=90,historyMaxAge=20,snapshot=copy.deepcopy(snap),snapshotReceipts={1:encode(snap)},now=100,clockDomain='FIXTURE_MONOTONIC',timeUnit='tick',consumptionPolicy=1,approvedPolicies=[1,2],allocations={'A1':alloc})
    q=dict(identity=copy.deepcopy(ids),event=41,allocation='A1',currency='USD',digits=2,consumptionPolicy=1,bucket='FinalReserve',purpose='CatchUp',amount=Decimal(10))
    seal(q,a);return q,s,{},a


def seal(q,a):
    alloc=a['allocations']['A1'];r=a['history'][alloc['source']]
    q['proofDigest']=fingerprint(dict(record=r,allocation=alloc,expected=a['identity']))


def cases(m=oracle):
    rows=[]
    def add(cid,group,actual,want,assertions=1):
        rows.append(dict(id=cid,group=group,actual=actual,expected=want,assertions=assertions,result='PASS' if actual==want else 'FAIL'))
    def exercise(cid,edit=lambda q,s,j,a:None,want='REJECT',reseal=False,base=None):
        q,s,j,a=fixture() if base is None else copy.deepcopy(base)
        edit(q,s,j,a)
        if reseal:seal(q,a)
        before=copy.deepcopy((q,s,j,a))
        status,ss,jj,aa=m.apply_for_test(q,s,j,a)
        add(cid,'BOUNDARY',(status,ss==s,jj==j,aa==a,(q,s,j,a)==before),(want,True,True,True,True),5)
    q,s,j,a=fixture()
    add('CONTROL-commit','CONTROL',m.apply_for_test(*fixture())[:2],('COMMITTED_IN_MEMORY',dict(copy.deepcopy(s),remaining=dict(s['remaining'],FinalReserve=Decimal(40)),consumed=dict(s['consumed'],FinalReserve=Decimal(10)),revision=2)))
    add('CONTROL-eligibility','CONTROL',m.authorize(q,s,j,a),'ELIGIBLE_FOR_COMMIT')
    for field in IDS:
        exercise('IDENTITY-'+field,lambda q,s,j,a,f=field:q['identity'].update({f:999 if type(q['identity'][f]) is int else 'FOREIGN'}))
    for field in ('Broker','Server','Account','Symbol','Magic','Deal','Order','Position','Cycle'):
        exercise('RECORD-'+field,lambda q,s,j,a,f=field:a['history'][s['source']]['identity'].update({f:999 if type(a['identity'][f]) is int else 'FOREIGN'}),want='CONFLICT' if field in ('Broker','Server','Account','Deal') else 'REJECT',reseal=True)
    exercise('DIGEST-forged',lambda q,s,j,a:q.update(proofDigest='0'*64))
    exercise('RAW-net-mismatch',lambda q,s,j,a:a['history'][s['source']].update(rawNet=Decimal(999)),want='CONFLICT',reseal=True)
    exercise('POSTED-net-mismatch',lambda q,s,j,a:(a['history'][s['source']].update(profit=Decimal(56),rawNet=Decimal(51)),a['history'][s['source']]['receipt'].update(raw=Decimal(51),posted=Decimal(51))),want='CONFLICT',reseal=True)
    for component in ('profit','swap','commission','fee'):
        exercise('COMPONENT-'+component,lambda q,s,j,a,k=component:a['history'][s['source']].update({k:a['history'][s['source']][k]+Decimal(1)}),want='CONFLICT',reseal=True)
    exercise('SNAPSHOT-id',lambda q,s,j,a:(a['snapshot'].update(id=999),a['snapshotReceipts'].update({999:encode(a['snapshot'])})))
    for value in (0,True,None):exercise('SNAPSHOT-invalid-'+str(value),lambda q,s,j,a,v=value:a['snapshot'].update(id=v))
    exercise('SNAPSHOT-missing-id',lambda q,s,j,a:a['snapshot'].pop('id'))
    exercise('SNAPSHOT-unknown',lambda q,s,j,a:a.update(snapshotReceipts={}),want='UNAVAILABLE')
    exercise('SNAPSHOT-content',lambda q,s,j,a:a['snapshot'].update(marketFingerprint='OTHER'),want='CONFLICT')
    exercise('SNAPSHOT-expired',lambda q,s,j,a:(a['snapshot'].update(validUntil=99),a['snapshotReceipts'].update({1:encode(a['snapshot'])})),want='UNAVAILABLE')
    for value in (True,False,0,-1,1.5,'41',None,2**64):
        exercise('EVENT-invalid-'+repr(value),lambda q,s,j,a,v=value:q.update(event=v))
    for value in (1,2**64-1):
        qq=copy.deepcopy(q);qq['event']=value
        add('EVENT-boundary-'+str(value),'EVENT',m.apply_for_test(qq,s,j,a)[0],'COMMITTED_IN_MEMORY')
    for field,value in [('Account',2**63),('Account',True),('Magic',0),('Magic',2**63),('Deal',2**64),('Plan',True)]:
        exercise('ID-domain-'+field+'-'+str(value),lambda q,s,j,a,k=field,v=value:q['identity'].update({k:v}))
    qq,ss,jj,aa=fixture();qq['identity']['Magic']=-7;aa['identity']['Magic']=-7;aa['history'][ss['source']]['identity']['Magic']=-7;seal(qq,aa)
    add('ID-negative-magic','DOMAIN',m.authorize(qq,ss,jj,aa),'ELIGIBLE_FOR_COMMIT')
    for path in ('event','identity','identity.Plan'):
        def remove(q,s,j,a,path=path):
            if '.' in path:q['identity'].pop(path.split('.')[1])
            else:q.pop(path)
        exercise('MISSING-'+path,remove)
    for path in ('receipt','posted'):
        def remove(q,s,j,a,path=path):
            r=a['history'][s['source']]
            if path=='receipt':r.pop('receipt')
            else:r['receipt'].pop('posted')
        exercise('MISSING-'+path,remove)
    exercise('MISSING-allocation',lambda q,s,j,a:a.update(allocations={}))
    for bad in (Decimal('NaN'),Decimal('Infinity'),'bad',None,True,1.5):
        exercise('MONEY-invalid-'+repr(bad),lambda q,s,j,a,v=bad:q.update(amount=v))
    for label,index,bad in [('state',1,[]),('journal',2,[]),('history',3,[])]:
        qq,ss,jj,aa=fixture();args=[qq,ss,jj,aa]
        if label=='history':aa['history']=bad
        else:args[index]=bad
        exercise('DTO-type-'+label,want='REJECT',base=args)
    exercise('AUTHORITY-none',want='UNAVAILABLE',base=(q,s,j,None))
    exercise('JOURNAL-none',want='UNAVAILABLE',base=(q,s,None,a))
    exercise('HISTORY-none',lambda q,s,j,a:a.update(history=None),want='UNAVAILABLE')
    exercise('RECEIPT-unavailable',lambda q,s,j,a:a['history'][s['source']].update(receipt=None),want='UNAVAILABLE')
    exercise('HISTORY-empty',lambda q,s,j,a:a.update(history={}))
    exercise('AUTHORITY-incomplete',lambda q,s,j,a:a.update(complete=False),want='UNAVAILABLE')
    exercise('JOURNAL-incomplete',lambda q,s,j,a:a.update(journalComplete=False),want='UNAVAILABLE')
    exercise('TIME-future',lambda q,s,j,a:a.update(historyObservedAt=1000),want='UNAVAILABLE')
    exercise('TIME-too-old',lambda q,s,j,a:a.update(historyObservedAt=79),want='UNAVAILABLE')
    exercise('TIME-missing',lambda q,s,j,a:a.pop('historyObservedAt'))
    exercise('TIME-domain',lambda q,s,j,a:(a.update(clockDomain='UTC'),a['snapshot'].update(clockDomain='UTC'),a['snapshotReceipts'].update({1:encode(a['snapshot'])})),want='UNAVAILABLE')
    exercise('TIME-unit',lambda q,s,j,a:a.update(timeUnit='seconds'),want='UNAVAILABLE')
    exercise('TIME-negative',lambda q,s,j,a:a.update(historyObservedAt=-1))
    exercise('TIME-snapshot-domain',lambda q,s,j,a:a['snapshot'].update(clockDomain='OTHER'),want='UNAVAILABLE')
    for label,edit in [('max-age',lambda a:a.update(historyObservedAt=80)),('snapshot-end',lambda a:a.update(now=110))]:
        qq,ss,jj,aa=fixture();edit(aa)
        add('TIME-control-'+label,'TIME',m.authorize(qq,ss,jj,aa),'ELIGIBLE_FOR_COMMIT')
    qq,st,jj,au=fixture();au['history'][st['source']]['identity'].update(Plan=999,StateRevision=999,SnapshotID=999);seal(qq,au)
    add('ORIGIN-context-distinct','AUTHORITY',m.authorize(qq,st,jj,au),'ELIGIBLE_FOR_COMMIT')
    exercise('ALLOCATION-internal',lambda q,s,j,a:a['allocations']['A1'].update(allocation='OTHER'),want='CONFLICT',reseal=True)
    exercise('REVISION-exhausted',lambda q,s,j,a:(q['identity'].update(StateRevision=2**64-1),s.update(revision=2**64-1),a['identity'].update(StateRevision=2**64-1)),want='UNAVAILABLE',reseal=True)
    exercise('REVISION-state',lambda q,s,j,a:s.update(revision=999))
    exercise('ALLOCATION-state',lambda q,s,j,a:s.update(allocation='A2'))
    exercise('ALLOCATION-source',lambda q,s,j,a:s.update(source=('B1','S1',1,999)))
    exercise('ALLOCATION-event',lambda q,s,j,a:a['allocations']['A1'].update(event=32),want='CONFLICT',reseal=True)
    exercise('ALLOCATION-policy',lambda q,s,j,a:a['allocations']['A1'].update(policyVersion=2),want='CONFLICT',reseal=True)
    exercise('ALLOCATION-grant-type',lambda q,s,j,a:a['allocations']['A1'].update(grant=[]))
    exercise('ALLOCATION-grant-missing-bucket',lambda q,s,j,a:a['allocations']['A1']['grant'].pop('Carry'))
    exercise('ALLOCATION-grant-snan',lambda q,s,j,a:a['allocations']['A1']['grant'].update(Carry=Decimal('sNaN')))
    exercise('ALLOCATION-vector',lambda q,s,j,a:(s['grant'].update(FinalReserve=Decimal(40),PartialFar=Decimal(10)),s['remaining'].update(FinalReserve=Decimal(40),PartialFar=Decimal(10))),want='CONFLICT')
    exercise('BALANCE-sum',lambda q,s,j,a:(s['grant'].update(FinalReserve=Decimal(40)),s['remaining'].update(FinalReserve=Decimal(40)),a['allocations']['A1']['grant'].update(FinalReserve=Decimal(40))),reseal=True)
    exercise('BALANCE-consumed',lambda q,s,j,a:s['consumed'].update(PartialFar=Decimal(1)))
    exercise('BALANCE-reserved',lambda q,s,j,a:s['reserved'].update(PartialFar=Decimal(1)))
    exercise('BALANCE-negative',lambda q,s,j,a:s['remaining'].update(FinalReserve=Decimal(-1)))
    exercise('BALANCE-prepared',lambda q,s,j,a:s.update(phase='PREPARED'))
    exercise('AMOUNT-precision',lambda q,s,j,a:q.update(amount=Decimal('.005')))
    exercise('AMOUNT-exceeds',lambda q,s,j,a:q.update(amount=Decimal(51)))
    exercise('SOURCE-unconfirmed',lambda q,s,j,a:a['history'][s['source']].update(closingConfirmed=False),reseal=True)
    exercise('SOURCE-role',lambda q,s,j,a:a['history'][s['source']].update(role='Small'),reseal=True)
    exercise('CURRENCY',lambda q,s,j,a:q.update(currency='EUR'))
    exercise('PRECISION-metadata',lambda q,s,j,a:q.update(digits=3))
    exercise('BUCKET-forbidden',lambda q,s,j,a:q.update(bucket='PartialFar'))
    exercise('PURPOSE-forbidden',lambda q,s,j,a:q.update(purpose='PartialFar'))
    status,ss,jj,aa=m.apply_for_test(q,s,j,a)
    for label,edit in [('exact',lambda q,s,j,a:None),('revision-policy-snapshot',lambda q,s,j,a:(a.update(consumptionPolicy=2,now=1000),a['identity'].update(Plan=999,SnapshotID=999)))]:
        exercise('REPLAY-'+label,edit,want='NO_OP',base=(q,ss,jj,aa))
    exercise('REPLAY-changed',lambda q,s,j,a:q.update(amount=Decimal(11)),want='CONFLICT',base=(q,ss,jj,aa))
    full=copy.deepcopy(q);full.update(event=42,amount=Decimal(40));full['identity']['StateRevision']=2;seal(full,aa)
    st,sss,jjj,aaa=m.apply_for_test(full,ss,jj,aa)
    add('SPEND-full','SPEND',(st,sss['remaining']['FinalReserve'],sss['consumed']['FinalReserve'],sss['revision']),('COMMITTED_IN_MEMORY',Decimal(0),Decimal(50),3),4)
    exercise('SPEND-full-replay',want='NO_OP',base=(full,sss,jjj,aaa))
    extra=copy.deepcopy(full);extra.update(event=43,amount=Decimal(1));extra['identity']['StateRevision']=3;seal(extra,aaa)
    exercise('SPEND-no-reuse',base=(extra,sss,jjj,aaa))
    q,s,j,a=fixture()
    original=copy.deepcopy((q,s,j,a));m.apply_for_test(q,s,j,a)
    add('APPLY-input-unchanged','ATOMICITY',(q,s,j,a)==original,True)
    # Independent literal money and geometry vectors, not expected values from subject.
    for val,want in [('0',Decimal(0)),('-15',Decimal(0)),('50',Decimal(50))]:
        add('ALLOC-'+val,'MONEY',sum(m.allocate(val,['.5','.25','.1','.1'],2).values()),want)
    add('ALLOC-residual','MONEY',m.allocate('.01',['.5','.5','0','0'],2)['ResidualHeld'],Decimal('.01'))
    for raw,digits,want in [('1.005',2,'1.00'),('1.015',2,'1.02'),('-1.015',2,'-1.02'),('1.5',0,'2'),('1.0015',3,'1.002')]:
        add('ROUND-'+raw,'MONEY',m.candidate_round(raw,digits),Decimal(want))
    rec=dict(currency='USD',digits=2,raw='1.005',posted='1.01')
    add('POSTING-A','MONEY',m.posted('1.005','USD',2,rec),('POSTED',Decimal('1.01')))
    add('POSTING-B','MONEY',m.posted('1.005','USD',2,rec,'LOCAL_VERIFIED',True),('UNAVAILABLE',None))
    add('POSTING-C','MONEY',m.posted('1.005','USD',None,None),('UNAVAILABLE',None))
    l1=dict(id=1,available='50',loss='20',buffer='1',transitionLoss='100',currency='USD',sourceFresh=True,snapshotFresh=True,complete=True,share='.5',bnet='4',far='1')
    l2=dict(l1,id=2,available='5',transitionLoss='10')
    add('CR09-A','CR09',m.worst([l1,l2],[1,2]),('REJECT',2,Decimal(-16)))
    add('CR09-B','CR09',m.worst([l1,l2],[1,2],'B'),('SINGLE_LEVEL_POSITIVE',1,Decimal(29)))
    add('CR09-all-positive','CR09',m.worst([l1,dict(l2,available='40')],[1,2]),('ALL_LEVEL_POSITIVE',2,Decimal(19)))
    for name,levels,required,want in [('zero',[l1,dict(l2,available='21')],[1,2],'REJECT'),('duplicate',[l1,l1],[1,2],'UNPROVEN'),('stale-source',[l1,dict(l2,sourceFresh=False)],[1,2],'UNPROVEN'),('stale-snapshot',[l1,dict(l2,snapshotFresh=False)],[1,2],'UNPROVEN'),('currency',[l1,dict(l2,currency='EUR')],[1,2],'UNAVAILABLE'),('lot-gate',[l1,dict(l2,bnet='2')],[1,2],'REJECT'),('required-mismatch',[l1,l2],[1,3],'UNPROVEN')]:
        add('CR09-'+name,'CR09',m.worst(levels,required)[0],want)
    add('CR09-tie','CR09',m.worst([dict(l1,id=2),dict(l1,id=1,transitionLoss='1')],[1,2]),('ALL_LEVEL_POSITIVE',1,Decimal(29)))
    add('CR09-missing','CR09',m.worst([l1],[1,2])[0],'UNPROVEN')
    add('SEQUENTIAL-exhaust','CR09',m.sequential('50',['30','20'])[1][-1]['ReserveAfter'],Decimal(0))
    add('SEQUENTIAL-no-reuse','CR09',m.sequential('50',['30','30'])[0],'REJECT')
    add('SEQUENTIAL-unknown','CR09',m.sequential(None,['30'])[0],'UNPROVEN')
    for name,args,want in [('zero',('.10','.01','3','.1','.01','100','.01'),'REJECT'),('min',('.10','.1','3','.1','.01','100','.01'),'GEOMETRY_ONLY'),('unknown-grid',('.10','2','1','.5','.015','100','.01'),'UNPROVEN')]:
        add('CORE-'+name,'GEOMETRY',m.geometry(*args)['status'],want)
    # All mandatory DTO keys are independently deleted, one at a time.
    for key in q:
        exercise('SHAPE-request-'+key,lambda q,s,j,a,k=key:q.pop(k))
    for key in s:
        exercise('SHAPE-state-'+key,lambda q,s,j,a,k=key:s.pop(k))
    for key in a:
        exercise('SHAPE-authority-'+key,lambda q,s,j,a,k=key:a.pop(k))
    for key in a['snapshot']:
        exercise('SHAPE-snapshot-'+key,lambda q,s,j,a,k=key:a['snapshot'].pop(k))
    for key in a['history'][s['source']]:
        exercise('SHAPE-record-'+key,lambda q,s,j,a,k=key:a['history'][s['source']].pop(k))
    for key in a['history'][s['source']]['receipt']:
        exercise('SHAPE-receipt-'+key,lambda q,s,j,a,k=key:a['history'][s['source']]['receipt'].pop(k))
    for key in a['allocations']['A1']:
        exercise('SHAPE-allocation-'+key,lambda q,s,j,a,k=key:a['allocations']['A1'].pop(k))
    exercise('SHAPE-unserializable-extra',lambda q,s,j,a:q.update(extra={1,2}))
    exercise('SHAPE-invalid-source-key',lambda q,s,j,a:a['allocations']['A1'].update(source=[]))
    exercise('SHAPE-journal-bool-key',lambda q,s,j,a:j.update({('B1','S1',1,True):'x'}))
    exercise('MONEY-profile-limit',lambda q,s,j,a:q.update(amount=Decimal('1e-65')))
    qq,st,jj,au=fixture();huge=Decimal('1000000000000000000000000000000.00')
    qq['amount']=Decimal('.01');st['net']=huge;st['grant']['FinalReserve']=huge;st['remaining']['FinalReserve']=huge
    au['allocations']['A1']['grant']['FinalReserve']=huge;r=au['history'][st['source']]
    r.update(profit=huge,commission=Decimal(0),rawNet=huge);r['receipt'].update(raw=huge,posted=huge);seal(qq,au)
    bigStatus,bigState,_,_=m.apply_for_test(qq,st,jj,au)
    add('MONEY-exact-large','MONEY',(bigStatus,bigState['remaining']['FinalReserve'],bigState['consumed']['FinalReserve']),('COMMITTED_IN_MEMORY',Decimal('999999999999999999999999999999.99'),Decimal('.01')),3)
    # Domain is closed under a legal unreserved debit, including exponent boundary.
    qq,st,jj,au=fixture();edge=Decimal('1e64');qq['amount']=Decimal('.01')
    st['net']=edge;st['grant']['FinalReserve']=edge;st['remaining']['FinalReserve']=edge
    au['allocations']['A1']['grant']['FinalReserve']=edge;r=au['history'][st['source']]
    r.update(profit=edge,commission=Decimal(0),rawNet=edge);r['receipt'].update(raw=edge,posted=edge);seal(qq,au)
    statusEdge,edgeState,edgeJournal,edgeAuthority=m.apply_for_test(qq,st,jj,au)
    nextq=copy.deepcopy(qq);nextq['event']=42;nextq['identity']['StateRevision']=2;seal(nextq,edgeAuthority)
    add('MONEY-domain-closure','MONEY',(statusEdge,m.authorize(nextq,edgeState,edgeJournal,edgeAuthority)),('COMMITTED_IN_MEMORY','ELIGIBLE_FOR_COMMIT'),2)
    # Expected programming errors remain visible, not converted into a success/REJECT.
    q,s,j,a=fixture();original=copy.deepcopy((q,s,j,a))
    saved=m.digest
    def broken(x):raise RuntimeError('injected internal defect')
    m.digest=broken
    try:
        try:m.apply_for_test(q,s,j,a);actual='SWALLOWED'
        except RuntimeError:actual='VISIBLE_INTERNAL_ERROR'
    finally:m.digest=saved
    add('INTERNAL-error-visible','ATOMICITY',actual,'VISIBLE_INTERNAL_ERROR')
    add('INTERNAL-error-inputs-unchanged','ATOMICITY',(q,s,j,a)==original,True)
    q,s,j,a=fixture();original=copy.deepcopy((q,s,j,a));savedAuth=m.authorize;savedCanonical=m.canonical
    def fault_after_authorization(*args):
        status=savedAuth(*args)
        if status=='ELIGIBLE_FOR_COMMIT':m.canonical=broken
        return status
    m.authorize=fault_after_authorization
    try:
        try:m.apply_for_test(q,s,j,a);actual='SWALLOWED'
        except RuntimeError:actual='VISIBLE_INTERNAL_ERROR'
    finally:m.authorize=savedAuth;m.canonical=savedCanonical
    add('INTERNAL-serialization-visible','ATOMICITY',actual,'VISIBLE_INTERNAL_ERROR')
    add('INTERNAL-serialization-unchanged','ATOMICITY',(q,s,j,a)==original,True)
    return rows


def metadata():return dict(testedSHA=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),executedUtc=datetime.now(timezone.utc).isoformat(),contractStatus='PROPOSED',brokerEvidence='NOT_RUN',durableRestart='UNPROVEN',MQL5_COMPILE='NOT_RUN',MQL5_TESTS='NOT_RUN',STRATEGY_TESTER='NOT_RUN')


def save(path,data):
    path=Path(path).resolve();assert path.is_relative_to(ROOT) and 'R0C' in path.name
    path.write_text(json.dumps(wire(data),ensure_ascii=False,indent=2)+'\n')


def main():
    p=argparse.ArgumentParser();p.add_argument('--output');a=p.parse_args()
    started=datetime.now(timezone.utc).isoformat()
    rows=cases();out=dict(metadata(),StartedUtc=started,FinishedUtc=datetime.now(timezone.utc).isoformat(),Command=[sys.executable,*sys.argv],ExitCode=int(any(x['result']=='FAIL' for x in rows)),sourceHashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (Path(oracle.__file__),Path(__file__).resolve())},scenarios=len(rows),assertions=sum(x['assertions'] for x in rows),passed=sum(x['result']=='PASS' for x in rows),failed=sum(x['result']=='FAIL' for x in rows),tests=rows)
    if a.output:save(a.output,out)
    print(json.dumps({k:v for k,v in out.items() if k!='tests'}))
    for row in rows:
        if row['result']=='FAIL':print(wire(row))
    return int(out['failed']>0)


if __name__=='__main__':raise SystemExit(main())
