#!/usr/bin/env python3
"""02B-R0: independent proposed oracle + execution of extracted MQL C++ subset.

No terminal/broker emulation claim. All scratch files remain inside project.
Exit 0 = evidence generated with all sensitivity checks; --enforce-contract
additionally fails on normative mismatches. Never interpret exit 0 as money acceptance.
"""
import argparse
import copy
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
BASE = '4e7d911002824a4a92e49b54f0f964afcf8cf703'


def read(path):
    return (ROOT / path).read_text(encoding='utf-8-sig')


def function(text, name):
    """Balanced braces, exact named definition; abort on ambiguous extraction."""
    hits = list(re.finditer(r'(?m)^[\w]+\s+' + name + r'\s*\(', text))
    if len(hits) != 1:
        raise ValueError(('ambiguous function', name, len(hits)))
    start = hits[0].start()
    left = text.index('{', hits[0].end())
    depth = 1
    pos = left + 1
    while depth:
        depth += (text[pos] == '{') - (text[pos] == '}')
        pos += 1
    return text[start:pos]


def struct(text, name):
    hit = re.search(r'struct\s+' + name + r'\s*\{[^}]+\};', text)
    if not hit:
        raise ValueError(name)
    return hit[0]


def clean(text):
    return '\n'.join(x for x in text.splitlines() if not x.startswith('#'))


def oracle_consumption(allocation, request, registry, ready=True):
    """Proposed CR-01/07/08, independent of production helper results."""
    if not ready or registry is None:
        return 'UNAVAILABLE'
    if not math.isfinite(allocation['available']) or allocation['available']<0:
        return 'REJECT'
    key = request['event']
    if key in registry:
        return 'NO_OP' if registry[key] == request else 'CONFLICT'
    if any(request[k] != allocation[k] for k in ('account', 'symbol', 'magic', 'cycle', 'deal', 'allocation', 'allocationEvent', 'policy')):
        return 'REJECT'
    if request['bucket'] != 'FinalReserve' or request['purpose'] != 'CatchUp':
        return 'REJECT'
    if not math.isfinite(request['amount']) or request['amount'] <= 0 or request['amount'] > allocation['available']:
        return 'REJECT'
    return 'ALLOW'


def oracle_identity(record, allocation, proof, context, history, journal_ready=True):
    """CR-02: expected comes from history/reconciled record, never proof."""
    if not journal_ready or history is None:
        return 'UNAVAILABLE'
    if not all(math.isfinite(v) for v in [record[k] for k in ('profit','swap','commission','fee','dealNet')]+[allocation['available'],proof['dealNet']]):
        return 'REJECT'
    if record['deal'] not in history or history[record['deal']] != record:
        return 'REJECT'
    if not record['confirmed'] or not record['event']:
        return 'REJECT'
    if allocation['deal'] != record['deal'] or allocation['available'] <= 0:
        return 'REJECT'
    fields = ('account', 'symbol', 'magic', 'cycle', 'position', 'role', 'direction', 'deal', 'event')
    expected = {k: record[k] for k in fields}
    expected.update(context)
    if proof['identity'] != expected or not proof['fresh']:
        return 'REJECT'
    net = sum(record[k] for k in ('profit', 'swap', 'commission', 'fee'))
    if proof['dealNet'] != net or record['dealNet'] != net:
        return 'REJECT'
    canonical = json.dumps({'record': record, 'allocation': allocation, 'context': context}, sort_keys=True, separators=(',', ':'))
    return 'ALLOW' if proof['digest'] == hashlib.sha256(canonical.encode()).hexdigest() else 'REJECT'


SHIM = r'''
#include <string>
#include <cmath>
#include <algorithm>
#include <sstream>
#include <iomanip>
#include <iostream>
#include <limits>
using string=std::string; using datetime=long;
#define MathAbs std::abs
#define MathMin std::min
#define MathMax std::max
#define MathFloor std::floor
#define MathCeil std::ceil
#define MathRound std::round
#define MathIsValidNumber std::isfinite
template<class T> void ZeroMemory(T &x){x=T{};}
string LongToString(long x){return std::to_string(x);}
string HSBI_UlongToString(ulong x){return std::to_string(x);}
string IntegerToString(int x){return std::to_string(x);}
string DoubleToString(double x,int n){std::ostringstream s;s<<std::fixed<<std::setprecision(n)<<x;return s.str();}
'''


