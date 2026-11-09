#!/usr/bin/env python3
"""R0E literal contracts; independent integer-scale/wire utility from frozen R0D tests.

No expected outcome is obtained from a subject evaluator.
"""
import argparse
import copy
from datetime import datetime,timezone
from decimal import Decimal,localcontext
import hashlib
import json
from pathlib import Path
import subprocess
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'Tests/Reference'))
import hsbi_02b_r0e_contract_model as model
import check_hsbi_02b_r0d_contracts as wire
N=wire.N
view=wire.view


def record(net='50',role='BigCore',deal=11,account=1):
    ids=dict(zip(model.IDENTITY,('B1','S1',account,'EURUSD',7,1,13,deal,12,31,role,1,1,1,1)))
    return dict(identity=ids,kind='ReconciledEconomicNet',entry='CLOSE',currency='USD',digits=2,profit=Decimal(net),swap=Decimal(0),commission=Decimal(0),fee=Decimal(0),rawNet=Decimal(net),postedNet=Decimal(net))


def fixture():
    r=record();source=('B1','S1',1,11);history={wire.encode(source):r}
    state=dict(schema='HSBI-R0E-FREE-1',revision=1,sources={},allocations={},events={},journalComplete=True)
    return state,history,source


def grants(amount='50',bucket='FinalReserve'):
    out=dict.fromkeys(model.BUCKETS,Decimal(0));out[bucket]=Decimal(amount);return out


def funded(m,amount='50',bucket='FinalReserve'):
    state,history,source=fixture();status,state=m.fund(state,history,source,'A1',1,grants(amount,bucket));return state,history,source


def summary(m,state,source,allocation='A1',bucket='FinalReserve'):
    row=state['allocations'][wire.encode(tuple(source[:3])+(allocation,))]['buckets'][bucket]
    return dict(grant=view(row['OriginalGrant']),consumed=view(row['Consumed']),reserved=view(row['Reserved']),free=view(row['RemainingFree']),revision=state['revision'])


def no_change(status,state,before):return dict(status=status,unchanged=view(state,True)==view(before,True),revision=state['revision'])


def deny_operation(m,kind='CONSUME_FREE',amount='51',intent='I1',purpose='CatchUp',bucket='FinalReserve'):
    s,h,k=funded(m);before=copy.deepcopy(s);status,out=m.operate(s,h,k,'A1',2,kind,bucket,Decimal(amount),intent,purpose)
    return dict(status=status,stateUnchanged=view(out,True)==view(before,True),inputsUnchanged=view(s,True)==view(before,True))


def reserve_cycle(m):
    s,h,k=funded(m)
    statuses=[]
    for event,kind,amount in [(2,'CONSUME_FREE','10'),(3,'RESERVE','15'),(4,'CONSUME_RESERVED','5'),(5,'RELEASE','5')]:
        status,s=m.operate(s,h,k,'A1',event,kind,'FinalReserve',Decimal(amount));statuses.append(status)
    return dict(statuses=statuses,balance=summary(m,s,k))


def split_funding(m):
    s,h,k=fixture();first,s=m.fund(s,h,k,'A1',1,grants('25'),False)
    before=copy.deepcopy(s);blocked,ss=m.operate(s,h,k,'A1',3,'CONSUME_FREE','FinalReserve',Decimal(1))
    second,s=m.fund(s,h,k,'A2',2,grants('25'),True)
    available=m.reserve_available(s,h,k[:3])
    return dict(first=first,preparedBlocked=blocked,preparedUnchanged=view(ss,True)==view(before,True),second=second,available=view(available),sourceGrant=view(s['sources'][wire.encode(k)]['granted']))


def overfund(m):
    s,h,k=fixture();_,s=m.fund(s,h,k,'A1',1,grants('40'),False);before=copy.deepcopy(s);status,out=m.fund(s,h,k,'A2',2,grants('20'),False)
    return dict(status=status,unchanged=view(out,True)==view(before,True),revision=out['revision'])


