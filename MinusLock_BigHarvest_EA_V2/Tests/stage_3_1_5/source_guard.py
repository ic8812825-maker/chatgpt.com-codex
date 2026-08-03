#!/usr/bin/env python3
import ast
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def guards():
 oracle=(ROOT/'Tools'/'stage_3_1_5_money_oracle.py').read_text();mutation=(ROOT/'Tools'/'stage_3_1_5_mutation_oracle.py').read_text();tests=(ROOT/'Tests'/'test_stage_3_1_5_money_model.py').read_text();validator=(ROOT/'Tests'/'validate_stage_3_1_5_money_model.py').read_text()
 collected=sum(isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name.startswith('test_') for n in ast.walk(ast.parse(tests)))
 return {'HARDCODED_POSITIVE_COUNT':int('return 38' in tests or 'return 65' in tests),'UNCONDITIONAL_STATUS_PASS':int('for s in STATUSES' in validator),'BLOCKER_FROM_NAME_MEMBERSHIP':int('int(name in mutations)' in mutation),'ZERO_PYTEST_TESTS':int(collected==0),'DIRECT_DISCOVERED_TO_PERSISTED':int('self.states[key] = "PERSISTED"' in oracle),'FINAL_CLOSE_SCALAR_TRUST':int('def final_close_allowed(recovery' in oracle),'UNUSED_DEAL_ENTRY_FIELD':int('.entry' not in oracle)}
def main():
 g=guards()
 for k,v in g.items():print(f'{k}={v}')
 raise SystemExit(any(g.values()))
if __name__=='__main__':main()