def native_source(source_root=ROOT):
    def read(path):
        return (source_root/path).read_text(encoding='utf-8-sig')
    sources = []
    for path in ('Core/HSBI_Enums', 'Core/HSBI_ReasonCodes', 'Money/HSBI_BrokerMoneyTypes',
                 'Core/HSBI_RuntimePolicy', 'Money/HSBI_MoneyProofIdentity', 'Money/HSBI_AllocationPolicyTypes',
                 'Money/HSBI_EconomicLedgerTypes', 'Money/HSBI_AllocationLedgerTypes', 'Money/HSBI_ReserveAllocationTypes'):
        sources.append(clean(read('Include/' + path + '.mqh')))
    sources.append(struct(read('Include/Money/HSBI_MoneyState.mqh'), 'HSBI_MoneyState'))
    sources.append(function(read('Include/Money/HSBI_MoneyState.mqh'), 'HSBI_ValidateMoneyState'))
    sources.append(struct(read('Include/Money/HSBI_LevelMoneyEvaluator.mqh'), 'HSBI_BrokerMoneyEvaluationResult'))
    sources.append(clean(read('Include/Money/HSBI_ReserveCatchUpEvaluator.mqh')))
    sources.append(clean(read('Include/Planning/HSBI_BrokerGrid.mqh')))
    geom = read('Include/Planning/HSBI_GeometrySolver.mqh')
    sources.append(struct(geom, 'HSBI_GeometryResult'))
    sources += [function(geom, name) for name in ('HSBI_ValidateRecoverySlope', 'HSBI_SolveBigGeometry')]
    types = read('Include/Planning/HSBI_FutureSmallTypes.mqh')
    sources.append(re.search(r'enum HSBI_FutureSmallProofStatus[^;]+;', types)[0])
    sources += [struct(types, name) for name in ('HSBI_FutureSmallLevelProof', 'HSBI_FutureSmallResult')]
    # Digest irrelevant to selection experiment; explicitly a shim, not proof integrity evidence.
    sources.append('string HSBI_FutureSmallLevelDigest(const HSBI_FutureSmallLevelProof &p){return p.levelDigest;}')
    sources.append(clean(read('Include/Planning/HSBI_FutureSmallProofAggregator.mqh')))
    assembly=re.search(r'(?m)^\s*(.*ci.expectedFarIdentity=control.farLossProof.identity;)',read('Include/Planning/HSBI_NewFarSolver.mqh'))[1]
    sources.append('void AssembleExpected(HSBI_ReserveCatchUpInput &ci,const HSBI_ReserveCatchUpInput &control){'+assembly+'}')
    rhs=re.search(r'r.reserveGainMoney=([^;]+);',read('Include/Money/HSBI_BasketMoneyEvaluator.mqh'))[1]
    sources.append('double ExtractedReserveMetric(double c,double t,double s){struct Leg{double netMoney;};struct Basket{Leg core,trend,small;};Basket r{{c},{t},{s}};return '+rhs+';}')
    return SHIM + '\n'.join(sources)


CASES = []


def case(cid, contract, expected, code, note=''):
    CASES.append(dict(id=cid, contract=contract, expected=expected, code=code, note=note))


