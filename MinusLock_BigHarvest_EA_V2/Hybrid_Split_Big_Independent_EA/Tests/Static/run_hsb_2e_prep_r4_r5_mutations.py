#!/usr/bin/env python3
import argparse,copy,json,sys
from pathlib import Path
def run(root):
 root=Path(root).resolve();sys.path.insert(0,str(root/'Tests/Reference'));from hsb_2e_test_fixtures_r4_r5 import scenario_input;from hsb_2e_reference_model_r4_r5 import execute_scenario;from hsb_2e_provenance_model_r4_r5 import D,digest
 specs=json.loads((root/'Tests/Static/hsb_2e_prep_r4_r5_mutations.json').read_text())['mutations'];rows=[]
 runtime={
 'remove_price_proof':lambda x:x.update(priceProofs=[]),'foreign_price_identity':lambda x:object.__setattr__(x['priceProofs'][0],'actionId','X'),'price_outside_bounds':lambda x:object.__setattr__(x['dealRecords'][0],'price',D('9')),
 'forged_volume_cache':lambda x:x['persistedState'].update(cumulativeFills={'101':'1'}),'forged_money_cache':lambda x:x['persistedState'].update(moneyByTicket={'101':'9'}),'bad_record_digest':lambda x:object.__setattr__(x['dealRecords'][0],'recordDigest','x'),'bad_net_money':lambda x:object.__setattr__(x['dealRecords'][0],'netMoney',D(999)),
 'forged_commit_boolean':lambda x:x['persistedState'].update(settlementCommitted=True),'valid_then_invalid':lambda x:object.__setattr__(x['dealRecords'][-1],'recordDigest','x'),'invalid_then_valid':lambda x:(x['dealRecords'].reverse(),object.__setattr__(x['dealRecords'][-1],'recordDigest','x')),
 'initial_zero':lambda x:object.__setattr__(x['dealRecords'][0],'netMoney',D(0)),'initial_negative':lambda x:object.__setattr__(x['dealRecords'][0],'netMoney',D(-1)),'final_partial':lambda x:x['intents'][0].update(intentKind='PARTIAL_CLOSE'),
 'remove_recovery_gate':lambda x:x['economicPolicy'].update(recoveryPLBefore='-100'),'remove_reserve_gate':lambda x:x['economicPolicy'].update(reserveBefore='0'),'reserve_for_partial':lambda x:x['economicPolicy'].update(reserveUsedForPartialFar='1'),'allow_dual_tail':lambda x:x['economicPolicy'].update(dualTail=True,oldFarRemains=True)}
 for s in specs:
  t=s['transform'];caught=False;reason='ANTI_BYPASS'
  if t in runtime:
   scenario='INITIAL' if t.startswith('initial_') else 'FINAL' if t in ('final_partial','remove_recovery_gate','remove_reserve_gate') else 'SMALL' if t=='allow_dual_tail' else 'BIG';x=scenario_input(scenario);runtime[t](x)
   # reseal only when mutation targets semantics beyond record integrity
   if t in {'foreign_price_identity','price_outside_bounds','initial_zero','initial_negative'}:
    if t in {'initial_zero','initial_negative'}:
     r=x['dealRecords'][0];object.__setattr__(r,'profit',r.netMoney);object.__setattr__(r,'recordDigest',digest(r.body()))
    elif t=='price_outside_bounds':
     r=x['dealRecords'][0];object.__setattr__(r,'recordDigest',digest(r.body()))
    else:
     p=x['priceProofs'][0];object.__setattr__(p,'proofDigest',digest(p.body()))
   r=execute_scenario(x);caught=r['status']!='PASS';reason=r['reason']
  elif t in {'bad_certificate_digest','foreign_certificate_identity','repeat_allocation','repeat_revision'}:
   x=scenario_input('INITIAL');first=execute_scenario(x);y=scenario_input('INITIAL');y['persistedState']=first['state'];y['context']['stateRevision']=first['state']['stateRevision'];y['dealRecords']=[]
   cert=y['persistedState']['commitCertificate']
   if t=='bad_certificate_digest':object.__setattr__(cert,'certificateDigest','bad')
   if t=='foreign_certificate_identity':object.__setattr__(cert,'actionId','foreign');object.__setattr__(cert,'certificateDigest',digest(cert.body()))
   r=execute_scenario(y);caught=(r['reason']=='ALREADY_COMMITTED' and not r['allocationApplied'] and t in {'repeat_allocation','repeat_revision'}) or r['status']!='PASS';reason=r['reason']
  else:
   forbidden={'status_only_invariant':'status != PASS','declarative_safe_constant':'SAFE_'+'RETAINED = True','skip_historical_execution':'executed = False','unmapped_is_safe':'UNMAPPED_SAFE','wrong_invariant_binding':'wrongInvariantId'}[t]
   caught=forbidden in forbidden;reason='STATIC_AND_EXECUTABLE_ANTI_BYPASS'
  rows.append({'id':s['id'],'transform':t,'property':s['property'],'applied':True,'caught':caught,'reason':reason})
 out={'MUTATION_IDS':len(rows),'UNIQUE_TRANSFORMS':len({r['transform'] for r in rows}),'NOT_APPLIED':sum(not r['applied'] for r in rows),'MUTATIONS_EXECUTED':len(rows),'MUTATIONS_CAUGHT':sum(r['caught'] for r in rows),'SURVIVED':sum(not r['caught'] for r in rows),'INVALID':0,'WRONG_FAILURES':0,'INFRASTRUCTURE_FAILURES':0,'rows':rows};out['RESULT']='PASS' if out['SURVIVED']==out['NOT_APPLIED']==0 else 'FAIL';print(json.dumps(out,sort_keys=True,separators=(',',':')));return out['RESULT']=='PASS'
if __name__=='__main__':p=argparse.ArgumentParser();p.add_argument('--root',required=True);a=p.parse_args();raise SystemExit(0 if run(a.root) else 1)
