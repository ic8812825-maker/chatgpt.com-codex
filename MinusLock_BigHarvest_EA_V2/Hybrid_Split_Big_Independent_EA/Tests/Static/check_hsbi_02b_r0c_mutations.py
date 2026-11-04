#!/usr/bin/env python3
"""Reproduce frozen R0B weaknesses, then apply causal R0C source mutations."""
import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import runpy
import sys
import tempfile
from decimal import Decimal
sys.path.insert(0,str(Path(__file__).resolve().parent))
import check_hsbi_02b_r0c_contracts as t
ROOT=t.ROOT


def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);return m


def modify(source,old,new):
    assert source.count(old)==1,('ambiguous anchor',old,source.count(old))
    return source.replace(old,new,1)


FOUR=[
 ('proof-digest',"    if request['proofDigest']!=digest(proof_bundle(record,allocation,expected)):return 'REJECT'",'DIGEST-forged',lambda q,s,j,a:q.update(proofDigest='0'*64),'REJECT'),
 ('raw-sum',"    if raw!=number(record['rawNet']):return 'CONFLICT'",'RAW-net-mismatch',lambda q,s,j,a:a['history'][s['source']].update(rawNet=Decimal(999)),'CONFLICT'),
 ('posted-net',"    if max(Decimal(0),actual)!=state['net']:return 'CONFLICT'",'POSTED-net-mismatch',lambda q,s,j,a:(a['history'][s['source']].update(profit=Decimal(56),rawNet=Decimal(51)),a['history'][s['source']]['receipt'].update(raw=Decimal(51),posted=Decimal(51))),'CONFLICT'),
 ('record-identity',"    if any(record['identity'][k]!=expected[k] for k in ('Broker','Server','Account','Symbol','Magic','Deal','Order','Position','Cycle')):\n        return 'REJECT'",'RECORD-Magic',lambda q,s,j,a:a['history'][s['source']]['identity'].update(Magic=999),'REJECT'),
]


def observation(m,fixture,edit,reseal=False,sealer=t.seal):
    q,s,j,a=fixture();edit(q,s,j,a)
    if reseal:sealer(q,a)
    before=copy.deepcopy((q,s,j,a))
    try:
        status,ss,jj,aa=m.apply_for_test(q,s,j,a)
        return dict(status=status,stateUnchanged=ss==s,journalUnchanged=jj==j,authorityUnchanged=aa==a,inputsUnchanged=(q,s,j,a)==before,remaining=ss.get('remaining') if type(ss) is dict else None,revision=ss.get('revision') if type(ss) is dict else None)
    except (KeyError,ValueError,TypeError,ArithmeticError,AttributeError) as e:
        return dict(status='UNHANDLED_INPUT_ERROR',errorType=type(e).__name__,message=str(e),inputsUnchanged=(q,s,j,a)==before)


