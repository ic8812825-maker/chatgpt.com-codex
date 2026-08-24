#!/usr/bin/env python3
"""R5 transaction barrier joining sealed broker evidence to economic math."""
import argparse,copy
from dataclasses import asdict
from decimal import Decimal
from hsb_2e_provenance_model_r4_r5 import *
from hsb_2e_economic_model_r4_r5 import build_economic_proposal

REQUIRED={"INITIAL":{"WINNER"},"BIG":{"BIG","SMALL"},"SMALL":{"SMALL","OLD_FAR","BIG"},"FINAL":{"FAR"}}
def outcome(status,reason,phase,state,**extra):return {"status":status,"reason":reason,"phase":phase,"state":state,"settlementApplied":False,"allocationApplied":False,**extra}
def execute_scenario(inp):
    try:
        scenario=inp["scenario"];ctx=inp["context"];state=copy.deepcopy(inp["persistedState"]);positions=inp["positions"];intents=inp["intents"]
        if scenario not in REQUIRED:return outcome("REJECT","UNKNOWN_SCENARIO","VALIDATION_BLOCKED",state)
        if state.get("settlementCommitted") is True and not state.get("commitCertificate"):return outcome("REJECT","COMMIT_CERTIFICATE_MISSING","VALIDATION_BLOCKED",state)
        if state.get("commitCertificate"):
            cert=state["commitCertificate"];expected={"accountLogin":ctx["accountLogin"],"symbol":ctx["symbol"],"magic":ctx["magic"],"cycleId":ctx["cycleId"],"transactionId":ctx["transactionId"],"actionId":ctx["actionId"],"inputStateRevision":ctx["stateRevision"]-1,"outputStateRevision":ctx["stateRevision"],"scenario":scenario}
            e=validate_certificate(cert,expected)
            if e:return outcome("REJECT",e,"VALIDATION_BLOCKED",state)
            return outcome("PASS","ALREADY_COMMITTED","IDEMPOTENT_REPLAY",state,settlementApplied=False,allocationApplied=False)
        roles=[p["role"] for p in positions]
        if set(roles)!=REQUIRED[scenario] or len(roles)!=len(set(roles)):return outcome("REJECT","MANDATORY_LEGS_INVALID","VALIDATION_BLOCKED",state)
        pmap={p["positionTicket"]:p for p in positions};imap={i["positionTicket"]:i for i in intents}
        if set(pmap)!=set(imap) or len(intents)!=len(imap):return outcome("REJECT","ONE_POSITION_ONE_INTENT_VIOLATION","VALIDATION_BLOCKED",state)
        for ticket,p in pmap.items():
            i=imap[ticket]
            if scenario=="FINAL" and i["intentKind"]!="FULL_CLOSE":return outcome("REJECT","FINAL_REQUIRES_FULL_CLOSE","VALIDATION_BLOCKED",state)
            if i["intentKind"]=="FULL_CLOSE" and D(i["requestedVolume"])!=D(p["positionVolume"]):return outcome("REJECT","FULL_CLOSE_VOLUME_MISMATCH","VALIDATION_BLOCKED",state)
        new_state,e=validate_all_then_apply(state,inp.get("dealRecords",[]),inp.get("priceProofs",[]),ctx)
        if e:return outcome("UNAVAILABLE" if e=="EMPTY_BATCH" else "REJECT",e,"VALIDATION_BLOCKED",state)
        fills={str(t):D(new_state["cumulativeFills"].get(str(t),0)) for t in pmap}
        if any(fills[str(t)]>D(imap[t]["requestedVolume"]) for t in pmap):return outcome("CONFLICT","OVERFILL","RECONCILING",state)
        if any(fills[str(t)]<D(imap[t]["requestedVolume"]) for t in pmap):return outcome("UNAVAILABLE","PARTIAL_FILL","WAITING_FOR_FULL_FILL",new_state)
        money_role={p["role"]:new_state["moneyByTicket"][str(t)] for t,p in pmap.items()};broker={"scenario":scenario,"cycleId":ctx["cycleId"],"actionId":ctx["actionId"],"transactionId":ctx["transactionId"],"stateRevision":ctx["stateRevision"],"moneyByTicket":new_state["moneyByTicket"],"moneyByRole":money_role,"sealed":True};broker["brokerProposalDigest"]=digest(broker)
        economic,e=build_economic_proposal(broker,inp["economicPolicy"])
        if e:return outcome("REJECT",e,"ECONOMIC_BLOCKED",new_state)
        settlement_id=digest((ctx["cycleId"],ctx["transactionId"],ctx["actionId"],ctx["stateRevision"]))
        tickets=tuple(sorted(pmap));ledger_digest=digest([r.recordDigest for r in new_state["acceptedDealRecords"]]);persistence_digest=digest({k:v for k,v in new_state.items() if k!="acceptedDealRecords"})
        cert=HSBI_SettlementCommitCertificate(1,settlement_id,ctx["accountLogin"],ctx["symbol"],ctx["magic"],ctx["cycleId"],ctx["transactionId"],ctx["actionId"],ctx["stateRevision"],ctx["stateRevision"]+1,ctx["snapshotId"],ctx["snapshotVersion"],scenario,tickets,digest(fills),ledger_digest,economic.economicProposalDigest,economic.allocationPolicyDigest,persistence_digest,f"{scenario}_COMMIT",new_state.get("settlementRevision",0)+1).sealed()
        new_state.update(settlementCommitted=True,commitCertificate=cert,stateRevision=ctx["stateRevision"]+1,settlementRevision=new_state.get("settlementRevision",0)+1)
        return {"status":"PASS","reason":"OK","phase":"FSM_COMMITTED","state":new_state,"settlementApplied":True,"allocationApplied":True,"brokerProposal":broker,"economicProposal":economic,"commitCertificate":cert}
    except (KeyError,TypeError,ValueError,ArithmeticError) as e:return outcome("REJECT","MALFORMED_INPUT_"+type(e).__name__.upper(),"VALIDATION_BLOCKED",inp.get("persistedState",{}))

def self_test():
    from hsb_2e_test_fixtures_r4_r5 import scenario_input
    good=execute_scenario(scenario_input("INITIAL"));bad=scenario_input("INITIAL",money="-1");b=execute_scenario(bad);final=scenario_input("FINAL");final["intents"][0]["intentKind"]="PARTIAL_CLOSE";f=execute_scenario(final)
    checks=[good["status"]=="PASS",b["reason"]=="INITIAL_NET_NOT_POSITIVE",f["reason"]=="FINAL_REQUIRES_FULL_CLOSE"]
    print(f"REFERENCE_R4_R5_SELF_TESTS={sum(checks)}/{len(checks)}");return all(checks)
if __name__=="__main__":p=argparse.ArgumentParser();p.add_argument("--self-test",action="store_true");a=p.parse_args();raise SystemExit(0 if a.self_test and self_test() else 1)
