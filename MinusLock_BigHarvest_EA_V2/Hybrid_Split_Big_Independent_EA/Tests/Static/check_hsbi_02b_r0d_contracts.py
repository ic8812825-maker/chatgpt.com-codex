#!/usr/bin/env python3
"""Independent literal/integer-scale expected outcomes, no Fraction expected arithmetic."""
import argparse
import copy
import decimal
from decimal import Decimal
from datetime import datetime,timezone
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'Tests/Reference'))
import hsbi_02b_r0d_independent_oracle as oracle
B=('FinalReserve','PartialFar','Transition','Carry','ResidualHeld')
IDS=('Broker','Server','Account','Symbol','Magic','Deal','Order','Position','Cycle','Plan','StateRevision','AllocationEvent','PolicyVersion','SnapshotID')


def integer_ratio(text):
    # Independent decimal coefficient/scale parser for literal test vectors.
    text=str(text);sign=-1 if text.startswith('-') else 1;text=text.lstrip('+-')
    if 'e' in text.lower():mantissa,exponent=text.lower().split('e');exponent=int(exponent)
    else:mantissa=text;exponent=0
    whole,_,fraction=mantissa.partition('.');n=int((whole or '0')+fraction)*sign;scale=len(fraction)-exponent
    n,d=n*10**max(-scale,0),10**max(scale,0);g=math.gcd(n,d)
    return n//g,d//g


def ratio(value):
    if type(value) is Decimal:
        x=value.as_tuple();n=int(''.join(map(str,x.digits)) or '0')*(-1 if x.sign else 1);d=10**max(-x.exponent,0);n*=10**max(x.exponent,0);g=math.gcd(n,d);return n//g,d//g
    if type(value) is int:return value,1
    return value.numerator,value.denominator


def N(text):n,d=integer_ratio(text);return ['NUMBER',str(n),str(d)]


def view(value,strict=False):
    if type(value) is Decimal or hasattr(value,'denominator') and type(value) not in (int,bool):
        if type(value) is Decimal and not value.is_finite():return ['NONFINITE',str(value)]
        n,d=ratio(value);return [type(value).__name__ if strict else 'NUMBER',str(n),str(d)]
    if type(value) is dict:
        if all(type(k) is str for k in value):return {k:view(v,strict) for k,v in sorted(value.items())}
        return ['MAPPING',[[view(k,strict),view(v,strict)] for k,v in value.items()]]
    if type(value) in (list,tuple):return [type(value).__name__,[view(v,strict) for v in value]] if strict else [view(v,strict) for v in value]
    return value


def independent_token(x):
    if x is None:return ['null']
    if type(x) is bool:return ['bool',x]
    if type(x) is int:return ['int',str(x)]
    if type(x) is Decimal or hasattr(x,'denominator') and type(x) is not int:
        n,d=ratio(x);return ['number',str(n),str(d)]
    if type(x) is str:return ['str',x]
    if type(x) in (list,tuple):return ['list' if type(x) is list else 'tuple',[independent_token(v) for v in x]]
    if type(x) is dict:return ['map',[[k,independent_token(v)] for k,v in sorted(x.items())]]
    raise TypeError('unsupported test wire type')


def encode(x):return json.dumps(['HSBI-R0D-TYPED-1',independent_token(x)],ensure_ascii=False,separators=(',',':'))
def fingerprint(x):return hashlib.sha256(encode(x).encode()).hexdigest()


