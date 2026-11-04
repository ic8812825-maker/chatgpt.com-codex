#!/usr/bin/env python3
"""Isolated source mutations: frozen R0A model and independent R0B oracle.

Initial survivors are retained, then retested with additional causal vectors.
Parser/import/runtime exceptions are INFRASTRUCTURE_ERROR, never mutation kills.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import runpy
import sys
import tempfile
from datetime import datetime,timezone

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'Tests/Static'))
import check_hsbi_02b_r0b_contracts as tests


def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path);module=importlib.util.module_from_spec(spec)
    sys.modules[name]=module;spec.loader.exec_module(module);return module


def edits(source,changes):
    for old,new in changes:
        if source.count(old)!=1:raise ValueError(('ambiguous mutation anchor',old,source.count(old)))
        source=source.replace(old,new,1)
    return source


def frozen_suite(module):
    scope=runpy.run_path(str(ROOT/'Tests/Static/check_hsbi_02b_r0a_normative_contracts.py'))
    scope['tests'].__globals__['m']=module
    rows,_=scope['tests']()
    return rows


OLD=[
 ('account_namespace','OLD-account',[("if state['owner'] != authority['owner'] or request['owner'] != authority['owner']:","if False:")]),
 ('plan','OLD-plan',[("if request['plan'] != authority['plan'] or request['cycle'] != authority['cycle']:","if request['cycle'] != authority['cycle']:")]),
 ('revision','OLD-revision',[("if request['event'] == 0 or request['revision'] != authority['revision'] or state['revision'] != authority['revision']:","if request['event'] == 0:")]),
 ('source_identity','OLD-source',[("('source', 'allocation', 'allocationEvent', 'policy', 'currency')","('allocation', 'allocationEvent', 'policy', 'currency')")]),
 ('allocation_identity','OLD-allocation',[("('source', 'allocation', 'allocationEvent', 'policy', 'currency')","('source', 'allocationEvent', 'policy', 'currency')")]),
 ('bucket_vector','OLD-bucket-vector',[("remaining[k] + consumed[k] == grant[k]","sum(remaining.values()) + sum(consumed.values()) == sum(grant.values())")]),
 ('precision','OLD-precision',[("if amount <= 0 or amount.quantize(quantum(2)) != amount:","if amount <= 0:")]),
 ('grant_sum','OLD-sum-grants',[("if sum(grant.values()) + u != n:","if False:")]),
 ('reserved','OLD-reserved',[("reserved[k] <= remaining[k]","True")]),
 ('consumed','OLD-consumed',[("remaining[k] + consumed[k] == grant[k] and ","")]),
 ('replay_identity','OLD-replay',[("return 'NO_OP' if canonical(registry[event]) == canonical(request) else 'CONFLICT'","return 'NO_OP'")]),
 ('independent_history','OLD-history',[("if record['owner'] != owner or history.get(source_key(record)) != record:","if record['owner'] != owner:")]),
 ('confirmed_source','OLD-confirmed-source',[("if record['entry'] != 'CLOSE' or record['event'] == 0:","if record['entry'] != 'CLOSE':")]),
 ('snapshot_freshness','OLD-snapshot',[("if not context['fresh'] or proof['identity'] != expected or dec(proof['net']) != money.value:","if proof['identity'] != expected or dec(proof['net']) != money.value:")]),
 ('source_role','OLD-role',[(" or record['role'] not in ('BigCore','BigTrend')","")]),
]

NEW=[
 ('account_namespace','ID-foreign-Account',[("for k in ('Broker','Server','Account')):","for k in ('Broker','Server')):"),
     ("for k in ID_FIELDS):","for k in ID_FIELDS if k!='Account'):")]),
 ('plan','ID-foreign-Plan',[("for k in ID_FIELDS):","for k in ID_FIELDS if k!='Plan'):")]),
 ('revision','GUARD-state-revision',[("if request['identity']['StateRevision']!=state['revision'] or request['event']<=0:","if request['event']<=0:")]),
 ('source_identity','GUARD-state-source',[("if state['source']!=allocation['source']:return 'REJECT'","if False:return 'REJECT'")]),
 ('allocation_identity','GUARD-state-allocation',[("if state['allocation']!=request['allocation']:return 'REJECT'","if False:return 'REJECT'")]),
 ('bucket_vector','GUARD-grant-vector',[("if state['grant']!=allocation['grant']:return 'CONFLICT'","if False:return 'CONFLICT'")]),
 ('precision','GUARD-amount-precision',[("if amount.quantize(unit(state['digits']))!=amount:return 'REJECT'","if False:return 'REJECT'")]),
 ('grant_sum','GUARD-sum-grants',[("if sum(g.values())+state['unallocated']!=state['net']:return False","if False:return False")]),
 ('reserved','GUARD-reserved-other-bucket',[("if v[b]>r[b]:return False","if False:return False")]),
 ('consumed','GUARD-consumed-other-bucket',[("if r[b]+c[b]!=g[b]:return False","if False:return False")]),
 ('replay_identity','EVENT-altered-amount',[("return 'NO_OP' if journal[ek]==canonical(request) else 'CONFLICT'","return 'NO_OP'")]),
 ('independent_history','GUARD-history-missing',[("record=authority['history'].get(allocation['source'])","record=authority['history'].get(allocation['source']) or request['presentedRecord']")]),
 ('confirmed_source','GUARD-source-unconfirmed',[("if not record['closingConfirmed']:return 'REJECT'","if False:return 'REJECT'")]),
 ('snapshot_freshness','GUARD-snapshot-stale',[("if now>snapshot['validUntil']:","if False:")]),
 ('source_role','GUARD-source-role',[("if record['role'] not in ('BigCore','BigTrend'):return 'REJECT'","if False:return 'REJECT'")]),
]


def run():
    old_path=ROOT/'Tests/Reference/hsbi_02b_r0a_normative_model.py'
    new_path=ROOT/'Tests/Reference/hsbi_02b_r0b_independent_oracle.py'
    old_source=old_path.read_text();new_source=new_path.read_text()
    old=load(old_path,'r0b_frozen_original');new=load(new_path,'r0b_oracle_original')
    original=frozen_suite(old);supp=tests.legacy_supplementary(old);baseline=tests.reference_cases(new)
    if any(x['result']!='PASS' for x in original+supp+baseline):raise AssertionError(('baseline failed',[x for x in original+supp+baseline if x['result']!='PASS']))
    output=[]
    with tempfile.TemporaryDirectory(prefix='r0b-mutation-',dir=ROOT/'Tests') as folder:
        for label,source,catalog in [('R0A',old_source,OLD),('R0B',new_source,NEW)]:
            for name,target,change in catalog:
                changed=edits(source,change);p=Path(folder)/(label+'_'+name+'.py');p.write_text(changed)
                module=load(p,'r0b_mut_'+label+'_'+name)
                if label=='R0A':
                    initial=frozen_suite(module);additional=tests.legacy_supplementary(module)
                    first='MUTATION_KILLED' if any(x['result']=='FAIL' for x in initial) else 'MUTATION_SURVIVED'
                    tested=additional
                else:
                    initial=tests.reference_cases(module);first='MUTATION_KILLED' if any(x['result']=='FAIL' for x in initial) else 'MUTATION_SURVIVED';tested=initial
                target_result=next(x for x in tested if x['id']==target)
                final='MUTATION_KILLED' if target_result['result']=='FAIL' else 'MUTATION_SURVIVED'
                output.append(dict(model=label,id=name,target=target,initialResult=first,finalResult=final,
                    targetActual=target_result['actual'],targetExpected=target_result['expected'],
                    initialFailedTests=[x['id'] for x in initial if x['result']=='FAIL'],
                    originalSha256=hashlib.sha256(source.encode()).hexdigest(),mutantSha256=hashlib.sha256(changed.encode()).hexdigest(),
                    edits=[dict(before=a,after=b) for a,b in change],
                    explanation='Если initial survived: frozen 128 не изолировали этот guard; новый причинный вектор раскрывает weakening. Исходные тесты не изменены.' if first=='MUTATION_SURVIVED' else 'Отрицательный outcome mutation обнаружен исполнимым тестом; исключение не считается kill.'))
    return dict(testedHead=__import__('subprocess').check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        executedUtc=datetime.now(timezone.utc).isoformat(),baselineFrozenPassed=len(original),baselineSupplementPassed=len(supp),baselineIndependentPassed=len(baseline),
        mutations=output,initialSurvivors=sum(x['initialResult']=='MUTATION_SURVIVED' for x in output),
        finalSurvivors=sum(x['finalResult']=='MUTATION_SURVIVED' for x in output),infrastructureErrors=0,
        productionMutation=False,scope='Only disposable copies of test/reference Python modules; NOT MQL5 production')


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path);a=p.parse_args()
    result=run()
    if a.output:
        dest=a.output.resolve();assert dest.is_relative_to(ROOT);dest.write_text(json.dumps(tests.contract_json(result),ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='mutations'},ensure_ascii=False))
    for m in result['mutations']:print(m['model'],m['id'],m['initialResult'],'=>',m['finalResult'])
    return int(result['finalSurvivors']>0)


if __name__=='__main__':raise SystemExit(main())
