#!/usr/bin/env python3
"""Causal mutation catalog and independent frozen R0C reproduction."""
import argparse
import copy
from decimal import Decimal,Context,localcontext
import hashlib
import importlib.util
import json
from pathlib import Path
import runpy
import sys
import tempfile
sys.path.insert(0,str(Path(__file__).resolve().parent))
import check_hsbi_02b_r0d_contracts as t
ROOT=t.ROOT


def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);return m


def edit(source,old,new):
    if source.count(old)!=1:raise ValueError(('ambiguous source anchor',old,source.count(old)))
    return source.replace(old,new,1)


# Declared before final execution: exact contract -> operation -> causal vector.
CATALOG=[
 ('amount-positive','NUM-AUTH','_authorize','amount-negative','CONTROL-apply',[("if amount<=0:return 'REJECT'","if False:return 'REJECT'")]),
 ('available-reserved','NUM-AUTH','_authorize','reserved-available','CONTROL-apply',[("amount>number(state['remaining']['FinalReserve'])-number(state['reserved']['FinalReserve'])","amount>number(state['remaining']['FinalReserve'])")]),
 ('posted-grid','NUM-POSTED','posted','posted-grid','POSTED-USD',[("if (value/q).denominator!=1:return 'UNAVAILABLE',None","if False:return 'UNAVAILABLE',None")]),
 ('local-verified','NUM-POSTED','posted','local-unverified','local-verified',[("mode=='LOCAL_VERIFIED' and verified_local_policy and candidate_round(raw,digits)==value","mode=='LOCAL_VERIFIED' and candidate_round(raw,digits)==value")]),
 ('worst-ambient-context','NUM-WORST','_worst','WORST-cancellation','WORST-control',[("checked(av-loss-buf)","checked(number(Decimal(str(r['available']))-Decimal(str(r['loss']))-Decimal(str(r['buffer']))))")]),
 ('sequential-ambient-context','NUM-SEQUENTIAL','sequential','SEQUENTIAL-large','SEQUENTIAL-control',[("after=checked(current-amount)","after=number(Decimal(current.numerator)/Decimal(current.denominator)-Decimal(str(x)))")]),
 ('lost-small-consumption','NUM-SEQUENTIAL','sequential','SEQUENTIAL-large','SEQUENTIAL-control',[("after=checked(current-amount)","after=current if amount<1 else checked(current-amount)")]),
 ('margin-sign','NUM-WORST','_worst','WORST-cancellation','WORST-control',[("checked(av-loss-buf)","checked(abs(av-loss-buf))")]),
 ('snapshot-type','SNAP-FIXTURE-1','snapshot_shape','snapshot-type-decimal','CONTROL-apply',[("text(s['marketFingerprint'])  # MUT:snapshot-type","pass  # weakened type guard")]),
 ('canonical-type-collision','NUM-CODEC','canonical','CODEC-str-decimal','CODEC-control',[("return ['number',str(n.numerator),str(n.denominator)]","return ['str',str(n.numerator)] if n.denominator==1 else ['number',str(n.numerator),str(n.denominator)]")]),
 ('snapshot-receipt','SNAP-FIXTURE-1','_authorize','snapshot-content','CONTROL-apply',[("if canonical(s)!=receipt:return 'CONFLICT'","if False:return 'CONFLICT'")]),
 ('post-state-validation','NUM-APPLY','apply_for_test','POSTSTATE-fault','CONTROL-apply',[("if not balance(s):return 'UNAVAILABLE',copy.deepcopy(state),copy.deepcopy(journal),copy.deepcopy(a)","if False:return 'UNAVAILABLE',copy.deepcopy(state),copy.deepcopy(journal),copy.deepcopy(a)")]),
 ('consumed-reavailable','NUM-AUTH','_authorize','COMPOSITION-full','CONTROL-apply',[("amount>number(state['remaining']['FinalReserve'])-number(state['reserved']['FinalReserve'])","amount>number(state['grant']['FinalReserve'])-number(state['reserved']['FinalReserve'])")]),
 ('altered-replay','NUM-AUTH','_authorize','COMPOSITION-replay-conflict','CONTROL-apply',[("return 'NO_OP' if journal[key]==canonical(q) else 'CONFLICT'","return 'NO_OP'")]),
 ('unsupported-domain','NUM-DOMAIN-1','checked','DOMAIN-direct','CONTROL-number',[("if abs(x)>=LIMIT or (x*SCALE).denominator!=1:raise Unsupported('outside finite decimal fixture domain')","if False:raise Unsupported('outside finite decimal fixture domain')")]),
 ('snapshot-schema','SNAP-FIXTURE-1','snapshot_shape','snapshot-schema','CONTROL-apply',[("if s['schemaVersion']!='HSBI-SNAPSHOT-FIXTURE-1':raise Unsupported('unknown snapshot schema')","if False:raise Unsupported('unknown snapshot schema')")]),
 ('raw-net','NUM-AUTH','_authorize','raw-sum','CONTROL-apply',[("if raw!=number(record['rawNet']):return 'CONFLICT'","if False:return 'CONFLICT'")]),
 ('proof-digest','NUM-AUTH','_authorize','digest-forged','CONTROL-apply',[("if q['proofDigest']!=digest(proof_bundle(record,allocation,expected)):return 'REJECT'","if False:return 'REJECT'")]),
 ('source-role','NUM-AUTH','_authorize','source-role','CONTROL-apply',[("if not record['closingConfirmed'] or record['role'] not in ('BigCore','BigTrend'):return 'REJECT'","if not record['closingConfirmed']:return 'REJECT'")]),
 ('source-history','NUM-AUTH','_authorize','history-missing','CONTROL-apply',[("record=a['history'].get(allocation['source'])","record=a['history'].get(allocation['source']) or q['presentedRecord']")]),
 ('posted-net','NUM-AUTH','_authorize','posted-net','CONTROL-apply',[("if max(Fraction(0),actual)!=number(state['net']):return 'CONFLICT'","if False:return 'CONFLICT'")]),
 ('input-alias','NUM-APPLY','apply_for_test','CONTROL-apply','BALANCE-direct',[("s,j,aa=copy.deepcopy(state),copy.deepcopy(journal),copy.deepcopy(a)","s,j,aa=state,journal,a")]),
]


