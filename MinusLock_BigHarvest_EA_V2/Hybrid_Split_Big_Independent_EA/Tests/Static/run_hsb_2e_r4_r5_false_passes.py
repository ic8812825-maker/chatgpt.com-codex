#!/usr/bin/env python3
"""Executable reproduction of the six R4-R4 false-positive classes reopened by R5."""
import argparse, copy, hashlib, json, sys
from pathlib import Path

BASELINE = "5679b34f66c4f75cc1f6ee9e7882630d1453f9cc"

def sha(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

def main(root):
    root = Path(root).resolve()
    sys.path.insert(0, str(root / "Tests/Reference"))
    from hsb_2e_reference_model_r4_r4 import execute_scenario
    vectors = json.loads((root / "Tests/Vectors/HSB_2E_R4_R4_VECTORS.json").read_text())["vectors"]
    by_id = {v["VECTOR_ID"]: v["INPUT"] for v in vectors}
    cases = []
    def add(cid, source, mutate, expected, root_cause):
        value = copy.deepcopy(by_id[source]); mutate(value)
        actual = execute_scenario(copy.deepcopy(value))
        reproduced = (actual["status"] == "PASS" and actual["phase"] in {"FSM_COMMITTED", "IDEMPOTENT_REPLAY"}) or (
            cid == "FP-R5-04" and actual["status"] != "PASS" and "atomicBatchValidated" not in actual.get("output", {}))
        record = {"COUNTEREXAMPLE_ID":cid,"BASELINE_SHA":BASELINE,"SOURCE_VECTOR_ID":source,
                  "MUTATED_FIELDS":mutate.__name__.removeprefix("m_"),"HISTORICAL_ACTUAL":{"status":actual["status"],"phase":actual["phase"],"reason":actual["reason"]},
                  "NORMATIVE_EXPECTED":expected,"ROOT_CAUSE":root_cause,"INPUT_SHA256":sha(value),"OUTPUT_SHA256":sha(actual),"EXIT_CODE":0,"REPRODUCED":reproduced}
        cases.append(record)
    def m_price(x): x["executionPriceWindowProven"]=True; x["deals"][0]["price"]="99999.00"
    def m_cache(x):
        x["deals"]=[]; s=x["persistedState"]; s.update(cumulativeFills={str(i["positionTicket"]):i["requestedVolume"] for i in x["intents"]},consumedDealIds=[],seenEventIds=[],dealEventBindings={},moneyByDeal={},moneyByTicket={},settlementCommitted=False)
    def m_commit(x): x["deals"]=[]; x["persistedState"]["settlementCommitted"]=True
    def m_batch(x): x["deals"].append({"malformed":True})
    def m_initial(x):
        d=x["deals"][0]; d.update(profit="-100",commission="-1",swap="0",fee="0")
    def m_final(x):
        x["intents"][0]["intentKind"]="PARTIAL_CLOSE"; x["intents"][0]["requestedVolume"]=".25"; x["deals"][0]["volume"]=".25"
    add("FP-R5-01","R4_VALID_BIG",m_price,{"status":"NOT_PASS","reason":"EXECUTION_PRICE_PROOF_INVALID"},"bare Boolean bypasses price provenance")
    add("FP-R5-02","R4_VALID_BIG",m_cache,{"status":"NOT_PASS","reason":"CUMULATIVE_FILL_PROVENANCE_MISSING"},"derived fill cache is trusted without source records")
    add("FP-R5-03","R4_VALID_BIG",m_commit,{"status":"REJECT","reason":"COMMIT_CERTIFICATE_MISSING"},"committed Boolean is trusted without certificate")
    add("FP-R5-04","R4_VALID_BIG",m_batch,{"status":"ATOMIC_REJECT"},"validation and application are interleaved")
    add("FP-R5-05","R4_VALID_INITIAL",m_initial,{"status":"REJECT","reason":"INITIAL_NET_NOT_POSITIVE"},"Initial settlement lacks positive actual-net gate")
    add("FP-R5-06","R4_VALID_FINAL",m_final,{"status":"REJECT","reason":"FINAL_REQUIRES_FULL_CLOSE"},"Final incorrectly allows partial Far close")
    result={"BASELINE_SHA":BASELINE,"R5_FALSE_PASS_REQUIRED":len(cases),"R5_FALSE_PASS_EXECUTED":len(cases),"R5_FALSE_PASS_REPRODUCED":sum(c["REPRODUCED"] for c in cases),"cases":cases}
    result["RESULT"]="PASS" if result["R5_FALSE_PASS_REPRODUCED"]==len(cases) else "FAIL"
    print(json.dumps(result,sort_keys=True,separators=(",",":")))
    return result["RESULT"]=="PASS"

if __name__ == "__main__":
    p=argparse.ArgumentParser(); p.add_argument("--root",required=True); a=p.parse_args()
    raise SystemExit(0 if main(a.root) else 1)
