#!/usr/bin/env python3
import argparse,copy,json,sys
from pathlib import Path
def run(root):
 root=Path(root).resolve();sys.path.insert(0,str(root/'Tests/Reference'));from hsb_2e_test_fixtures_r4_r7 import broker_fixture;from hsb_2e_reference_model_r4_r7 import execute_scenario;from hsb_2e_provenance_model_r4_r7 import digest
 cases=[]
 for kind in ('SIDES','FOREIGN'):
  x=broker_fixture('INITIAL')
  if kind=='SIDES':object.__setattr__(x['pricePolicy'],'buyCloseSide','ASK');object.__setattr__(x['pricePolicy'],'sellCloseSide','BID');object.__setattr__(x['pricePolicy'],'policyDigest',digest(x['pricePolicy'].body()));expected='NORMATIVE_CLOSE_SIDE_MISMATCH'
  else:object.__setattr__(x['snapshot'],'accountLogin',99);object.__setattr__(x['snapshot'],'digestValue',digest(x['snapshot'].body()));expected='SNAPSHOT_CONTEXT_IDENTITY_MISMATCH'
  r=execute_scenario(x);cases.append(r['reason']==expected)
 out={'SNAPSHOT_CONTEXT_IDENTITY':'PASS' if cases[1] else 'FAIL','BUY_CLOSE_SIDE_BID':'PASS' if cases[0] else 'FAIL','SELL_CLOSE_SIDE_ASK':'PASS' if cases[0] else 'FAIL','RESULT':'PASS' if all(cases) else 'FAIL'};print(json.dumps(out,sort_keys=True,separators=(',',':')));return all(cases)
if __name__=='__main__':p=argparse.ArgumentParser();p.add_argument('--root',required=True);a=p.parse_args();raise SystemExit(0 if run(a.root) else 1)