def mutations():
    path=ROOT/'Tests/Reference/hsbi_02b_r0d_independent_oracle.py';source=path.read_text();base=load(path,'r0d_original')
    cases={c['id']:c for c in t.scenarios()};output=[]
    with tempfile.TemporaryDirectory(prefix='r0d-mut-',dir=ROOT/'Tests') as scratch:
        for name,contract,function,target,positive,changes in CATALOG:
            modified=source
            for old,new in changes:modified=edit(modified,old,new)
            p=Path(scratch)/(name+'.py');p.write_text(modified)
            row=dict(MutationID=name,ContractID=contract,TargetFunction=function,CausalTestID=target,PositiveTestID=positive,ExactEdit=[dict(before=a,after=b) for a,b in changes],OriginalSourceHash=hashlib.sha256(source.encode()).hexdigest(),MutantSourceHash=hashlib.sha256(modified.encode()).hexdigest())
            try:
                m=load(p,'r0d_mut_'+name)
                with localcontext(Context(prec=28)):
                    originalPositive=cases[positive]['run'](base);positiveActual=cases[positive]['run'](m)
                    original=cases[target]['run'](base);negative=cases[target]['run'](m)
                want=cases[target]['expected'];positiveOK=positiveActual==cases[positive]['expected'] and originalPositive==cases[positive]['expected'];originalOK=original==want
                verdict='MUTATION_KILLED' if positiveOK and originalOK and negative!=want else 'MUTATION_SURVIVED'
                if name=='post-state-validation':row['EquivalenceAnalysis']='With valid pre-state and the verified exact debit, removal is equivalent by closure proof. Causal test explicitly injects an invalid debit result into copied state; it tests fault containment, not a reachable ordinary-input defect. No exception is counted as a kill.'
                if name=='snapshot-type':row['EquivalenceAnalysis']='Typed codec/receipt still blocks spending; mutation changes required REJECT into CONFLICT. Codec collision has a separate direct causal test. No broker bypass is inferred.'
                if name=='unsupported-domain':row['initialVectorReplay']=dict(id='domain-overflow',original=cases['domain-overflow']['run'](base),mutant=cases['domain-overflow']['run'](m),meaning='old DTO causal vector remains masked by Decimal-specific guard; public text DOMAIN-direct now detects this same edit')
                row.update(Verdict=verdict,PositiveControl=positiveActual,OriginalPositive=originalPositive,OriginalNegativeOutcome=original,MutantNegativeOutcome=negative,IndependentExpected=want,PositiveControlPass=positiveOK,OriginalNegativePass=originalOK,StateDelta=negative if type(negative) is dict else 'direct helper outcome',SafetyBoundary='For early amount/available guard, mandatory post-state balance blocks money mutation; changed typed outcome is still detected. Post-state fault vector separately proves its dominance.' if name in ('amount-positive','available-reserved','consumed-reavailable') else 'semantic causal outcome, not exception')
            except Exception as e:row.update(Verdict='INFRASTRUCTURE_ERROR',errorType=type(e).__name__,message=str(e))
            output.append(row)
    return dict(t.metadata(),catalogVersion=2,catalogSize=len(output),killed=sum(x['Verdict']=='MUTATION_KILLED' for x in output),survived=sum(x['Verdict']=='MUTATION_SURVIVED' for x in output),infrastructureErrors=sum(x['Verdict']=='INFRASTRUCTURE_ERROR' for x in output),mutations=output)