def cases():
    CASES.clear()
    for cid, change, want in [
        ('M01-control', '', 'ALLOW'),
        ('M01-foreign-deal', 'x.consumptionKey.sourceDealKey="D2";', 'REJECT'),
        ('M01-foreign-allocation', 'x.consumptionKey.sourceAllocationKey="A2";', 'REJECT'),
        ('M01-foreign-cycle-in-key', 'x.consumptionKey.sourceDealKey="EUR|7|99|11";', 'REJECT'),
        ('M01-foreign-allocation-event', 'x.reserveAllocationSource.allocationEventId=999;', 'REJECT'),
        ('M01-exact-replay', 'x.hasPriorConsumption=true;x.priorConsumptionKey=x.consumptionKey;', 'NO_OP'),
        ('M01-altered-replay', 'x.hasPriorConsumption=true;x.priorConsumptionKey=x.consumptionKey;x.priorConsumptionKey.consumer="PartialFar";', 'CONFLICT'),
        ('M01-restart-unknown-registry', 'x.hasPriorConsumption=false;', 'UNAVAILABLE'),
        ('M01-spent-bucket', 'x.reserveAllocationSource.residualAllocated=40;x.reserveAllocationSource.alreadyConsumed=10;', 'REJECT'),
        ('M01-spent-unallocated-path', 'x.reserveAllocationSource.residualAllocated=40;x.reserveAllocationSource.alreadyConsumed=10;x.reserveEligibleMoneyAlreadyAllocated=false;', 'REJECT'),
        ('M01-invalid-source-control', 'x.reserveAllocationSource.valid=false;', 'REJECT'),
    ]:
        case(cid, 'CR-01/07/08', want, 'auto x=base();'+change+'std::cout<<outcome(HSBI_EvaluateReserveCatchUp(x));')
    fields = {'accountLogin': '999', 'magic': '999', 'cycleId': '999', 'positionIdentifier': '999',
              'sourceDealId': '999', 'sourceEventId': '999', 'planId': '999', 'stateRevision': '999', 'snapshotId': '999'}
    for field, value in fields.items():
        case('M02-self-copy-'+field, 'CR-02', 'REJECT',
             f'auto x=base();x.reserveSourceProof.identity.{field}={value};'
             + ('x.reserveAllocationSource.sourceDealId=999;' if field=='sourceDealId' else '')
             + 'AssembleExpected(x,x);std::cout<<outcome(HSBI_EvaluateReserveCatchUp(x));',
             'Isolated Catch-Up identity-boundary experiment; full NewFar selection NOT_RUN')
        case('M02-independent-'+field, 'CR-02', 'REJECT',
             f'auto x=base();x.reserveSourceProof.identity.{field}={value};std::cout<<outcome(HSBI_EvaluateReserveCatchUp(x));')
    case('M02-control', 'CR-02', 'ALLOW', 'auto x=base();std::cout<<outcome(HSBI_EvaluateReserveCatchUp(x));')
    case('M02-zero-deal', 'CR-02', 'REJECT', 'auto x=base();x.reserveSourceProof.identity.sourceDealId=0;x.expectedReserveIdentity=x.reserveSourceProof.identity;std::cout<<outcome(HSBI_EvaluateReserveCatchUp(x));')
    case('M02-zero-event', 'CR-02', 'REJECT', 'auto x=base();x.reserveSourceProof.identity.sourceEventId=0;x.expectedReserveIdentity=x.reserveSourceProof.identity;std::cout<<outcome(HSBI_EvaluateReserveCatchUp(x));')
    case('M02-stale-flag-control', 'CR-02', 'UNAVAILABLE', 'auto x=base();x.fresh=false;std::cout<<outcome(HSBI_EvaluateReserveCatchUp(x));')
    # No imported production outcome is used to construct expected classifications.
    econ = 'HSBI_EconomicLedgerRecord a{};a.sourceDealKey="D1";a.volume=1;a.price=100;a.dealNet=50;a.profit=55;a.commission=-5;auto b=a;'
    case('L01-control', 'CR-03', 'NO_OP', econ+'std::cout<<dup(HSBI_ClassifyEconomicDuplicate(a,b));')
    for name, change in [('components','b.profit=60;b.commission=-10;'), ('event','b.eventId=99;'),
                         ('position','b.positionIdentifier=99;'), ('role','b.role=HSBI_ROLE_FAR;'),
                         ('timestamp','b.timestamp=99;'), ('swap-fee','b.swap=2;b.fee=-2;')]:
        case('L01-'+name, 'CR-03', 'CONFLICT', econ+change+'std::cout<<dup(HSBI_ClassifyEconomicDuplicate(a,b));')
    alloc='auto a=allocation();auto b=a;'
    case('L02-control', 'CR-04', 'NO_OP', alloc+'std::cout<<dup(HSBI_ClassifyAllocationDuplicate(a,b));')
    for name, change in [('bucket-permutation','b.finalReserveAllocated=0;b.partialFarAllocated=50;'),
                         ('consumed','b.consumed=10;'),('available','b.available=40;'),
                         ('residual','b.finalReserveAllocated=40;b.residual=10;'),
                         ('source-net','b.sourceDealNet=60;'),('status','b.status=HSBI_STATUS_CONFLICT;')]:
        case('L02-'+name, 'CR-04', 'CONFLICT', alloc+change+'std::cout<<dup(HSBI_ClassifyAllocationDuplicate(a,b));')
    case('L02-negative-offset','CR-04','CONFLICT',alloc+'b.finalReserveAllocated=-10;b.partialFarAllocated=60;std::cout<<dup(HSBI_ClassifyAllocationDuplicate(a,b));')
    case('L02-nan','CR-04','CONFLICT',alloc+'b.finalReserveAllocated=NAN;std::cout<<dup(HSBI_ClassifyAllocationDuplicate(a,b));')
    for name, change, want in [
        ('control','', 'ALLOW'), ('invalid','a.valid=false;', 'REJECT'),
        ('negative-bucket','a.finalReserveAllocated=-10;', 'REJECT'),
        ('offset-negative','a.finalReserveAllocated=-10;a.partialFarAllocated=60;', 'REJECT'),
        ('infinity','a.sourceDealNet=INFINITY;a.finalReserveAllocated=INFINITY;', 'REJECT'),
        ('nan','a.finalReserveAllocated=NAN;', 'REJECT'),
        ('negative-consumed','a.consumed=-1;', 'REJECT'),
        ('over-consumed','a.consumed=51;', 'REJECT'),
        ('unassigned','a.finalReserveAllocated=40;', 'REJECT'),
        ('invalid-status','a.status=HSBI_STATUS_CONFLICT;', 'REJECT'),
        ('foreign-source','a.sourceDealKey="FOREIGN";', 'REJECT'),
        ('negative-net-offset','a.sourceDealNet=-10;a.finalReserveAllocated=-1;', 'REJECT')]:
        case('E-allocation-'+name, 'CR-04', want, 'auto a=allocation();'+change+'std::cout<<allow(HSBI_ValidateAllocationConservation(a));',
             'unassigned uses proposed D-01; foreign-source requires mandatory authoritative caller')
    for name, change, want in [('control','', 'ALLOW'),('invalid','s.valid=false;', 'REJECT'),
                              ('zero-revision','s.revision=0;', 'REJECT'),('unknown-revision','s.revision=999;', 'REJECT'),
                              ('negative','s.finalReserve=-1;', 'REJECT'),('infinity','s.finalReserve=INFINITY;', 'REJECT'),
                              ('nan','s.realizedCycleNet=NAN;', 'REJECT')]:
        case('E-state-'+name,'CR-05',want,'HSBI_MoneyState s{};s.valid=true;s.revision=1;'+change+'std::cout<<allow(HSBI_ValidateMoneyState(s));')
    case('E-bucket-control','CR-05','ALLOW','std::cout<<allow(HSBI_CanConsumeBucket(HSBI_BUCKET_PARTIAL_FAR_BUDGET,true));')
    case('E-bucket-final-for-partial','CR-05','REJECT','std::cout<<allow(HSBI_CanConsumeBucket(HSBI_BUCKET_FINAL_RESERVE,true));')
    case('E-bucket-unknown','CR-05','REJECT','std::cout<<allow(HSBI_CanConsumeBucket((HSBI_MoneyBucket)999,false));')
    case('E-amount-over','CR-05','REJECT','auto a=allocation();std::cout<<allow(HSBI_CanConsumeAmount(a,51));')
    case('E-amount-control','CR-05','ALLOW','auto a=allocation();std::cout<<allow(HSBI_CanConsumeAmount(a,10));')
    case('E-amount-invalid-state','CR-05','REJECT','auto a=allocation();a.valid=false;std::cout<<allow(HSBI_CanConsumeAmount(a,10));')
    case('F-zero-core','CR-06','REJECT','auto p=broker();auto r=HSBI_SolveBigGeometry(0.1,0.01,3.0,0.1,p,true,true);std::cout<<allow(r.valid);')
    case('F-geometry-control','CR-06','ALLOW','auto p=broker();auto r=HSBI_SolveBigGeometry(0.1,2.0,1.0,0.5,p,true,true);std::cout<<allow(r.valid);')
    case('G-worst-contradictory-extrema','CR-09','2','auto p=levels();auto r=HSBI_AggregateFutureSmallProof(p,HSBI_PROOF_POLICY_WORST_CASE,0);std::cout<<r.catchUpControlLevel;', 'DECISION_REQUIRED: expected 2 only under minimum Catch-Up margin proposal')
    case('G-final-control','CR-09','2','auto p=levels();auto r=HSBI_AggregateFutureSmallProof(p,HSBI_PROOF_POLICY_FINAL_LEVEL,0);std::cout<<r.catchUpControlLevel;')
    case('G-incomplete-control','CR-09','REJECT','auto p=levels();p.levels[1].moneyIncluded=false;std::cout<<allow(HSBI_AggregateFutureSmallProof(p,HSBI_PROOF_POLICY_WORST_CASE,0).valid);')
    # Compile the exact production RHS, not a reimplementation of the formula.
    for cid, core, trend, small, want in [('M05-small-only',0,0,10,'0'),('M05-core-control',10,0,0,'10')]:
        case(cid,'CR-10',want,f'std::cout<<ExtractedReserveMetric({core},{trend},{small});')
    return CASES


