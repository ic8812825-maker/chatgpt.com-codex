#!/usr/bin/env python3
import ast
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def _tree(path):return ast.parse(path.read_text())
def guards():
 op=ROOT/'Tools'/'stage_3_1_5_money_oracle.py';mp=ROOT/'Tools'/'stage_3_1_5_mutation_oracle.py';sp=ROOT/'Tests'/'stage_3_1_5'/'scenario_catalog.py';vp=ROOT/'Tests'/'validate_stage_3_1_5_money_model.py';rp=ROOT/'Tests'/'stage_3_1_5'/'restart_fixtures.py';ap=ROOT/'Tests'/'stage_3_1_5'/'counter_audit.py'
 o,m,s,v,r,a=(p.read_text() for p in (op,mp,sp,vp,rp,ap));mt=_tree(mp);at=_tree(ap)
 hardcoded=sum(isinstance(value,ast.Constant) and value.value is True for node in ast.walk(mt) if isinstance(node,ast.Dict) for value in node.values)
 self_compare=sum(isinstance(node,ast.Compare) and ast.dump(node.left)==ast.dump(node.comparators[0]) for node in ast.walk(at) if isinstance(node,ast.Compare) and node.comparators)
 return {
 'HARDCODED_EXTENDED_RESULT':hardcoded,'RESULTS_UPDATE_TRUE':int('results.update({' in m and ':True' in m.replace(' ','')),'MUTATION_POLICY_COPY':int('Observables(' in m or 'class Policy' in m),'RENAME_SELF_COMPARE':self_compare,'LEDGER_COUNTER_FROM_CHANGED_FIELDS':int("'NO_LEDGER_CHANGE':sum(not r.changed_fields" in a),'STATE_COUNTER_FROM_CHANGED_FIELDS':int("'NO_STATE_CHANGE':sum(not r.changed_fields" in a),'SOURCE_POOLS_NOT_SERIALIZED':int("'source_pools':pools" not in o),'POSITIONS_NOT_SERIALIZED':int("'managed_positions':positions" not in o),'SOURCE_POOLS_NOT_RESTORED':int("allocation.source_pools[tickets]=pool" not in o),'OPENING_IN_ALLOCATION':int("closing harvest required" not in o),'TRANSITION_ONLY_RESTART':int('next(iter(ALLOWED_TRANSITIONS' in r),'UNORDERED_NEXT_STATE':int('next(iter(' in r),'REQUIRED_CATEGORIES_NOT_COMPUTED':int('missing_scenario_categories' not in s),'FINAL_CLOSE_REVISIONS_MISSING':int('expected_version' not in o),'VALIDATOR_EXTENDED_PROBES_MISSING':int('extended_counterexample_probes' not in v),'VALIDATOR_EXPLOITS_MISSING':int('SourcePoolPersistence' not in v),
 'EXPECTED_ALIASES_ACTUAL':int('expected=actual' in s),'UNCONDITIONAL_PASS':int('owner==\'pytest\'' in v),'MUTATION_MONEY_ORACLE_MISSING':int('projected_profit(' not in m or 'EconomicLedger(' not in m)}
def main():
 g=guards();[print(f'{k}={x}') for k,x in g.items()];raise SystemExit(any(g.values()))
if __name__=='__main__':main()
