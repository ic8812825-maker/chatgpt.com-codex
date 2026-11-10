#!/usr/bin/env python3
"""C2 semantic mutations: isolated in-memory modules, no original source edits."""
import ast,hashlib,types,sys
from pathlib import Path
import check_hsbi_02b_r0e_c2_contracts as t
import check_hsbi_02b_r0e_c1_mutations as historical
from check_hsbi_02b_r0e_c2_reproduction import SIX
TARGET=t.TARGET

def catalog():
 rows=[]
 def add(i,fn,pos,neg,edits,file=t.TARGET,redundancy=None):rows.append(dict(MutationID='C2-MUT-'+i,TargetFile=file,TargetFunction=fn,PositiveTestID=pos,NegativeTestID=neg,Edits=edits,RedundancyProof=redundancy))
 for r in historical.catalog():
  # New mandatory schema caller makes these old entry-string coercion edits obsolete.
  if r['MutationID'] in ('C1-MUT-event-bool-coercion','C1-MUT-event-range-default'):continue
  proof=r.get('RedundancyProof')
  if r['MutationID'] in ('C1-MUT-malformed-default-identity','C1-MUT-malformed-source-ignore','C1-MUT-digest-format','C1-MUT-journal-self-repair'):
   proof='C2 public authorize/_reconcile_store/verify_allocation_identity validates nested schema before this old clause. Mandatory schema cannot be bypassed by public apply. Original and mutant preserve the typed rejection on this causal input; not an unsafe acceptance kill.'
  rows.append(dict(MutationID='C2-'+r['MutationID'],TargetFile=t.TARGET,TargetFunction=r['TargetFunction'],PositiveTestID='C2-BASE-'+r['PositiveTestID'],NegativeTestID='C2-BASE-'+r['NegativeTestID'],Edits=r['Edits'],RedundancyProof=proof))
 mapping={'receipt-digest':'C2-receipt-digest','receipt-equation':'C2-receipt-equation','planned-purpose':'C2-planned-purpose','planned-intent':'C2-planned-intent','ledger-event':'C2-ledger-allocationEvent','ledger-policy':'C2-ledger-PolicyVersion'}
 for i,a,b in SIX:add(i,'_reconcile_store' if i.startswith('receipt') else '_authorize' if i.startswith('planned') else '_bind_allocation','C2-BASE-RECOVER-control' if i.startswith('receipt') else 'C2-BASE-APPLY-positive',mapping[i],[(a,b)])
 add('receipt-risk-nonnegative','_reconcile_store','C2-BASE-RECOVER-control','C2-receipt-clause-nonnegative',[("number(receipt['AdditionalRisk'])>=0 and ",'')])
 add('receipt-principal','_reconcile_store','C2-BASE-RECOVER-control','C2-receipt-clause-principal',[("number(receipt['DebitAmount'])==number(q['PrincipalAmount']) and ",'')])
 add('receipt-core-debit','_reconcile_store','C2-BASE-RECOVER-control','C2-receipt-clause-core',[(" and number(e['amount'])==number(receipt['DebitAmount'])",'')])
 add('cost-shape-caller','cost_coverage','C2-BASE-COST-control','C2-cost-bool-direct',[("if expected is not None:dto.validate(\"CostSet\",expected)",'pass')],redundancy='Mandatory CostClaim schema rejects the boolean claim before fact comparison; removing only the CostSet caller cannot bypass it. Direct cost_coverage and public apply both preserve rejection. Dual caller mutation separately demonstrates necessity of the complete layer.')
 add('cost-dual-shape-callers','cost_coverage','C2-BASE-COST-control','C2-cost-bool-direct',[("if expected is not None:dto.validate(\"CostSet\",expected)",'pass'),("dto.validate({\"list\":\"CostClaim\"},rows)",'pass')])
 add('bool-id','validate','C2-BASE-APPLY-positive','C2-bool-policy',[("elif spec=='uid':x.require(x.uid(value))","elif spec=='uid':x.require(x.uid(value) or type(value) is bool)")],file=t.SCHEMA)
 add('unknown-fields','validate','C2-BASE-COST-control','C2-schema-unknown-field',[("x.fields(value,tuple(spec['object']))","x.require(type(value) is dict and set(spec['object'])<=value.keys())")],file=t.SCHEMA)
 add('mandatory-authority-caller','_authorize','C2-BASE-APPLY-positive','C2-authority-unused-malformed',[("if a is not None:dto.validate(\"Authority\",a)",'pass'),("if authority is not None:dto.validate(\"Authority\",authority)",'pass')])
 add('json-last-wins','pairs','C2-JSON-control','C2-JSON-duplicate',[("if k in out:raise ValueError('duplicate JSON key: '+k)","if False:raise ValueError('duplicate JSON key: '+k)")],file='Tests/Reference/hsbi_02b_r0e_c2_evidence.py')
 add('json-constants','loads','C2-JSON-control','C2-JSON-nan',[("parse_constant=constant","parse_constant=lambda x:None")],file='Tests/Reference/hsbi_02b_r0e_c2_evidence.py')
 add('json-counter-bool','integer','C2-JSON-control','C2-JSON-counter',[("if type(value) is not int:","if not isinstance(value,int):")],file='Tests/Reference/hsbi_02b_r0e_c2_evidence.py')
 return rows

