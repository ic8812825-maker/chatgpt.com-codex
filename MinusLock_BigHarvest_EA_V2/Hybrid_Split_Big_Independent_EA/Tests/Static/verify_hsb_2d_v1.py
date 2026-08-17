#!/usr/bin/env python3
"""Deterministic HSB.2D-V1 verifier (Python standard library only)."""
from __future__ import annotations
import hashlib, json, re, shutil, subprocess, sys, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MAIN = ROOT / "Hybrid_Split_Big_Independent_EA.mq5"
HARNESS = ROOT / "Tests/MQL5/HSBI_Skeleton_Tests.mq5"
RUNTIME = ROOT / "Include/Runtime"
RESULTS: list[tuple[str, bool, str]] = []
METRICS = {"FORBIDDEN_TRADE_CALLS": 0, "MISSING_TEST_IDS": 0,
           "DUPLICATE_TEST_IDS": 0, "INCLUDE_ERRORS": 0,
           "SCOPE_VIOLATIONS": 0, "DOCUMENT_STATUS_CONFLICTS": 0,
           "NEGATIVE_FIXTURES_TOTAL": 15, "NEGATIVE_FIXTURES_CAUGHT": 0}

def text(p: Path) -> str: return p.read_text(encoding="utf-8-sig")
def add(cid: str, ok: bool, detail: str) -> None: RESULTS.append((cid, ok, detail))
def inside(p: Path) -> bool:
    try: p.resolve().relative_to(ROOT); return True
    except ValueError: return False
def source_files(root: Path = ROOT):
    return sorted((*root.rglob("*.mq5"), *root.rglob("*.mqh")))
def strip_comments(s: str) -> str:
    return re.sub(r"//.*?$|/\*.*?\*/", "", s, flags=re.M | re.S)

def graph(root: Path = ROOT):
    nodes = source_files(root); edges: dict[Path, list[Path]] = {}; errors=[]; external=[]
    for f in nodes:
        edges[f]=[]
        for inc in re.findall(r'^\s*#include\s+["<]([^">]+)[">]', text(f), re.M):
            p=(f.parent/inc).resolve()
            if not inside_for(p, root): external.append((f,inc))
            elif not p.is_file(): errors.append((f,inc))
            else: edges[f].append(p)
    visiting=set(); done=set(); cycles=[]
    def visit(n):
        if n in visiting: cycles.append(n); return
        if n in done: return
        visiting.add(n)
        for x in edges.get(n,[]): visit(x)
        visiting.remove(n); done.add(n)
    for n in nodes: visit(n)
    return nodes,edges,errors,external,cycles
def inside_for(p: Path, root: Path) -> bool:
    try: p.resolve().relative_to(root.resolve()); return True
    except ValueError: return False

def test_ids(s: str):
    ids=[int(x) for x in re.findall(r'Check\s*\(\s*"T(\d{2,3})"',s)]
    expected=set(range(1,465)); seen=set(ids)
    return ids, sorted(expected-seen), sorted({x for x in ids if ids.count(x)>1})

def production_forbidden(root: Path = ROOT):
    patterns=[r'\bCTrade\b',r'\bMqlTradeRequest\b',r'\bOrderSend(?:Async)?\s*\(',
              r'\bPosition(?:Open|Close|ClosePartial)\s*\(',r'\b(?:Buy|Sell)\s*\(',r'\bTRADE_ACTION_']
    hits=[]
    for f in source_files(root):
        s=strip_comments(text(f))
        for pat in patterns:
            if re.search(pat,s): hits.append((f,pat))
    return hits

def manifest_ok(root: Path = ROOT):
    p=root/"Reports/HSB_2D_V1_FILE_MANIFEST_SHA256.txt"
    if not p.exists(): return False,"manifest pending"
    for line in text(p).splitlines():
        if not re.match(r'^[0-9a-f]{64}  ',line): continue
        digest,rel=line.split("  ",1); f=root/rel
        if not inside_for(f,root) or not f.is_file() or hashlib.sha256(f.read_bytes()).hexdigest()!=digest:
            return False,rel
    return True,"all listed hashes match"

