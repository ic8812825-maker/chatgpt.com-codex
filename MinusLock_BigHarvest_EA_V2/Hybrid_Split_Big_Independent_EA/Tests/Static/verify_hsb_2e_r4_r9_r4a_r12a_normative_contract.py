#!/usr/bin/env python3
"""Independent R12A ledger canonicalizer; deliberately independent from production code."""
import hashlib,json,unicodedata
from decimal import Decimal
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];D=json.loads((ROOT/'Tests/Contracts/HSB_2E_R4_R9_R4A_R12A_NORMATIVE_DECISIONS.json').read_text())
def dec(x):
 d=Decimal(str(x)).normalize();return '0' if d==0 else format(d,'f')
def entry(x):
 o={}
 for k in D['ledger']['entryFields']:
  v=x[k]
  if k in ('volume','price'):v=dec(v)
  elif isinstance(v,str):v=unicodedata.normalize('NFC',v)
  o[k]=v
 return o
def root(entries):
 if len({x['dealId'] for x in entries})!=len(entries) or len({x['eventId'] for x in entries})!=len(entries):raise ValueError('DUPLICATE_LEDGER_ID')
 b={'version':D['ledger']['canonicalizationVersion'],'entries':[entry(x) for x in sorted(entries,key=lambda z:z['dealId'])]};return hashlib.sha256(json.dumps(b,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
if __name__=='__main__':print(root([]))
