#!/usr/bin/env python3
"""Causal source mutations. Exceptions are infrastructure errors, never kills."""
import ast,copy,hashlib,importlib.util,json,sys,tempfile
from pathlib import Path
from datetime import datetime,timezone
import check_hsbi_02b_r0e_contracts as t
ROOT=t.ROOT;TARGET='Tests/Reference/hsbi_02b_r0e_contract_model.py'
def catalog():
 return [
 ('source-cap','_fund','D01-prepared-and-split','D07-overfund-prepared',[("if total>net:return 'REJECT',copy.deepcopy(state)","if False:return 'REJECT',copy.deepcopy(state)")]),
 ('reserved-doublecount','balance','D01-zero-reserved','D01-double-count',[("g!=c+v+f","g!=c+f")]),
 ('projected-authority','economic_record','D07-exact-fund-replay','D02-projected-not-source',[("if r['kind']!='ReconciledEconomicNet':","if False:")]),
 ('small-role','_fund','D01-operations','D03-small-isolation',[("if role=='Small' and any(values[b]!=0 for b in BUCKETS if b!='ResidualHeld'):","if False:")]),
 ('replay-payload','_event','D07-exact-consume-replay','D07-altered-consume-replay',[("('NO_OP' if canonical(prior['payload'])==canonical(payload) else 'CONFLICT')","'NO_OP'")]),
 ('expected-magic','verify_identity','D08-independent-control','D08-foreign-Magic',[("for k in expected) else 'REJECT'","for k in expected if k!='Magic') else 'REJECT'")]),
 ('actual-cap','_transition_status','D05-partial-pending','D05-over-cap',[("if loss>number(cap):","if False:")]),
 ('cost-double','costs_status','D06-once','D06-double-cost',[("if row['AlreadyIncluded'] and row['AdditionalDeduction']:","if False:")]),
 ('unknown-history-zero','reserve_available','D02-known-zero','D02-unknown-history',[("def reserve_available(state,history,account,complete=True):\n    if history is None or not complete:return 'UNAVAILABLE',None","def reserve_available(state,history,account,complete=True):\n    if not complete:return 'UNAVAILABLE',None")]),
 ('recovery-rebuild','recover','RESTART-committed','RESTART-forged-consumed',[("if canonical(rebuilt)!=canonical(chosen):","if False:")]),
 ('snapshot-fresh','verify_identity','D08-independent-control','D08-stale-snapshot',[("if not context['fresh']:","if False:")]),
 ('checked-overflow','checked_add','MQL-add-ok','NUM-domain-unsupported',[("if b>0 and a>maximum-b or b<0 and a<minimum-b:","if False:"),("if not minimum<=result<=maximum:","if False:")]),
 ('reservation-owner','_operate','D01-operations','D01-reservation-owner',[("row['Reservations'].get(intent,0)","row['Reserved']"),("b['Reservations'][intent]-=n","b['Reservations'][intent if intent in b['Reservations'] else next(iter(b['Reservations']))]-=n")])]
def main():
 source=(ROOT/TARGET).read_text();tests={x['TestID']:x for x in t.cases()};rows=[]
 for name,fn,pos,neg,edits in catalog():
  row=dict(MutationID='R0E-MUT-'+name,TargetFile=TARGET,TargetFunction=fn,CausalTestID=neg,PositiveTestID=pos,OriginalSourceHash=hashlib.sha256(source.encode()).hexdigest(),ExactEdit=[],IndependentExpected=t.view(tests[neg]['Expected']))
  mutant=source
  try:
   for old,new in edits:
    count=mutant.count(old)
    if not count:raise ValueError('mutation target absent')
    row['ExactEdit'].append(dict(old=old,new=new,count=count));mutant=mutant.replace(old,new)
   ast.parse(mutant);row['MutantSourceHash']=hashlib.sha256(mutant.encode()).hexdigest()
   with tempfile.TemporaryDirectory(prefix='R0E_mut_',dir=ROOT/'Tests') as td:
    p=Path(td)/'r0e_mutant.py';p.write_text(mutant);spec=importlib.util.spec_from_file_location('r0e_mutant',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    op=t.view(tests[pos]['run'](t.model));on=t.view(tests[neg]['run'](t.model));mp=t.view(tests[pos]['run'](m));mn=t.view(tests[neg]['run'](m))
   row.update(PositiveControl=op,MutantPositiveControl=mp,PositiveExpected=t.view(tests[pos]['Expected']),OriginalNegativeOutcome=on,MutantNegativeOutcome=mn,StateDelta='Included in causal outcome for stateful scenarios; identity/arithmetic functions pure')
   row['Verdict']='MUTATION_KILLED' if op==row['PositiveExpected']==mp and on==row['IndependentExpected'] and mn!=row['IndependentExpected'] else 'MUTATION_SURVIVED'
  except Exception as e:row.update(Verdict='INFRASTRUCTURE_ERROR',errorType=type(e).__name__,error=str(e))
  rows.append(row);print(row['MutationID'],row['Verdict'],flush=True)
 out=dict(t.metadata(),Command=[sys.executable,*sys.argv],UTC=datetime.now(timezone.utc).isoformat(),catalogSize=len(rows),killed=sum(r['Verdict']=='MUTATION_KILLED' for r in rows),survived=sum(r['Verdict']=='MUTATION_SURVIVED' for r in rows),infrastructureErrors=sum(r['Verdict']=='INFRASTRUCTURE_ERROR' for r in rows),mutations=rows,SourceHashes={TARGET:hashlib.sha256(source.encode()).hexdigest(),str(Path(__file__).relative_to(ROOT)):hashlib.sha256(Path(__file__).read_bytes()).hexdigest()})
 path=ROOT/'Tests/Evidence/NEXT_STAGE_02B_R0E_MUTATION_RESULTS.json';t.save(path,out);return int(out['survived']+out['infrastructureErrors']>0)
if __name__=='__main__':raise SystemExit(main())