def fixture():
    ids=dict(zip(IDS,('B1','S1',1,'EURUSD',7,11,12,13,1,1,1,31,1,1)));source=('B1','S1',1,11)
    grant=dict(zip(B,map(Decimal,('50','0','0','0','0'))));zero=dict.fromkeys(B,Decimal(0))
    record=dict(identity=copy.deepcopy(ids),closingConfirmed=True,role='BigCore',profit=Decimal(55),swap=Decimal(0),commission=Decimal(-5),fee=Decimal(0),rawNet=Decimal(50),currency='USD',digits=2,receipt=dict(currency='USD',digits=2,raw=Decimal(50),posted=Decimal(50)))
    allocation=dict(allocation='A1',source=source,grant=copy.deepcopy(grant),policyVersion=1,event=31)
    state=dict(allocation='A1',source=source,currency='USD',digits=2,net=Decimal(50),unallocated=Decimal(0),grant=copy.deepcopy(grant),remaining=copy.deepcopy(grant),consumed=zero.copy(),reserved=zero.copy(),phase='COMMITTED',revision=1)
    snapshot=dict(schemaVersion='HSBI-SNAPSHOT-FIXTURE-1',id=1,validUntil=110,clockDomain='FIXTURE_MONOTONIC',timeUnit='tick',marketFingerprint='1')
    authority=dict(identity=copy.deepcopy(ids),complete=True,journalComplete=True,history={source:record},historyObservedAt=90,historyMaxAge=20,snapshot=copy.deepcopy(snapshot),snapshotReceipts={1:encode(snapshot)},now=100,clockDomain='FIXTURE_MONOTONIC',timeUnit='tick',consumptionPolicy=1,approvedPolicies=[1,2],allocations={'A1':allocation})
    request=dict(identity=copy.deepcopy(ids),event=41,allocation='A1',currency='USD',digits=2,consumptionPolicy=1,bucket='FinalReserve',purpose='CatchUp',amount=Decimal(10))
    seal(request,authority);return request,state,{},authority


def seal(q,a):
    allocation=a['allocations']['A1'];record=a['history'].get(allocation['source'],q.get('presentedRecord'))
    q['proofDigest']=fingerprint(dict(record=record,allocation=allocation,expected=a['identity']))


def apply_summary(m,args):
    before=view(args,True);status,s,j,a=m.apply_for_test(*args)
    return dict(status=status,remaining=view(s['remaining']['FinalReserve']),consumed=view(s['consumed']['FinalReserve']),reserved=view(s['reserved']['FinalReserve']),revision=s['revision'],journalCount=len(j),inputsUnchanged=view(args,True)==before)


def negative(m,edit,want='REJECT',reseal=False):
    args=fixture();edit(*args)
    if reseal:seal(args[0],args[3])
    before=view(args,True);snapshots=[view(x,True) for x in args];status,s,j,a=m.apply_for_test(*args)
    return dict(status=status,stateUnchanged=view(s,True)==snapshots[1],journalUnchanged=view(j,True)==snapshots[2],authorityUnchanged=view(a,True)==snapshots[3],inputsUnchanged=view(args,True)==before)


def levels(available='50',loss='20',buffer='1'):
    row=dict(id=1,available=available,loss=loss,buffer=buffer,transitionLoss='100',currency='KWD',digits=3,sourceFresh=True,snapshotFresh=True,complete=True,share='.5',bnet='4',far='1')
    return [row,dict(row,id=2,transitionLoss='10')]


def big_fixture():
    q,s,j,a=fixture();huge=Decimal('1e28');q['amount']=Decimal('.01')
    for bucket in ('grant','remaining'):s[bucket]['FinalReserve']=huge
    s['net']=huge;a['allocations']['A1']['grant']['FinalReserve']=huge;r=a['history'][s['source']]
    r.update(profit=huge,commission=Decimal(0),rawNet=huge);r['receipt'].update(raw=huge,posted=huge);seal(q,a)
    return q,s,j,a


def composite(m):
    q,s,j,a=fixture();grants=m.allocate('50',['1','0','0','0'],2)
    s['grant']=copy.deepcopy(grants);s['remaining']=copy.deepcopy(grants);a['allocations']['A1']['grant']=copy.deepcopy(grants);seal(q,a)
    status,s1,j1,a1=m.apply_for_test(q,s,j,a)
    full=copy.deepcopy(q);full.update(event=42,amount=Decimal(40));full['identity']['StateRevision']=2;seal(full,a1)
    eligible=m.authorize(full,s1,j1,a1);done,s2,j2,a2=m.apply_for_test(full,s1,j1,a1)
    replay=m.apply_for_test(full,s2,j2,a2)
    more=copy.deepcopy(full);more.update(event=43,amount=Decimal(1));more['identity']['StateRevision']=3;seal(more,a2)
    return dict(first=status,next=eligible,second=done,balance1=m.balance(s1),balance2=m.balance(s2),remaining=view(s2['remaining']['FinalReserve']),consumed=view(s2['consumed']['FinalReserve']),revision=s2['revision'],journalCount=len(j2),replay=replay[0],replayUnchanged=view(replay[1:],True)==view((s2,j2,a2),True),extra=m.apply_for_test(more,s2,j2,a2)[0])


