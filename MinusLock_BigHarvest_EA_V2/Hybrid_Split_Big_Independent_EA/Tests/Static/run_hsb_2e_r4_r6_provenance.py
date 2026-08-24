#!/usr/bin/env python3
import argparse,copy,json,sys
from pathlib import Path
def run(root):
 root=Path(root).resolve();sys.path.insert(0,str(root/'Tests/Reference'));from hsb_2e_test_fixtures_r4_r6 import broker_fixture;from hsb_2e_provenance_model_r4_r6 import *
 checks={};x=broker_fixture();state,e=validate_all_then_apply(x['persistedState'],x['dealRecords'],x['context'],x['positions'],x['intents'],x['snapshot'],x['pricePolicy']);checks['R6_BINDING_POSITIVE']=e is None
 y=broker_fixture();r=y['dealRecords'][0];object.__setattr__(r,'positionTicket',999);object.__setattr__(r,'recordDigest',digest(r.body()));checks['R6_ORPHAN_DEAL_BLOCK']=validate_binding(r,y['context'],y['positions'],y['intents'],y['snapshot'],y['pricePolicy'])=='ORPHAN_DEAL'
 y=broker_fixture();r=y['dealRecords'][0];object.__setattr__(r,'positionRole','FAR');object.__setattr__(r,'recordDigest',digest(r.body()));checks['R6_DEAL_ROLE_BINDING']=validate_binding(r,y['context'],y['positions'],y['intents'],y['snapshot'],y['pricePolicy'])=='DEAL_ROLE_MISMATCH'
 y=broker_fixture();r=y['dealRecords'][0];object.__setattr__(r,'intentId','UNKNOWN');object.__setattr__(r,'recordDigest',digest(r.body()));checks['R6_DEAL_INTENT_BINDING']=validate_binding(r,y['context'],y['positions'],y['intents'],y['snapshot'],y['pricePolicy'])=='DEAL_INTENT_MISSING'
 y=broker_fixture();r=y['dealRecords'][0];object.__setattr__(r,'price',D('99999'));object.__setattr__(r,'recordDigest',digest(r.body()));checks['R6_TRUSTED_PRICE_DERIVATION']=validate_binding(r,y['context'],y['positions'],y['intents'],y['snapshot'],y['pricePolicy'])=='EXECUTION_PRICE_OUTSIDE_TRUSTED_POLICY'
 corrupted=copy.deepcopy(state);object.__setattr__(corrupted['acceptedDealRecords'][0],'recordDigest','bad');checks['R6_PERSISTED_RECORD_REVALIDATION']=revalidate_persisted(corrupted,x['context'],x['positions'],x['intents'],x['snapshot'],x['pricePolicy'])=='SOURCE_RECORD_DIGEST_MISMATCH'
 out={'checks':checks,'RESULT':'PASS' if all(checks.values()) else 'FAIL'};print(json.dumps(out,sort_keys=True,separators=(',',':')));return out['RESULT']=='PASS'
if __name__=='__main__':p=argparse.ArgumentParser();p.add_argument('--root',required=True);a=p.parse_args();raise SystemExit(0 if run(a.root) else 1)
