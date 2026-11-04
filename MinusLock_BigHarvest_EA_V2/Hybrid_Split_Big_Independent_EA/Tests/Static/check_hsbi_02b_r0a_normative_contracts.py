#!/usr/bin/env python3
"""Independent executable checks of PROPOSED R0A contracts, not production fixes."""
import argparse
import ast
import copy
from datetime import datetime, timezone
from decimal import Decimal
import hashlib
import json
from pathlib import Path
import runpy
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'Tests/Reference'))
import hsbi_02b_r0a_normative_model as m


def fixtures():
    owner=dict(broker='B1',server='S1',account=1)
    record=dict(owner=owner,deal=11,event=21,order=12,position=13,magic=7,symbol='EURUSD',
                cycle=1,plan=1,action=1,role='BigCore',direction='BUY',entry='CLOSE',
                profit=m.dec('55'),swap=m.dec('0'),commission=m.dec('-5'),fee=m.dec('0'),rawNet=m.dec('50'))
    history={m.source_key(record):copy.deepcopy(record)}
    actual=m.Money(m.dec('50'),'USD',2,'ReconciledEconomicNet')
    grant=m.allocate(actual,['1','0','0','0'])
    zero=dict.fromkeys(m.BUCKETS,Decimal(0))
    state=dict(owner=owner,source=m.source_key(record),allocation='A1',allocationEvent=31,policy=1,
               currency='USD',phase='COMMITTED',net=m.dec('50'),revision=1,grant=grant,
               remaining=copy.deepcopy(grant),consumed=zero.copy(),reserved=zero.copy())
    authority=dict(owner=owner,complete=True,fresh=True,revision=1,plan=1,cycle=1)
    request={k:copy.deepcopy(state[k]) for k in ('owner','source','allocation','allocationEvent','policy','currency')}
    request.update(event=41,plan=1,cycle=1,revision=1,bucket='FinalReserve',purpose='CatchUp',amount=m.dec('10'))
    context=dict(owner=owner,symbol='EURUSD',magic=7,plan=1,cycle=1,revision=1,snapshot=1,fresh=True,currency='USD')
    identity={k:copy.deepcopy(record[k]) for k in ('owner','symbol','magic','deal','event','position','role','direction','cycle','action')}
    identity.update({k:context[k] for k in ('plan','revision','snapshot')})
    proof=dict(identity=identity,net=m.dec('50'),digest=m.digest(dict(record=record,grant=grant,context=context)))
    return record,history,state,authority,request,context,proof


def reject(fn):
    try:fn()
    except ValueError:return 'REJECT'
    return 'ACCEPTED'


