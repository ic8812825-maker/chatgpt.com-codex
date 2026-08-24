#!/usr/bin/env python3
"""R4-R6 immutable-code compatibility at its published baseline."""
import argparse,hashlib,subprocess
from pathlib import Path
BASE='78520488d53f3f19eebc254a9cc5a7338714ceb4'
FILES=('Tests/Reference/hsb_2e_reference_model_r4_r6.py','Tests/Reference/hsb_2e_provenance_model_r4_r6.py','Tests/Reference/hsb_2e_economic_model_r4_r6.py','Tests/Static/verify_hsb_2e_prep_r4_r6.py','Tests/Evidence/HSB_2E_PREP_R4_R6_EVIDENCE_SEAL_SHA256.txt')
def run(root):
 root=Path(root).resolve();prefix='MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/';ok=True
 for f in FILES:
  old=subprocess.check_output(['git','show',f'{BASE}:{prefix}{f}'],cwd=root);cur=(root/f).read_bytes();same=hashlib.sha256(old).digest()==hashlib.sha256(cur).digest();ok&=same;print(f'R6_PROTECTED|{f}|{"UNCHANGED" if same else "CHANGED"}')
 print('R6_CANONICAL_STATUS_MISMATCH=EXPECTED_AFTER_R4_R7');print('RESULT='+('PASS' if ok else 'FAIL'));return ok
if __name__=='__main__':p=argparse.ArgumentParser();p.add_argument('--root',required=True);a=p.parse_args();raise SystemExit(0 if run(a.root) else 1)
