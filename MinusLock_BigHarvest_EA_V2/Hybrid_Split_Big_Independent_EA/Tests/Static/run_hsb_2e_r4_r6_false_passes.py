#!/usr/bin/env python3
"""Reproduce the ten independently reported R4-R5 false positives exactly."""
import argparse, copy, json, sys
from dataclasses import asdict, is_dataclass
from decimal import Decimal
from pathlib import Path

def encode(x):
    if is_dataclass(x): return {"__type__":type(x).__name__, **{k:encode(v) for k,v in asdict(x).items()}}
    if isinstance(x,Decimal): return {"__decimal__":str(x)}
    if isinstance(x,dict): return {str(k):encode(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)): return [encode(v) for v in x]
    return x

def run(root,write=False):
    root=Path(root).resolve();sys.path.insert(0,str(root/'Tests/Reference'))
    from hsb_2e_test_fixtures_r4_r5 import scenario_input
    from hsb_2e_reference_model_r4_r5 import execute_scenario
    from hsb_2e_provenance_model_r4_r5 import D,digest,derive,HSBI_DealEvidenceRecord,HSBI_ExecutionPriceProof,HSBI_SettlementCommitCertificate
    cases=[]
    def add(cid,inp,check,check_id):
        actual=execute_scenario(copy.deepcopy(inp));reproduced=check(actual)
        exact=encode(inp);cases.append({"CASE_ID":cid,"HISTORICAL_MODEL":"hsb_2e_reference_model_r4_r5.execute_scenario","exactInput":exact,"EXACT_INPUT_SHA256":digest(exact),"HISTORICAL_STATUS":actual['status'],"HISTORICAL_REASON":actual['reason'],"HISTORICAL_SETTLEMENT_APPLIED":actual.get('settlementApplied',False),"HISTORICAL_ALLOCATION_APPLIED":actual.get('allocationApplied',False),"FALSE_PASS_REPRODUCED":reproduced,"EXPECTED_R6_CHECK_ID":check_id})
    # 001 orphan deal contributes money despite having no position/intent.
    x=scenario_input('BIG');base=x['dealRecords'][0];p=x['priceProofs'][0]
    op=HSBI_ExecutionPriceProof('P999',1,'EURUSD',7,'C','TX','A',3,'S',2,999,'BUY',D('1.1'),D('1.2'),'BID',D('.00001'),D('1.1'),D('1.1'),1900,2200,'EXACT_SIDE','SNAPSHOT').sealed()
    od=HSBI_DealEvidenceRecord(1,1,'EURUSD',7,'C','TX','A',3,'S',2,'D999','E999','O999',999,'UNKNOWN','BUY',D('1'),D('1.1'),D('100'),D(0),D(0),D(0),D(100),True,2000,99,'P999','BROKER').sealed();x['priceProofs'].append(op);x['dealRecords'].append(od)
    add('FP-R6-001',x,lambda r:r['status']=='PASS' and r['economicProposal'].totalActualNetMoney>D(18),'R6_ORPHAN_DEAL_BLOCK')
    x=scenario_input('BIG');object.__setattr__(x['dealRecords'][0],'positionRole','SMALL');object.__setattr__(x['dealRecords'][0],'recordDigest',digest(x['dealRecords'][0].body()))
    add('FP-R6-002',x,lambda r:r['status']=='PASS','R6_DEAL_ROLE_BINDING')
    x=scenario_input('BIG');r=x['dealRecords'][0];q=x['priceProofs'][0];object.__setattr__(r,'price',D('99999'));object.__setattr__(q,'minimumAllowedPrice',D('99999'));object.__setattr__(q,'maximumAllowedPrice',D('99999'));object.__setattr__(q,'proofDigest',digest(q.body()));object.__setattr__(r,'recordDigest',digest(r.body()))
    add('FP-R6-003',x,lambda r:r['status']=='PASS','R6_TRUSTED_PRICE_DERIVATION')
    x=scenario_input('INITIAL');r=x['dealRecords'][0];object.__setattr__(r,'volume',D('.5'));object.__setattr__(r,'recordDigest',digest(r.body()));partial=execute_scenario(x);state=partial['state'];object.__setattr__(state['acceptedDealRecords'][0],'recordDigest','CORRUPTED');y=scenario_input('INITIAL');y['persistedState']=state;nr=y['dealRecords'][0];object.__setattr__(nr,'dealId','DNEW');object.__setattr__(nr,'eventId','ENEW');object.__setattr__(nr,'volume',D('.5'));object.__setattr__(nr,'recordDigest',digest(nr.body()));y['dealRecords']=[nr]
    add('FP-R6-004',y,lambda r:r['status']=='PASS','R6_PERSISTED_RECORD_REVALIDATION')
    x=scenario_input('INITIAL');x['dealRecords']=[];x['priceProofs']=[];c=x['context'];cert=HSBI_SettlementCommitCertificate(1,'FAKE',1,'EURUSD',7,'C','TX','A',2,3,'S',2,'INITIAL',(101,),'F','L','E','A','P','FSM',1).sealed();x['persistedState'].update(settlementCommitted=True,commitCertificate=cert);x['context']['stateRevision']=3
    add('FP-R6-005',x,lambda r:r['status']=='PASS' and r['reason']=='ALREADY_COMMITTED','R6_CERTIFICATE_LEDGER_BINDING')
    x=scenario_input('BIG');x['economicPolicy'].update(closeFarShare='1',reserveShare='1',farLossBefore='100')
    add('FP-R6-006',x,lambda r:r['status']=='PASS' and r['economicProposal'].closeFarBudget+r['economicProposal'].reserveAddition>r['economicProposal'].totalActualNetMoney,'R6_MONEY_CONSERVATION')
    x=scenario_input('INITIAL');
    add('FP-R6-007',x,lambda r:r['status']=='PASS' and r['economicProposal'].recoveryPLAfter>r['economicProposal'].recoveryPLBefore,'R6_INITIAL_POSITIVE_PROFIT_EXCLUDED')
    x=scenario_input('FINAL');
    add('FP-R6-008',x,lambda r:r['status']=='PASS' and r['economicProposal'].reserveAfter==r['economicProposal'].reserveBefore,'R6_FINAL_RESERVE_CONSUMPTION')
    x=scenario_input('BIG');x['economicPolicy']['farLossBefore']='100'
    add('FP-R6-009',x,lambda r:r['status']=='PASS' and r['economicProposal'].closeFarBudget>0 and r['economicProposal'].partialFarVolume==0,'R6_PARTIAL_FAR_CALCULATION')
    x=scenario_input('SMALL');x['economicPolicy'].update(newFarTicketSource=987654,newFarVolume='.33')
    add('FP-R6-010',x,lambda r:r['status']=='PASS' and r['economicProposal'].newFarTicketSource==987654 and r['economicProposal'].newFarVolume==D('.33'),'R6_NEW_FAR_DERIVATION')
    n=sum(c['FALSE_PASS_REPRODUCED'] for c in cases);out={"R5_FALSE_PASSES_REQUIRED":10,"R5_FALSE_PASSES_REPRODUCED":n,"cases":cases,"RESULT":"PASS" if n==10 else "FAIL"}
    if write:(root/'Tests/Vectors/HSB_2E_R4_R6_EXACT_R5_FALSE_PASSES.json').write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps(out,sort_keys=True,separators=(',',':')));return n==10
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',required=True);p.add_argument('--write-fixtures',action='store_true');a=p.parse_args();raise SystemExit(0 if run(a.root,a.write_fixtures) else 1)
