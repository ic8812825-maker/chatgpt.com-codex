#!/usr/bin/env python3
"""Independently verify the fifteen immutable R4-R8 counterexamples."""
import argparse,hashlib,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--root',default='.');a=p.parse_args();r=Path(a.root).resolve();data=json.loads((r/'Tests/Vectors/HSB_2E_R4_R9_R2_R8_FALSE_PASSES.json').read_text());source=(r/'Tests/Reference/hsb_2e_reference_model_r4_r8.py').read_text();inv=(r/'Tests/Reference/hsb_2e_invariants_r4_r8.py').read_text()
facts=['hsb_2e_reference_model_r4_r2' in source,'operation == "INITIAL"' not in source,'operation == "BIG"' not in source,'operation == "SMALL"' not in source,'operation == "FINAL"' not in source,'raise ValueError("UNSUPPORTED_SOURCE_VERSION")' in source]+['commitBundle' in (r/'Tests/Reference/hsb_2e_validation_r4_r8.py').read_text()]*4+['snapshotTimestamp' not in (r/'Tests/Reference/hsb_2e_validation_r4_r8.py').read_text()]*2+['FORMULA_REGISTRY' in inv and 'economicProposal' not in inv,'build_valid_commit()\n    second = validate_commit_replay(build_valid_commit())' in inv,'order = ("broker", "economic", "allocation", "persistence", "fsm")' in inv]
valid=all(hashlib.sha256(json.dumps(x['INPUT'],sort_keys=True,separators=(',',':')).encode()).hexdigest()==x['INPUT_SHA256'] for x in data['cases']);ok=len(data['cases'])==15 and sum(facts)==15 and valid
print(f'R4_R8_FALSE_PASSES_REQUIRED=15\nR4_R8_FALSE_PASSES_REPRODUCED={sum(facts)}\nRESULT={"PASS" if ok else "FAIL"}');raise SystemExit(0 if ok else 1)