def reproduce():
    frozen=runpy.run_path(str(ROOT/'Tests/Static/check_hsbi_02b_r0b_contracts.py'))
    old=load(ROOT/'Tests/Reference/hsbi_02b_r0b_independent_oracle.py','r0c_original_r0b')
    fixture=frozen['fixtures'];source=Path(old.__file__).read_text();mutations=[]
    def reseal(q,a):
        alloc=a['allocations']['A1'];q['proofDigest']=t.fingerprint(dict(record=a['history'][alloc['source']],allocation=alloc,expected=a['identity']))
    with tempfile.TemporaryDirectory(prefix='r0c-reproduce-',dir=ROOT/'Tests') as scratch:
        for name,anchor,target,edit,want in FOUR:
            changed=modify(source,anchor,'    pass');p=Path(scratch)/(name+'.py');p.write_text(changed);m=load(p,'r0c_old_mut_'+name)
            control=observation(old,fixture,lambda *args:None);mutcontrol=observation(m,fixture,lambda *args:None)
            rows=frozen['reference_cases'](m)
            neg=observation(old,fixture,edit,name!='proof-digest',reseal);mutneg=observation(m,fixture,edit,name!='proof-digest',reseal)
            confirmed=all(x['status']=='COMMITTED_IN_MEMORY' for x in (control,mutcontrol,mutneg)) and neg['status']==want and all(x['result']=='PASS' for x in rows)
            mutations.append(dict(FindingID='R0C-01',MutationID=name,classification='CONFIRMED' if confirmed else 'NOT_REPRODUCED',OriginalSourceHash=hashlib.sha256(source.encode()).hexdigest(),MutantSourceHash=hashlib.sha256(changed.encode()).hexdigest(),ExactEdit=dict(before=anchor,after='    pass'),PositiveControl=control,MutantPositiveControl=mutcontrol,OriginalNegative=neg,MutantNegative=mutneg,OldSuitePassed=sum(x['result']=='PASS' for x in rows),OldSuiteFailed=sum(x['result']=='FAIL' for x in rows),ExpectedOriginal=want,ExpectedMutant='COMMITTED_IN_MEMORY',CausalTestID=target,scope='disposable R0B Python copy, no production mutation'))
    examples=[]
    edits=[('R0C-02','snapshot-id',lambda q,s,j,a:a['snapshot'].update(id=999)),('R0C-02','snapshot-missing',lambda q,s,j,a:a['snapshot'].pop('id')),('R0C-02','snapshot-zero',lambda q,s,j,a:a['snapshot'].update(id=0)),('R0C-02','snapshot-bool',lambda q,s,j,a:a['snapshot'].update(id=True)),('R0C-02','snapshot-content',lambda q,s,j,a:a['snapshot'].update(content='changed')),('R0C-02','snapshot-expired',lambda q,s,j,a:a['snapshot'].update(validUntil=99)),('R0C-05','history-future',lambda q,s,j,a:a.update(historyObservedAt=1000))]
    edits += [('R0C-03','event-'+repr(v),lambda q,s,j,a,v=v:q.update(event=v)) for v in (True,False,0,-1,1.5,'41',None,2**64,1,2**64-1)]
    edits += [('R0C-04','missing-'+k,lambda q,s,j,a,k=k:q.pop(k)) for k in ('event','identity')]
    edits += [('R0C-04','missing-plan',lambda q,s,j,a:q['identity'].pop('Plan')),('R0C-04','missing-receipt',lambda q,s,j,a:a['history'][s['source']].pop('receipt')),('R0C-04','missing-posted',lambda q,s,j,a:a['history'][s['source']]['receipt'].pop('posted')),('R0C-04','missing-allocation',lambda q,s,j,a:a.update(allocations={}))]
    edits += [('R0C-04','state-type',lambda q,s,j,a:s.clear()),('R0C-04','history-type',lambda q,s,j,a:a.update(history=[])),('R0C-04','journal-type',lambda q,s,j,a:j.update({1:'malformed'})),('R0C-04','money-nan',lambda q,s,j,a:q.update(amount=Decimal('NaN'))),('R0C-04','money-invalid',lambda q,s,j,a:q.update(amount='bad')),('R0C-05','history-max-age',lambda q,s,j,a:a.update(historyObservedAt=80)),('R0C-05','history-too-old',lambda q,s,j,a:a.update(historyObservedAt=79)),('R0C-05','history-missing-time',lambda q,s,j,a:a.pop('historyObservedAt')),('R0C-05','snapshot-end',lambda q,s,j,a:a.update(now=110)),('R0C-05','unknown-clock-domain',lambda q,s,j,a:a.update(clockDomain='OTHER')),('R0C-05','unknown-time-unit',lambda q,s,j,a:a.update(timeUnit='OTHER'))]
    for fid,name,edit in edits:
        o=observation(old,fixture,edit)
        expected='REJECT'
        if name in ('snapshot-expired','history-future','history-too-old','unknown-clock-domain','unknown-time-unit'):expected='UNAVAILABLE'
        if name in ('event-1','event-18446744073709551615','history-max-age','snapshot-end'):expected='COMMITTED_IN_MEMORY'
        unproven=name in ('snapshot-content','unknown-clock-domain','unknown-time-unit','journal-type')
        classification='UNPROVEN' if unproven else 'CONFIRMED' if o['status']!=expected else 'NOT_REPRODUCED'
        examples.append(dict(FindingID=fid,case=name,actual=o,MathematicalExpected=expected,PositiveControl=observation(old,fixture,lambda *x:None),classification=classification,interpretation='CONFIRMED denotes a counterexample; NOT_REPRODUCED denotes correct rejection/control for this input, not dismissal of whole finding',proofBoundary='R0B fixture API only; unsupported content/clock metadata has no independent contract in frozen schema'))
    for label,index in [('state',1),('journal',2)]:
        def wrong_fixture(index=index):
            args=list(fixture());args[index]=[];return args
        o=observation(old,wrong_fixture,lambda *x:None)
        examples.append(dict(FindingID='R0C-04',case='wrong-type-'+label,actual=o,MathematicalExpected='REJECT',classification='CONFIRMED' if o['status']!='REJECT' else 'NOT_REPRODUCED',proofBoundary='R0B malformed DTO boundary'))
    import ast,re
    recorded=json.loads((ROOT/'Tests/Evidence/NEXT_STAGE_02B_R0B_REGRESSIONS.json').read_text())
    cmd=next(r['command'][2] for r in recorded['runs'] if r['id']=='02A_no_trade_scan')
    node=next(n for n in ast.walk(ast.parse(cmd)) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='compile')
    pattern=ast.literal_eval(node.args[0]);scannerMatches=bool(re.compile(pattern).search('OrderSend(request,result);'))
    scannerReview=dict(check='SCAN-ESCAPING-HYPOTHESIS',classification='NOT_REPRODUCED' if scannerMatches else 'CONFIRMED',oldPattern=pattern,positivePayload='OrderSend(request,result);',oldScannerMatches=scannerMatches,interpretation='AST-literal проверка: предположение о неверном escaping опровергнуто, если oldScannerMatches=True. Новый R0C scan дополнительно имеет 7 positive/3 negative controls.')
    newsource=(ROOT/'Tests/Reference/hsbi_02b_r0c_independent_oracle.py').read_text()
    harnessRegression={}
    with tempfile.TemporaryDirectory(prefix='r0c-harness-proof-',dir=ROOT/'Tests') as scratch:
        text=modify(newsource,'s,j,a=copy.deepcopy(state),copy.deepcopy(journal),copy.deepcopy(authority)','s,j,a=state,journal,authority')
        path=Path(scratch)/'alias.py';path.write_text(text);alias=load(path,'r0c_alias_harness_proof')
        args=t.fixture();before=copy.deepcopy(args);alias.apply_for_test(*args);changed=args!=before
        alreadyChanged=copy.deepcopy(args);again=alias.apply_for_test(*args)[0]
        harnessRegression['alias']=dict(originalInputsChangedOnFirstCall=changed,oldPatternSecondStatus=again,oldPatternFalsePass=args==alreadyChanged,exactEdit='deep copies -> aliases',correctTestCapturesBeforeFirstCall=True)
        text=modify(newsource,"require(type(request['event']) is int)",'require(True)')
        path=Path(scratch)/'event_type.py';path.write_text(text);etype=load(path,'r0c_event_harness_proof')
        try:t.cases(etype);observed='NO_ERROR'
        except Exception as e:observed='INFRASTRUCTURE_ERROR:'+type(e).__name__
        args=t.fixture();args[0]['event']=True
        harnessRegression['eventType']=dict(fullSuiteOutcome=observed,isolatedTrueOutcome=etype.apply_for_test(*args)[0],interpretation='full-suite exception is never a kill; isolated causal True-vector permits semantic detection')
    q,s,j,a=fixture();q['event']=True;status,ss,jj,aa=old.apply_for_test(q,s,j,a);q['event']=1
    collision=dict(first=status,second=old.authorize(q,ss,jj,aa),keys=[repr(k) for k in jj])
    return dict(t.metadata(),fourMutations=mutations,observations=examples,eventBoolCollision=collision,harnessRegression=harnessRegression,scannerReview=scannerReview,allFourConfirmed=all(x['classification']=='CONFIRMED' for x in mutations),snapshotContentR0B='UNPROVEN: no content receipt in frozen schema')


