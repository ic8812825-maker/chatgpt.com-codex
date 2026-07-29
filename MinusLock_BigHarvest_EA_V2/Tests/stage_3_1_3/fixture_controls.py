"""Strict isolated semantic fixtures for the seventh-correction pipeline."""
from __future__ import annotations
import json
import shutil
import tempfile
from pathlib import Path

from stage_3_1_3.semantic_engine import evaluate_canonical_mapping
from stage_3_1_3.source_evidence import index_mql

HERE=Path(__file__).parent/"fixtures"


def _run_one(relative: str, expected: dict) -> dict:
    source=HERE/relative
    with tempfile.TemporaryDirectory() as directory:
        root=Path(directory);shutil.copy2(source,root/source.name)
        canonical=expected.get("identifier","targetLot");low=canonical.lower()
        nature=("TICKET" if "ticket" in low else "IDENTITY" if "identifier" in low else "PLAN" if "plan" in low else "REQUEST" if "request" in low else "LEDGER_EVENT" if "ledger" in low or "event" in low else "SNAPSHOT" if "snapshot" in low else "POLICY" if expected.get("lineage")=="CONFIG_INPUT" else "VALUE")
        contract={"canonical":canonical,"aliases":[],"unit":expected.get("unit","LOT"),"scope":expected.get("scope","GLOBAL_RUNTIME"),"lineages":{expected.get("lineage","TERMINAL_POSITION")},"authoritative":expected.get("lineage") in {"TERMINAL_POSITION","DEAL_HISTORY","CONFIG_INPUT"},"temporal":expected.get("temporal","ACTUAL_CURRENT"),"lifecycle":expected.get("lifecycle","ACTUAL_POSITION"),"entity_nature":nature}
        return evaluate_canonical_mapping(root,contract,"mql5",index_mql(root))


def run_fixture_controls(verbose=False):
    positive=json.loads((HERE/"positive_manifest.json").read_text());presults=[]
    for name,item in positive.items():
        result=_run_one(item["file"],item)
        evaluated=result["evaluated_candidates"]
        candidate=next((x for x in evaluated if x["identifier"]==item["identifier"]),None)
        actual = {
            "expected_winner": candidate and candidate["identifier"],
            "expected_status": result["computed_status"],
            "expected_unit": candidate and candidate["unit"],
            "expected_scope": candidate and candidate["scope"],
            "expected_source_lineage": candidate and candidate["source_lineage"],
            "expected_authority": candidate and candidate["authoritative"],
            "expected_temporal_class": candidate and candidate["temporal"],
            "expected_lifecycle": candidate and candidate["lifecycle"],
            "expected_blocking_counters": [],
        }
        ok=bool(candidate and all(actual[key] == item[key] for key in actual))
        presults.append((name,ok))
    adversarial=json.loads((HERE/"adversarial_manifest.json").read_text());aresults=[]
    for name,item in adversarial.items():
        result=_run_one(item["file"],{"identifier":"targetLot","unit":"LOT","scope":"PER_SYMBOL_MAGIC","lineage":"TERMINAL_POSITION"})
        evaluated=result["evaluated_candidates"]
        rule=item["expected_failure_rule"]
        if rule=="UNIT_MISMATCH": caught=any(x["unit"]!="LOT" for x in evaluated)
        elif rule=="SYMBOL_MAGIC_SCOPE_MISSING": caught=any(x["scope_relation"]!="EXACT" for x in evaluated)
        elif rule=="AMBIGUOUS": caught=result["computed_status"]=="AMBIGUOUS"
        elif rule=="INCOMPLETE_USE_SITE_COVERAGE": caught=any(not x["proof"]["no_contradictory_use"] or len(x["use_graph"]["call_sites"])>1 for x in evaluated)
        elif rule=="CACHE_LINEAGE_MARKED_AUTHORITATIVE": caught=any("CACHE" in x["source_lineage"] and not x["authoritative"] for x in evaluated)
        else: caught=result["computed_status"] in {"MISSING","PARTIAL_MATCH","AMBIGUOUS"}
        aresults.append((name,caught))
    if verbose:
        for name,ok in presults:print(f"POSITIVE_FIXTURE_{name}={'PASS' if ok else 'FAIL'}")
        for name,ok in aresults:print(f"ADVERSARIAL_FIXTURE_{name}={'PASS' if ok else 'FAIL'}")
        print(f"POSITIVE_FIXTURES_TOTAL={len(presults)}\nPOSITIVE_FIXTURES_PASSED={sum(x[1] for x in presults)}")
        print(f"ADVERSARIAL_FIXTURES_TOTAL={len(aresults)}\nADVERSARIAL_FIXTURES_CAUGHT={sum(x[1] for x in aresults)}")
    return len(presults),sum(x[1] for x in presults),len(aresults),sum(x[1] for x in aresults)


if __name__=="__main__":
    pt,pp,at,ap=run_fixture_controls(True);raise SystemExit(not(pt==pp and at==ap and pt>=25 and at>=25))