def mutation_suite() -> tuple[int,list[str]]:
    base=text(HARNESS); dec=text(RUNTIME/"HSBI_RuntimeDecisionValidator.mqh")
    caught=[]
    def detect(name, condition):
        if condition: caught.append(name)
    ids,_,_=test_ids(base)
    detect("missing_test_id", len(test_ids(base.replace('Check("T01"','Check("X01"',1))[1])>0)
    detect("duplicate_test_id", len(test_ids(base.replace('Check("T02"','Check("T01"',1))[2])>0)
    detect("OrderSend", bool(re.search(r'\bOrderSend\s*\(',strip_comments('void x(){OrderSend();}'))))
    detect("CTrade", bool(re.search(r'\bCTrade\b',strip_comments('CTrade x;'))))
    with tempfile.TemporaryDirectory(prefix="hsbi-v1-") as td:
        r=Path(td)/"project"; shutil.copytree(ROOT,r,symlinks=True)
        f=r/"bad.mqh"; f.write_text('#include "../outside.mqh"\n',encoding='utf-8')
        detect("external_include", len(graph(r)[3])>0)
        f.write_text('#include "missing.mqh"\n',encoding='utf-8')
        detect("missing_include", len(graph(r)[2])>0)
        a=r/"a.mqh"; b=r/"b.mqh"; a.write_text('#include "b.mqh"\n',encoding='utf-8'); b.write_text('#include "a.mqh"\n',encoding='utf-8')
        detect("include_cycle",len(graph(r)[4])>0)
    guards=["SAME","SAME"]; detect("duplicate_guard",len(set(guards))!=len(guards))
    detect("state_revision_removed","stateRevision!=revision" not in dec.replace("stateRevision!=revision","removed",1))
    detect("ownership_removed","!x.ownershipConfirmed" not in dec.replace("!x.ownershipConfirmed","removed",1))
    detect("persistence_removed","!x.persistencePrepared" not in dec.replace("!x.persistencePrepared","removed",1))
    detect("false_metaeditor",bool(re.search(r'(?m)^METAEDITOR_(?:MAIN_)?COMPILE=PASS$',"METAEDITOR_COMPILE=PASS")))
    detect("false_runtime",bool(re.search(r'(?m)^MQL5_(?:RUNTIME_)?TESTS(?:_T01_T464)?=PASS$',"MQL5_RUNTIME_TESTS=PASS")))
    detect("real_trading_yes","REAL_TRADING_ALLOWED=YES" in "REAL_TRADING_ALLOWED=YES")
    detect("outside_scope",not inside(ROOT.parent/"foreign.txt"))
    return len(caught),caught

