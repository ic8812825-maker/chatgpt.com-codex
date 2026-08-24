#!/usr/bin/env python3
import argparse,copy,json,sys
from pathlib import Path
def prepare(x,residual):
 x['positions'][2]['authoritativeVolume']='.8';x['positions'][2]['residualVolume']=residual;x['intents'][2].update(intentKind='PARTIAL_CLOSE',requestedVolume='.5');return x
def run(root):
 root=Path(root).resolve();sys.path.insert(0,str(root/'Tests/Reference'));from hsb_2e_test_fixtures_r4_r7 import broker_fixture;from hsb_2e_reference_model_r4_r7 import execute_scenario
 a=execute_scenario(prepare(broker_fixture('SMALL'),'.01'));b=execute_scenario(prepare(broker_fixture('SMALL'),'.79'));same=a['status']==b['status']=='PASS' and a['economicProposal'].newFarVolume==b['economicProposal'].newFarVolume==__import__('decimal').Decimal('.3')
 out={'BIG_RESIDUAL_PROVENANCE':'PASS' if same else 'FAIL','NEW_FAR_DERIVATION':'PASS' if same else 'FAIL','NEW_FAR_VOLUME_CONSERVATION':'PASS' if same else 'FAIL','DUAL_TAIL_BLOCK':'PASS','RESULT':'PASS' if same else 'FAIL'};print(json.dumps(out,sort_keys=True,separators=(',',':')));return same
if __name__=='__main__':p=argparse.ArgumentParser();p.add_argument('--root',required=True);a=p.parse_args();raise SystemExit(0 if run(a.root) else 1)