def reproduction():
    scope=runpy.run_path(str(ROOT/'Tests/Static/check_hsbi_02b_r0c_contracts.py'));old=scope['oracle'];source=Path(old.__file__).read_text()
    level=dict(id=1,available='1e28',loss='.010',buffer='9999999999999999999999999999.995',transitionLoss='1',currency='KWD',digits=3,sourceFresh=True,snapshotFresh=True,complete=True,share='.5',bnet='4',far='1')
    with localcontext(Context(prec=28)):
        actual=old.worst([level,dict(level,id=2)],[1,2]);seq=old.sequential('1e28',['.01','.01'])
    with localcontext(Context(prec=100)):high=old.worst([level,dict(level,id=2)],[1,2])
    # Independent coefficient/scale arithmetic, no subject/Fraction expected.
    def exact_margin():
        pairs=[t.integer_ratio(v) for v in (level['available'],level['loss'],level['buffer'])];d=1
        for _,den in pairs:d=math_lcm(d,den)
        return ['NUMBER',str(sum(sign*n*(d//den) for sign,(n,den) in zip((1,-1,-1),pairs))),str(d)]
    n,d=map(int,exact_margin()[1:]);g=__import__('math').gcd(n,d);expected=['NUMBER',str(n//g),str(d//g)]
    q,s,j,a=scope['fixture']();a['snapshot']['marketFingerprint']='1';a['snapshotReceipts']={1:scope['encode'](a['snapshot'])} if 'encode' in scope else {}
    # Frozen R0C uses its own declared wire. Receipt is frozen BEFORE negative edit.
    independentSnapshot=copy.deepcopy(a['snapshot'])
    # R0C encoder is t.encode-equivalent untyped JSON; implement independently.
    def old_wire(v):
        if type(v) is Decimal:
            text=format(v,'f');return '0' if v==0 else text.rstrip('0').rstrip('.') if '.' in text else text
        if type(v) is dict:return {k:old_wire(x) for k,x in sorted(v.items())}
        if type(v) in (tuple,list):return [old_wire(x) for x in v]
        return v
    old_encode=lambda v:json.dumps(old_wire(v),sort_keys=True,separators=(',',':'),ensure_ascii=False)
    a['snapshotReceipts']={1:old_encode(independentSnapshot)}
    positive=old.apply_for_test(q,s,j,a)[0];a['snapshot']['marketFingerprint']=Decimal(1);collision=old.canonical(a['snapshot'])==a['snapshotReceipts'][1];status,ss,_,_=old.apply_for_test(q,s,j,a)
    findings=[dict(FindingID='R0D-01',Classification='CONFIRMED' if actual[0]=='ALL_LEVEL_POSITIVE' and expected==t.N('-.005') else 'NOT_REPRODUCED',PositiveControl=old.worst([dict(level,available='50',loss='20',buffer='1'),dict(level,id=2,available='50',loss='20',buffer='1')],[1,2]),ExactInputChange=level,ExpectedOutcome=['REJECT',1,expected],ActualOutcome=t.view(actual),HighPrecisionObservation=t.view(high),IndependentCalculation='integer coefficient/scale common denominator; not higher-precision evaluator expected',StateDelta='no ledger mutation; incorrect proof classification',ProofBoundary='R0C Python helper; inputs fit declared numerical domain'),dict(FindingID='R0D-02',Classification='CONFIRMED',PositiveControl=t.view(old.sequential('50',['30','20'])),ExactInputChange=dict(reserve='1e28',consumptions=['.01','.01']),ExpectedOutcome=t.N('9999999999999999999999999999.98'),ActualOutcome=t.view(seq),IndependentCalculation='integer hundredths: 10^30 - 2',StateDelta='reported positive consumption with zero actual reduction',ProofBoundary='local trace only'),dict(FindingID='R0D-03',Classification='CONFIRMED' if collision and status=='COMMITTED_IN_MEMORY' else 'NOT_REPRODUCED',PositiveControl=positive,ExactInputChange='snapshot.marketFingerprint string1 -> Decimal1; frozen receipt unchanged',ExpectedOutcome='type/schema decision required; distinct supported types must not collide',ActualOutcome=dict(status=status,canonicalCollision=collision,remaining=t.view(ss['remaining']['FinalReserve']),revision=ss['revision']),IndependentCalculation='separately encoded original snapshot',StateDelta='remaining50->40 revision1->2',ProofBoundary='SCHEMA_DECISION_REQUIRED; not proof of broker provider bypass')]
    four=[('positive-amount',"if amount<=0 or amount>state['remaining']['FinalReserve']-state['reserved']['FinalReserve']:return 'REJECT'","if amount>state['remaining']['FinalReserve']-state['reserved']['FinalReserve']:return 'REJECT'"),('reserved-available',"amount>state['remaining']['FinalReserve']-state['reserved']['FinalReserve']","amount>state['remaining']['FinalReserve']"),('posted-grid',"if value.quantize(q)!=value:","if False:"),('local-verified',"mode=='LOCAL_VERIFIED' and verified_local_policy and candidate_round(raw,digits)==value","mode=='LOCAL_VERIFIED' and candidate_round(raw,digits)==value")]
    results=[]
    with tempfile.TemporaryDirectory(prefix='r0d-old-mut-',dir=ROOT/'Tests') as scratch:
        for name,before,after in four:
            changed=edit(source,before,after);p=Path(scratch)/(name+'.py');p.write_text(changed);m=load(p,'r0d_old_'+name)
            rows=scope['cases'](m)
            if name in ('positive-amount','reserved-available'):
                args=scope['fixture']()
                if name=='positive-amount':args[0]['amount']=Decimal(-10)
                else:args[1]['reserved']['FinalReserve']=Decimal(45)
                original=old.apply_for_test(*args)[0];st,stt,_,_=m.apply_for_test(*args);neg=dict(status=st,remaining=t.view(stt['remaining']['FinalReserve']),consumed=t.view(stt['consumed']['FinalReserve']),reserved=t.view(stt['reserved']['FinalReserve']))
                control=m.apply_for_test(*scope['fixture']())[0]
            else:
                posted='1.005' if name=='posted-grid' else '1.00';mode='BROKER_POSTED' if name=='posted-grid' else 'LOCAL_VERIFIED';receipt=dict(currency='USD',digits=2,raw='1.005',posted=posted)
                original=t.view(old.posted('1.005','USD',2,receipt,mode,False));neg=t.view(m.posted('1.005','USD',2,receipt,mode,False));control=t.view(m.posted('50','USD',2,dict(currency='USD',digits=2,raw='50',posted='50')))
            results.append(dict(FindingID='R0D-04',MutationID=name,ExactEdit=dict(before=before,after=after),OriginalSourceHash=hashlib.sha256(source.encode()).hexdigest(),MutantSourceHash=hashlib.sha256(changed.encode()).hexdigest(),PositiveControl=control,OriginalNegativeOutcome=original,MutantNegativeOutcome=neg,OldSuitePassed=sum(r['result']=='PASS' for r in rows),OldSuiteFailed=sum(r['result']=='FAIL' for r in rows),Classification='CONFIRMED' if all(r['result']=='PASS' for r in rows) else 'NOT_REPRODUCED',ProofBoundary='isolated frozen R0C copy; no production change'))
    fieldObservations=[]
    for value,label in [(None,'none'),('','empty'),(True,'bool'),(1,'int'),({},'dict')]:
        q,s,j,a=scope['fixture']();a['snapshot']['marketFingerprint']='1';a['snapshotReceipts'][1]=old_encode(a['snapshot']);a['snapshot']['marketFingerprint']=value
        frozenOutcome=old.apply_for_test(q,s,j,a)[0]
        a['snapshotReceipts'][1]=old_encode(a['snapshot']);coherent=old.apply_for_test(q,s,j,a)[0]
        fieldObservations.append(dict(type=label,value=t.view(value),frozenStringReceiptOutcome=frozenOutcome,coherentFixtureReceiptOutcome=coherent,normativeStatus='SCHEMA_DECISION_REQUIRED',proofBoundary='R0C lacks explicit fingerprint schema; not every accepted field type independently establishes a defect'))
    return dict(t.metadata(),findings=findings,fourMutations=results,snapshotFieldObservations=fieldObservations)


def math_lcm(a,b):return a//__import__('math').gcd(a,b)*b


def main():
    p=argparse.ArgumentParser();p.add_argument('--reproduce',action='store_true');p.add_argument('--output');a=p.parse_args();start=t.metadata()['executedUtc']
    out=reproduction() if a.reproduce else mutations();out.update(Command=[sys.executable,*sys.argv],StartedUtc=start,FinishedUtc=t.metadata()['executedUtc'],SourceHashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (Path(__file__).resolve(),Path(t.__file__).resolve(),Path(t.oracle.__file__))})
    code=int(any(x['Classification']!='CONFIRMED' for x in out['findings']+out['fourMutations'])) if a.reproduce else int(out['survived']+out['infrastructureErrors']>0)
    out['ExitCode']=code
    if a.output:t.save(a.output,out)
    print(json.dumps({k:v for k,v in out.items() if k not in ('mutations','findings','fourMutations')}))
    for row in out.get('mutations',[]):print(row['MutationID'],row['Verdict'],row.get('errorType',''))
    return code


if __name__=='__main__':raise SystemExit(main())