def identity_fixture():
    s,h,k=fixture();r=h[wire.encode(k)];context=dict(Plan=10,Revision=2,Snapshot=3,fresh=True);allocation=dict(source=k,PolicyVersion=1,allocationEvent=1)
    expected=copy.deepcopy(r['identity']);expected.update(Plan=10,Revision=2,Snapshot=3)
    return h,k,context,allocation,expected


def restart_case(m,kind):
    s,h,k=funded(m);prior=m.snapshot(s);_,after=m.operate(s,h,k,'A1',2,'CONSUME_FREE','FinalReserve',Decimal(10));latest=m.snapshot(after)
    if kind=='before':out=m.recover(prior,None,s['events'],h)
    elif kind=='prepared':out=m.recover(prior,None,dict(s['events'],PENDING=dict(sequence=99,payload={},digest='unknown')),h)
    elif kind=='committed':out=m.recover(latest,prior,after['events'],h)
    elif kind=='incomplete':out=m.recover(latest,prior,None,h)
    elif kind=='history-missing':out=m.recover(latest,prior,after['events'],None)
    elif kind=='torn':latest['checksum']='0'*64;out=m.recover(latest,prior,after['events'],h)
    elif kind=='fallback':latest['checksum']='0'*64;out=m.recover(latest,prior,s['events'],h)
    elif kind=='forged-consumed':
        row=latest['payload']['allocations'][wire.encode(tuple(k[:3])+('A1',))]['buckets']['FinalReserve'];row['Consumed']=Decimal(0);row['RemainingFree']=Decimal(50);latest['checksum']=m.digest(latest['payload']);out=m.recover(latest,None,after['events'],h)
    else:raise ValueError(kind)
    result=dict(status=out['status'],fallback=out['fallbackUsed'],remaining=None,replay=None)
    if out['state'] is not None:
        result['remaining']=summary(m,out['state'],k)['free']
        if kind=='committed':result['replay']=m.operate(out['state'],h,k,'A1',2,'CONSUME_FREE','FinalReserve',Decimal(10),revision=2)[0]
    return result


def arithmetic_boundary(m,operation,a,b):
    try:return dict(status='VALUE',value=getattr(m,operation)(a,b))
    except m.Unsupported:return dict(status='UNAVAILABLE',value=None)


