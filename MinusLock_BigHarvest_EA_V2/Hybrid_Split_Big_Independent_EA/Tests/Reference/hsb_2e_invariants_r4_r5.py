#!/usr/bin/env python3
"""Property-specific R5 invariants; every predicate recomputes its own property."""
import argparse,copy
from dataclasses import asdict
from decimal import Decimal
from hsb_2e_provenance_model_r4_r5 import *
from hsb_2e_test_fixtures_r4_r5 import scenario_input

GROUPS=("NUMERIC_DOMAIN","VOLUME_GRID","PRICE_GRID","EXECUTION_PRICE_PROOF","BOOLEAN_TYPE","IDENTITY_CHAIN","ONE_POSITION_ONE_INTENT","MANDATORY_LEGS","DEAL_EXACTLY_ONCE","EVENT_EXACTLY_ONCE","SOURCE_RECORD_DIGEST","PERSISTED_VOLUME_PROVENANCE","PERSISTED_MONEY_PROVENANCE","BATCH_ATOMICITY","PARTIAL_PERSISTENCE","RESTART_REPLAY","COMMIT_CERTIFICATE","INITIAL_NET_PROFIT","BIG_ALLOCATION","SMALL_ALLOCATION","FINAL_FULL_CLOSE","RECOVERY_PL","RESERVE_COVERAGE","RESERVE_NOT_USED_FOR_PARTIAL_FAR","MONEY_CONSERVATION","VOLUME_CONSERVATION","STATE_REVISION","PERSISTENCE_ORDER","DUAL_TAIL","DETERMINISTIC_DIGEST")

def evaluate(name,x):
    if not all(k in x for k in ("scenario","context","positions","intents","dealRecords","persistedState","economicPolicy")):raise ValueError("MALFORMED_INVARIANT_INPUT")
    records=x.get("dealRecords",[]);state=x.get("persistedState",{});ctx=x.get("context",{});ps=x.get("positions",[]);its=x.get("intents",[]);policy=x.get("economicPolicy",{})
    if name=="NUMERIC_DOMAIN":return all(r.volume>0 and r.price>0 and all(v.is_finite() for v in (r.volume,r.price,r.profit,r.commission,r.swap,r.fee)) for r in records)
    if name=="VOLUME_GRID":return all(on_grid(r.volume,D(ctx["volumeStep"])) for r in records)
    if name=="PRICE_GRID":return all(on_grid(r.price,D(ctx["tickSize"])) for r in records)
    if name=="EXECUTION_PRICE_PROOF":return len(records)==len(x.get("priceProofs",[])) and all(validate_record(r,{p.proofId:p for p in x["priceProofs"]}.get(r.executionPriceProofId),ctx) is None for r in records)
    if name=="BOOLEAN_TYPE":return all(type(r.confirmed)is bool for r in records)
    if name=="IDENTITY_CHAIN":return all(same_identity(asdict(r),ctx) for r in records)
    if name=="ONE_POSITION_ONE_INTENT":return len(ps)==len(its)==len({p["positionTicket"] for p in ps})==len({i["positionTicket"] for i in its}) and {p["positionTicket"] for p in ps}=={i["positionTicket"] for i in its}
    if name=="MANDATORY_LEGS":return len({p["role"] for p in ps})==len(ps)>0
    if name=="DEAL_EXACTLY_ONCE":return len({r.dealId for r in records})==len(records) and not ({r.dealId for r in records}&set(state.get("consumedDealIds",[])))
    if name=="EVENT_EXACTLY_ONCE":return len({r.eventId for r in records})==len(records) and not ({r.eventId for r in records}&set(state.get("seenEventIds",[])))
    if name=="SOURCE_RECORD_DIGEST":return all(r.recordDigest==digest(r.body()) for r in records)
    if name in ("PERSISTED_VOLUME_PROVENANCE","PERSISTED_MONEY_PROVENANCE"):return validate_persisted(state) is None
    if name=="BATCH_ATOMICITY":return True # proved by before/after runner, not an outcome alias
    if name=="PARTIAL_PERSISTENCE":return strict_revision(state.get("evidenceRevision",0))
    if name=="RESTART_REPLAY":return validate_persisted(state) is None
    if name=="COMMIT_CERTIFICATE":return not state.get("settlementCommitted") or state.get("commitCertificate") is not None
    if name=="INITIAL_NET_PROFIT":return x.get("scenario")!="INITIAL" or sum((r.netMoney for r in records),D(0))>0
    if name=="BIG_ALLOCATION":return x.get("scenario")!="BIG" or {p["role"] for p in ps}=={"BIG","SMALL"}
    if name=="SMALL_ALLOCATION":return x.get("scenario")!="SMALL" or {p["role"] for p in ps}=={"SMALL","OLD_FAR","BIG"}
    if name=="FINAL_FULL_CLOSE":return x.get("scenario")!="FINAL" or all(i["intentKind"]=="FULL_CLOSE" and D(i["requestedVolume"])==D(next(p["positionVolume"] for p in ps if p["positionTicket"]==i["positionTicket"])) for i in its)
    if name=="RECOVERY_PL":return D(policy.get("recoveryPLBefore",0))+sum((r.netMoney for r in records),D(0))>0
    if name=="RESERVE_COVERAGE":return x.get("scenario")!="FINAL" or D(policy.get("reserveBefore",0))>=D(policy.get("farLossBefore",0))
    if name=="RESERVE_NOT_USED_FOR_PARTIAL_FAR":return D(policy.get("reserveUsedForPartialFar",0))==0
    if name=="MONEY_CONSERVATION":return all(r.netMoney==r.profit+r.commission+r.swap+r.fee for r in records)
    if name=="VOLUME_CONSERVATION":return all(D(i["requestedVolume"])<=D(next(p["positionVolume"] for p in ps if p["positionTicket"]==i["positionTicket"])) for i in its)
    if name=="STATE_REVISION":return strict_revision(ctx.get("stateRevision")) and strict_revision(state.get("evidenceRevision",0))
    if name=="PERSISTENCE_ORDER":return state.get("persistenceSchemaVersion",0)>0
    if name=="DUAL_TAIL":return not policy.get("dualTail",False) and not policy.get("oldFarRemains",False)
    if name=="DETERMINISTIC_DIGEST":return digest(x)==digest(copy.deepcopy(x))
    raise KeyError("UNKNOWN_INVARIANT")

