#!/usr/bin/env python3
"""Independent AST audit: a frozen ownership field must feed a FAIL-capable evaluator guard."""
import ast,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
M=json.loads((ROOT/'Tests/Contracts/HSB_2E_R4_R9_R4A_R12A_OWNERSHIP_MATRIX.json').read_text())['fields']
SRC=ROOT/'Tests/Static/evaluate_hsb_2e_r4_r9_r4a_r12a_implementation.py'
FUNCTION={
 'POSITION_VALIDATION':'evaluate_position_validation','INTENT_VALIDATION':'evaluate_intent_validation',
 'DEAL_EVENT_UNIQUENESS':'evaluate_deal_event_uniqueness','DEAL_POSITION_INTENT_BINDING':'evaluate_deal_position_intent_binding',
 'PERSISTED_LEDGER_REVALIDATION':'evaluate_persisted_ledger_revalidation','BATCH_ATOMICITY':'evaluate_batch_atomicity','PER_TICKET_FILL':'evaluate_per_ticket_fill'}
# Explicit, independently maintained source obligations; it is not generated from the contract.
READS={
 'positions[*].ticket':'ticket','positions[*].direction':'direction','positions[*].role':'role','positions[*].volume':'volume','positions[*].openPrice':'openPrice',
 'intents[*].intentId':'intentId','intents[*].requestedVolume':'requestedVolume','intents[*].createdTimestamp':'createdTimestamp','intents[*].expiresTimestamp':'expiresTimestamp',
 'deals[*].dealId':'dealId','events[*].eventId':'eventId','deals[*].eventId':'eventId','deals[*].positionTicket':'positionTicket','deals[*].intentId':'intentId',
 'persistedState.consumedDealIds':'consumedDealIds','persistedState.authoritativeLedgerRoot':'authoritativeLedgerRoot',
 'context.transactionId':'transactionId','context.actionId':'actionId','phase':'phase','deals[*].volume':'volume'}
def main():
 tree=ast.parse(SRC.read_text()); funcs={x.name:x for x in tree.body if isinstance(x,ast.FunctionDef)};findings=[];rows=[]
 for field in M:
  pid=field['predicate'];fn=FUNCTION[pid];node=funcs[fn];text=ast.get_source_segment(SRC.read_text(),node) or ''
  token=READS[field['field']];read=token in text
  # Follow one local assignment layer: source fields are often normalized into Decimal aliases.
  aliases={token}
  for assignment in ast.walk(node):
   if isinstance(assignment,(ast.Assign,ast.AnnAssign)) and token in ast.unparse(assignment.value):
    targets=assignment.targets if isinstance(assignment,ast.Assign) else [assignment.target]
    aliases.update(t.id for t in targets if isinstance(t,ast.Name))
   if isinstance(assignment,ast.Assign) and any(a in ast.unparse(assignment.value) for a in aliases):
    aliases.update(t.id for t in assignment.targets if isinstance(t,ast.Name))
  # A semantic use requires a field (or local derivative) in an If test whose body returns fail(...).
  semantic=False
  for branch in ast.walk(node):
   if not isinstance(branch,ast.If) or not any(a in ast.unparse(branch.test) for a in aliases): continue
   if any(isinstance(y,ast.Return) and isinstance(y.value,ast.Call) and getattr(y.value.func,'id','')=='fail' for y in ast.walk(branch)):
    semantic=True
    break
  if not semantic:findings.append({'field':field['field'],'predicate':pid,'function':fn,'reason':'NOT_READ_IN_FAIL_CAPABLE_SEMANTIC_GUARD'})
  rows.append({'predicate':pid,'field':field['field'],'function':fn,'evaluatorReads':read,'semanticUse':semantic,'status':'PASS' if semantic else 'FAIL'})
 out={'ACTUAL_EVALUATOR_COVERAGE':'PASS' if not findings else 'FAIL','source':str(SRC.relative_to(ROOT)),'rows':rows,'findings':findings}
 print(json.dumps(out,sort_keys=True));return 0 if not findings else 1
if __name__=='__main__':raise SystemExit(main())
