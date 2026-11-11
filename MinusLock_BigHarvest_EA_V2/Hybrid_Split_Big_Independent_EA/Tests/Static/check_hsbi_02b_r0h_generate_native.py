#!/usr/bin/env python3
"""Generate only test harness/goldens from independent frozen literal fixtures.
No subject encoder is called to generate expected bytes. --check is read-only.
"""
import sys,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'Tests/Reference'))
import hsbi_02b_r0f_independent_fixtures as f

def content():
 lines=['// Independent R0F fixture struct.pack/literal goldens; not subject encoder.','#ifndef R0H_GOLDENS','#define R0H_GOLDENS',f'string R0H_GoldenRecordHex="{f.binary_record(f.record()).hex()}";']
 for idx,(name,value,text,bits) in enumerate(f.GOLDENS):lines+=[f'// {name}',f'string R0H_GoldenBits{idx}="{bits}";',f'string R0H_GoldenText{idx}="{text}";']
 lines+=['#endif'];return '\n'.join(lines)+'\n'
if __name__=='__main__':
 target=ROOT/'Tests/Reference/hsbi_02b_r0h_native_goldens.mqh';expected=content()
 if '--check' in sys.argv:
  assert target.read_text()==expected;print('native independent goldens MATCH')
 else:target.write_text(expected)
