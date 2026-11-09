#!/usr/bin/env python3
"""Versioned semantic C1 mutations; typed status kills separated from unsafe acceptance."""
import ast,hashlib,importlib.util,json,sys,tempfile
from pathlib import Path
import check_hsbi_02b_r0e_c1_contracts as t
ROOT=t.ROOT;TARGET='Tests/Reference/hsbi_02b_r0e_c1_contract_model.py'
def catalog():
 rows=[]
 def add(name,fn,pos,neg,edits,kind='UNSAFE_ACCEPTANCE_KILL',proof=None):rows.append(dict(MutationID='C1-MUT-'+name,TargetFunction=fn,PositiveTestID=pos,NegativeTestID=neg,Edits=edits,KillClass=kind,RedundancyProof=proof))
 add('raw-sum','economic_record','SOURCE-positive','SOURCE-raw',[("raw==number(r['rawNet']) and ",'')])
 add('posted-grid','economic_record','SOURCE-positive','RECORD-grid',[(" and exact.grid(r['postedNet'],r['digits'])",'')])
 add('source-namespace','economic_record','SOURCE-positive','SOURCE-namespace',[("require(source_key(r)==tuple(source))","require(True)")])
 add('balance-reserved','balance','BALANCE-no-reserve','BALANCE-doublecount',[("g!=c+v+f","g!=c+f")])
 add('source-cap','_fund','SOURCE-positive','SOURCE-overfund',[("if total>net:","if False:")])
 add('small-role','_fund','SOURCE-positive','SOURCE-small',[("if role=='Small' and any(values[b]!=0 for b in BUCKETS if b!='ResidualHeld'):","if False:")])
 add('projected-source','economic_record','SOURCE-positive','SOURCE-projected',[("if r['kind']!='ReconciledEconomicNet':","if False:")])
 add('fund-replay','_event','FUND-exact','FUND-changed',[("('NO_OP' if canonical(prior['payload'])==canonical(payload) else 'CONFLICT')","'NO_OP'")])
 add('fund-immutable-before-replay','_fund','FUND-exact','FUND-authority-change',[("if old_source and old_source['recordDigest']!=digest(r):","if False:")])
 for f in ('Broker','Server','Account','Symbol','Magic','Cycle','Position','Deal','Order','Role','EconomicEventID','AllocationEventID','ConsumptionEventID','AllocationID','PolicyVersion','Plan','Revision','Snapshot'):
  add('identity-'+f,'verify_allocation_identity','IDENTITY-control','IDENTITY-foreign-'+f,[("for k in expected) else 'REJECT'  # GUARD:C1-IDENTITY","for k in expected if k!='"+f+"') else 'REJECT'  # GUARD:C1-IDENTITY")])
 add('batch-namespace','assess_batch','BATCH-control','BATCH-foreign-account',[("require(k[:3]==(expected['Broker'],expected['Server'],expected['Account']))","require(True)")])
 add('batch-lineage','assess_batch','BATCH-control','BATCH-foreign-Order',[("require(all(type(fill[f]) is type(expected[f]) and fill[f]==expected[f] for f in ('BatchID','Symbol','Cycle','Order','Position','currency','digits')))","require(True)")])
 add('batch-completeness','assess_batch','BATCH-control','BATCH-pending',[("if unique!=set(required) or volume!=planned:","if False:")])
 add('cost-inventory','cost_coverage','COST-control','COST-missing',[("require(len(set(ids))==len(ids) and set(ids)==set(facts))","require(True)")])
 add('cost-once','cost_coverage','COST-control','COST-omitted',[("require(row['AdditionalDeduction']==needed)","require(True)")],kind='STATUS_CONTRACT_KILL')
 add('available-journal-layer','available','AVAILABLE-control','AVAILABLE-external-missing',[("_reconcile_store(store,authority)\n        return _arithmetic_reserve_balance","pass\n        return _arithmetic_reserve_balance")])
 add('composition-batch','_authorize','APPLY-positive','APPLY-bypass-batch',[("if assessment['status']!='CONFIRMED':","if False:")])
 add('composition-cost','_authorize','APPLY-positive','APPLY-bypass-cost',[("if costs['status']!='COVERED':return _answer('REJECT' if costs['status']=='CONFLICT' else 'UNAVAILABLE')","if costs['status']!='COVERED':costs=_answer('COVERED',AdditionalRisk=Fraction(0))")])
 add('planned-operation','_authorize','APPLY-positive','APPLY-bypass-planned',[("require(number(context['PrincipalAmount'])==number(q['PrincipalAmount']) and all(context[k]==q[k] for k in ('bucket','purpose','intent')))","require(True)")])
 add('composed-replay','_authorize','REPLAY-exact','REPLAY-changed',[("_answer('NO_OP' if canonical(prior['request'])==canonical(q) else 'CONFLICT')","_answer('NO_OP')")])
 add('immutable-before-replay','_authorize','REPLAY-exact','REPLAY-authority',[("if known is not None and known['recordDigest']!=digest(r):","if False:")],kind='STATUS_CONTRACT_KILL')
 add('apply-revalidation','apply_for_test','APPLY-positive','APPLY-bypass-identity',[("result=authorize(q,store,authority)","result=_answer('ELIGIBLE_FOR_COMMIT',DebitAmount=number(q['PrincipalAmount']),RequiredBalance=number(q['PrincipalAmount']),AdditionalRisk=Fraction(0),sourceDigest=digest(economic_record(authority['history'],q['source'])),allocationDigest=digest(authority['allocations'][q['allocation']]),batchDigest=digest(authority['batches'][q['BatchID']]),costDigest=digest(authority['costSets'][q['CostSetID']]))")])
 add('outer-poststate','apply_for_test','APPLY-positive','APPLY-forged-allocation',[("if not balance(b['OriginalGrant'],b['Consumed'],b['Reserved'],b['RemainingFree'],b['Reservations']):return _answer('UNAVAILABLE'),copy.deepcopy(store)","if False:return _answer('UNAVAILABLE'),copy.deepcopy(store)")],kind='REDUNDANT_GUARD_SURVIVOR',proof='Public apply always authorizes: _reconcile_store reconstructs ALL pre-state rows from independent journal. _operate_for_registry_replay calls _apply_registry_delta, which validates selected row before and after exact delta and returns no commit on failure. apply checks returned status. Other rows unchanged. Thus outer repeat is redundant over the declared public input domain; mutation of mandatory private delta itself is outside this equivalence claim.')
 add('snapshot-fresh','verify_allocation_identity','IDENTITY-control','IDENTITY-stale',[("if not context['fresh']:return 'UNAVAILABLE'\n        require(context['AllocationID']","if False:return 'UNAVAILABLE'\n        require(context['AllocationID']")])
 add('batch-policy','assess_batch','BATCH-control','BATCH-unknown-policy',[("if not expected['historyComplete'] or expected['NettingPolicy']!='PROPOSED_SIGNED_BATCH_NET_V1':","if False:")])
 add('cost-provider-complete','cost_coverage','COST-control','COST-provider-incomplete',[("if not expected['Complete']:","if False:")])
 add('cost-headroom','_authorize','APPLY-positive','APPLY-insufficient-headroom',[("number(q['PrincipalAmount'])+costs['AdditionalRisk']","number(q['PrincipalAmount'])")])
 add('receipt-inventory','_reconcile_store','RECOVER-control','RECOVER-no-receipt',[("require(set(store['receipts'])==needed)","require(True)")])
 add('receipt-source','_reconcile_store','RECOVER-control','RECOVER-bad-source-digest',[("require(receipt['sourceDigest']==store['ledger']['sources'][key(q['source'])]['recordDigest'])","require(True)")])
 add('malformed-default-identity','verify_allocation_identity','IDENTITY-control','IDENTITY-malformed-none',[("require(type(presented) is dict and allocation['source']==source)","require(allocation['source']==source)"),("require(set(presented)==set(expected))","presented=copy.deepcopy(expected) if presented is None else presented\n        require(set(presented)==set(expected))")])
 add('event-bool-coercion','_authorize','APPLY-positive','REQUEST-eventbool',[("def _authorize(q,store,a):\n    request_shape(q)","def _authorize(q,store,a):\n    if type(q.get('consumptionEvent')) is bool:q['consumptionEvent']=2\n    request_shape(q)")])
 add('event-range-default','_authorize','APPLY-positive','REQUEST-eventzero',[("def _authorize(q,store,a):\n    request_shape(q)","def _authorize(q,store,a):\n    if q.get('consumptionEvent')==0:q['consumptionEvent']=2\n    request_shape(q)")])
 add('historical-allocation','_reconcile_store','RECOVER-control','RECOVER-historical-allocation',[("require(q['allocationEvent']==historical['allocationEvent'] and receipt['allocationDigest']==digest(historical))","require(True)")])
 add('historical-identity','_reconcile_store','RECOVER-control','RECOVER-historical-identity',[("require(verify_allocation_identity(q['identity'],authority['history'],q['source'],ctx,historical)=='PASS')","require(True)")])
 add('historical-plan','_reconcile_store','RECOVER-control','RECOVER-historical-plan',[("require((ctx['ConsumptionEventID'],ctx['Revision'],number(ctx['PrincipalAmount']),ctx['bucket'],ctx['purpose'],ctx['intent'],ctx['BatchID'],ctx['CostSetID'])==(q['consumptionEvent'],q['revision'],number(q['PrincipalAmount']),q['bucket'],q['purpose'],q['intent'],q['BatchID'],q['CostSetID']))","require(True)")])
 add('digest-format','_reconcile_store','RECOVER-control','RECOVER-digest-format',[(" and all(c in '0123456789abcdef' for c in receipt[field])",'')])
 add('journal-self-repair','_reconcile_store','APPLY-positive','APPLY-bad-journal-entry',[("_validate_core_journal(authority['coreJournal'])","if any(type(e) is not dict for e in authority['coreJournal'].values()):authority['coreJournal']=copy.deepcopy(store['ledger']['events'])")])
 add('malformed-source-ignore','_authorize','APPLY-positive','APPLY-bad-store-source',[("if known is not None:\n        exact.fields(known,('source','recordDigest','granted','net','phase','unallocated'));require(type(known['recordDigest']) is str)","if type(known) is not dict:known=None")],kind='STATUS_CONTRACT_KILL')
 return rows