SUPPORT = r'''
string allow(bool x){return x?"ALLOW":"REJECT";}
string dup(int x){return x==1?"NO_OP":x==2?"CONFLICT":"NEW";}
string outcome(const HSBI_ReserveCatchUpResult &r){
 if(r.details=="DUPLICATE_CONSUMPTION_NOOP")return "NO_OP";
 if(r.details=="CONSUMPTION_CONFLICT")return "CONFLICT";
 if(r.status==HSBI_CALC_UNAVAILABLE)return "UNAVAILABLE";
 return r.valid?"ALLOW":"REJECT";
}
HSBI_ReserveCatchUpInput base(){
 HSBI_ReserveCatchUpInput x{};x.runtimeMode=HSBI_RUNTIME_ADMIN_VERIFICATION;
 x.allocationPolicy={0.5,0,0,0,1,1,true,true};x.reserveEligibleMoney=100;x.reserveEligibleMoneyAlreadyAllocated=true;
 x.farLossIncreaseMoney=10;x.executionSafetyBuffer=1;x.netBigVolume=4;x.farVolume=1;x.farDirection=HSBI_DIRECTION_SELL;
 auto &p=x.reserveSourceProof;p.valid=true;p.status=HSBI_CALC_PASS;p.projected=true;p.runtimeConfirmed=true;p.netMoney=100;
 p.identity={1,"EUR",7,1,1,HSBI_ROLE_BIG_CORE,HSBI_DIRECTION_BUY,11,21,1,1,1};
 x.farLossProof=p;x.farLossProof.netMoney=-10;x.farLossProof.identity.role=HSBI_ROLE_FAR;x.farLossProof.identity.direction=HSBI_DIRECTION_SELL;
 x.expectedReserveIdentity=p.identity;x.expectedFarIdentity=x.farLossProof.identity;
 x.reserveAllocationSource={"D1","A1",11,31,1,100,50,0,0,0,50,0,true,true,true};
 x.consumptionKey={"D1","A1",1,1,41,"CatchUp"};x.sourceDealId=11;x.sourceEventId=21;
 x.planId=1;x.stateRevision=1;x.snapshotId=1;x.projected=true;x.moneyAvailable=true;x.fresh=true;return x;
}
HSBI_AllocationLedgerRecord allocation(){HSBI_AllocationLedgerRecord a{};a.sourceDealKey="D1";a.allocationEventId=31;a.sourceDealNet=50;a.finalReserveAllocated=50;a.available=50;a.valid=true;a.status=HSBI_STATUS_VALID;return a;}
HSBI_BrokerProperties broker(){return {"EUR",0.01,0.01,2,0.01,100,0.01,1,1,true,true,1,1};}
HSBI_FutureSmallResult levels(){
 HSBI_FutureSmallResult p{};p.valid=true;p.status=HSBI_FS_EXACT_PROOF;p.provenDepth=2;
 for(int i=0;i<2;i++){auto &l=p.levels[i];l.levelIndex=i+1;l.valid=true;l.moneyIncluded=true;l.marginIncluded=true;l.riskIncluded=true;
 l.transitionLossIncluded=true;l.controlSnapshotValid=true;l.costSnapshotValid=true;l.farProjectionValid=true;l.runtimeConfirmed=true;
 l.proofStatus=HSBI_FS_EXACT_PROOF;l.moneyProofStatus=l.marginProofStatus=l.riskProofStatus=l.transitionLossProofStatus=HSBI_CALC_PASS;
 l.transitionLoss=i==0?100:10;l.reserveSourceProof.netMoney=i==0?50:5;l.farLossProof.netMoney=i==0?-20:-20;
 l.farAfter=i==0?0.5:0.2;l.compressionLots=0.1;l.compressionRatio=0.2;}
 return p;
}
'''