def cases():
    out=[]
    def add(cid,req,fn,want,classes=('Positive',),predicates=1):out.append(dict(TestID=cid,RequirementID=req,run=fn,Expected=want,Classes=list(classes),predicates=predicates,Input=dict(Fixture='record50/source(B1,S1,1,11); explicit literals in named scenario',Scenario=cid,Source='Tests/Static/check_hsbi_02b_r0e_contracts.py#cases')))
    add('D01-equivalent-fields','D-01',lambda m:view(m.legacy_view('50','10','15','40')),dict(OriginalGrant=N('50'),Consumed=N('10'),Reserved=N('15'),RemainingGross=N('40'),RemainingFree=N('25'),Available=N('25'),SpendAuthorization='UNAVAILABLE_WITHOUT_OWNER_PROVENANCE'),('Positive','Conservation'),7)
    add('D01-double-count','D-01',lambda m:m.balance('50','10','15','40'),False,('Negative','Conservation'))
    add('D01-zero-reserved','D-01',lambda m:m.balance('50','0','0','50'),True,('Positive','Conservation'))
    add('D01-control','D-01',lambda m:m.balance('50','10','15','25'),True,('Positive','Conservation'))
    add('D01-operations','D-01',reserve_cycle,dict(statuses=['COMMITTED_IN_MEMORY']*4,balance=dict(grant=N('50'),consumed=N('15'),reserved=N('5'),free=N('30'),revision=6)),('Positive','Conservation'),6)
    def wrong_owner(m):
        s,h,k=funded(m);_,s=m.operate(s,h,k,'A1',2,'RESERVE','FinalReserve',Decimal(15),intent='OWNER');before=copy.deepcopy(s);status,x=m.operate(s,h,k,'A1',3,'CONSUME_RESERVED','FinalReserve',Decimal(5),intent='FOREIGN');return no_change(status,x,before)
    add('D01-reservation-owner','D-01',wrong_owner,dict(status='REJECT',unchanged=True,revision=3),('Negative','Identity conflict'),3)
    add('D01-negative-consumption','D-01',lambda m:deny_operation(m,amount='-10'),dict(status='REJECT',stateUnchanged=True,inputsUnchanged=True),('Negative','Boundary'),3)
    add('D01-prepared-and-split','FUNDING-SOURCE-CAP',split_funding,dict(first='COMMITTED_IN_MEMORY',preparedBlocked='REJECT',preparedUnchanged=True,second='COMMITTED_IN_MEMORY',available=['KNOWN_MODEL_AVAILABLE',N('50')],sourceGrant=N('50')),('Positive','Cross-allocation','Conservation'),6)
    add('D07-overfund-prepared','FUNDING-SOURCE-CAP',overfund,dict(status='REJECT',unchanged=True,revision=2),('Negative','Cross-allocation'),3)
    def double(m):
        s,h,k=funded(m);before=copy.deepcopy(s);status,x=m.fund(s,h,k,'A2',2,grants());return no_change(status,x,before)
    add('D07-double-allocation','FUNDING-SOURCE-CAP',double,dict(status='REJECT',unchanged=True,revision=2),('Negative','Cross-allocation'),3)
    def replay(m,changed=False):
        s,h,k=funded(m);before=copy.deepcopy(s);g=grants();
        if changed:g=grants('50','PartialFar')
        status,x=m.fund(s,h,k,'A1',1,g);return no_change(status,x,before)
    add('D07-exact-fund-replay','D-07',lambda m:replay(m),dict(status='NO_OP',unchanged=True,revision=2),('Positive','Duplicate/replay'),3)
    add('D07-altered-fund-replay','D-07',lambda m:replay(m,True),dict(status='CONFLICT',unchanged=True,revision=2),('Negative','Duplicate/replay'),3)
    def op_replay(m,changed=False):
        s,h,k=funded(m);_,s=m.operate(s,h,k,'A1',2,'CONSUME_FREE','FinalReserve',Decimal(10));before=copy.deepcopy(s);status,x=m.operate(s,h,k,'A1',2,'CONSUME_FREE','FinalReserve',Decimal(11 if changed else 10),revision=2);return no_change(status,x,before)
    add('D07-exact-consume-replay','D-07',lambda m:op_replay(m),dict(status='NO_OP',unchanged=True,revision=3),('Positive','Duplicate/replay'),3)
    add('D07-altered-consume-replay','D-07',lambda m:op_replay(m,True),dict(status='CONFLICT',unchanged=True,revision=3),('Negative','Duplicate/replay'),3)
    add('D02-known-zero','D-02',lambda m:view(m.reserve_available(fixture()[0],{},('B1','S1',1))),['KNOWN_MODEL_AVAILABLE',N('0')],('Positive',),2)
    add('D02-unknown-history','D-02',lambda m:view(m.reserve_available(fixture()[0],None,('B1','S1',1))),['UNAVAILABLE',None],('Negative',),2)
    def projected(m):
        s,h,k=fixture();h[wire.encode(k)]['kind']='ProjectedBasketNet';h[wire.encode(k)]['profit']=Decimal(100);h[wire.encode(k)]['rawNet']=Decimal(100);h[wire.encode(k)]['postedNet']=Decimal(100)
        status,x=m.fund(s,h,k,'A1',1,grants('100'));return dict(status=status,allocations=len(x['allocations']))
    add('D02-projected-not-source','D-02',projected,dict(status='REJECT',allocations=0),('Negative',),2)
    def small(m):
        s,h,k=fixture();h[wire.encode(k)]=record('10','Small');reject,_=m.fund(s,h,k,'BAD',1,grants('10'));ok,s=m.fund(s,h,k,'A1',2,grants('10','ResidualHeld'));return dict(reserveAttempt=reject,residualCommit=ok,available=view(m.reserve_available(s,h,k[:3])))
    add('D03-small-isolation','D-03',small,dict(reserveAttempt='REJECT',residualCommit='COMMITTED_IN_MEMORY',available=['KNOWN_MODEL_AVAILABLE',N('0')]),('Positive','Negative'),3)
    def opening(m):
        s,h,k=fixture();h[wire.encode(k)]['entry']='OPEN';return m.fund(s,h,k,'A1',1,grants())[0]
    add('D03-opening-no-grant','D-03',opening,'REJECT',('Negative',))
    def debit(m):
        s,h,k=funded(m);d=record('-20','Small',deal=99);h[wire.encode(('B1','S1',1,99))]=d;before=copy.deepcopy(s);status,x=m.operate(s,h,k,'A1',2,'CONSUME_FREE','FinalReserve',Decimal(10));return dict(available=view(m.reserve_available(s,h,k[:3])),spend=status,unchanged=view(x,True)==view(before,True))
    add('D07-unattributed-debit','FUNDING-GLOBAL-ATTRIBUTION',debit,dict(available=['UNPROVEN',None],spend='UNAVAILABLE',unchanged=True),('Negative','Conservation'),3)
    add('D04-absolute-baseline','D-04',lambda m:view(m.far_loss('-50',dict(absolute='40',basis='OLD',fresh=True),'OLD')),dict(absolute=N('50'),incremental=N('10'),incrementalStatus='DIAGNOSTIC_ONLY',workingMetric='ABSOLUTE_PROPOSED'),('Positive',),4)
    for reason,base,basis in [('partial-volume',dict(absolute='40',basis='OLD',fresh=True),'NEW_VOLUME'),('stale',dict(absolute='40',basis='OLD',fresh=False),'OLD'),('restart',None,'OLD')]:
        add('D04-'+reason,'D-04',lambda m,b=base,c=basis:view(m.far_loss('-50',b,c)),dict(absolute=N('50'),incremental=None,incrementalStatus='UNAVAILABLE',workingMetric='ABSOLUTE_PROPOSED'),('Negative','Boundary'),4)
    # Fixture close-now quote side; broker calculation itself remains NOT_RUN.
    add('D04-buy-bid-sell-ask','D-04',lambda m:(m.close_side('BUY'),m.close_side('SELL')),('Bid','Ask'),('Positive',),2)
    f1=dict(source=('B1','S1',1,101),volume='0.4',net='-5');f2=dict(source=('B1','S1',1,102),volume='0.6',net='-10')
    hist={f1['source']:f1,f2['source']:f2}
    add('D05-partial-pending','D-05',lambda m:view(m.transition_status([f1],hist,'1','12')),['PENDING',N('5')],('Positive','Partial fills'),2)
    add('D05-over-cap','D-05',lambda m:view(m.transition_status([f1,f2],hist,'1','12')),['OVER_CAP',N('15')],('Negative','Partial fills'),2)
    add('D05-exact-fill-replay','D-05',lambda m:view(m.transition_status([f1,f1],hist,'1','12')),['PENDING',N('5')],('Positive','Duplicate/replay'),2)
    add('D05-changed-fill','D-05',lambda m:view(m.transition_status([f1,dict(f1,net='-6')],hist,'1','12')),['CONFLICT',None],('Negative','Identity conflict'),2)
    add('D05-actual-history-unavailable','D-05',lambda m:view(m.transition_status([f1],None,'1','12')),['UNAVAILABLE',None],('Negative',),2)
    basis={'COMMISSION':dict(RiskBasis='brokerCommission',Window='deal11',AlreadyIncluded=True,OverlapKnown=True),'EXEC':dict(RiskBasis='executionUncertainty',Window='intent1',AlreadyIncluded=False,OverlapKnown=True)}
    costs=[dict(CostID='COMMISSION',RiskBasis='brokerCommission',Window='deal11',AlreadyIncluded=True,AdditionalDeduction=False),dict(CostID='EXEC',RiskBasis='executionUncertainty',Window='intent1',AlreadyIncluded=False,AdditionalDeduction=True)]
    add('D06-once','D-06',lambda m:m.costs_status(costs,basis),'PASS',('Positive',))
    add('D06-double-cost','D-06',lambda m:m.costs_status([dict(costs[0],AdditionalDeduction=True)],basis),'CONFLICT',('Negative',))
    add('D06-unknown-overlap','D-06',lambda m:m.costs_status(costs,dict(basis,EXEC=dict(basis['EXEC'],OverlapKnown=None))),'UNPROVEN',('Negative',))
    def identity(m,changed=None):
        h,k,c,a,p=identity_fixture()
        if changed:p[changed]=999 if type(p[changed]) is int else 'FOREIGN'
        return m.verify_identity(p,h,k,c,a)
    add('D08-independent-control','D-08',identity,'PASS',('Positive',))
    for field in model.IDENTITY:add('D08-foreign-'+field,'D-08',lambda m,f=field:identity(m,f),'REJECT',('Negative','Identity conflict'))
    def absent(m):
        h,k,c,a,p=identity_fixture();return m.verify_identity(p,{},k,c,a)
    add('D08-nonzero-deal-not-existence','D-08',absent,'REJECT',('Negative',))
    def foreign_allocation(m):
        h,k,c,a,p=identity_fixture();a['source']=('B1','S1',1,999);return m.verify_identity(p,h,k,c,a)
    add('D08-foreign-authoritative-allocation','D-08',foreign_allocation,'REJECT',('Negative','Cross-allocation'))
    def stale(m):
        h,k,c,a,p=identity_fixture();c['fresh']=False;return m.verify_identity(p,h,k,c,a)
    add('D08-stale-snapshot','SNAP-FIXTURE-1',stale,'UNAVAILABLE',('Negative','Snapshot mismatch'))
    for kind,status,remaining,fallback,replay_status in [('before','RECONCILED_MODEL_ONLY','50',False,None),('prepared','UNAVAILABLE',None,False,None),('committed','RECONCILED_MODEL_ONLY','40',False,'NO_OP'),('incomplete','UNAVAILABLE',None,False,None),('history-missing','UNAVAILABLE',None,False,None),('torn','UNAVAILABLE',None,True,None),('fallback','RECONCILED_MODEL_ONLY','50',True,None),('forged-consumed','CONFLICT',None,False,None)]:
        add('RESTART-'+kind,'D-07',lambda m,k=kind:restart_case(m,k),dict(status=status,fallback=fallback,remaining=N(remaining) if remaining is not None else None,replay=replay_status),('Restart model','Boundary'),4)
    level=wire.levels('50','20','1');level[1]['available']='5'
    add('CR09-A-negative','CR-09',lambda m:view(m.assess_levels(level,[1,2])),['REJECT',2,N('-16')],('Negative','Worst-case selection'),3)
    add('CR09-B-single','CR-09',lambda m:view(m.assess_levels(level,[1,2],'B')),['SINGLE_LEVEL_POSITIVE',1,N('29')],('Positive','Worst-case selection'),3)
    add('NUM-exact-cancellation','NUM-EXACT-1',lambda m:view(m.assess_levels(wire.levels('1e28','.010','9999999999999999999999999999.995'),[1,2])),['REJECT',1,N('-.005')],('Boundary','Precision/rounding'),3)
    add('NUM-minor-remainder','NUM-EXACT-1',lambda m:view(m.exact.allocate('.01',['.5','.5','0','0'],2)),dict(zip(model.BUCKETS,[N('0')]*4+[N('.01')])),('Boundary','Conservation'),5)
    add('NUM-double-round','NUM-EXACT-1',lambda m:view((m.exact.candidate_round('1.2451',2),m.exact.candidate_round(m.exact.candidate_round('1.2451',3),2))),[N('1.25'),N('1.24')],('Boundary','Precision/rounding'),2)
    add('NUM-domain-unsupported','NUM-DOMAIN-1',lambda m:arithmetic_boundary(m,'checked_add',2**63-1,1),dict(status='UNAVAILABLE',value=None),('Boundary',),2)
    for label,fn,a,b,want in [('add-ok','checked_add',2**63-2,1,2**63-1),('add-min','checked_add',-(2**63),0,-(2**63)),('add-underflow','checked_add',-(2**63),-1,None),('mul-ok','checked_mul',-(2**63),1,-(2**63)),('mul-overflow','checked_mul',-(2**63),-1,None),('mul-positive','checked_mul',2**62,2,None),('operand-domain','checked_add',2**64,-(2**64),None)]:
        add('MQL-'+label,'MQL-DOMAIN',lambda m,f=fn,a=a,b=b:arithmetic_boundary(m,f,a,b),dict(status='VALUE' if want is not None else 'UNAVAILABLE',value=want),('Boundary',),2)
    add('CODEC-str-decimal','NUM-CODEC',lambda m:m.canonical('1')!=m.canonical(Decimal(1)),True,('Positive',))
    add('ZERO-core','CR-09',lambda m:m.exact.geometry('.1','.01','3','.1','.01','100','.01')['status'],'REJECT',('Negative','Zero-Core'))
    def changed_source(m,field):
        s,h,k=funded(m);h[wire.encode(k)]['identity'][field]+=1;before=copy.deepcopy(s)
        status,out=m.fund(s,h,k,'A2',3,grants('0'))
        return no_change(status,out,before)
    for field in ('Magic','Cycle'):
        add('SOURCE-changed-'+field,'FUNDING-SOURCE-CAP',lambda m,f=field:changed_source(m,f),dict(status='CONFLICT',unchanged=True,revision=2),('Negative','Cross-allocation'),3)
    for net in ('0','-10'):
        def no_gain(m,net=net):
            s,h,k=fixture();h[wire.encode(k)]=record(net);before=copy.deepcopy(s);status,out=m.fund(s,h,k,'A1',1,grants('1'))
            return no_change(status,out,before)
        add('SOURCE-nonpositive-'+net,'D-01',no_gain,dict(status='REJECT',unchanged=True,revision=1),('Negative','Conservation'),3)
    def mixed_currency(m):
        s,h,k=funded(m);k2=('B1','S1',1,22);r=record('50',deal=22);r['currency']='EUR';h[wire.encode(k2)]=r
        _,s=m.fund(s,h,k2,'A2',2,grants());return view(m.reserve_available(s,h,k[:3]))
    add('NUM-currency-mismatch','NUM-DOMAIN-1',mixed_currency,['UNAVAILABLE',None],('Negative',),2)
    add('D01-finalreserve-purpose','D-01',lambda m:deny_operation(m,amount='1',purpose='PartialFar'),dict(status='REJECT',stateUnchanged=True,inputsUnchanged=True),('Negative',),3)
    add('D04-direction-unknown','D-04',lambda m:invalid_direction(m),'REJECT',('Negative',))
    def level_case(m,change,variant='A'):
        levels=wire.levels('50','20','1')
        if change=='missing':levels.pop()
        elif change=='duplicate':levels[1]['id']=1
        elif change=='unknown-transition':levels[0]['transitionLoss']=None
        elif change=='stale':levels[1]['snapshotFresh']=False
        elif change=='zero':levels[1]['available']='21'
        return view(m.assess_levels(levels,[1,2],variant))
    for change,want in [('missing',['UNPROVEN',None,None]),('duplicate',['UNPROVEN',None,None]),('unknown-transition',['UNAVAILABLE',None,None]),('stale',['UNPROVEN',None,None]),('zero',['REJECT',2,N('0')])]:
        add('CR09-'+change,'CR-09',lambda m,c=change:level_case(m,c),want,('Negative','Worst-case selection'),3)
    def seq(m):
        x=m.exact.sequential('50',['30','30']);return dict(status=x['status'],remaining=view(x['remaining']),appliedCount=x['appliedCount'],rejectedIndex=x['rejectedIndex'])
    add('CR09-sequential-reuse','CR-09',seq,dict(status='REJECT',remaining=N('20'),appliedCount=1,rejectedIndex=2),('Negative','Conservation'),4)
    def namespace(m):
        s,h,k=funded(m);other=('B1','S1',2,11);h[wire.encode(other)]=record(account=2)
        status,s=m.fund(s,h,other,'A1',2,grants());return dict(status=status,one=view(m.reserve_available(s,h,k[:3])),two=view(m.reserve_available(s,h,other[:3])),sources=len(s['sources']))
    add('D08-independent-account-namespace','D-08',namespace,dict(status='COMMITTED_IN_MEMORY',one=['KNOWN_MODEL_AVAILABLE',N('50')],two=['KNOWN_MODEL_AVAILABLE',N('50')],sources=2),('Positive','Cross-allocation'),4)
    def changed_components(m):
        s,h,k=funded(m);h[wire.encode(k)]['profit']=Decimal('60');h[wire.encode(k)]['commission']=Decimal('-10');before=copy.deepcopy(s)
        status,out=m.fund(s,h,k,'A2',3,grants('0'));return no_change(status,out,before)
    add('L01-same-net-changed-components','D-08',changed_components,dict(status='CONFLICT',unchanged=True,revision=2),('Negative','Identity conflict'),3)
    def unsupported_batch(m):
        fills=[dict(source=('B1','S1',1,i),volume='1',net='-9e64') for i in (101,102)]
        return view(m.transition_status(fills,{f['source']:f for f in fills},'2','1e64'))
    add('D05-unsupported-aggregate','NUM-DOMAIN-1',unsupported_batch,['UNAVAILABLE',None],('Boundary','Partial fills'),2)
    return out


