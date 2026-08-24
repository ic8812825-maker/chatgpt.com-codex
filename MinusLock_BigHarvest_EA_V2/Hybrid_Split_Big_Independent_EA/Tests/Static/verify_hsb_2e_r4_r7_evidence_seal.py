#!/usr/bin/env python3
import argparse,hashlib,json
from pathlib import Path
EXPECTED={'BASELINE_RESULT','R6_FALSE_PASS_REPRODUCTION','EXACT_FALSE_PASS_FIXTURES','LOSSLESS_ADAPTER_MAPS','SEMANTIC_ORACLE','CROSS_VERSION_RESULTS','MIGRATION_DECISIONS','SNAPSHOT_CONTEXT_PROOF','CLOSE_SIDE_PROOF','NEW_FAR_PROVENANCE','CERTIFICATE_RECOMPUTATION','INVARIANT_RESULTS','SEMANTIC_MUTATION_CATALOG','MUTATION_RESULTS','SCOPE_AUDIT','PRODUCTION_DIFF','FINAL_VERDICT','IMPLEMENTATION_HANDOFF'}
def run(root):
 root=Path(root).resolve();ev=root/'Tests/Evidence';m=json.loads((ev/'HSB_2E_PREP_R4_R7_MANIFEST.json').read_text());entries=m['entries'];actual={Path(x['path']).stem.removeprefix('HSB_2E_PREP_R4_R7_') for x in entries};hashes=all(hashlib.sha256((root/x['path']).read_bytes()).hexdigest()==x['sha256'] for x in entries);seal=hashlib.sha256(json.dumps(entries,sort_keys=True,separators=(',',':')).encode()).hexdigest();sealed=(ev/'HSB_2E_PREP_R4_R7_EVIDENCE_SEAL_SHA256.txt').read_text().strip()==seal;ok=actual==EXPECTED and len(entries)==len(actual) and hashes and sealed
 print(f'MISSING={len(EXPECTED-actual)}\nEXTRA={len(actual-EXPECTED)}\nDUPLICATES={len(entries)-len(actual)}\nHASH_MISMATCHES={0 if hashes else 1}\nUNSEALED_EVIDENCE={0 if sealed else 1}\nMANIFEST_COMPLETENESS={"PASS" if actual==EXPECTED else "FAIL"}\nEVIDENCE_INTEGRITY={"PASS" if hashes and sealed else "FAIL"}\nRESULT={"PASS" if ok else "FAIL"}');return ok
if __name__=='__main__':p=argparse.ArgumentParser();p.add_argument('--root',required=True);a=p.parse_args();raise SystemExit(0 if run(a.root) else 1)