def execute_native(source, rows, folder):
    cpp=folder/'probe.cpp';exe=folder/'probe'
    main='\nint main(){\n'+ '\n'.join('std::cout<<"'+r['id']+'|";{'+r['code']+'}std::cout<<"\\n";' for r in rows)+'\n}'
    cpp.write_text(source+SUPPORT+main)
    env=dict(os.environ,TMPDIR=str(folder))
    c=subprocess.run(['g++','-std=c++17','-O0','-fno-fast-math',str(cpp),'-o',str(exe)],capture_output=True,text=True,env=env)
    if c.returncode:
        raise RuntimeError(c.stderr)
    run=subprocess.run([str(exe)],capture_output=True,text=True,check=True)
    observed=dict(line.split('|',1) for line in run.stdout.splitlines())
    if set(observed)!=set(r['id'] for r in rows):
        raise AssertionError('missing/duplicate native outcomes')
    return observed


def reference_cases():
    a=dict(account=1,symbol='EUR',magic=7,cycle=1,deal=11,allocation='A1',allocationEvent=31,policy=1,available=50)
    q={k:a[k] for k in a if k!='available'}
    q.update(event=41,bucket='FinalReserve',purpose='CatchUp',amount=10,plan=1,revision=1)
    rows=[]
    def add(cid,got,want):
        if got!=want:raise AssertionError((cid,got,want))
        rows.append(dict(id=cid,actual=got,expected=want,result='PASS',layer='independent proposed oracle'))
    add('O-consumption-control',oracle_consumption(a,q,{}),'ALLOW')
    for k in ('account','symbol','magic','cycle','deal','allocation','allocationEvent','policy'):
        z=copy.deepcopy(q);z[k]='FOREIGN'
        add('O-foreign-'+k,oracle_consumption(a,z,{}),'REJECT')
    add('O-exact-replay',oracle_consumption(a,q,{41:q}),'NO_OP')
    z=copy.deepcopy(q);z['amount']=11
    add('O-changed-amount-replay',oracle_consumption(a,z,{41:q}),'CONFLICT')
    add('O-restart-unknown',oracle_consumption(a,q,None),'UNAVAILABLE')
    spent=dict(a,available=0)
    add('O-spent-bucket',oracle_consumption(spent,q,{}),'REJECT')
    for k,v in [('amount',51),('amount',-1),('amount',float('nan')),('bucket','PartialFar'),('purpose','PartialFar')]:
        z=dict(q);z[k]=v
        add('O-consumption-'+k+'-'+str(v),oracle_consumption(a,z,{}),'REJECT')
    record=dict(account=1,symbol='EUR',magic=7,cycle=1,position=1,role='BigCore',direction='BUY',deal=11,event=21,
                confirmed=True,profit=55,swap=0,commission=-5,fee=0,dealNet=50)
    ctx=dict(plan=1,revision=1,snapshot=1)
    ident={k:record[k] for k in ('account','symbol','magic','cycle','position','role','direction','deal','event')};ident.update(ctx)
    body=json.dumps(dict(record=record,allocation=a,context=ctx),sort_keys=True,separators=(',',':'))
    proof=dict(identity=ident,dealNet=50,fresh=True,digest=hashlib.sha256(body.encode()).hexdigest())
    history={11:record}
    add('O-proof-control',oracle_identity(record,a,proof,ctx,history),'ALLOW')
    for k in ident:
        z=copy.deepcopy(proof);z['identity'][k]='FOREIGN'
        add('O-proof-'+k,oracle_identity(record,a,z,ctx,history),'REJECT')
    for k,v in [('fresh',False),('digest','0'*64),('dealNet',51)]:
        z=copy.deepcopy(proof);z[k]=v
        add('O-proof-'+k,oracle_identity(record,a,z,ctx,history),'REJECT')
    add('O-missing-deal',oracle_identity(record,a,proof,ctx,{}),'REJECT')
    z=dict(record,event=0)
    add('O-missing-event',oracle_identity(z,a,proof,ctx,{11:z}),'REJECT')
    add('O-allocation-reuse',oracle_identity(record,spent,proof,ctx,history),'REJECT')
    add('O-history-unavailable',oracle_identity(record,a,proof,ctx,None),'UNAVAILABLE')
    # Ledger immutable payload independent oracle: complete object equality.
    add('O-ledger-control','NO_OP' if record==copy.deepcopy(record) else 'CONFLICT','NO_OP')
    for k,v in [('profit',60),('swap',2),('commission',-10),('fee',-2),('account',2),('event',99)]:
        z=dict(record);z[k]=v
        add('O-ledger-'+k,'NO_OP' if z==record else 'CONFLICT','CONFLICT')
    for k,v in [('policy',2),('available',40),('consumed',10),('residual',10)]:
        z=dict(a);z[k]=v
        add('O-allocation-'+k,'NO_OP' if z==a else 'CONFLICT','CONFLICT')
    # Immutable grants and mutable balances are distinct (proposed D-01).
    def conservation(net,grants,remaining,consumed):
        numbers=[net,*grants,*remaining,*consumed]
        return all(math.isfinite(v) and v>=0 for v in numbers) and sum(grants)==net and all(g==r+c for g,r,c in zip(grants,remaining,consumed))
    add('O-conservation-control', 'ALLOW' if conservation(50,[50,0],[40,0],[10,0]) else 'REJECT','ALLOW')
    add('O-conservation-double-count', 'ALLOW' if conservation(50,[50,0],[50,0],[10,0]) else 'REJECT','REJECT')
    add('O-conservation-unallocated', 'ALLOW' if conservation(50,[40,0],[40,0],[0,0]) else 'REJECT','REJECT')
    add('O-consume-first',oracle_consumption(a,q,{}),'ALLOW')
    remaining=dict(a,available=40);second=dict(q,event=42,amount=41)
    add('O-consume-over-remaining',oracle_consumption(remaining,second,{41:q}),'REJECT')
    add('O-allocation-infinite-balance',oracle_consumption(dict(a,available=float('inf')),q,{}),'REJECT')
    for k in ('profit','commission','dealNet'):
        bad=dict(record);bad[k]=float('inf')
        add('O-history-nonfinite-'+k,oracle_identity(bad,a,proof,ctx,{11:bad}),'REJECT')
    return rows


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path);p.add_argument('--enforce-contract',action='store_true');args=p.parse_args()
    rows=cases();source=native_source()
    with tempfile.TemporaryDirectory(prefix='02b-r0-',dir=ROOT/'Tests') as tmp:
        folder=Path(tmp);observed=execute_native(source,rows,folder)
        mutations=[]
        changes=[
            ('reject-positive-source','return x.reserveAllocated+x.partialFarAllocated', 'return false;return x.reserveAllocated+x.partialFarAllocated','M01-control'),
            ('remove-partial-isolation','if(partialFarConsumer&&bucket==HSBI_BUCKET_FINAL_RESERVE)return false;', 'if(false)return false;','E-bucket-final-for-partial'),
            ('remove-identity-account','a.accountLogin==b.accountLogin&&','', 'M02-independent-accountLogin'),
            ('remove-consumption-history','bool duplicate=x.hasPriorConsumption&&','bool duplicate=false&&','M01-exact-replay'),
            ('disable-economic-duplicate','return HSBI_SameEconomicRecord(existing,incoming)?1:2;', 'return 2;', 'L01-control'),
            ('disable-allocation-duplicate','return same?1:2;', 'return 2;', 'L02-control'),
            ('repair-m01-cross-binding','r.consumptionAllowed=HSBI_ValidateReserveConsumption(x.consumptionKey,x.planId,x.stateRevision);',
             'r.consumptionAllowed=HSBI_ValidateReserveConsumption(x.consumptionKey,x.planId,x.stateRevision)&&x.consumptionKey.sourceDealKey==x.reserveAllocationSource.sourceDealKey&&x.consumptionKey.sourceAllocationKey==x.reserveAllocationSource.sourceAllocationKey;', 'M01-foreign-deal'),
            ('repair-l01-components','return a.sourceDealKey==b.sourceDealKey&&MathAbs(a.dealNet-b.dealNet)',
             'return a.profit==b.profit&&a.swap==b.swap&&a.commission==b.commission&&a.fee==b.fee&&a.sourceDealKey==b.sourceDealKey&&MathAbs(a.dealNet-b.dealNet)', 'L01-components'),
            ('repair-l02-buckets','bool same=MathAbs(HSBI_AllocatedTotal(a)-HSBI_AllocatedTotal(b))<0.0000001;',
             'bool same=a.finalReserveAllocated==b.finalReserveAllocated&&a.partialFarAllocated==b.partialFarAllocated&&a.transitionAllocated==b.transitionAllocated&&a.carryAllocated==b.carryAllocated&&a.residual==b.residual;', 'L02-bucket-permutation'),
            ('repair-zero-core','bool coreGrid=(r.coreVolume==0.0||', 'bool coreGrid=(r.coreVolume>=p.volumeMin&&', 'F-zero-core'),
            ('repair-m02-independent-expected','ci.expectedReserveIdentity=control.reserveSourceProof.identity;', ';', 'M02-self-copy-accountLogin'),
            ('m05-small-term-sensitivity','MathMax(0.0,r.core.netMoney+r.trend.netMoney+r.small.netMoney)', 'MathMax(0.0,r.core.netMoney+r.trend.netMoney)', 'M05-small-only'),
            ('worst-policy-selection-sensitivity','a.catchUpControlLevel=a.worstTransitionLossLevel;', 'a.catchUpControlLevel=p.provenDepth;', 'G-worst-contradictory-extrema'),
        ]
        for name,old,new,cid in changes:
            if source.count(old)!=1:raise AssertionError(('mutation anchor',name,source.count(old)))
            isolated=folder/name
            shutil.copytree(ROOT/'Include',isolated/'Include')
            targets=[p for p in (isolated/'Include').rglob('*.mqh') if old in p.read_text(encoding='utf-8-sig')]
            if name=='remove-identity-account':
                targets=[p for p in targets if p.name=='HSBI_MoneyProofIdentity.mqh']
            if len(targets)!=1:raise AssertionError(('source-file mutation anchor',name,len(targets)))
            target=targets[0];original=target.read_text(encoding='utf-8-sig')
            if original.count(old)!=1:raise AssertionError(('nonunique raw source mutation',name,original.count(old)))
            changed=original.replace(old,new,1);target.write_text(changed)
            mutant=native_source(isolated)
            if mutant!=source.replace(old,new,1):raise AssertionError('extraction did not preserve source mutation')
            got=execute_native(mutant,[r for r in rows if r['id']==cid],folder)[cid]
            killed=got!=observed[cid]
            if not killed:raise AssertionError(('survived',name,cid,got))
            mutations.append(dict(id=name,target=cid,baseline=observed[cid],mutant=got,detected=killed,
                                  kind='repair sensitivity' if name.startswith('repair') else 'diagnostic sensitivity' if 'sensitivity' in name else 'regression mutation',
                                  sourceFile=str(target.relative_to(isolated)),
                                  rawOriginalSha256=hashlib.sha256(original.encode()).hexdigest(),rawMutantSha256=hashlib.sha256(changed.encode()).hexdigest(),
                                  originalSha256=hashlib.sha256(source.encode()).hexdigest(),mutantSha256=hashlib.sha256(mutant.encode()).hexdigest()))
    results=[{k:v for k,v in r.items() if k!='code'}|dict(actual=observed[r['id']],contractPass=observed[r['id']]==r['expected'],layer='extracted production C++ subset') for r in rows]
    out=dict(schema='HSBI.02B_R0/1',baseSha=BASE,testedHead=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
             executedUtc=datetime.now(timezone.utc).isoformat(),runnerSha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
             scope='test-only; proposed contracts unapproved',nativeCases=results,referenceCases=reference_cases(),mutations=mutations,
             normativeMismatchCount=sum(not r['contractPass'] for r in results),
             mql5Compile='NOT_RUN',mql5Tests='NOT_RUN',strategyTester='NOT_RUN',brokerProof='NOT_RUN',
             fullNewFarSelection='NOT_RUN',durableRestart='UNPROVEN',evidenceExecution='PASS',
             moneyIntegrity='FAIL',decisionStatus='AWAITING_ADMIN_APPROVAL')
    if args.output:
        dest=args.output.resolve()
        if not dest.is_relative_to(ROOT):raise ValueError('output outside allowed project')
        dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('nativeCases','referenceCases','mutations')},ensure_ascii=False))
    print(f"NATIVE={len(results)} ORACLE={len(out['referenceCases'])} MUTATIONS={len(mutations)} MISMATCHES={out['normativeMismatchCount']}")
    return 1 if args.enforce_contract and out['normativeMismatchCount'] else 0


if __name__=='__main__':
    raise SystemExit(main())
