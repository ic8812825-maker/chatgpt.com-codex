"""Insert computed tables into the Russian report."""
from pathlib import Path
from audit2 import load


def table(header, rows):
    return "\n".join("| "+" | ".join(map(str,row))+" |"
                     for row in (header,["---"]*len(header),*rows))


def pct(a):
    return f"{100*float(a):.2f}%" if a!="" else "—"


def amount(a):
    return f"{float(a):.2f}" if a!="" else "—"


comp=table(["Политика","H","Recovery","Wilson 95%","FLAT","Среднее","Худший","CVaR99","Расходы + резерв, макс."],
           [(r["label"],r["horizon"],pct(r["recovery_rate"]),
             f'{pct(r["wilson_lo"])}–{pct(r["wilson_hi"])}',r["flat"],amount(r["mean_pnl"]),
             amount(r["worst_pnl"]),amount(r["cvar99"]),amount(r["max_cost_reserve"]))
            for r in load("COMPARISON_RESULTS")])
front=table(["B","Доп. бюджет","C","Политика","Recovery","Худший","Макс. расходы с резервом"],
            [(r["loss_budget"],int(r["loss_budget"])-58,r["cost_budget"],r["policy"] or "—",
              pct(r["recovery_rate"]),amount(r["worst"]),amount(r["max_cost"]))
             for r in load("COST_BUDGET_FRONTIER") if int(r["cost_budget"])>=30])
data=load("EXHAUSTIVE_RESULTS")
coverage=[]
for a in ("K-EXECUTABLE","A3-selected","M-selected"):
    for h in (4,6,8,12):
        rows=[r for r in data if r["label"]==a and int(r["horizon"])==h]
        completed=[r for r in rows if r["status"]=="COMPLETE"]
        n=sum(int(r["paths"]) for r in completed)
        s=sum(int(r["successes"]) for r in completed)
        min_pnl=amount(str(min(float(r["low"]) for r in completed))) if completed else "—"
        coverage.append((a,h,len(completed),f"{n:,}" if n else "—",f"{s:,}" if n else "—",min_pnl))
exact=table(["Политика","H","Полные ориентации","Пути","Восстановления","Худший внутрисценарный"],
            coverage)
source=Path("report_basis.md").read_text()
Path("FINAL_REPORT_RU.md").write_text(source.replace("{{COMPARISON}}",comp)
                                   .replace("{{BUDGET}}",front).replace("{{EXACT}}",exact))
