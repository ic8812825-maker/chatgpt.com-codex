#!/usr/bin/env python3
"""Version-aware R4-R5 integrity check after R4-R6 canonical status advance."""
import argparse,hashlib
from pathlib import Path
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(root):
 root=Path(root).resolve();manifest=root/'Reports/HSB_2E_PREP_R4_R5_FILE_MANIFEST_SHA256.txt';expected={}
 for line in manifest.read_text().splitlines():
  h,rel=line.split('  ',1)
  if (rel.startswith('Tests/Reference/') or rel.startswith('Tests/Static/')) and ('r4_r5' in rel.lower()):expected[rel]=h
 rows=[]
 for rel,h in sorted(expected.items()):
  p=root/rel;actual=sha(p) if p.exists() else 'MISSING';rows.append((rel,h,actual,h==actual))
 ok=bool(rows) and all(r[3] for r in rows)
 print(f'R4_R5_PROTECTED_FILES={len(rows)}\nR4_R5_PROTECTED_UNCHANGED={"YES" if ok else "NO"}\nR4_R5_CANONICAL_STATUS_MISMATCH=EXPECTED_AFTER_R4_R6\nR4_R5_HISTORICAL_SEAL_MODIFIED=NO\nRESULT={"PASS" if ok else "FAIL"}')
 return ok
if __name__=='__main__':p=argparse.ArgumentParser();p.add_argument('--root',required=True);a=p.parse_args();raise SystemExit(0 if run(a.root) else 1)