# Exact source anchors, one causal negative per mutation; positive commit must survive.
CATALOG=[
 ('account','IDENTITY-Account',"if any(request['identity'][k]!=expected[k] for k in ('Broker','Server','Account')):return 'REJECT'","if any(request['identity'][k]!=expected[k] for k in ('Broker','Server')):return 'REJECT'", "if any(request['identity'][k]!=expected[k] for k in ID_FIELDS):return 'REJECT'", "if any(request['identity'][k]!=expected[k] for k in ID_FIELDS if k!='Account'):return 'REJECT'"),
 ('plan','IDENTITY-Plan',"for k in ID_FIELDS):return 'REJECT'","for k in ID_FIELDS if k!='Plan'):return 'REJECT'"),
 ('revision','REVISION-state',"if request['identity']['StateRevision']!=state['revision']:return 'REJECT'","if False:return 'REJECT'"),
 ('revision-exhausted','REVISION-exhausted',"if state['revision']==2**64-1:return 'UNAVAILABLE'","if False:return 'UNAVAILABLE'"),
 ('source','ALLOCATION-source',"if state['source']!=allocation['source']:return 'REJECT'","if False:return 'REJECT'"),
 ('allocation','ALLOCATION-state',"if state['allocation']!=request['allocation']:return 'REJECT'","if False:return 'REJECT'"),
 ('bucket-vector','ALLOCATION-vector',"if state['grant']!=allocation['grant']:return 'CONFLICT'","if False:return 'CONFLICT'"),
 ('precision','AMOUNT-precision',"if amount.quantize(unit(state['digits']))!=amount:return 'REJECT'","if False:return 'REJECT'"),
 ('grant-sum','BALANCE-sum',"if sum(g.values())+state['unallocated']!=state['net']:return False","if False:return False"),
 ('reserved','BALANCE-reserved',"if v[b]>r[b]:return False","if False:return False"),
 ('consumed','BALANCE-consumed',"if r[b]+c[b]!=g[b]:return False","if False:return False"),
 ('replay','REPLAY-changed',"return 'NO_OP' if journal[ek]==canonical(request) else 'CONFLICT'  # GUARD:replay","return 'NO_OP'"),
 ('history','HISTORY-empty',"if record is None:return 'REJECT'","if record is None:return 'ELIGIBLE_FOR_COMMIT'"),
 ('confirmed','SOURCE-unconfirmed',"if not record['closingConfirmed']:return 'REJECT'","if False:return 'REJECT'"),
 ('freshness','SNAPSHOT-expired',"if now>snapshot['validUntil']:return 'UNAVAILABLE'","if False:return 'UNAVAILABLE'"),
 ('role','SOURCE-role',"if record['role'] not in ('BigCore','BigTrend'):return 'REJECT'","if False:return 'REJECT'"),
 ('proof-digest','DIGEST-forged',"if request['proofDigest']!=digest(proof_bundle(record,allocation,expected)):return 'REJECT'","if False:return 'REJECT'"),
 ('raw-sum','RAW-net-mismatch',"if raw!=number(record['rawNet']):return 'CONFLICT'","if False:return 'CONFLICT'"),
 ('posted-net','POSTED-net-mismatch',"if max(Decimal(0),actual)!=state['net']:return 'CONFLICT'","if False:return 'CONFLICT'"),
 ('record-identity','RECORD-Magic',"if any(record['identity'][k]!=expected[k] for k in ('Broker','Server','Account','Symbol','Magic','Deal','Order','Position','Cycle')):return 'REJECT'","if False:return 'REJECT'"),
 ('snapshot-id','SNAPSHOT-id',"if snapshot['id']!=expected['SnapshotID']:return 'REJECT'","if False:return 'REJECT'"),
 ('snapshot-content','SNAPSHOT-content',"if canonical(snapshot)!=receipt:return 'CONFLICT'","if False:return 'CONFLICT'"),
 ('event-type','EVENT-invalid-True',"require(type(request['event']) is int)","require(True)"),
 ('event-range','EVENT-invalid-18446744073709551616',"require(1<=request['event']<=2**64-1)","require(True)"),
 ('future','TIME-future',"if authority['historyObservedAt']>now:return 'UNAVAILABLE'","if False:return 'UNAVAILABLE'"),
 ('missing-field-default','MISSING-event',"    request_shape(request)  # GUARD:request-shape","    if type(request) is dict and 'event' not in request:request['event']=41\n    request_shape(request)  # GUARD:request-shape"),
 ('atomic-input','DIGEST-forged',"    s,j,a=copy.deepcopy(state),copy.deepcopy(journal),copy.deepcopy(authority)","    if status!='ELIGIBLE_FOR_COMMIT' and type(state) is dict:state['revision']+=1\n    s,j,a=copy.deepcopy(state),copy.deepcopy(journal),copy.deepcopy(authority)"),
 ('success-input-alias','APPLY-input-unchanged',"s,j,a=copy.deepcopy(state),copy.deepcopy(journal),copy.deepcopy(authority)","s,j,a=state,journal,authority"),
 ('allocation-internal','ALLOCATION-internal',"if allocation['allocation']!=request['allocation']:return 'CONFLICT'","if False:return 'CONFLICT'"),
 ('time-domain','TIME-domain',"if authority['clockDomain']!='FIXTURE_MONOTONIC' or authority['timeUnit']!='tick':return 'UNAVAILABLE'","if False:return 'UNAVAILABLE'"),
]


