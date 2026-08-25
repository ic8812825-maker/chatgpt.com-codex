#!/usr/bin/env python3
"""Independently construct and verify the required R4-R8 evidence set."""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
EXPECTED={'BASELINE','R7_FALSE_PASS_REPRODUCTION','ORACLE_PROVENANCE','ORACLE_INDEPENDENCE','ADAPTER_MAPS','CALL_GRAPH','CROSS_VERSION_RESULTS','PRICE_AUTHORITY','CERTIFICATE_MATRIX','FILL_CLASSIFICATION','ECONOMIC_AUTHORITY','INVARIANT_RESULTS','MUTATION_RESULTS','HANDOFF','SCOPE_AUDIT','PRODUCTION_DIFF','FINAL_VERDICT'}
def run(root: str) -> bool:
    project=Path(root).resolve();evidence=project/'Tests/Evidence';entries=json.loads((evidence/'HSB_2E_PREP_R4_R8_MANIFEST.json').read_text())['entries']
    actual={Path(entry['path']).stem.removeprefix('HSB_2E_PREP_R4_R8_') for entry in entries}
    hashes=all(hashlib.sha256((project/entry['path']).read_bytes()).hexdigest()==entry['sha256'] for entry in entries)
    seal=hashlib.sha256(json.dumps(entries,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    sealed=(evidence/'HSB_2E_PREP_R4_R8_EVIDENCE_SEAL_SHA256.txt').read_text().strip()==seal
    unique=len(entries)==len(actual);complete=actual==EXPECTED;result=hashes and sealed and unique and complete
    print(f'MISSING={len(EXPECTED-actual)}');print(f'EXTRA={len(actual-EXPECTED)}');print(f'DUPLICATES={len(entries)-len(actual)}');print(f'HASH_MISMATCHES={0 if hashes else 1}');print(f'UNSEALED_EVIDENCE={0 if sealed else 1}');print(f'MANIFEST_COMPLETENESS={"PASS" if complete else "FAIL"}');print(f'EVIDENCE_INTEGRITY={"PASS" if hashes and sealed else "FAIL"}');print(f'RESULT={"PASS" if result else "FAIL"}');return result
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--root',required=True);args=parser.parse_args();raise SystemExit(0 if run(args.root) else 1)