def tests():
    rows=[]
    def check(cid,contract,actual,expected):
        rows.append(dict(id=cid,contract=contract,actual=actual,expected=expected,
                         result='PASS' if actual==expected else 'FAIL',normativeStatus='PROPOSED_CONTRACT'))
    r,h,s,a,q,c,p=fixtures()
    check('D01-signed-net','D-01',m.reconciled_net(r,h,r['owner'])[1].value,Decimal(50))
    broken=copy.deepcopy(r);broken['profit']=Decimal(56)
    check('D01-components-sum-mismatch','D-01',m.reconciled_net(broken,{m.source_key(broken):broken},r['owner'])[0],'CONFLICT')
    opening=dict(r,entry='OPEN')
    check('D03-opening-no-grant-source','D-03',m.reconciled_net(opening,{m.source_key(opening):opening},r['owner'])[0],'REJECT')
    for value,want in [('-15','0'),('0','0'),('1.005','1.00'),('1.015','1.02')]:
        amt=m.Money(m.dec(value).quantize(m.quantum(2),rounding=m.ROUND_HALF_EVEN),'USD',2,'ReconciledEconomicNet')
        check('D01-allocatable-'+value,'D-01',sum(m.allocate(amt,['.5','.25','.1','.1']).values()),m.dec(want))
    small=m.allocate(m.Money(m.dec('.01'),'USD',2,'ReconciledEconomicNet'),['.5','.5','0','0'])
    check('D01-rounding-residual','D-01',tuple(small.values()),tuple(map(Decimal,['0','0','0','0','.01'])))
    check('D01-valid-balance','D-01',m.valid_balance(s['net'],s['grant'],s['remaining'],s['consumed'],s['reserved']),True)
    z=copy.deepcopy(s);z['consumed']['FinalReserve']=Decimal(1)
    check('D01-no-double-count','D-01',m.valid_balance(z['net'],z['grant'],z['remaining'],z['consumed'],z['reserved']),False)
    z=copy.deepcopy(s);z['grant']['FinalReserve']=Decimal(40);z['remaining']['FinalReserve']=Decimal(40)
    check('D01-partial-committed','D-01',m.valid_balance(z['net'],z['grant'],z['remaining'],z['consumed'],z['reserved'],'10'),False)
    check('D01-partial-prepared','D-01',m.valid_balance(z['net'],z['grant'],z['remaining'],z['consumed'],z['reserved'],'10','PREPARED'),True)
    z['phase']='PREPARED';check('D01-prepared-no-consume','D-01',m.authorize(q,z,{},a),'REJECT')
    z=copy.deepcopy(s);z['reserved']['FinalReserve']=Decimal(51)
    check('D01-negative-available','D-01',m.valid_balance(z['net'],z['grant'],z['remaining'],z['consumed'],z['reserved']),False)
    z=copy.deepcopy(s);del z['consumed']['Carry']
    check('D01-missing-bucket','D-01',m.valid_balance(z['net'],z['grant'],z['remaining'],z['consumed'],z['reserved']),False)
    for kind in ('ProjectedBasketNet','ProjectedCloseNowNet','ActualRealizedDealNet','AllocationGrant','AvailableReserve'):
        amt=m.Money(Decimal(100),'USD',2,kind)
        check('D02-no-implicit-'+kind,'D-02',reject(lambda:m.allocate(amt,['1','0','0','0'])),'REJECT')
    check('D02-history-missing','D-02',m.reconciled_net(r,None,r['owner'])[0],'UNAVAILABLE')
    check('D02-no-confirmed-closes','D-02',m.reconciled_net(r,{},r['owner'])[0],'REJECT')
    check('D02-projected100-available0','D-02',sum(m.allocate(m.Money(Decimal(0),'USD',2,'ReconciledEconomicNet'),['1','0','0','0']).values()),Decimal(0))
    sg=m.allocate(m.Money(Decimal(10),'USD',2,'ReconciledEconomicNet'),['1','0','0','0'],'Small')
    check('D03-small-not-reserve','D-03',sg['FinalReserve'],Decimal(0))
    check('D03-small-not-lost','D-03',sg['ResidualHeld'],Decimal(10))
    for role in ('BigCore','BigTrend'):
        check('D03-role-'+role,'D-03',m.allocate(m.Money(Decimal(10),'USD',2,'ReconciledEconomicNet'),['1','0','0','0'],role)['FinalReserve'],Decimal(10))
    for value in (float('nan'),float('inf'),'NaN','Infinity',True):
        check('FINITE-'+str(value),'D-01',reject(lambda:m.dec(value)),'REJECT')
    for reserve,want in [('20',('-35','5')),('60',('5','45'))]:
        absolute,increment=m.far_loss('-50','40')
        check('D04-margins-'+reserve,'D-04',(m.dec(reserve)-absolute-5,m.dec(reserve)-increment-5),tuple(map(Decimal,want)))
    check('D04-missing-baseline','D-04',m.far_loss('-50')[1],None)
    check('D04-stale-baseline','D-04',m.far_loss('-50','40',False)[1],None)
    check('D04-baseline-unneeded-absolute','D-04',m.far_loss('-50')[0],Decimal(50))
    check('D04-loss-decrease','D-04',m.far_loss('-30','40'),(Decimal(30),Decimal(0)))
    check('D04-BUY-Bid-cost','D-04',m.close_now_net('BUY','100','90','92','1','-2'),Decimal(-12))
    check('D04-SELL-Ask-cost','D-04',m.close_now_net('SELL','100','108','110','1','-2'),Decimal(-12))
    # Baseline validity must bind all these dimensions; no silent reuse after mutation.
    baseline=dict(side='SELL',volume='1',cycle=1,plan=1,revision=1,snapshot=1,costVersion=1)
    check('D04-baseline-control','D-04',m.baseline_binding(baseline,baseline),True)
    for key in baseline:
        altered=dict(baseline);altered[key]='FOREIGN'
        check('D04-baseline-binding-'+key,'D-04',m.far_loss('-50','40',m.baseline_binding(altered,baseline))[1],None)
    check('D04-restart-not-restored','D-04',m.baseline_binding(baseline,baseline,restored=False),False)
    partial_net=m.close_now_net('SELL','100','108','110','.5','-1')
    check('D04-partial-close-rebase','D-04',m.far_loss(partial_net,'12',m.baseline_binding(dict(baseline,volume='.5'),baseline)),(Decimal(6),None))
    deal=dict(id=1,confirmed=True,profit='-13',swap='-1',commission='-1',fee='0')
    check('D05-overcap','D-05',m.transition([deal],True,'12'),('SAFE_BLOCKED',Decimal(15)))
    actual_loss=m.transition([deal],True,'12')[1]
    check('D05-slippage-diagnostic-only','D-05',(actual_loss,actual_loss-Decimal(10)),(Decimal(15),Decimal(5)))
    check('D05-partial-overcap','D-05',m.transition([deal],False,'12'),('SAFE_BLOCKED',Decimal(15)))
    less=dict(deal,profit='-8')
    check('D05-partial-under-cap','D-05',m.transition([less],False,'12'),('PENDING',Decimal(10)))
    check('D05-complete-under-cap','D-05',m.transition([less],True,'12'),('RECONCILED',Decimal(10)))
    check('D05-duplicate-fill','D-05',m.transition([deal,deal],True,'12')[0],'CONFLICT')
    check('D05-unconfirmed-fill','D-05',m.transition([dict(deal,confirmed=False)],True,'12')[0],'UNAVAILABLE')
    item=dict(value='1',currency='USD',riskBasis='leg1',window='W1',alreadyIncludedInNet=False,policyVersion=1)
    four=[dict(item,riskBasis='leg'+str(i)) for i in range(4)]
    check('D06-independent-five','D-06',m.buffer_total(four+[dict(item,riskBasis='CatchUpRisk')]),('VALID',Decimal(5)))
    check('D06-overlap-not-silent','D-06',m.buffer_total(four+[dict(item,riskBasis='leg0')])[0],'CONFLICT')
    check('D06-already-in-net','D-06',m.buffer_total([dict(item,alreadyIncludedInNet=True)]),('VALID',Decimal(0)))
    check('D06-currency','D-06',m.buffer_total([dict(item,currency='EUR')])[0],'UNAVAILABLE')
    check('D06-negative','D-06',m.buffer_total([dict(item,value='-1')])[0],'REJECT')
    check('D07-eligible-not-commit','D-07',m.authorize(q,s,{},a),'ELIGIBLE_FOR_COMMIT')
    check('D07-no-mutation-on-eligibility','D-07',s['remaining']['FinalReserve'],Decimal(50))
    status,ss,jj,aa=m.apply_for_test(q,s,{},a)
    check('D07-first10','D-07',(status,ss['remaining']['FinalReserve']),('COMMITTED_IN_MEMORY',Decimal(40)))
    no,ss2,jj2,aa2=m.apply_for_test(q,ss,jj,aa)
    check('D07-exact-noop','D-07',(no,ss2,jj2,aa2),('NO_OP',ss,jj,aa))
    check('D07-altered11','D-07',m.authorize(dict(q,amount=Decimal(11)),ss,jj,aa),'CONFLICT')
    check('D07-next41','D-07',m.authorize(dict(q,event=42,revision=2,amount=Decimal(41)),ss,jj,aa),'REJECT')
    full_request=dict(q,event=42,revision=2,amount=Decimal(40))
    full,fs,fj,fa=m.apply_for_test(full_request,ss,jj,aa)
    check('D07-full-consumption','D-07',(full,fs['remaining']['FinalReserve'],fs['consumed']['FinalReserve']),('COMMITTED_IN_MEMORY',Decimal(0),Decimal(50)))
    check('D07-full-replay-noop','D-07',m.authorize(full_request,fs,fj,fa),'NO_OP')
    check('D07-spent-bucket-new-event','D-07',m.authorize(dict(q,event=43,revision=3,amount=Decimal(1)),fs,fj,fa),'REJECT')
    check('D07-missing-registry','D-07',m.authorize(q,s,None,a),'UNAVAILABLE')
    check('D07-reserved-not-available','D-07',m.authorize(dict(q,amount=Decimal(41)),dict(s,reserved=dict(s['reserved'],FinalReserve=Decimal(10))),{},a),'REJECT')
    for field,value in [('plan',999),('revision',999),('cycle',999),('policy',999),('allocationEvent',999),('source',('FOREIGN',))]:
        check('D07-binding-'+field,'D-07',m.authorize(dict(q,**{field:value}),s,{},a),'REJECT')
    check('D08-proof-control','D-08',m.verify_proof(p,r,s,h,c),'VERIFIED')
    check('D08-missing-history','D-08',m.verify_proof(p,r,s,None,c),'UNAVAILABLE')
    check('D08-authority-stale','D-08',m.authorize(q,s,{},dict(a,fresh=False)),'UNAVAILABLE')
    check('D08-authority-incomplete','D-08',m.authorize(q,s,{},dict(a,complete=False)),'UNAVAILABLE')
    check('D08-invented-deal','D-08',m.verify_proof(p,r,s,{},c),'REJECT')
    for key in ('broker','server','account'):
        rr=copy.deepcopy(r);rr['owner'][key]='FOREIGN'
        check('D08-namespace-'+key,'D-08',m.source_key(rr)!=m.source_key(r),True)
    for key in p['identity']:
        pp=copy.deepcopy(p);pp['identity'][key]='FOREIGN';pp['expected']=copy.deepcopy(pp['identity'])
        check('D08-self-copy-'+key,'D-08',m.verify_proof(pp,r,s,h,c),'REJECT')
    check('D08-wrong-digest','D-08',m.verify_proof(dict(p,digest='0'*64),r,s,h,c),'REJECT')
    check('D08-stale','D-08',m.verify_proof(p,r,s,h,dict(c,fresh=False)),'REJECT')
    check('D08-wrong-net','D-08',m.verify_proof(dict(p,net=Decimal(51)),r,s,h,c),'REJECT')
    check('D08-context-magic','D-08',m.verify_proof(p,r,s,h,dict(c,magic=99)),'REJECT')
    check('D08-context-symbol','D-08',m.verify_proof(p,r,s,h,dict(c,symbol='FOREIGN')),'REJECT')
    small_record=dict(r,role='Small')
    check('D08-forbidden-reserve-role','D-08',m.verify_proof(p,small_record,s,{m.source_key(small_record):small_record},c),'REJECT')
    spent=copy.deepcopy(s);spent['remaining']['FinalReserve']=Decimal(0);spent['consumed']['FinalReserve']=Decimal(50)
    check('D08-allocation-reused','D-08',m.verify_proof(p,r,spent,h,c),'REJECT')
    wrong=copy.deepcopy(s);wrong['owner']['account']=99
    check('D08-allocation-owner','D-08',m.verify_proof(p,r,wrong,h,c),'REJECT')
    # Immutable complete record equality, independent of production duplicate helpers.
    rr=copy.deepcopy(r);rr.update(profit=Decimal(60),commission=Decimal(-10))
    check('L01-component-digest','D-08',m.digest(rr)!=m.digest(r),True)
    check('L01-same-record-digest','D-08',m.digest(copy.deepcopy(r)),m.digest(r))
    b=copy.deepcopy(s['grant']);b['FinalReserve']=Decimal(0);b['PartialFar']=Decimal(50)
    check('L02-bucket-digest','D-01',m.digest(b)!=m.digest(s['grant']),True)
    l1=dict(id=1,transitionLoss='100',available='50',farLoss='20',buffer='1',share='.5',bnet='4',farVolume='1',complete=True,fresh=True,sourceProof=True,currency='USD')
    l2=dict(l1,id=2,transitionLoss='10',available='5')
    check('CR09-A-negative-level','CR-09',m.worst_case([l1,l2],[1,2]),('REJECT',2,Decimal(-16)))
    check('CR09-B-limited-positive','CR-09',m.worst_case([l1,l2],[1,2],'B'),('POSITIVE',1,Decimal(29)))
    check('CR09-zero','CR-09',m.worst_case([dict(l1,available='21'),dict(l2,available='30')],[1,2]),('REJECT',1,Decimal(0)))
    check('CR09-tie','CR-09',m.worst_case([dict(l1,id=2),dict(l1,id=1)],[1,2]),('POSITIVE',1,Decimal(29)))
    for field in ('complete','fresh','sourceProof'):
        check('CR09-missing-'+field,'CR-09',m.worst_case([l1,dict(l2,**{field:False})],[1,2])[0],'UNAVAILABLE')
    check('CR09-no-filter-bad-level','CR-09',m.worst_case([l1],[1,2])[0],'UNAVAILABLE')
    check('CR09-lot-failure','CR-09',m.worst_case([l1,dict(l2,bnet='2')],[1,2])[0],'REJECT')
    equivalent=[dict(l1,available='100',farLoss='100'),dict(l2,available='100',farLoss='10')]
    check('CR09-equivalence-sufficient','CR-09',m.worst_case(equivalent,[1,2])[1],m.worst_case(equivalent,[1,2],'B')[1])
    g=m.core_geometry('.10','.01','3','.1','.01','.01')
    check('ZERO-raw-to-rounded','ZERO-CORE',(g['core'],g['slope'],g['outcome']),(Decimal(0),Decimal('.19'),'REJECT'))
    check('ZERO-positive-control','ZERO-CORE',m.core_geometry('.10','2','1','.5','.01','.01')['outcome'],'GEOMETRY_ONLY')
    # Inspect real policy behavior through unchanged R0 extracted subset (no broker IO).
    old=runpy.run_path(str(ROOT/'Tests/Static/check_hsbi_02b_r0_ledger_integrity.py'))
    source=old['native_source']()
    import tempfile
    with tempfile.TemporaryDirectory(prefix='r0a-guard-',dir=ROOT/'Tests') as tmp:
        modes=['HSBI_RUNTIME_UNSPECIFIED','HSBI_RUNTIME_PRODUCTION','HSBI_RUNTIME_ADMIN_VERIFICATION','HSBI_RUNTIME_UNIT_TEST','HSBI_RUNTIME_REAL_LIMITED']
        probes=[dict(id='guard-'+str(i),code='std::cout<<allow(HSBI_IsBrokerDispatchAllowed('+mode+'));') for i,mode in enumerate(modes)]
        got=old['execute_native'](source,probes,Path(tmp))
        for key,value in got.items():check(key,'INV-16',value,'REJECT')
    # Independence limits of historical oracle: do not edit or silently upgrade it.
    legacy=dict(account=1,symbol='EUR',magic=7,cycle=1,deal=11,allocation='A1',allocationEvent=31,policy=1,available=50)
    lq={k:v for k,v in legacy.items() if k!='available'};lq.update(event=41,bucket='FinalReserve',purpose='CatchUp',amount=10,plan=999,revision=999)
    old_out=old['oracle_consumption'](legacy,lq,{})
    observations=[dict(id='LEGACY-ORACLE-plan-revision',actual=old_out,completeProposedContractExpected='REJECT',
                       classification='ORACLE_COVERAGE_GAP' if old_out=='ALLOW' else 'RECHECK_REQUIRED')]
    return rows,observations


def serial(value):
    if isinstance(value,Decimal):return str(value)
    if isinstance(value,dict):return {str(k):serial(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)):return [serial(x) for x in value]
    return value


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path);args=p.parse_args()
    rows,observations=tests()
    result=dict(schema='HSBI.R0A.PROPOSED_TESTS/1',testedHead=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
                executedUtc=datetime.now(timezone.utc).isoformat(),tests=rows,observations=observations,
                passed=sum(x['result']=='PASS' for x in rows),failed=sum(x['result']=='FAIL' for x in rows),
                approval='AWAITING_ADMIN_APPROVAL',mql5Compile='NOT_RUN',brokerProof='NOT_RUN')
    if args.output:
        target=args.output.resolve()
        if not target.is_relative_to(ROOT):raise ValueError('outside allowed project')
        target.write_text(json.dumps(serial(result),ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('tests','observations')}))
    for x in rows:
        if x['result']=='FAIL':print(x)
    print('LEGACY_ORACLE_LIMITS='+json.dumps(observations))
    return int(result['failed']!=0)


if __name__=='__main__':raise SystemExit(main())
