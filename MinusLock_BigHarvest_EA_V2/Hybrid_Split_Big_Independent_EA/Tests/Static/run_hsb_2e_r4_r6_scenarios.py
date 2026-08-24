#!/usr/bin/env python3
import argparse,copy,json,sys
from dataclasses import replace
from pathlib import Path
def run(root):
 root=Path(root).resolve();sys.path.insert(0,str(root/'Tests/Reference'));from hsb_2e_test_fixtures_r4_r6 import broker_fixture;from hsb_2e_reference_model_r4_r6 import execute_scenario;from hsb_2e_provenance_model_r4_r6 import D,digest
 checks={s:execute_scenario(broker_fixture(s))['status']=='PASS' for s in ('INITIAL','BIG','SMALL','FINAL')}
 x=broker_fixture('INITIAL',money='-1');checks['INITIAL_NEGATIVE_BLOCK']=execute_scenario(x)['reason']=='INITIAL_NET_NOT_POSITIVE'
 x=broker_fixture('BIG');x['dealRecords']=x['dealRecords'][:1];checks['BIG_FULL_FILL_GATE']=execute_scenario(x)['reason']=='PARTIAL_FILL'
 x=broker_fixture('SMALL');x['positions']=x['positions'][:2];x['intents']=x['intents'][:2];x['dealRecords']=x['dealRecords'][:2];checks['SMALL_MANDATORY_GATE']=execute_scenario(x)['reason']=='MANDATORY_LEGS_INVALID'
 x=broker_fixture('FINAL');x['intents'][0]['intentKind']='PARTIAL_CLOSE';checks['FINAL_FULL_CLOSE_GATE']=execute_scenario(x)['reason']=='FULL_CLOSE_REQUIRED'
 first=execute_scenario(broker_fixture('FINAL'));y=broker_fixture('FINAL');y['persistedState']=first['state'];y['context']['stateRevision']=first['state']['stateRevision'];replay=execute_scenario(y);checks['FINAL_EXACTLY_ONCE']=replay['reason']=='ALREADY_COMMITTED' and not replay['settlementApplied']
 out={'checks':checks,'RESULT':'PASS' if all(checks.values()) else 'FAIL'};print(json.dumps(out,sort_keys=True,separators=(',',':')));return out['RESULT']=='PASS'
if __name__=='__main__':p=argparse.ArgumentParser();p.add_argument('--root',required=True);a=p.parse_args();raise SystemExit(0 if run(a.root) else 1)