def scenarios():
    cases=[]
    def add(cid,fn,want,predicates=1,contract='NUM-AUTH'):cases.append(dict(id=cid,run=fn,expected=want,predicates=predicates,contract=contract))
    add('CONTROL-authorize',lambda m:m.authorize(*fixture()),'ELIGIBLE_FOR_COMMIT',contract='NUM-AUTH')
    add('CONTROL-apply',lambda m:apply_summary(m,fixture()),dict(status='COMMITTED_IN_MEMORY',remaining=N('40'),consumed=N('10'),reserved=N('0'),revision=2,journalCount=1,inputsUnchanged=True),7)
    add('CODEC-cyclic',codec_cycle,'REJECT',contract='NUM-CODEC')
    add('CODEC-control',lambda m:m.canonical('1'),'["HSBI-R0D-TYPED-1",["str","1"]]',contract='NUM-CODEC')
    add('DOMAIN-direct',lambda m:number_outcome(m,'1e65'),dict(status='UNAVAILABLE',value=None),2,'NUM-DOMAIN-1')
    add('CONTROL-number',lambda m:view(m.number('1.005')),N('1.005'),contract='NUM-PARSE')
    for raw,want in [('1.005','1.00'),('1.015','1.02'),('-1.005','-1.00'),('-1.015','-1.02')]:add('ROUND-'+raw,lambda m,x=raw:view(m.candidate_round(x,2)),N(want),contract='NUM-ROUND')
    add('POSTED-unknown-precision',lambda m:view(m.posted('1.005','USD',None,None)),['UNAVAILABLE',None],2,'NUM-POSTED')
    add('POSTED-missing-receipt',lambda m:view(m.posted('1.005','USD',2,None)),['UNAVAILABLE',None],2,'NUM-POSTED')
    for currency,digits,raw,posted in [('USD',2,'1.005','1.01'),('JPY',0,'1.5','2'),('KWD',3,'1.0015','1.002')]:
        add('POSTED-'+currency,lambda m,c=currency,d=digits,r=raw,p=posted:view(m.posted(r,c,d,dict(currency=c,digits=d,raw=r,posted=p))),['POSTED',N(posted)],2,'NUM-POSTED')
    for cid,receipt,verified,want in [('posted-grid','1.005',False,['UNAVAILABLE',None]),('local-unverified','1.00',False,['UNAVAILABLE',None]),('local-verified','1.00',True,['POSTED',N('1')])]:
        add(cid,lambda m,p=receipt,v=verified,cid=cid:view(m.posted('1.005','USD',2,dict(currency='USD',digits=2,raw='1.005',posted=p),'BROKER_POSTED' if cid=='posted-grid' else 'LOCAL_VERIFIED',v)),want,2,'NUM-POSTED')
    for cents in (0,1,2,3,49,50,99,10001,10**30,10**66):
        money=f'{cents//100}.{cents%100:02d}';grants=[cents//2,cents//4,cents//10,cents//10];grants.append(cents-sum(grants))
        expected=dict(zip(B,[N(f'{v//100}.{v%100:02d}') for v in grants]))
        add('ALLOC-integer-units-'+str(cents),lambda m,x=money:view(m.allocate(x,['.5','.25','.1','.1'],2)),expected,5,'NUM-GRANT')
    add('ALLOC-full',lambda m:view(m.allocate('50',['.5','.25','.1','.1'],2)),dict(zip(B,[N('25'),N('12.5'),N('5'),N('5'),N('2.5')])),5,'NUM-GRANT')
    add('ALLOC-residual',lambda m:view(m.allocate('.01',['.5','.5','0','0'],2)),dict(zip(B,[N('0')]*4+[N('.01')])),5,'NUM-GRANT')
    add('ALLOC-negative',lambda m:view(m.allocate('-10',['1','0','0','0'],2)),dict.fromkeys(B,N('0')),5,'NUM-GRANT')
    add('ALLOC-small',lambda m:view(m.allocate('10',['1','0','0','0'],2,'Small')),dict(zip(B,[N('0')]*4+[N('10')])),5,'NUM-GRANT')
    add('BALANCE-direct',lambda m:m.balance(fixture()[1]),True,contract='NUM-BALANCE')
    add('BALANCE-large',lambda m:m.balance(big_fixture()[1]),True,contract='NUM-BALANCE')
    add('COMPOSITION-full',composite,dict(first='COMMITTED_IN_MEMORY',next='ELIGIBLE_FOR_COMMIT',second='COMMITTED_IN_MEMORY',balance1=True,balance2=True,remaining=N('0'),consumed=N('50'),revision=3,journalCount=2,replay='NO_OP',replayUnchanged=True,extra='REJECT'),12,'NUM-APPLY')
    add('COMPOSITION-replay-conflict',altered_replay,dict(status='CONFLICT',stateUnchanged=True,journalUnchanged=True,authorityUnchanged=True,inputsUnchanged=True),5,'NUM-AUTH')
    add('CLOSURE-edge',domain_edge,dict(first='COMMITTED_IN_MEMORY',balance=True,next='ELIGIBLE_FOR_COMMIT'),3,'NUM-APPLY')
    add('APPLY-large',lambda m:apply_summary(m,big_fixture()),dict(status='COMMITTED_IN_MEMORY',remaining=N('9999999999999999999999999999.99'),consumed=N('.01'),reserved=N('0'),revision=2,journalCount=1,inputsUnchanged=True),7,'NUM-APPLY')
    denied=dict(status='REJECT',stateUnchanged=True,journalUnchanged=True,authorityUnchanged=True,inputsUnchanged=True)
    def deny(cid,edit,want='REJECT',reseal=False,contract='NUM-AUTH'):add(cid,lambda m,e=edit,w=want,r=reseal:negative(m,e,w,r),dict(denied,status=want),5,contract)
    deny('amount-negative',lambda q,s,j,a:q.update(amount=Decimal(-10)))
    deny('amount-zero',lambda q,s,j,a:q.update(amount=Decimal(0)))
    deny('reserved-available',lambda q,s,j,a:s['reserved'].update(FinalReserve=Decimal(45)))
    deny('amount-exceeds',lambda q,s,j,a:q.update(amount=Decimal(51)))
    deny('amount-offgrid',lambda q,s,j,a:q.update(amount=Decimal('.005')))
    deny('digest-forged',lambda q,s,j,a:q.update(proofDigest='0'*64))
    deny('raw-sum',lambda q,s,j,a:a['history'][s['source']].update(rawNet=Decimal(999)),'CONFLICT',True)
    deny('posted-net',lambda q,s,j,a:(a['history'][s['source']].update(profit=Decimal(56),rawNet=Decimal(51)),a['history'][s['source']]['receipt'].update(raw=Decimal(51),posted=Decimal(51))),'CONFLICT',True)
    deny('record-magic',lambda q,s,j,a:a['history'][s['source']]['identity'].update(Magic=999),reseal=True)
    deny('history-missing',lambda q,s,j,a:(q.update(presentedRecord=copy.deepcopy(a['history'][s['source']])),a.update(history={})))
    deny('history-unavailable',lambda q,s,j,a:a.update(history=None),'UNAVAILABLE')
    deny('source-unconfirmed',lambda q,s,j,a:a['history'][s['source']].update(closingConfirmed=False),reseal=True)
    deny('source-role',lambda q,s,j,a:a['history'][s['source']].update(role='Small'),reseal=True)
    deny('bucket-vector',lambda q,s,j,a:(s['grant'].update(FinalReserve=Decimal(40),PartialFar=Decimal(10)),s['remaining'].update(FinalReserve=Decimal(40),PartialFar=Decimal(10))),'CONFLICT')
    deny('prepared',lambda q,s,j,a:s.update(phase='PREPARED'))
    deny('snapshot-content',lambda q,s,j,a:a['snapshot'].update(marketFingerprint='OTHER'),'CONFLICT',contract='SNAP-FIXTURE-1')
    deny('snapshot-id',lambda q,s,j,a:(a['snapshot'].update(id=999),a['snapshotReceipts'].update({999:encode(a['snapshot'])})),contract='SNAP-FIXTURE-1')
    deny('snapshot-unknown',lambda q,s,j,a:a.update(snapshotReceipts={}),'UNAVAILABLE',contract='SNAP-FIXTURE-1')
    for value,label,status in [(Decimal(1),'decimal','REJECT'),(1,'int','REJECT'),(True,'bool','REJECT'),(None,'none','UNAVAILABLE'),('','empty','REJECT'),({},'dict','REJECT'),([],'list','REJECT'),((),'tuple','REJECT')]:
        deny('snapshot-type-'+label,lambda q,s,j,a,v=value:a['snapshot'].update(marketFingerprint=v),status,contract='SNAP-FIXTURE-1')
    deny('snapshot-missing',lambda q,s,j,a:a['snapshot'].pop('marketFingerprint'),contract='SNAP-FIXTURE-1')
    deny('snapshot-schema',lambda q,s,j,a:a['snapshot'].update(schemaVersion='UNKNOWN'),'UNAVAILABLE',contract='SNAP-FIXTURE-1')
    deny('snapshot-extra',lambda q,s,j,a:a['snapshot'].update(extra=1),contract='SNAP-FIXTURE-1')
    for f in IDS:deny('identity-'+f,lambda q,s,j,a,k=f:q['identity'].update({k:999 if type(q['identity'][k]) is int else 'FOREIGN'}))
    for value,label in [(True,'bool'),(0,'zero'),(-1,'negative'),(1.5,'float'),('41','string'),(2**64,'overflow')]:deny('event-'+label,lambda q,s,j,a,v=value:q.update(event=v))
    deny('missing-event',lambda q,s,j,a:q.pop('event'))
    deny('money-nan',lambda q,s,j,a:q.update(amount=Decimal('NaN')))
    deny('domain-overflow',lambda q,s,j,a:q.update(amount=Decimal('1e65')),'UNAVAILABLE',contract='NUM-DOMAIN-1')
    deny('domain-subgrid',lambda q,s,j,a:q.update(amount=Decimal('1e-65')),'UNAVAILABLE',contract='NUM-DOMAIN-1')
    deny('future-history',lambda q,s,j,a:a.update(historyObservedAt=1000),'UNAVAILABLE')
    deny('stale-snapshot',lambda q,s,j,a:a['snapshot'].update(validUntil=99),'UNAVAILABLE')
    add('WORST-control',lambda m:view(m.worst(levels(),[1,2])),['ALL_LEVEL_POSITIVE',1,N('29')],3,'NUM-WORST')
    add('WORST-cancellation',lambda m:view(m.worst(levels('1e28','.010','9999999999999999999999999999.995'),[1,2])),['REJECT',1,N('-.005')],3,'NUM-WORST')
    for margin,av in [('-1','20.999'),('0','21'),('+1','21.001')]:add('WORST-boundary-'+margin,lambda m,v=av:view(m.worst(levels(v),[1,2])),['ALL_LEVEL_POSITIVE' if margin=='+1' else 'REJECT',1,N('-.001' if margin=='-1' else '.001' if margin=='+1' else '0')],3,'NUM-WORST')
    add('WORST-scope-B',lambda m:view(m.worst([levels()[0],dict(levels()[1],available='5')],[1,2],'B')),['SINGLE_LEVEL_POSITIVE',1,N('29')],3,'NUM-WORST')
    add('WORST-malformed-currency',lambda m:m.worst([dict(levels()[0],currency=[]),levels()[1]],[1,2])[0],'REJECT',contract='NUM-WORST')
    add('WORST-required',lambda m:m.worst(levels(),[1,3])[0],'UNPROVEN',contract='NUM-WORST')
    def seq(m,reserve,costs):
        r=m.sequential(reserve,costs);return dict(status=r['status'],remaining=view(r['remaining']),appliedCount=r['appliedCount'],rejectedIndex=r['rejectedIndex'],trace=view(r['trace']))
    def row(i,b,c,a):return dict(level=i,ReserveBefore=N(b),Consumption=N(c),ReserveAfter=N(a))
    add('SEQUENTIAL-control',lambda m:seq(m,'50',['30','20']),dict(status='CONSERVATION_ONLY',remaining=N('0'),appliedCount=2,rejectedIndex=None,trace=[row(1,'50','30','20'),row(2,'20','20','0')]),5,'NUM-SEQUENTIAL')
    add('SEQUENTIAL-large',lambda m:seq(m,'1e28',['.01','.01']),dict(status='CONSERVATION_ONLY',remaining=N('9999999999999999999999999999.98'),appliedCount=2,rejectedIndex=None,trace=[row(1,'1e28','.01','9999999999999999999999999999.99'),row(2,'9999999999999999999999999999.99','.01','9999999999999999999999999999.98')]),5,'NUM-SEQUENTIAL')
    add('SEQUENTIAL-prefix-reject',lambda m:seq(m,'50',['30','30']),dict(status='REJECT',remaining=N('20'),appliedCount=1,rejectedIndex=2,trace=[row(1,'50','30','20')]),5,'NUM-SEQUENTIAL')
    add('SEQUENTIAL-prefix-malformed',lambda m:seq(m,'50',['30','bad']),dict(status='REJECT',remaining=N('20'),appliedCount=1,rejectedIndex=2,trace=[row(1,'50','30','20')]),5,'NUM-SEQUENTIAL')
    add('SEQUENTIAL-prefix-unsupported',lambda m:seq(m,'50',['30','1e65']),dict(status='UNAVAILABLE',remaining=N('20'),appliedCount=1,rejectedIndex=2,trace=[row(1,'50','30','20')]),5,'NUM-SEQUENTIAL')
    add('SEQUENTIAL-unknown',lambda m:m.sequential('50',['30',None])['status'],'UNPROVEN',contract='NUM-SEQUENTIAL')
    add('GEOMETRY-positive',lambda m:m.geometry('.1','.1','3','.1','.01','100','.01')['status'],'GEOMETRY_ONLY',contract='NUM-GEOMETRY')
    add('GEOMETRY-zero',lambda m:m.geometry('.1','.01','3','.1','.01','100','.01')['status'],'REJECT',contract='NUM-GEOMETRY')
    add('GEOMETRY-grid-unknown',lambda m:m.geometry('.1','2','1','.5','.015','100','.01')['status'],'UNPROVEN',contract='NUM-GEOMETRY')
    for name,a,b in [('str-decimal','1',Decimal(1)),('str-int','1',1),('int-bool',1,True),('null-missing',{'x':None},{}),('empty-missing',{'x':''},{}),('list-tuple',[1],(1,))]:
        add('CODEC-'+name,lambda m,a=a,b=b:m.canonical(a)!=m.canonical(b),True,contract='NUM-CODEC')
    add('POSTSTATE-fault',poststate_fault,dict(status='UNAVAILABLE',stateUnchanged=True,journalUnchanged=True,authorityUnchanged=True,inputsUnchanged=True),5,'NUM-APPLY')
    add('INTERNAL-error-visible',internal_fault,dict(errorVisible=True,inputsUnchanged=True),2,'NUM-APPLY')
    return cases


def domain_edge(m):
    q,s,j,a=big_fixture();edge=Decimal('1e64')
    s['net']=edge;s['grant']['FinalReserve']=edge;s['remaining']['FinalReserve']=edge;a['allocations']['A1']['grant']['FinalReserve']=edge;r=a['history'][s['source']]
    r.update(profit=edge,commission=Decimal(0),rawNet=edge);r['receipt'].update(raw=edge,posted=edge);seal(q,a)
    status,s,j,a=m.apply_for_test(q,s,j,a);q['event']=42;q['identity']['StateRevision']=2;seal(q,a)
    return dict(first=status,balance=m.balance(s),next=m.authorize(q,s,j,a))


def codec_cycle(m):
    value=[];value.append(value)
    try:m.canonical(value);return 'ACCEPTED'
    except m.Malformed:return 'REJECT'


def number_outcome(m,value):
    try:return dict(status='VALUE',value=view(m.number(value)))
    except m.Unsupported:return dict(status='UNAVAILABLE',value=None)
    except m.Malformed:return dict(status='REJECT',value=None)


def altered_replay(m):
    q,s,j,a=fixture();_,s,j,a=m.apply_for_test(q,s,j,a);q['amount']=Decimal(11)
    before=[view(x,True) for x in (q,s,j,a)];status,ss,jj,aa=m.apply_for_test(q,s,j,a)
    return dict(status=status,stateUnchanged=view(ss,True)==before[1],journalUnchanged=view(jj,True)==before[2],authorityUnchanged=view(aa,True)==before[3],inputsUnchanged=[view(x,True) for x in (q,s,j,a)]==before)


def poststate_fault(m):
    args=fixture();before=[view(x,True) for x in args];saved=m.debit_for_test
    def faulty(s,amount):
        saved(s,amount);s['remaining']['FinalReserve']=m.number('-1')
    m.debit_for_test=faulty
    try:status,s,j,a=m.apply_for_test(*args)
    finally:m.debit_for_test=saved
    return dict(status=status,stateUnchanged=view(s,True)==before[1],journalUnchanged=view(j,True)==before[2],authorityUnchanged=view(a,True)==before[3],inputsUnchanged=[view(x,True) for x in args]==before)


def internal_fault(m):
    args=fixture();before=view(args,True);saved=m.debit_for_test
    def broken(s,amount):raise RuntimeError('injected programming failure')
    m.debit_for_test=broken
    try:
        try:m.apply_for_test(*args);visible=False
        except RuntimeError:visible=True
    finally:m.debit_for_test=saved
    return dict(errorVisible=visible,inputsUnchanged=view(args,True)==before)


def context_state(c):return dict(prec=c.prec,rounding=c.rounding,Emax=c.Emax,Emin=c.Emin,capitals=c.capitals,clamp=c.clamp,flags={k.__name__:v for k,v in c.flags.items()},traps={k.__name__:v for k,v in c.traps.items()})


def contexts():
    specs=[(28,decimal.ROUND_HALF_EVEN,999999,-999999,False,False),(2,decimal.ROUND_UP,9,-9,True,True),(1,decimal.ROUND_FLOOR,0,0,True,False),(9,decimal.ROUND_CEILING,99,-99,False,True),(100,decimal.ROUND_DOWN,64,-64,True,True),(256,decimal.ROUND_HALF_UP,9,-9,True,False),(3,decimal.ROUND_05UP,0,0,False,True),(64,decimal.ROUND_HALF_DOWN,64,-64,False,False)]
    out=[]
    for prec,rounding,emax,emin,trap,flag in specs:
        c=decimal.Context(prec=prec,rounding=rounding,Emax=emax,Emin=emin,clamp=int(prec==3))
        for signal in c.traps:c.traps[signal]=trap;c.flags[signal]=flag
        out.append(c)
    return out


def run(m=oracle):
    scenarios_list=scenarios();rows=[];configs=contexts()
    for index,config in enumerate(configs):
        for case in scenarios_list:
            with decimal.localcontext(config) as context:
                before=context_state(context)
                try:
                    actual=case['run'](m);same=context_state(context)==before
                    result='PASS' if actual==case['expected'] and same else 'FAIL'
                    row=dict(id=case['id'],context=index,contract=case['contract'],actual=actual,expected=case['expected'],contextUnchanged=same,result=result,predicates=case['predicates']+1)
                except Exception as e:row=dict(id=case['id'],context=index,contract=case['contract'],result='INFRASTRUCTURE_ERROR',errorType=type(e).__name__,message=str(e),predicates=case['predicates']+1)
                rows.append(row)
    return dict(scenarios=len(scenarios_list),contextConfigurations=[context_state(c) for c in configs],executions=len(rows),comparisonPredicates=sum(r['predicates'] for r in rows),passed=sum(r['result']=='PASS' for r in rows),failed=sum(r['result']=='FAIL' for r in rows),infrastructureErrors=sum(r['result']=='INFRASTRUCTURE_ERROR' for r in rows),tests=rows)


def metadata():return dict(testedSHA=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),executedUtc=datetime.now(timezone.utc).isoformat(),status='PROPOSED',MQL5_COMPILE='NOT_RUN',MQL5_TESTS='NOT_RUN',STRATEGY_TESTER='NOT_RUN')


def save(path,data):
    path=Path(path).resolve();assert path.is_relative_to(ROOT) and 'R0D' in path.name
    path.write_text(json.dumps(view(data),ensure_ascii=False,indent=2)+'\n')


def main():
    p=argparse.ArgumentParser();p.add_argument('--output');a=p.parse_args();start=datetime.now(timezone.utc).isoformat();out=dict(metadata(),**run())
    out.update(Command=[sys.executable,*sys.argv],StartedUtc=start,FinishedUtc=datetime.now(timezone.utc).isoformat(),ExitCode=int(out['failed']+out['infrastructureErrors']>0),SourceHashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (Path(__file__).resolve(),Path(oracle.__file__))})
    if a.output:save(a.output,out)
    print(json.dumps({k:v for k,v in out.items() if k not in ('tests','contextConfigurations')}))
    for r in out['tests']:
        if r['result']!='PASS':print(r)
    return out['ExitCode']


if __name__=='__main__':raise SystemExit(main())