def vector(name):
    q,s,j,a=t.fixture();want='REJECT'
    if name=='account':q['identity']['Account']=999
    elif name=='plan':q['identity']['Plan']=999
    elif name=='revision':s['revision']=999
    elif name=='revision-exhausted':
        q['identity']['StateRevision']=2**64-1;s['revision']=2**64-1;a['identity']['StateRevision']=2**64-1;t.seal(q,a);want='UNAVAILABLE'
    elif name=='source':s['source']=('B1','S1',1,999)
    elif name=='allocation':s['allocation']='A2'
    elif name=='bucket-vector':
        s['grant'].update(FinalReserve=Decimal(40),PartialFar=Decimal(10));s['remaining'].update(FinalReserve=Decimal(40),PartialFar=Decimal(10));want='CONFLICT'
    elif name=='precision':q['amount']=Decimal('.005')
    elif name=='grant-sum':
        s['grant']['FinalReserve']=Decimal(40);s['remaining']['FinalReserve']=Decimal(40);a['allocations']['A1']['grant']['FinalReserve']=Decimal(40);t.seal(q,a)
    elif name=='reserved':s['reserved']['PartialFar']=Decimal(1)
    elif name=='consumed':s['consumed']['PartialFar']=Decimal(1)
    elif name=='replay':
        j[('B1','S1',1,41)]=t.encode(q);q['amount']=Decimal(11);want='CONFLICT'
    elif name=='history':a['history']={}
    elif name=='confirmed':a['history'][s['source']]['closingConfirmed']=False;t.seal(q,a)
    elif name=='freshness':a['snapshot']['validUntil']=99;a['snapshotReceipts'][1]=t.encode(a['snapshot']);want='UNAVAILABLE'
    elif name=='role':a['history'][s['source']]['role']='Small';t.seal(q,a)
    elif name in ('proof-digest','atomic-input'):q['proofDigest']='0'*64
    elif name=='raw-sum':a['history'][s['source']]['rawNet']=Decimal(999);t.seal(q,a);want='CONFLICT'
    elif name=='posted-net':
        a['history'][s['source']].update(profit=Decimal(56),rawNet=Decimal(51));a['history'][s['source']]['receipt'].update(raw=Decimal(51),posted=Decimal(51));t.seal(q,a);want='CONFLICT'
    elif name=='record-identity':a['history'][s['source']]['identity']['Magic']=999;t.seal(q,a)
    elif name=='snapshot-id':a['snapshot']['id']=999;a['snapshotReceipts'][999]=t.encode(a['snapshot'])
    elif name=='snapshot-content':a['snapshot']['marketFingerprint']='OTHER';want='CONFLICT'
    elif name=='event-type':q['event']=True
    elif name=='event-range':q['event']=2**64
    elif name=='future':a['historyObservedAt']=1000;want='UNAVAILABLE'
    elif name=='missing-field-default':q.pop('event')
    elif name=='success-input-alias':want='COMMITTED_IN_MEMORY'
    elif name=='allocation-internal':a['allocations']['A1']['allocation']='OTHER';t.seal(q,a);want='CONFLICT'
    elif name=='time-domain':
        a['clockDomain']='UTC';a['snapshot']['clockDomain']='UTC';a['snapshotReceipts'][1]=t.encode(a['snapshot']);want='UNAVAILABLE'
    else:raise AssertionError(name)
    return (q,s,j,a),want