def clone(src,name):
 m=types.ModuleType(name);m.__file__=name;exec(compile(src,name,'exec'),m.__dict__);return m

def run():
 tests={c['TestID']:c for c in t.cases()};rows=[]
 for spec in catalog():
  row={k:v for k,v in spec.items() if k!='Edits'};src=(t.ROOT/spec['TargetFile']).read_text();row['OriginalSourceHash']=hashlib.sha256(src.encode()).hexdigest()
  try:
   edited=src;edits=[]
   for old,new in spec['Edits']:
    assert edited.count(old)==1,(spec['MutationID'],old,edited.count(old));edited=edited.replace(old,new);edits.append(dict(old=old,new=new))
   ast.parse(edited);row.update(ExactEdit=edits,MutantSourceHash=hashlib.sha256(edited.encode()).hexdigest())
   if spec['TargetFile']==t.SCHEMA:m=clone((t.ROOT/t.TARGET).read_text(),'c2model');m.dto=clone(edited,'c2schema')
   elif spec['TargetFile'].endswith('_evidence.py'):m=clone((t.ROOT/t.TARGET).read_text(),'c2model');m.evidence=clone(edited,'c2evidence')
   else:m=clone(edited,'c2mutant')
   pos,neg=tests[spec['PositiveTestID']],tests[spec['NegativeTestID']];pe=t.view(pos['IndependentExpected']);ne=t.view(neg['IndependentExpected'])
   op,mp,on,mn=[t.view(c['run'](sub)) for c,sub in ((pos,t.subject),(pos,m),(neg,t.subject),(neg,m))]
   controls=op==mp==pe and on==ne;violates=mn!=ne
   row.update(PositiveExpected=pe,OriginalPositive=op,MutantPositive=mp,IndependentExpected=ne,OriginalNegative=on,MutantNegative=mn,ControlsPass=controls,StateDelta='Explicit in stateful outcomes; pure scopes unchanged')
   if controls and violates:row['Verdict']='UNSAFE_ACCEPTANCE_KILL' if ('COMMITTED_IN_MEMORY' in str(mn) or 'RECONCILED_MODEL_ONLY' in str(mn) or 'COVERED' in str(mn) or "'PASS'" in repr(mn)) else 'STATUS_CONTRACT_KILL'
   elif controls and spec.get('RedundancyProof'):
    domain=t.run(m,with_schema=False);row['DomainRegression']={k:v for k,v in domain.items() if k not in ('Rows','SchemaRows','ContextConfigurations')};row['Verdict']='REDUNDANT_GUARD_SURVIVOR' if domain['Fail']==domain['InfrastructureErrors']==0 else 'UNEXPLAINED_SURVIVOR'
   else:row['Verdict']='UNEXPLAINED_SURVIVOR'
  except Exception as e:row.update(Verdict='INFRASTRUCTURE_ERROR',ErrorType=type(e).__name__,Error=str(e))
  rows.append(row);print(spec['MutationID'],row['Verdict'],flush=True)
 return dict(CatalogSize=len(rows),Killed=sum(r['Verdict'].endswith('_KILL') for r in rows),RedundantSurvivors=sum(r['Verdict']=='REDUNDANT_GUARD_SURVIVOR' for r in rows),UnexplainedSurvivors=sum(r['Verdict']=='UNEXPLAINED_SURVIVOR' for r in rows),InfrastructureErrors=sum(r['Verdict']=='INFRASTRUCTURE_ERROR' for r in rows),Rows=rows)
def main():
 started=t.now();out=dict(t.metadata(),**run(),Command=[sys.executable,*sys.argv],StartedUtc=started,FinishedUtc=t.now(),SourceHashes={**t.hashes(),str(Path(__file__).relative_to(t.ROOT)):t.sha(Path(__file__))});out['ExitCode']=int(out['UnexplainedSurvivors']+out['InfrastructureErrors']>0);t.save(t.ROOT/'Tests/Evidence/NEXT_STAGE_02B_R0E_C2_MUTATION_RESULTS.json',out);return out['ExitCode']
if __name__=='__main__':raise SystemExit(main())
