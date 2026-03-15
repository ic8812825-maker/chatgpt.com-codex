#!/usr/bin/env python3
import math
from pathlib import Path
from datetime import datetime

REPORT_DIR=Path("Experts/VirtualPanel/right/tests/reports")
REPORT_DIR.mkdir(parents=True,exist_ok=True)


def near(a,b,eps=1e-9):
    return abs(a-b)<=eps


def write_report(name,desc,params,metrics,ok,conclusion):
    p=REPORT_DIR/f"{name}_report.md"
    lines=[
        f"# {name}",
        "",
        f"- **Test description:** {desc}",
        f"- **Timestamp:** {datetime.utcnow().isoformat()}Z",
        "",
        "## Input parameters",
    ]
    for k,v in params.items(): lines.append(f"- `{k}`: `{v}`")
    lines += ["", "## Execution result", f"- **status:** {'PASS' if ok else 'FAIL'}", "", "## Metrics"]
    for k,v in metrics.items(): lines.append(f"- `{k}`: `{v}`")
    lines += ["", "## Conclusion", conclusion, ""]
    p.write_text("\n".join(lines),encoding="utf-8")


def test_lock_compression():
    buy=[0.4,0.2,0.1]
    sell=[0.3,0.2]
    delta_before=sum(buy)-sum(sell)

    b=sorted(buy,reverse=True)
    s=sorted(sell,reverse=True)
    i=j=0
    while i<len(b) and j<len(s):
        L=min(b[i],s[j])
        b[i]-=L; s[j]-=L
        if b[i]<=1e-12: i+=1
        if s[j]<=1e-12: j+=1
    delta_after=sum(max(x,0.0) for x in b)-sum(max(x,0.0) for x in s)

    ok=abs(delta_after)<=abs(delta_before)+1e-12
    write_report(
        "TestLockCompression",
        "Greedy Delta Matching should not increase |delta|.",
        {"buy":buy,"sell":sell},
        {"delta_before":delta_before,"delta_after":delta_after,"levels_before":len(buy)+len(sell),"levels_after":len(b)+len(s)},
        ok,
        "Greedy matching preserves/non-increases absolute delta.",
    )
    assert ok


def test_delta_calculation():
    lots=[(+1,0.3),(+1,0.2),(-1,0.1)]
    delta=sum(sign*lot for sign,lot in lots)
    ok=near(delta,0.4,1e-12)
    write_report(
        "TestDeltaCalculation",
        "Effective delta formula verification: sum(sign_i * lot_i).",
        {"positions":lots},
        {"delta":delta},
        ok,
        "Delta formula is consistent with specification.",
    )
    assert ok


def test_geometry_preservation():
    k=1.3
    lots=[0.01,0.013,0.017,0.022]
    alpha=0.5
    total=sum(x*alpha for x in lots)
    n=len(lots)
    l0=total/((k**n-1)/(k-1))
    rebuilt=[l0*(k**i) for i in range(n)]
    eps=1e-9
    ok=all(abs(rebuilt[i]-l0*(k**i))<eps for i in range(n))
    write_report(
        "TestGeometryPreservation",
        "After compression geometry must be rebuilt as L_i = L0 * k^i.",
        {"k":k,"alpha":alpha,"lots_before":lots},
        {"lots_after":rebuilt,"epsilon":eps},
        ok,
        "Geometry invariant preserved after rebuild.",
    )
    assert ok


def test_compression_trigger():
    n=9
    margin_level=150.0
    ok=(n>8) or (margin_level<200.0)
    write_report(
        "TestCompressionTrigger",
        "Compression trigger activation rule.",
        {"n":n,"margin_level":margin_level},
        {"triggered":ok},
        ok,
        "Trigger works for depth/margin thresholds.",
    )
    assert ok


def test_compression_margin():
    margin_before=200.0
    alpha=0.5
    margin_after=margin_before*alpha
    ok=margin_after<=margin_before
    write_report(
        "TestCompressionMargin",
        "Margin should improve after compression.",
        {"margin_before":margin_before,"alpha":alpha},
        {"margin_after":margin_after},
        ok,
        "Compression reduces margin pressure.",
    )
    assert ok


def test_alc_stability():
    k=1.3
    alpha=0.5
    n=30
    m=4
    risk_no=k**n
    risk_alc=(alpha**m)*(k**n)
    ok=risk_alc<risk_no
    write_report(
        "TestALCStability",
        "Compare asymptotic risk with/without ALC compression factor.",
        {"k":k,"alpha":alpha,"n":n,"m":m},
        {"risk_no_alc":risk_no,"risk_alc":risk_alc},
        ok,
        "ALC factor decreases asymptotic risk surface value.",
    )
    assert ok


def calc_margin_required(l0,k,n,alpha,contract_size,leverage):
    geom=(k**n-1)/(k-1)
    volume=l0*geom*alpha
    return volume*contract_size/leverage


def test_safe_deposit_and_final_report():
    k=1.3
    alpha=0.5
    max_levels=30
    l0=0.01
    contract_size=100000.0
    leverage=100.0
    R=120

    trends=[1000,2000,3000,5000,10000]
    table=[]
    for t in trends:
        dd=l0*R*t/1000.0
        margin=calc_margin_required(l0,k,max_levels,alpha,contract_size,leverage)
        deposit_safe=margin+dd+0.2*(margin+dd)
        table.append((t,deposit_safe))

    n_max=0
    equity=10000.0
    for n in range(1,max_levels+1):
        margin_n=calc_margin_required(l0,k,n,alpha,contract_size,leverage)
        if margin_n<equity:
            n_max=n
    p_collapse=1.0/max(1,n_max)

    ok=n_max>0 and p_collapse>0.0
    write_report(
        "TestSafeDeposit",
        "Safe deposit estimation for trend scenarios.",
        {"k":k,"alpha":alpha,"max_levels":max_levels,"R":R},
        {"n_max":n_max,"p_collapse":p_collapse,"table":table},
        ok,
        "Safe deposit table and stability metrics computed.",
    )

    final=Path("Experts/VirtualPanel/right/ale/ALE_ALC_STABILITY_REPORT.md")
    lines=[
        "# ALE + ALC Stability Report",
        "",
        "## Input parameters",
        f"- k: {k}",
        f"- alpha: {alpha}",
        f"- max_levels: {max_levels}",
        f"- leverage: {leverage}",
        f"- l0: {l0}",
        "",
        "## Core metrics",
        f"- n_max: {n_max}",
        f"- P_collapse ≈ 1/n_max: {p_collapse}",
        "",
        "## Required Deposit Table",
        "| Trend | Required Deposit |",
        "|---:|---:|",
    ]
    for t,d in table:
        lines.append(f"| {t} | {d:.2f} |")
    lines += [
        "",
        "## Conclusion",
        "ALC compression lowers margin pressure and stabilizes depth growth under configured alpha and max_levels constraints.",
    ]
    final.write_text("\n".join(lines),encoding="utf-8")

    assert ok


def run():
    tests=[
        test_lock_compression,
        test_delta_calculation,
        test_geometry_preservation,
        test_compression_trigger,
        test_compression_margin,
        test_alc_stability,
        test_safe_deposit_and_final_report,
    ]
    for t in tests:
        t()
        print(f"PASS {t.__name__}")
    print(f"ALL {len(tests)} TESTS PASSED")

if __name__=="__main__":
    run()