def evaluate(m,args):
    before=copy.deepcopy(args);status,s,j,a=m.apply_for_test(*args)
    return dict(status=status,stateUnchanged=s==before[1],journalUnchanged=j==before[2],authorityUnchanged=a==before[3],inputsUnchanged=args==before,remaining=s['remaining']['FinalReserve'],consumed=s['consumed']['FinalReserve'],revision=s['revision'])


def mutations():
    path=ROOT/'Tests/Reference/hsbi_02b_r0c_independent_oracle.py';source=path.read_text();base=load(path,'r0c_mutation_base')
    baseline=t.cases(base);assert all(x['result']=='PASS' for x in baseline)
    output=[]
    with tempfile.TemporaryDirectory(prefix='r0c-mutations-',dir=ROOT/'Tests') as scratch:
        for name,target,*changes in CATALOG:
            edited=source
            for old,new in zip(changes[::2],changes[1::2]):edited=modify(edited,old,new)
            p=Path(scratch)/(name+'.py');p.write_text(edited)
            item=dict(MutationID=name,TargetFile=str(path.relative_to(ROOT)),TargetFunction='apply_for_test' if name=='atomic-input' else 'authorize/balance/shape',OriginalSourceHash=hashlib.sha256(source.encode()).hexdigest(),MutantSourceHash=hashlib.sha256(edited.encode()).hexdigest(),ExactEdit=[dict(before=x,after=y) for x,y in zip(changes[::2],changes[1::2])],CausalTestID=target)
            try:
                m=load(p,'r0c_mutant_'+name)
                control=evaluate(m,t.fixture());originalControl=evaluate(base,t.fixture())
                args,want=vector(name);original=evaluate(base,copy.deepcopy(args));negative=evaluate(m,copy.deepcopy(args))
                expected=dict(status=want,stateUnchanged=True,journalUnchanged=True,authorityUnchanged=True,inputsUnchanged=True)
                if name=='success-input-alias':expected=dict(status='COMMITTED_IN_MEMORY',inputsUnchanged=True,remaining=Decimal(40),consumed=Decimal(10),revision=2)
                originalOK=all(original[k]==v for k,v in expected.items())
                # Positive control checks financial success, separate from immutable-input negative.
                positiveOK=all(control[k]==v for k,v in dict(status='COMMITTED_IN_MEMORY',remaining=Decimal(40),consumed=Decimal(10),revision=2).items())
                changed=any(negative[k]!=v for k,v in expected.items())
                verdict='MUTATION_KILLED' if originalOK and positiveOK and changed else 'MUTATION_SURVIVED'
                item.update(MutationVerdict=verdict,PositiveControlResult=control,OriginalPositiveControl=originalControl,OriginalNegativeResult=original,MutantNegativeResult=negative,MathematicalExpected=expected,OriginalNegativePass=originalOK,PositiveControlPass=positiveOK)
            except Exception as e:
                item.update(MutationVerdict='INFRASTRUCTURE_ERROR',errorType=type(e).__name__,message=str(e))
            output.append(item)
    return dict(t.metadata(),catalogSize=len(output),killed=sum(x['MutationVerdict']=='MUTATION_KILLED' for x in output),survived=sum(x['MutationVerdict']=='MUTATION_SURVIVED' for x in output),infrastructureErrors=sum(x['MutationVerdict']=='INFRASTRUCTURE_ERROR' for x in output),mutations=output)


def main():
    p=argparse.ArgumentParser();p.add_argument('--reproduce',action='store_true');p.add_argument('--output');a=p.parse_args()
    started=t.metadata()['executedUtc']
    result=reproduce() if a.reproduce else mutations()
    result.update(StartedUtc=started,FinishedUtc=t.metadata()['executedUtc'],Command=[sys.executable,*sys.argv],SourceHashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (Path(__file__).resolve(),Path(t.__file__).resolve())})
    result['ExitCode']=int(not result['allFourConfirmed']) if a.reproduce else int(result['survived']+result['infrastructureErrors']>0)
    if a.output:t.save(a.output,result)
    print(json.dumps({k:v for k,v in result.items() if k not in ('mutations','fourMutations','observations')},ensure_ascii=False))
    for row in result.get('mutations',[]):print(row['MutationID'],row['MutationVerdict'],row.get('errorType',''))
    return int(not result['allFourConfirmed']) if a.reproduce else int(result['survived']+result['infrastructureErrors']>0)


if __name__=='__main__':raise SystemExit(main())