def materialize(source,spec):
 result=source;edits=[]
 for a,b in spec['Edits']:
  count=result.count(a)
  if count!=1:raise ValueError('Expected unique edit target: '+spec['MutationID']+' count='+str(count))
  edits.append(dict(old=a,new=b,count=count));result=result.replace(a,b)
 ast.parse(result);return result,edits

def run():
 source=(ROOT/TARGET).read_text();tests={x['TestID']:x for x in t.cases()};rows=[]
 for spec in catalog():
  row={k:v for k,v in spec.items() if k!='Edits'};row.update(TargetFile=TARGET,OriginalSourceHash=hashlib.sha256(source.encode()).hexdigest())
  try:
   mutant,edits=materialize(source,spec);row.update(ExactEdit=edits,MutantSourceHash=hashlib.sha256(mutant.encode()).hexdigest())
   with tempfile.TemporaryDirectory(prefix='R0E_C1_mut_',dir=ROOT/'Tests') as td:
    p=Path(td)/'c1_subject.py';p.write_text(mutant);loader=importlib.util.spec_from_file_location('c1_mutant',p);m=importlib.util.module_from_spec(loader);loader.loader.exec_module(m)
    pos=tests[spec['PositiveTestID']];neg=tests[spec['NegativeTestID']]
    op=t.view(pos['run'](t.subject));mp=t.view(pos['run'](m));on=t.view(neg['run'](t.subject));mn=t.view(neg['run'](m));pe=t.view(pos['IndependentExpected']);ne=t.view(neg['IndependentExpected'])
    controls=t.equal(op,pe) and t.equal(mp,pe) and t.equal(on,ne);violates=not t.equal(mn,ne)
    row.update(PositiveExpected=pe,OriginalPositive=op,MutantPositive=mp,IndependentExpected=ne,OriginalNegative=on,MutantNegative=mn,ControlsPass=controls,StateDelta='Explicit in stateful test outcome; pure APIs zero by construction')
    if controls and violates:row['Verdict']=spec['KillClass'] if spec['KillClass']!='REDUNDANT_GUARD_SURVIVOR' else 'UNEXPLAINED_SURVIVOR'
    elif controls and not violates and spec['KillClass']=='REDUNDANT_GUARD_SURVIVOR':
     whole=t.run(m);row['DomainRegression']={k:v for k,v in whole.items() if k not in ('Rows','ContextConfigurations')};row['Verdict']='REDUNDANT_GUARD_SURVIVOR' if not whole['Fail'] and not whole['InfrastructureErrors'] else 'UNEXPLAINED_SURVIVOR'
    else:row['Verdict']='UNEXPLAINED_SURVIVOR'
  except Exception as e:row.update(Verdict='INFRASTRUCTURE_ERROR',ErrorType=type(e).__name__,Error=str(e))
  rows.append(row);print(spec['MutationID'],row['Verdict'],flush=True)
 return dict(CatalogSize=len(rows),Killed=sum(r['Verdict'] in ('UNSAFE_ACCEPTANCE_KILL','STATUS_CONTRACT_KILL') for r in rows),RedundantSurvivors=sum(r['Verdict']=='REDUNDANT_GUARD_SURVIVOR' for r in rows),UnexplainedSurvivors=sum(r['Verdict']=='UNEXPLAINED_SURVIVOR' for r in rows),InfrastructureErrors=sum(r['Verdict']=='INFRASTRUCTURE_ERROR' for r in rows),Rows=rows)
def main():
 started=t.now();out=dict(t.metadata(),**run(),Command=[sys.executable,*sys.argv],StartedUtc=started,FinishedUtc=t.now(),SourceHashes={**t.hashes(),str(Path(__file__).relative_to(ROOT)):hashlib.sha256(Path(__file__).read_bytes()).hexdigest()});out['ExitCode']=int(out['UnexplainedSurvivors']+out['InfrastructureErrors']>0);t.save(ROOT/'Tests/Evidence/NEXT_STAGE_02B_R0E_C1_MUTATION_RESULTS.json',out);return out['ExitCode']
if __name__=='__main__':raise SystemExit(main())
