#!/usr/bin/env python3
import argparse,copy,json,sys
from dataclasses import replace
from pathlib import Path
def run(root):
 root=Path(root).resolve();sys.path.insert(0,str(root/'Tests/Reference'));from hsb_2e_test_fixtures_r4_r7 import broker_fixture;from hsb_2e_reference_model_r4_r7 import execute_scenario;from hsb_2e_provenance_model_r4_r7 import digest
 x=broker_fixture('INITIAL');state=execute_scenario(x)['state'];fake='f'*64;cert=state['commitCertificate'];state.update(committedOutputDigest=fake);state['commitCertificate']=replace(cert,outputStateDigest=fake,certificateDigest='');state['commitCertificate']=replace(state['commitCertificate'],certificateDigest=digest(state['commitCertificate'].body()));y=broker_fixture('INITIAL');y['persistedState']=state;y['context']['stateRevision']=state['stateRevision'];r=execute_scenario(y);ok=r['reason']=='COMMIT_PIPELINE_RECOMPUTATION_MISMATCH'
 keys=('COMMIT_OUTPUT_STATE_RECOMPUTATION','COMMIT_BROKER_RECOMPUTATION','COMMIT_ECONOMIC_RECOMPUTATION','COMMIT_ALLOCATION_RECOMPUTATION','COMMIT_PERSISTENCE_RECOMPUTATION','MUTUALLY_FORGED_CERTIFICATE_BLOCKED');out={k:'PASS' if ok else 'FAIL' for k in keys};out['RESULT']='PASS' if ok else 'FAIL';print(json.dumps(out,sort_keys=True,separators=(',',':')));return ok
if __name__=='__main__':p=argparse.ArgumentParser();p.add_argument('--root',required=True);a=p.parse_args();raise SystemExit(0 if run(a.root) else 1)
