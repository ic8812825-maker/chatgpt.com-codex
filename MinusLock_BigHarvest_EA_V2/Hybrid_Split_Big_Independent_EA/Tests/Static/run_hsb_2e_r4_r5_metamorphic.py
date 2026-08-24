#!/usr/bin/env python3
import argparse,copy,json,sys
from pathlib import Path
def run(root):
 root=Path(root).resolve();sys.path.insert(0,str(root/'Tests/Reference'));from hsb_2e_test_fixtures_r4_r5 import scenario_input;from hsb_2e_reference_model_r4_r5 import execute_scenario
 x=scenario_input('BIG');a=execute_scenario(x);y=copy.deepcopy(x);y['dealRecords'].reverse();y['priceProofs'].reverse();b=execute_scenario(y)
 checks={'PERMUTATION_STATUS':a['status']==b['status']=='PASS','PERMUTATION_MONEY':a['economicProposal'].totalActualNetMoney==b['economicProposal'].totalActualNetMoney,'DIGEST_DETERMINISTIC':a['economicProposal'].economicProposalDigest==b['economicProposal'].economicProposalDigest}
 out={'checks':checks,'RESULT':'PASS' if all(checks.values()) else 'FAIL'};print(json.dumps(out,sort_keys=True,separators=(',',':')));return out['RESULT']=='PASS'
if __name__=='__main__':p=argparse.ArgumentParser();p.add_argument('--root',required=True);a=p.parse_args();raise SystemExit(0 if run(a.root) else 1)
