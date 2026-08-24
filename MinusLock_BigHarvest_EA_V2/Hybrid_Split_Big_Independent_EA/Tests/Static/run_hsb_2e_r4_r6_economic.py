#!/usr/bin/env python3
import argparse,copy,json,sys
from pathlib import Path
def run(root):
 root=Path(root).resolve();sys.path.insert(0,str(root/'Tests/Reference'));from hsb_2e_test_fixtures_r4_r6 import broker_fixture;from hsb_2e_reference_model_r4_r6 import execute_scenario;from hsb_2e_provenance_model_r4_r6 import D
 checks={}
 initial_input=broker_fixture('INITIAL');initial=execute_scenario(initial_input);checks['R6_INITIAL_POSITIVE_PROFIT_EXCLUDED']=initial['status']=='PASS' and initial['economicProposal'].recoveryPLAfter==initial_input['economicPolicy'].recoveryPLBefore
 big=execute_scenario(broker_fixture('BIG'));ep=big['economicProposal'];checks['R6_MONEY_CONSERVATION']=ep.allocatedMoney+ep.remainingMoney==ep.availableMoney and ep.allocatedMoney<=ep.availableMoney;checks['R6_DISJOINT_ALLOCATION']=sum(ep.allocationAttribution.values(),D(0))==ep.allocatedMoney;checks['R6_PARTIAL_FAR_CALCULATION']=ep.partialFarVolume>0 and ep.partialFarVolume<broker_fixture('BIG')['economicPolicy'].farVolumeBefore;checks['R6_RESERVE_PARTIAL_ISOLATION']='FAR_LOSS_FROM_RESERVE' not in ep.allocationAttribution
 small=execute_scenario(broker_fixture('SMALL'));sp=small['economicProposal'];source=next(p for p in broker_fixture('SMALL')['positions'] if p['role']=='BIG');checks['R6_NEW_FAR_DERIVATION']=sp.newFarTicket==source['ticket'] and sp.newFarVolume==D(source['residualVolume']);checks['R6_CATCH_UP_PROOF']=sp.catchUpRatio==(broker_fixture('SMALL')['economicPolicy'].reserveBefore+sp.smallReserveAddition)/broker_fixture('SMALL')['economicPolicy'].farLossBefore;checks['R6_DUAL_TAIL_BLOCK']=not sp.dualTail
 final=execute_scenario(broker_fixture('FINAL'));fp=final['economicProposal'];checks['R6_FINAL_RESERVE_CONSUMPTION']=fp.reserveConsumed>0 and fp.reserveAfter==broker_fixture('FINAL')['economicPolicy'].reserveBefore-fp.reserveConsumed and fp.reserveAfter>=0
 checks['R6_VOLUME_CONSERVATION']=all(v<=D(next(p['authoritativeVolume'] for p in broker_fixture('BIG')['positions'] if str(p['ticket'])==t)) for t,v in big['state']['volumeByTicket'].items())
 out={'checks':checks,'RESULT':'PASS' if all(checks.values()) else 'FAIL'};print(json.dumps(out,sort_keys=True,separators=(',',':')));return out['RESULT']=='PASS'
if __name__=='__main__':p=argparse.ArgumentParser();p.add_argument('--root',required=True);a=p.parse_args();raise SystemExit(0 if run(a.root) else 1)