def invalid_direction(m):
    try:m.close_side('UNKNOWN');return 'ACCEPTED'
    except m.Malformed:return 'REJECT'


def run(m=model):
    scenarios=cases();rows=[];configs=wire.contexts()
    for index,c in enumerate(configs):
        for t in scenarios:
            with localcontext(c) as active:
                before=wire.context_state(active)
                try:
                    actual=t['run'](m);unchanged=wire.context_state(active)==before
                    rows.append(dict(TestID=t['TestID'],RequirementID=t['RequirementID'],context=index,Classes=t['Classes'],Input=t['Input'],Expected=t['Expected'],IndependentExpected=t['Expected'],Actual=actual,Result='PASS' if actual==t['Expected'] and unchanged else 'FAIL',ContextUnchanged=unchanged,predicates=2,Evidence='Tests/Evidence/NEXT_STAGE_02B_R0E_VERIFICATION_SUMMARY.json#'+t['TestID'],ProofBoundary='PROPOSED independent fixture model only; no broker/durable runtime'))
                except Exception as e:rows.append(dict(TestID=t['TestID'],RequirementID=t['RequirementID'],context=index,Result='INFRASTRUCTURE_ERROR',errorType=type(e).__name__,message=str(e),predicates=2))
    return dict(scenarios=len(scenarios),contextConfigurations=[wire.context_state(c) for c in configs],executions=len(rows),predicates=sum(r['predicates'] for r in rows),passed=sum(r['Result']=='PASS' for r in rows),failed=sum(r['Result']=='FAIL' for r in rows),infrastructureErrors=sum(r['Result']=='INFRASTRUCTURE_ERROR' for r in rows),tests=rows)


