#!/usr/bin/env python3
import argparse,copy,json,sys
from pathlib import Path
def run(root):
 root=Path(root).resolve();sys.path.insert(0,str(root/'Tests/Reference'));from hsb_2e_test_fixtures_r4_r5 import scenario_input;from hsb_2e_reference_model_r4_r5 import execute_scenario;from hsb_2e_provenance_model_r4_r5 import derive,digest
 rows=[]
 def row(i,ok,detail):rows.append({'id':i,'passed':ok,'detail':detail})
 x=scenario_input('INITIAL');a=x['dealRecords'][0];x['dealRecords']=[copy.deepcopy(a)];object.__setattr__(x['dealRecords'][0],'volume',a.volume/2);object.__setattr__(x['dealRecords'][0],'recordDigest',digest(x['dealRecords'][0].body()));r1=execute_scenario(x);y=scenario_input('INITIAL');y['persistedState']=r1['state'];b=copy.deepcopy(a);object.__setattr__(b,'dealId','D-B');object.__setattr__(b,'eventId','E-B');object.__setattr__(b,'volume',a.volume/2);object.__setattr__(b,'recordDigest',digest(b.body()));y['dealRecords']=[b];r2=execute_scenario(y);row('LIFECYCLE-01',r1['reason']=='PARTIAL_FILL' and r2['status']=='PASS','partial/restart/full')
 z=copy.deepcopy(y);z['persistedState']=r1['state'];z['dealRecords']=x['dealRecords'];r=execute_scenario(z);row('LIFECYCLE-02',r['reason']=='DEAL_ALREADY_CONSUMED' and digest(r['state'])==digest(r1['state']),'duplicate unchanged')
 q=copy.deepcopy(y);q['persistedState']=r2['state'];q['context']['stateRevision']=r2['state']['stateRevision'];q['dealRecords']=[];r=execute_scenario(q);row('LIFECYCLE-03',r['reason']=='ALREADY_COMMITTED' and not r['allocationApplied'],'committed replay')
 q=scenario_input('BIG');q['persistedState']['cumulativeFills']={'101':'1'};r=execute_scenario(q);row('LIFECYCLE-04',r['reason']=='CUMULATIVE_FILL_PROVENANCE_MISSING','aggregate cache')
 q=scenario_input('BIG');object.__setattr__(q['dealRecords'][0],'recordDigest','forged');r=execute_scenario(q);row('LIFECYCLE-05',r['reason']=='SOURCE_RECORD_DIGEST_MISMATCH','record digest')
 q=scenario_input('BIG');bad=copy.deepcopy(q['dealRecords'][1]);object.__setattr__(bad,'recordDigest','forged');q['dealRecords']=[q['dealRecords'][0],bad];before=digest(q['persistedState']);r=execute_scenario(q);row('LIFECYCLE-06',r['reason']=='SOURCE_RECORD_DIGEST_MISMATCH' and digest(r['state'])==before,'atomic reject')
 r=execute_scenario(scenario_input('INITIAL','-1'));row('LIFECYCLE-07',r['reason']=='INITIAL_NET_NOT_POSITIVE','initial negative')
 q=scenario_input('FINAL');q['intents'][0]['intentKind']='PARTIAL_CLOSE';r=execute_scenario(q);row('LIFECYCLE-08',r['reason']=='FINAL_REQUIRES_FULL_CLOSE','final partial')
 out={'LIFECYCLES_REQUIRED':8,'LIFECYCLES_EXECUTED':len(rows),'LIFECYCLES_PASSED':sum(x['passed'] for x in rows),'rows':rows};out['RESULT']='PASS' if out['LIFECYCLES_PASSED']==8 else 'FAIL';print(json.dumps(out,sort_keys=True,separators=(',',':')));return out['RESULT']=='PASS'
if __name__=='__main__':p=argparse.ArgumentParser();p.add_argument('--root',required=True);a=p.parse_args();raise SystemExit(0 if run(a.root) else 1)