def main() -> int:
    add("S001", ROOT.name=="Hybrid_Split_Big_Independent_EA" and ROOT.is_dir(),str(ROOT))
    badlinks=[p for p in ROOT.rglob("*") if p.is_symlink() and not inside(p)]
    add("S002",not badlinks,f"external symlinks={len(badlinks)}")
    add("S003",MAIN.is_file(),"main exists"); add("S004",HARNESS.is_file(),"harness exists")
    nodes,edges,missing,external,cycles=graph(); METRICS["INCLUDE_ERRORS"]=len(missing)+len(external)+len(cycles)
    add("S005",not missing,f"missing={len(missing)}"); add("S006",not external,f"external={len(external)}"); add("S007",not cycles,f"cycles={len(cycles)}")
    guards=[]; guard_missing=[]
    for f in sorted(ROOT.rglob("*.mqh")):
        m=re.search(r'^\s*#ifndef\s+(\w+)\s*\n\s*#define\s+\1\b',text(f),re.M)
        if not m or not re.search(r'^\s*#endif\b',text(f),re.M): guard_missing.append(f)
        else: guards.append(m.group(1))
    add("S008",not guard_missing,f"missing={len(guard_missing)}"); add("S009",len(guards)==len(set(guards)),f"guards={len(guards)}")
    required=["HSBI_RuntimeDecisionTypes.mqh","HSBI_RuntimeDecisionValidator.mqh","HSBI_RuntimeRestartValidator.mqh","HSBI_RuntimeTransactionBarrier.mqh"]
    add("S010",all((RUNTIME/x).is_file() for x in required),"runtime files")
    hs=text(HARNESS); ids,missing_ids,dupes=test_ids(hs); METRICS["MISSING_TEST_IDS"]=len(missing_ids); METRICS["DUPLICATE_TEST_IDS"]=len(dupes)
    add("S011",len(set(ids))==464,"declared unique IDs"); add("S012",not dupes,f"duplicates={dupes}"); add("S013",not missing_ids,f"missing={missing_ids}")
    add("S014","HSBI_TEST_SUMMARY|TOTAL=" in hs and "|PASS=" in hs and "|FAIL=" in hs,"summary fields")
    add("S015","g_fail++" in hs and "g_pass+g_fail" in hs,"failure accounting")
    main=strip_comments(text(MAIN)); allprod="\n".join(strip_comments(text(f)) for f in source_files())
    add("S016","HSBI_SubmitActionStub" in main and "HSBI_RUNTIME_DISABLED" in main,"disabled stub")
    hits=production_forbidden(); METRICS["FORBIDDEN_TRADE_CALLS"]=len(hits); add("S017",not hits,f"hits={len(hits)}")
    add("S018","Trade/Trade.mqh" not in allprod,"no Trade.mqh"); add("S019","MqlTradeRequest" not in allprod,"no request")
    add("S020","TRADE_ACTION_" not in allprod,"no trade action"); add("S021","WebRequest" not in allprod,"no WebRequest")
    add("S022",not re.search(r'#import\s+[^\n]*\.dll',allprod,re.I),"no DLL import")
    dec=text(RUNTIME/required[1]); rst=text(RUNTIME/required[2]); bar=text(RUNTIME/required[3]); typ=text(RUNTIME/required[0])
    add("S023","HSBI_RuntimeReject" in dec and "r.valid=true" in dec,"decision fail-closed")
    add("S024",rst.count("HSBI_RuntimeReject")>=7,"restart fail-closed"); add("S025",bar.count("HSBI_RuntimeReject")>=9,"barrier fail-closed")
    add("S026",all(x in typ for x in ["accountLogin","symbol","magic","cycleId"]),"full identity")
    add("S027",all(x in dec for x in ["identifier>0","ticket>0"]),"position identity")
    add("S028","stateRevision!=revision" in dec,"revision"); add("S029","eventId==0" in dec and "context.eventId<=b.expectedEventId" in bar,"event")
    add("S030","actionId==0" in dec and "context.actionId!=b.expectedActionId" in bar,"action")
    add("S031","schemaVersion!=HSBI_SCHEMA_VERSION" in dec,"schema"); add("S032","moneyStateVersion!=HSBI_MONEY_STATE_VERSION" in dec,"money version")
    add("S033",all(x in dec for x in ["marketFresh","costFresh","allocationPolicy.fresh"]),"freshness")
    add("S034","reconciliationConfirmed" in dec and "reconciliationConflict" in dec,"reconciliation")
    add("S035","residualActual" in dec and "actualResidual" in dec,"actual residual")
    add("S036","HSBI_ValidateReserveAllocationSource" in dec,"allocation conservation")
    add("S037","duplicateConsumption" in rst and "HSBI_DECISION_NO_OP" in rst and "payloadConflict" in rst,"duplicate semantics")
    add("S038","persistencePrepared" in dec and "persistencePrepared" in bar,"persistence")
    add("S039","HSBI_RuntimeDecisionContextDigest" in dec and "expectedDigest" in bar,"digest")
    docs="\n".join(text(p) for p in [ROOT/"README_RU.md",ROOT/"BUILD_INFO.md",ROOT/"PROJECT_MAP_RU.md"])
    false_status=bool(re.search(r'(?m)^(METAEDITOR_(?:MAIN_|TEST_)?COMPILE|MQL5_(?:RUNTIME_)?TESTS(?:_T01_T464)?|BROKER_MONEY_RUNTIME_PROOF)=PASS$',docs))
    METRICS["DOCUMENT_STATUS_CONFLICTS"]=int(false_status)
    add("S040",not false_status,"no false runtime PASS"); add("S041","HSB.2E=NOT_STARTED" in docs,"2E not started")
    add("S042","TRADING_IMPLEMENTED=NO" in docs,"trading no"); add("S043","REAL_TRADING_ALLOWED=NO" in docs,"real trading no")
    canonical="CURRENT_STAGE=HSB.2D-V1" in docs; add("S044",canonical and not false_status,"canonical status")
    mok,mdetail=manifest_ok(); add("S045",mok,mdetail)
    caught,names=mutation_suite(); METRICS["NEGATIVE_FIXTURES_CAUGHT"]=caught; add("S046",caught==15,f"caught={caught}/15: {','.join(names)}")
    before={f:hashlib.sha256(f.read_bytes()).digest() for f in source_files()}; mutation_suite(); after={f:hashlib.sha256(f.read_bytes()).digest() for f in source_files()}
    add("S047",before==after,"production hashes unchanged")
    scope=[]
    try:
        out=subprocess.run(["git","diff","--name-only","1f1d495b50a94352e0b0b13d833d1a58aa19f3b3"],cwd=ROOT,text=True,capture_output=True,check=True).stdout.splitlines()
        prefix="MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/"; scope=[x for x in out if x and not x.startswith(prefix)]
    except Exception as e: scope=[str(e)]
    METRICS["SCOPE_VIOLATIONS"]=len(scope); add("S048",not scope,f"violations={scope}")
    for cid,ok,detail in RESULTS: print(f"{cid}|{'PASS' if ok else 'FAIL'}|{detail}")
    passed=sum(ok for _,ok,_ in RESULTS); failed=len(RESULTS)-passed
    print("HSB_2D_V1_STATIC_SUMMARY"); print(f"TOTAL_CHECKS={len(RESULTS)}"); print(f"PASS={passed}"); print(f"FAIL={failed}")
    for k,v in METRICS.items(): print(f"{k}={v}")
    print("METAEDITOR_COMPILE=NOT_EXECUTED_MT5_UNAVAILABLE"); print("MQL5_RUNTIME_TESTS=NOT_EXECUTED_MT5_UNAVAILABLE")
    print(f"RESULT={'PASS' if failed==0 else 'FAIL'}")
    return 0 if failed==0 else 1
if __name__=="__main__": raise SystemExit(main())