def metadata():return dict(BaseSHA='2d34c3378edc5f2df064282fa067bb4af2a1e3b0',TestedSHA=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),UTC=datetime.now(timezone.utc).isoformat(),ApprovalStatus='AWAITING_ADMIN_APPROVAL',MQL5_COMPILE='NOT_RUN',MQL5_TESTS='NOT_RUN',STRATEGY_TESTER='NOT_RUN')


def save(path,data):
    path=Path(path).resolve();assert path.is_relative_to(ROOT) and 'R0E' in path.name
    path.write_text(json.dumps(view(data),ensure_ascii=False,indent=2)+'\n')


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',default='Tests/Evidence/NEXT_STAGE_02B_R0E_VERIFICATION_SUMMARY.json');a=p.parse_args();start=metadata()['UTC'];out=dict(metadata(),**run());out.update(Command=[sys.executable,*sys.argv],StartedUtc=start,FinishedUtc=metadata()['UTC'],SourceHashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (Path(__file__).resolve(),Path(model.__file__),Path(model.exact.__file__),Path(wire.__file__))});out['ExitCode']=int(out['failed']+out['infrastructureErrors']>0);save(a.output,out)
    print(json.dumps({k:v for k,v in out.items() if k not in ('tests','contextConfigurations')}))
    for r in out['tests']:
        if r['Result']!='PASS':print(r)
    return out['ExitCode']


if __name__=='__main__':raise SystemExit(main())