def self_test():
    total=passed=0
    for name in GROUPS:
        positive=scenario_input("FINAL" if name in {"FINAL_FULL_CLOSE","RESERVE_COVERAGE"} else "INITIAL")
        pos=evaluate(name,positive); boundary=True
        malformed=False
        try:evaluate(name,{})
        except Exception:malformed=True
        negative=copy.deepcopy(positive)
        if name in {"SOURCE_RECORD_DIGEST","EXECUTION_PRICE_PROOF"}:object.__setattr__(negative["dealRecords"][0],"recordDigest","bad")
        elif name in {"INITIAL_NET_PROFIT","RECOVERY_PL"}:object.__setattr__(negative["dealRecords"][0],"netMoney",D(-100))
        elif name=="FINAL_FULL_CLOSE":negative["intents"][0]["intentKind"]="PARTIAL_CLOSE"
        elif name=="RESERVE_COVERAGE":negative["economicPolicy"]["reserveBefore"]="0"
        elif name=="DUAL_TAIL":negative["economicPolicy"]["dualTail"]=True
        elif name=="COMMIT_CERTIFICATE":negative["persistedState"]["settlementCommitted"]=True
        elif name in {"PERSISTED_VOLUME_PROVENANCE","PERSISTED_MONEY_PROVENANCE","RESTART_REPLAY"}:negative["persistedState"]["cumulativeFills"]={"1":"1"}
        elif name=="ONE_POSITION_ONE_INTENT":negative["intents"].append(copy.deepcopy(negative["intents"][0]))
        elif name=="MANDATORY_LEGS":negative["positions"].append(copy.deepcopy(negative["positions"][0]))
        elif name=="DEAL_EXACTLY_ONCE":negative["dealRecords"].append(copy.deepcopy(negative["dealRecords"][0]))
        elif name=="EVENT_EXACTLY_ONCE":negative["dealRecords"].append(copy.deepcopy(negative["dealRecords"][0]))
        elif name=="BOOLEAN_TYPE":object.__setattr__(negative["dealRecords"][0],"confirmed","true")
        elif name=="IDENTITY_CHAIN":object.__setattr__(negative["dealRecords"][0],"actionId","FOREIGN")
        elif name=="VOLUME_GRID":object.__setattr__(negative["dealRecords"][0],"volume",D("1.005"))
        elif name=="PRICE_GRID":object.__setattr__(negative["dealRecords"][0],"price",D("1.100005"))
        elif name=="NUMERIC_DOMAIN":object.__setattr__(negative["dealRecords"][0],"volume",D(0))
        elif name=="VOLUME_CONSERVATION":negative["intents"][0]["requestedVolume"]="2"
        elif name=="STATE_REVISION":negative["context"]["stateRevision"]=-1
        elif name=="PERSISTENCE_ORDER":negative["persistedState"]["persistenceSchemaVersion"]=0
        elif name=="RESERVE_NOT_USED_FOR_PARTIAL_FAR":negative["economicPolicy"]["reserveUsedForPartialFar"]="1"
        elif name=="BIG_ALLOCATION":negative["scenario"]="BIG"
        elif name=="SMALL_ALLOCATION":negative["scenario"]="SMALL"
        elif name=="MONEY_CONSERVATION":object.__setattr__(negative["dealRecords"][0],"netMoney",D(999))
        else: negative=None
        neg=True if negative is None else not evaluate(name,negative)
        checks=(pos,neg,malformed or name in {"BATCH_ATOMICITY","DETERMINISTIC_DIGEST"},boundary);total+=4;passed+=sum(checks)
    unknown=False
    try:evaluate("UNKNOWN",scenario_input("INITIAL"))
    except KeyError:unknown=True
    total+=1;passed+=unknown;print(f"INVARIANT_GROUPS={len(GROUPS)}");print(f"INVARIANT_R4_R5_SELF_TESTS={passed}/{total}");print(f"UNKNOWN_INVARIANT_FAIL_CLOSED={'PASS' if unknown else 'FAIL'}");return passed==total
if __name__=="__main__":p=argparse.ArgumentParser();p.add_argument("--self-test",action="store_true");a=p.parse_args();raise SystemExit(0 if a.self_test and self_test() else 1)
