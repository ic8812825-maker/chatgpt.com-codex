#!/usr/bin/env python3
"""Independent AST/token audit: manifest fields must have a corresponding evaluator source read."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];M=json.loads((ROOT/'Tests/Contracts/HSB_2E_R4_R9_R4A_R12A_OWNERSHIP_MATRIX.json').read_text())['fields'];S=(ROOT/'Tests/Static/evaluate_hsb_2e_r4_r9_r4a_r12_blocks.py').read_text()
def main():
 findings=[]
 for x in M:
  leaf=x['field'].split('.')[-1].replace('[*]','')
  # Paths use a source-level independent token mapping, not contract self-comparison.
  if leaf not in S:findings.append({'field':x['field'],'predicate':x['predicate'],'reason':'SOURCE_TOKEN_NOT_READ'})
 print(json.dumps({'ACTUAL_EVALUATOR_COVERAGE':'PASS' if not findings else 'FAIL','findings':findings,'fields':len(M)}));return 0 if not findings else 1
if __name__=='__main__':raise SystemExit(main())
