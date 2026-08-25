#!/usr/bin/env python3
"""Publish the R4-R8 manifest and deterministic evidence seal."""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
EXPECTED = (
    'BASELINE','R7_FALSE_PASS_REPRODUCTION','ORACLE_PROVENANCE','ORACLE_INDEPENDENCE',
    'ADAPTER_MAPS','CALL_GRAPH','CROSS_VERSION_RESULTS','PRICE_AUTHORITY','CERTIFICATE_MATRIX',
    'FILL_CLASSIFICATION','ECONOMIC_AUTHORITY','INVARIANT_RESULTS','MUTATION_RESULTS','HANDOFF',
    'SCOPE_AUDIT','PRODUCTION_DIFF','FINAL_VERDICT',
)
def run(root: str) -> bool:
    project=Path(root).resolve(); evidence=project/'Tests/Evidence'; entries=[]
    for name in EXPECTED:
        path=evidence/f'HSB_2E_PREP_R4_R8_{name}.json'
        entries.append({'path':str(path.relative_to(project)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    manifest={'schemaVersion':1,'entries':entries}
    (evidence/'HSB_2E_PREP_R4_R8_MANIFEST.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
    seal=hashlib.sha256(json.dumps(entries,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    (evidence/'HSB_2E_PREP_R4_R8_EVIDENCE_SEAL_SHA256.txt').write_text(seal+'\n')
    print('PUBLISH_RESULT=PASS');return True
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--root',required=True);args=parser.parse_args();raise SystemExit(0 if run(args.root) else 1)
