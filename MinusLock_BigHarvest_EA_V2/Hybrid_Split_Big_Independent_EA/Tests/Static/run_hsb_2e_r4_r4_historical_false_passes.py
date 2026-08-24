#!/usr/bin/env python3
import argparse,subprocess,sys
from pathlib import Path
def main():
 p=argparse.ArgumentParser();p.add_argument('--root',required=True);a=p.parse_args();r=Path(a.root).resolve();cmds=[r/'Tests/Static/run_hsb_2e_prep_r4_r3_adversarial.py',r/'Tests/Static/run_hsb_2e_prep_r4_r4_adversarial.py'];ok=True
 for c in cmds:
  z=subprocess.run([sys.executable,str(c),'--root',str(r)],capture_output=True,text=True);print(z.stdout,end='');ok &= z.returncode==0
 print(f'HISTORICAL_FALSE_PASS_RUNNERS={"PASS" if ok else "FAIL"}');return 0 if ok else 1
if __name__=='__main__':raise SystemExit(main())
