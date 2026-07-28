"""Isolated end-to-end fixtures for the sixth-correction discovery pipeline."""
from __future__ import annotations
import json
import shutil
import tempfile
from pathlib import Path

from stage_3_1_3.discovery import discover
from stage_3_1_3.source_evidence import index_mql

HERE=Path(__file__).parent/"fixtures"


def _run_one(relative: str, expected: dict) -> dict:
    source=HERE/relative
    with tempfile.TemporaryDirectory() as directory:
        root=Path(directory);shutil.copy2(source,root/source.name)
        contract={"canonical":expected.get("identifier","targetLot"),"aliases":[],"unit":expected.get("unit","LOT"),"scope":expected.get("scope","GLOBAL_RUNTIME"),"lineages":{expected.get("lineage","TERMINAL_POSITION")},"authoritative":expected.get("lineage") in {"TERMINAL_POSITION","DEAL_HISTORY","CONFIG_INPUT"},"temporal":expected.get("temporal","ACTUAL_CURRENT"),"lifecycle":expected.get("lifecycle","ACTUAL_POSITION")}
        return discover(root,contract,"mql5",index_mql(root))


def run_fixture_controls(verbose=False):
    positive=json.loads((HERE/"positive_manifest.json").read_text());presults=[]
    for name,item in positive.items():
        result=_run_one(item["file"],item)
        evaluated=result["evaluated_candidates"]
        candidate=next((x for x in evaluated if x["identifier"]==item["identifier"]),None)
        ok=bool(candidate and candidate["unit"]==item["unit"] and candidate["use_graph"] is not None and result["computed_status"] in {"EXACT_MATCH","SEMANTIC_MATCH","PARTIAL_MATCH","AMBIGUOUS"})
        if name=="VALID_AMBIGUOUS_PAIR":ok=result["computed_status"]=="AMBIGUOUS"
        presults.append((name,ok))
    adversarial=json.loads((HERE/"adversarial_manifest.json").read_text());aresults=[]
    for name,item in adversarial.items():
        result=_run_one(item["file"],{"identifier":"targetLot","unit":"LOT","scope":"PER_SYMBOL_MAGIC","lineage":"TERMINAL_POSITION"})
        evaluated=result["evaluated_candidates"]
        # Each attack is caught by independent evidence: mismatch, partial/missing,
        # ambiguity, contradictory use, or full-use discovery beyond one claimed site.
        caught=result["computed_status"] in {"MISSING","PARTIAL_MATCH","AMBIGUOUS"}
        if name in {"SECOND_EQUAL_CANDIDATE_HIDDEN","WRONG_UNIQUE_WINNER","EXACT_WITH_COMPETING_CANDIDATE"}:caught=result["computed_status"]=="AMBIGUOUS"
        if name=="USE_SITE_WITH_CONTRADICTORY_ROLE_OMITTED":caught=any(not x["proof"]["no_contradictory_use"] for x in evaluated)
        if name=="PARTIAL_USE_GRAPH_CLAIMED_COMPLETE":caught=any(len(x["use_graph"]["call_sites"])>1 for x in evaluated)
        aresults.append((name,caught))
    if verbose:
        for name,ok in presults:print(f"POSITIVE_FIXTURE_{name}={'PASS' if ok else 'FAIL'}")
        for name,ok in aresults:print(f"ADVERSARIAL_FIXTURE_{name}={'PASS' if ok else 'FAIL'}")
        print(f"POSITIVE_FIXTURES_TOTAL={len(presults)}\nPOSITIVE_FIXTURES_PASSED={sum(x[1] for x in presults)}")
        print(f"ADVERSARIAL_FIXTURES_TOTAL={len(aresults)}\nADVERSARIAL_FIXTURES_CAUGHT={sum(x[1] for x in aresults)}")
    return len(presults),sum(x[1] for x in presults),len(aresults),sum(x[1] for x in aresults)


if __name__=="__main__":
    pt,pp,at,ap=run_fixture_controls(True);raise SystemExit(not(pt==pp and at==ap and pt>=20 and at>=20))
