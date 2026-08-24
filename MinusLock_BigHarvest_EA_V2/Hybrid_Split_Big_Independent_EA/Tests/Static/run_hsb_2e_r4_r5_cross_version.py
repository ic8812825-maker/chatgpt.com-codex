#!/usr/bin/env python3
"""Execute every historical vector through an adapter and its preserved model."""
import argparse, importlib, json, sys
from pathlib import Path
VERSIONS={
 "R4_R2":("HSB_2E_R4_R2_VECTORS.json","hsb_2e_r4_r2_to_r4_r5_adapter","hsb_2e_reference_model_r4_r2"),
 "R4_R3":("HSB_2E_R4_R3_VECTORS.json","hsb_2e_r4_r3_to_r4_r5_adapter","hsb_2e_reference_model_r4_r3"),
 "R4_R4":("HSB_2E_R4_R4_VECTORS.json","hsb_2e_r4_r4_to_r4_r5_adapter","hsb_2e_reference_model_r4_r4")}
FIELDS=("status","reason","phase")
def semantic(actual,expected):
    checks={k:actual.get(k)==expected.get(k) for k in FIELDS}
    ao,eo=actual.get("output",{}),expected.get("output",{})
    checks.update(fill_state=actual.get("phase")==expected.get("phase"),settlement_eligibility=bool(ao.get("settlementApplied"))==bool(eo.get("settlementApplied")),allocation_eligibility=bool(ao.get("allocationApplied"))==bool(eo.get("allocationApplied")),money_result=ao.get("moneyByTicket",ao.get("money"))==eo.get("moneyByTicket",eo.get("money")),volume_result=ao.get("confirmedVolumeByTicket",ao.get("confirmedVolume"))==eo.get("confirmedVolumeByTicket",eo.get("confirmedVolume")),exactly_once=ao.get("consumedDealIds")==eo.get("consumedDealIds"),persistence=actual.get("persistenceRecords")==expected.get("persistenceRecords"),fsm_mutation=ao.get("stateRevision")==eo.get("stateRevision"))
    return all(checks.values()),checks
def run(root):
    root=Path(root).resolve();sys.path.insert(0,str(root/"Tests/Reference"));results={};all_rows=[]
    for version,(file,adapter_name,model_name) in VERSIONS.items():
        vectors=json.loads((root/"Tests/Vectors"/file).read_text())["vectors"];adapter=importlib.import_module(adapter_name);model=importlib.import_module(model_name);rows=[]
        for vector in vectors:
            a=adapter.adapt(vector)
            if a["adapterResult"]!="ADAPTED":rows.append({"vectorId":vector.get("VECTOR_ID"),"adapterResult":a["adapterResult"],"executed":False});continue
            if version=="R4_R2":actual=model.execute(a["sourceFunction"],a["historicalInput"])
            elif version=="R4_R3":actual=model.settle(a["historicalInput"])
            else:actual=model.execute_scenario(a["historicalInput"])
            passed,checks=semantic(actual,a["historicalExpected"]);rows.append({"vectorId":a["sourceVectorId"],"adapterResult":"ADAPTED","executed":True,"passed":passed,"semanticChecks":checks})
        req=len(rows);counts={"REQUIRED":req,"ADAPTED":sum(x["adapterResult"]=="ADAPTED" for x in rows),"EXECUTED":sum(x.get("executed",False) for x in rows),"UNMAPPED":sum(x["adapterResult"]=="UNMAPPED" for x in rows),"AMBIGUOUS":sum(x["adapterResult"]=="AMBIGUOUS" for x in rows),"FAILED":sum(x.get("executed",False) and not x.get("passed",False) for x in rows)}
        results[version]=counts;all_rows.extend({"version":version,**x} for x in rows)
    ok=all(x["EXECUTED"]==x["REQUIRED"] and x["UNMAPPED"]==x["AMBIGUOUS"]==x["FAILED"]==0 for x in results.values())
    out={"versions":results,"rows":all_rows,"CROSS_VERSION_REGRESSIONS":sum(x["FAILED"] for x in results.values()),"RESULT":"PASS" if ok else "FAIL"};print(json.dumps(out,sort_keys=True,separators=(",",":")));return ok
if __name__=="__main__":p=argparse.ArgumentParser();p.add_argument("--root",required=True);a=p.parse_args();raise SystemExit(0 if run(a.root) else 1)
