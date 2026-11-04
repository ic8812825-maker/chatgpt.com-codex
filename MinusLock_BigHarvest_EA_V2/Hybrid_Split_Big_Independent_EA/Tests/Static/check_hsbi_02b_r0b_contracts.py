#!/usr/bin/env python3
"""Literal normative vectors, independent of production/R0A expected outputs."""
import argparse
import copy
from datetime import datetime,timezone
from decimal import Decimal,ROUND_HALF_EVEN
import hashlib
import json
from pathlib import Path
import runpy
import sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'Tests/Reference'))
import hsbi_02b_r0b_independent_oracle as oracle

# Test data/schema are not obtained from the model under test.
FIELDS=('Broker','Server','Account','Symbol','Magic','Deal','Order','Position','Cycle',
        'Plan','StateRevision','AllocationEvent','PolicyVersion','SnapshotID')
B=('FinalReserve','PartialFar','Transition','Carry','ResidualHeld')


def contract_json(x):
    if isinstance(x,Decimal):return '0' if x==0 else format(x.normalize(),'f')
    if isinstance(x,dict):return {k:contract_json(v) for k,v in sorted(x.items())}
    if isinstance(x,(list,tuple)):return [contract_json(v) for v in x]
    return x


def contract_digest(x):
    return hashlib.sha256(json.dumps(contract_json(x),sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()


def fixtures():
    identity=dict(zip(FIELDS,('B1','S1',1,'EURUSD',7,11,12,13,1,1,1,31,1,1)))
    source=('B1','S1',1,11)
    grant=dict(zip(B,map(Decimal,('50','0','0','0','0'))));zero=dict.fromkeys(B,Decimal(0))
    record=dict(identity=copy.deepcopy(identity),closingConfirmed=True,role='BigCore',profit=Decimal(55),
                swap=Decimal(0),commission=Decimal(-5),fee=Decimal(0),rawNet=Decimal(50),currency='USD',digits=2,
                receipt=dict(currency='USD',digits=2,raw=Decimal(50),posted=Decimal(50)))
    allocation=dict(allocation='A1',source=source,grant=grant,policyVersion=1,event=31)
    state=dict(allocation='A1',source=source,currency='USD',digits=2,net=Decimal(50),unallocated=Decimal(0),
               grant=copy.deepcopy(grant),remaining=copy.deepcopy(grant),consumed=zero.copy(),reserved=zero.copy(),phase='COMMITTED',revision=1)
    authority=dict(identity=identity,complete=True,history={source:record},historyObservedAt=90,historyMaxAge=20,
                   snapshot=dict(id=1,validUntil=110),now=100,consumptionPolicy=1,approvedPolicies=[1,2],allocations={'A1':allocation})
    request=dict(identity=copy.deepcopy(identity),event=41,allocation='A1',currency='USD',digits=2,consumptionPolicy=1,
                 bucket='FinalReserve',purpose='CatchUp',amount=Decimal(10),presentedRecord=copy.deepcopy(record))
    seal(request,authority)
    return request,state,{},authority


def seal(request,authority):
    row=authority['allocations']['A1'];record=authority['history'].get(row['source'],request['presentedRecord'])
    request['proofDigest']=contract_digest(dict(record=record,allocation=row,expected=authority['identity']))


def reference_cases(m=oracle):
    rows=[]
    def add(cid,group,actual,want):
        rows.append(dict(id=cid,group=group,actual=actual,expected=want,result='PASS' if actual==want else 'FAIL',normativeStatus='PROPOSED'))
    def denied(cid,q,s,j,a,want='REJECT'):
        before=copy.deepcopy((s,j,a));status,ss,jj,aa=m.apply_for_test(q,s,j,a)
        add(cid,'AUTHORITY',(status,ss==before[0],jj==before[1],aa==before[2]),(want,True,True,True))
    q,s,j,a=fixtures()
    for field in FIELDS:
        add('ID-control-'+field,'AUTHORITY',m.authorize(q,s,j,a),'ELIGIBLE_FOR_COMMIT')
        qq=copy.deepcopy(q);qq['identity'][field]=999 if isinstance(qq['identity'][field],int) else 'FOREIGN'
        denied('ID-foreign-'+field,qq,s,j,a)
    for field in ('Account','Deal'):
        qq=copy.deepcopy(q);qq['identity'][field]=True
        denied('ID-bool-'+field,qq,s,j,a)
    qq,st,jj,au=fixtures();qq['identity']['Magic']=-7;au['identity']['Magic']=-7;au['history'][st['source']]['identity']['Magic']=-7;seal(qq,au)
    add('ID-signed-Magic-control','AUTHORITY',m.authorize(qq,st,jj,au),'ELIGIBLE_FOR_COMMIT')
    status,ss,jj,aa=m.apply_for_test(q,s,j,a)
    add('EVENT-first','REPLAY',(status,ss['remaining']['FinalReserve'],ss['revision']),('COMMITTED_IN_MEMORY',Decimal(40),2))
    denied('EVENT-exact-revision-advanced',q,ss,jj,aa,'NO_OP')
    changed=copy.deepcopy(q);changed['amount']=Decimal(11)
    denied('EVENT-altered-amount',changed,ss,jj,aa,'CONFLICT')
    rotated=copy.deepcopy(aa);rotated['consumptionPolicy']=2
    denied('EVENT-exact-policy-advanced',q,ss,jj,rotated,'NO_OP')
    changed=copy.deepcopy(q);changed['consumptionPolicy']=2
    denied('EVENT-altered-policy',changed,ss,jj,rotated,'CONFLICT')
    for field in FIELDS:
        qq=copy.deepcopy(q);qq['identity'][field]=999 if isinstance(qq['identity'][field],int) else 'FOREIGN'
        denied('EVENT-altered-'+field,qq,ss,jj,aa,'REJECT' if field in ('Broker','Server','Account') else 'CONFLICT')
    full=copy.deepcopy(q);full['event']=42;full['identity']['StateRevision']=2;full['amount']=Decimal(40);seal(full,aa)
    done,sss,jjj,aaa=m.apply_for_test(full,ss,jj,aa)
    add('EVENT-full-consumed','REPLAY',(done,sss['remaining']['FinalReserve'],sss['consumed']['FinalReserve']),('COMMITTED_IN_MEMORY',Decimal(0),Decimal(50)))
    denied('EVENT-full-replay',full,sss,jjj,aaa,'NO_OP')
    extra=copy.deepcopy(full);extra['event']=43;extra['identity']['StateRevision']=3;extra['amount']=Decimal(1);seal(extra,aaa)
    denied('EVENT-spent-new',extra,sss,jjj,aaa)
    for cid,edit,want in [
        ('state-revision',lambda q,s,a:s.update(revision=999),'REJECT'),
        ('state-source',lambda q,s,a:s.update(source=('B1','S1',1,999)),'REJECT'),
        ('state-allocation',lambda q,s,a:s.update(allocation='A2'),'REJECT'),
        ('amount-precision',lambda q,s,a:q.update(amount=Decimal('.005')),'REJECT'),
        ('currency',lambda q,s,a:q.update(currency='EUR'),'REJECT'),
        ('precision-metadata',lambda q,s,a:q.update(digits=3),'REJECT'),
        ('source-unconfirmed',lambda q,s,a:a['history'][s['source']].update(closingConfirmed=False),'REJECT'),
        ('source-role',lambda q,s,a:a['history'][s['source']].update(role='Small'),'REJECT'),
        ('snapshot-stale',lambda q,s,a:a['snapshot'].update(validUntil=99),'UNAVAILABLE'),
        ('source-stale',lambda q,s,a:a.update(historyObservedAt=0),'UNAVAILABLE'),
        ('history-missing',lambda q,s,a:a.update(history={ }),'REJECT'),
        ('history-unavailable',lambda q,s,a:a.update(history=None),'UNAVAILABLE'),
        ('grant-vector',lambda q,s,a:(s['grant'].update(FinalReserve=Decimal(40),PartialFar=Decimal(10)),s['remaining'].update(FinalReserve=Decimal(40),PartialFar=Decimal(10))),'CONFLICT'),
        ('reserved-other-bucket',lambda q,s,a:s['reserved'].update(PartialFar=Decimal(1)),'REJECT'),
        ('consumed-other-bucket',lambda q,s,a:s['consumed'].update(PartialFar=Decimal(1)),'REJECT'),
        ('sum-grants',lambda q,s,a:(s['grant'].update(FinalReserve=Decimal(40)),s['remaining'].update(FinalReserve=Decimal(40)),a['allocations']['A1']['grant'].update(FinalReserve=Decimal(40))),'REJECT'),
        ('negative-remaining',lambda q,s,a:s['remaining'].update(FinalReserve=Decimal(-1)),'REJECT')]:
        qq,st,jj,au=fixtures();edit(qq,st,au)
        if au['history'] is not None:seal(qq,au)
        denied('GUARD-'+cid,qq,st,jj,au,want)
    for amount in (Decimal('NaN'),Decimal('Infinity')):
        qq=copy.deepcopy(q);qq['amount']=amount;denied('GUARD-amount-'+str(amount),qq,s,j,a)
    denied('GUARD-incomplete-authority',q,s,j,dict(a,complete=False),'UNAVAILABLE')
    denied('GUARD-missing-registry',q,s,None,a,'UNAVAILABLE')
    # Signed rebates are retained, not blindly subtracted as positive costs.
    qq,st,jj,au=fixtures();record=au['history'][st['source']]
    record.update(profit=Decimal(50),swap=Decimal(1),commission=Decimal('.5'),fee=Decimal('-.25'),rawNet=Decimal('51.25'))
    record['receipt'].update(raw=Decimal('51.25'),posted=Decimal('51.25'))
    st['net']=Decimal('51.25');st['grant']['FinalReserve']=Decimal('51.25');st['remaining']['FinalReserve']=Decimal('51.25');au['allocations']['A1']['grant']['FinalReserve']=Decimal('51.25');seal(qq,au)
    add('SOURCE-signed-components','AUTHORITY',m.authorize(qq,st,jj,au),'ELIGIBLE_FOR_COMMIT')
    # Ordinary grant replay is immutable; consumption is a separate event.
    row=a['allocations']['A1'];add('GRANT-replay','ALLOCATION',m.classify_grant(row,copy.deepcopy(row)),'NO_OP')
    changed=copy.deepcopy(row);changed['grant'].update(FinalReserve=Decimal(0),PartialFar=Decimal(50))
    add('GRANT-bucket-permutation','ALLOCATION',m.classify_grant(row,changed),'CONFLICT')
    for key in ('event','policyVersion'):
        changed=copy.deepcopy(row);changed[key]=999
        add('GRANT-altered-'+key,'ALLOCATION',m.classify_grant(row,changed),'CONFLICT')
    for val,want in [('0','0'),('-15','0'),('50','50')]:
        add('ALLOC-net-'+val,'ALLOCATION',sum(m.allocate(val,['.5','.25','.1','.1'],2).values()),Decimal(want))
    add('ALLOC-residual-cent','ALLOCATION',m.allocate('.01',['.5','.5','0','0'],2)['ResidualHeld'],Decimal('.01'))
    prepared=copy.deepcopy(s);prepared['grant']['FinalReserve']=Decimal(40);prepared['remaining']['FinalReserve']=Decimal(40);prepared.update(unallocated=Decimal(10),phase='PREPARED')
    add('BALANCE-prepared','ALLOCATION',m.balance(prepared),True)
    pa=copy.deepcopy(a);pa['allocations']['A1']['grant']=copy.deepcopy(prepared['grant']);pq=copy.deepcopy(q);seal(pq,pa)
    denied('GUARD-prepared-no-spend',pq,prepared,j,pa)
    committed=copy.deepcopy(prepared);committed['phase']='COMMITTED'
    add('BALANCE-committed-unallocated','ALLOCATION',m.balance(committed),False)
    for raw,digits,want in [('1.005',2,'1.00'),('1.015',2,'1.02'),('-1.005',2,'-1.00'),('-1.015',2,'-1.02'),('1.5',0,'2'),('2.5',0,'2'),('1.0005',3,'1.000'),('1.0015',3,'1.002')]:
        add('PREC-round-'+raw+'-'+str(digits),'PRECISION',m.candidate_round(raw,digits),Decimal(want))
    raw=sum([Decimal('.335')]*3);once=m.candidate_round(raw,2);twice=sum(m.candidate_round(x,2) for x in [Decimal('.335')]*3)
    add('PREC-component-vs-once','PRECISION',(once,twice),(Decimal('1.00'),Decimal('1.02')))
    add('PREC-double-round-boundary','PRECISION',(m.candidate_round(Decimal('1.2451'),2),m.candidate_round(m.candidate_round('1.2451',3),2)),(Decimal('1.25'),Decimal('1.24')))
    receipt=dict(currency='USD',digits=2,raw='1.005',posted='1.01')
    add('PREC-broker-posted','PRECISION',m.posted('1.005','USD',2,receipt),('POSTED',Decimal('1.01')))
    add('PREC-local-mismatch','PRECISION',m.posted('1.005','USD',2,receipt,'LOCAL_VERIFIED',True),('UNAVAILABLE',None))
    add('PREC-local-matched','PRECISION',m.posted('1.005','USD',2,dict(receipt,posted='1.00'),'LOCAL_VERIFIED',True),('POSTED',Decimal('1.00')))
    add('PREC-unverified-local','PRECISION',m.posted('1.005','USD',2,receipt,'LOCAL_VERIFIED',False),('UNAVAILABLE',None))
    add('PREC-unknown-digits','PRECISION',m.posted('1.005','USD',None,receipt),('UNAVAILABLE',None))
    add('PREC-missing-post','PRECISION',m.posted('1.005','USD',2,None),('UNAVAILABLE',None))
    for currency,digits,raw,amount in [('JPY',0,'1.5','2'),('KWD',3,'1.0015','1.002')]:
        rec=dict(currency=currency,digits=digits,raw=raw,posted=amount)
        add('PREC-currency-'+currency,'PRECISION',m.posted(raw,currency,digits,rec),('POSTED',Decimal(amount)))
        add('ALLOC-precision-'+currency,'PRECISION',sum(m.allocate(amount,['.5','.25','0','0'],digits).values()),Decimal(amount))
    add('PREC-posted-off-grid','PRECISION',m.posted('1.005','USD',2,dict(receipt,posted='1.005')),('UNAVAILABLE',None))
    for v in ('NaN','Infinity','-Infinity'):
        try:m.number(v);actual='ACCEPTED'
        except ValueError:actual='REJECT'
        add('FINITE-'+v,'PRECISION',actual,'REJECT')
    for value,want in [(0.0,'0000000000000000'),(-0.0,'0000000000000000'),(1.0,'3ff0000000000000'),(-5.0,'c014000000000000'),(0.1,'3fb999999999999a')]:
        add('CODEC-raw64-'+repr(value),'CODEC',m.raw64(value),want)
    l1=dict(id=1,available='50',loss='20',buffer='1',transitionLoss='100',currency='USD',sourceFresh=True,snapshotFresh=True,complete=True,share='.5',bnet='4',far='1')
    l2=dict(l1,id=2,available='5',transitionLoss='10')
    add('CR09-A-negative','CR09',m.worst([l1,l2],[1,2]),('REJECT',2,Decimal(-16)))
    add('CR09-B-positive-limited','CR09',m.worst([l1,l2],[1,2],'B'),('POSITIVE',1,Decimal(29)))
    add('CR09-all-positive','CR09',m.worst([l1,dict(l2,available='40')],[1,2]),('POSITIVE',2,Decimal(19)))
    add('CR09-zero','CR09',m.worst([l1,dict(l2,available='21')],[1,2]),('REJECT',2,Decimal(0)))
    add('CR09-missing-level','CR09',m.worst([l1],[1,2])[0],'UNPROVEN')
    add('CR09-single-depth','CR09',m.worst([l1],[1])[0],'UNPROVEN')
    add('CR09-duplicate-level','CR09',m.worst([l1,l1],[1,2])[0],'UNPROVEN')
    add('CR09-required-mismatch','CR09',m.worst([l1,l2],[1,3])[0],'UNPROVEN')
    for key in ('sourceFresh','snapshotFresh','complete'):
        add('CR09-'+key,'CR09',m.worst([l1,dict(l2,**{key:False})],[1,2])[0],'UNPROVEN')
    add('CR09-currency','CR09',m.worst([l1,dict(l2,currency='EUR')],[1,2])[0],'UNAVAILABLE')
    add('CR09-lot-gate','CR09',m.worst([l1,dict(l2,bnet='2')],[1,2])[0],'REJECT')
    add('CR09-negative-loss-invalid','CR09',m.worst([l1,dict(l2,loss='-100')],[1,2])[0],'REJECT')
    add('CR09-tie-different-loss','CR09',m.worst([dict(l1,id=2),dict(l1,id=1,transitionLoss='1')],[1,2]),('POSITIVE',1,Decimal(29)))
    seq=m.sequential('50',['30','20'])
    add('SEQUENTIAL-conserve','CR09',(seq[0],[x['ReserveAfter'] for x in seq[1]]),('CONSERVATION_ONLY',[Decimal(20),Decimal(0)]))
    add('SEQUENTIAL-no-reuse','CR09',m.sequential('50',['30','30'])[0],'REJECT')
    add('SEQUENTIAL-missing','CR09',m.sequential('50',['30',None])[0],'UNPROVEN')
    geometry=[('zero','.10','.01','3','.1','.01','100','.01','REJECT'),
              ('subminimum','.10','.2','3','.5','.03','100','.01','REJECT'),
              ('equal-minimum','.10','.1','3','.1','.01','100','.01','GEOMETRY_ONLY'),
              ('above-minimum','.10','2','1','.5','.01','100','.01','GEOMETRY_ONLY'),
              ('min-not-on-grid','.10','2','1','.5','.015','100','.01','UNPROVEN'),
              ('nonstandard-step','.10','2','1','.5','.025','100','.025','GEOMETRY_ONLY'),
              ('core-over-max','.10','2','1','.5','.01','.15','.01','REJECT'),
              ('slope-negative','.10','.1','0','.5','.01','100','.01','REJECT')]
    for name,*args,want in geometry:add('CORE-'+name,'CORE',m.geometry(*args)['status'],want)
    return rows


def legacy_supplementary(m):
    old=runpy.run_path(str(ROOT/'Tests/Static/check_hsbi_02b_r0a_normative_contracts.py'))
    def base():return old['fixtures']()
    rows=[]
    def add(cid,got,want):rows.append(dict(id=cid,actual=got,expected=want,result='PASS' if got==want else 'FAIL'))
    r,h,s,a,q,c,p=base();foreign=copy.deepcopy(q);foreign['owner']['account']=999
    add('OLD-account',m.authorize(foreign,s,{},a),'REJECT')
    for field in ('plan','revision','source','allocation'):
        r,h,s,a,q,c,p=base();q[field]=('FOREIGN',) if field=='source' else 'FOREIGN' if field=='allocation' else 999
        add('OLD-'+field,m.authorize(q,s,{},a),'REJECT')
    r,h,s,a,q,c,p=base();q['amount']=Decimal('.005');add('OLD-precision',m.authorize(q,s,{},a),'REJECT')
    for cid,change in [('bucket-vector',lambda s:(s['remaining'].update(FinalReserve=Decimal(40),PartialFar=Decimal(10)))),
                       ('sum-grants',lambda s:(s['grant'].update(FinalReserve=Decimal(40)),s['remaining'].update(FinalReserve=Decimal(40)))),
                       ('reserved',lambda s:s['reserved'].update(PartialFar=Decimal(1))),
                       ('consumed',lambda s:s['consumed'].update(PartialFar=Decimal(1)))]:
        r,h,s,a,q,c,p=base();change(s)
        add('OLD-'+cid,m.valid_balance(s['net'],s['grant'],s['remaining'],s['consumed'],s['reserved']),False)
    r,h,s,a,q,c,p=base();registry={('B1','S1',1,41):q};changed=dict(q,amount=Decimal(11))
    add('OLD-replay',m.authorize(changed,s,registry,a),'CONFLICT')
    r,h,s,a,q,c,p=base();add('OLD-history',m.reconciled_net(r,{},r['owner'])[0],'REJECT')
    r,h,s,a,q,c,p=base();r['event']=0;add('OLD-confirmed-source',m.reconciled_net(r,{m.source_key(r):r},r['owner'])[0],'REJECT')
    r,h,s,a,q,c,p=base();c['fresh']=False
    # Independently encode the declared R0A wire format (not its digest helper).
    p['digest']=contract_digest(dict(schema='R0A-CANDIDATE-1',payload=dict(record=r,grant=s['grant'],context=c)))
    add('OLD-snapshot',m.verify_proof(p,r,s,h,c),'REJECT')
    r,h,s,a,q,c,p=base();r['role']='Small';h={m.source_key(r):r};p['identity']['role']='Small';p['digest']=contract_digest(dict(schema='R0A-CANDIDATE-1',payload=dict(record=r,grant=s['grant'],context=c)))
    add('OLD-role',m.verify_proof(p,r,s,h,c),'REJECT')
    return rows


def audit_legacy():
    scope=runpy.run_path(str(ROOT/'Tests/Static/check_hsbi_02b_r0a_normative_contracts.py'))
    m=scope['tests'].__globals__['m'];observed=[]
    mapping={'Cycle':'cycle','Plan':'plan','StateRevision':'revision','AllocationEvent':'allocationEvent','PolicyVersion':'policy',
             'Symbol':'symbol','Magic':'magic','Deal':'deal','Order':'order','Position':'position','SnapshotID':'snapshot'}
    values=dict(zip(FIELDS,('B1','S1',1,'EURUSD',7,11,12,13,1,1,1,31,1,1)))
    for field in FIELDS:
        r,h,s,a,q,c,p=scope['fixtures']()
        if field in ('Broker','Server','Account'):
            key={'Broker':'broker','Server':'server','Account':'account'}[field]
            q['owner'][key]=values[field]
        else:q[mapping[field]]=values[field]
        positive=m.authorize(q,s,{},a)
        bad=copy.deepcopy(q);wrong=999 if isinstance(values[field],int) else 'FOREIGN'
        if field in ('Broker','Server','Account'):bad['owner'][key]=wrong
        else:bad[mapping[field]]=wrong
        status,ss,jj,aa=m.apply_for_test(bad,s,{},a)
        observed.append(dict(id='R0A-boundary-'+field,field=field,positive=positive,negative=status,
            completeContractExpected='REJECT',balanceUnchanged=ss==s,revisionUnchanged=aa==a,
            scope='authorize/apply_for_test only; unsupported extra fields do not establish full proof-chain behavior',
            classification='BINDING_GAP_AT_THIS_BOUNDARY' if status=='COMMITTED_IN_MEMORY' else 'REJECTED_AT_THIS_BOUNDARY'))
    old=runpy.run_path(str(ROOT/'Tests/Static/check_hsbi_02b_r0_ledger_integrity.py'))
    allocation=dict(account=1,symbol='EUR',magic=7,cycle=1,deal=11,allocation='A1',allocationEvent=31,policy=1,available=50)
    request={k:v for k,v in allocation.items() if k!='available'};request.update(event=41,bucket='FinalReserve',purpose='CatchUp',amount=10,plan=1,revision=1)
    for field in ('plan','revision'):
        bad=dict(request,**{field:999})
        observed.append(dict(id='R0-legacy-'+field,actual=old['oracle_consumption'](allocation,bad,{}),expected='REJECT',
            newOracleCase='ID-foreign-'+('Plan' if field=='plan' else 'StateRevision'),classification='LEGACY_ORACLE_GAP'))
    r,h,s,a,q,c,p=scope['fixtures']();r.update(profit=Decimal('1.005'),swap=Decimal(0),commission=Decimal(0),fee=Decimal(0),rawNet=Decimal('1.005'))
    status,amount=m.reconciled_net(r,{m.source_key(r):r},r['owner'])
    observed.append(dict(id='R0A-implicit-USD2-posting',actualStatus=status,actualAmount=amount.value,
        independentlySpecifiedBrokerPosted=Decimal('1.01'),classification='POSTED_AMOUNT_NOT_PART_OF_R0A_API',
        scope='Synthetic receipt counterexample, not observed broker behavior'))
    return observed


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path);args=ap.parse_args()
    rows=reference_cases();out=dict(testedHead=__import__('subprocess').check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
       executedUtc=datetime.now(timezone.utc).isoformat(),passed=sum(x['result']=='PASS' for x in rows),failed=sum(x['result']=='FAIL' for x in rows),tests=rows,legacyObservations=audit_legacy(),
       status='PROPOSED_CONTRACT',brokerEvidence='NOT_RUN',persistenceEvidence='UNPROVEN',mql5Runtime='NOT_RUN')
    if args.output:
        p=args.output.resolve();assert p.is_relative_to(ROOT);p.write_text(json.dumps(contract_json(out),ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('tests','legacyObservations')}))
    for row in rows:
        if row['result']=='FAIL':print(row)
    return int(out['failed']>0)


if __name__=='__main__':raise SystemExit(main())
