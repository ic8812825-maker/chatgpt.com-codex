"""Create the final report from the locked CSVs."""
from csv import DictReader
from pathlib import Path

def read(name):
    with open(name+".csv") as f:
        return list(DictReader(f))

def usd(x):
    return f"{float(x):.2f}" if x else "—"

def pct(x):
    return f"{100*float(x):.1f}%" if x else "—"

def table(fields,rows):
    return "\n".join("| "+" | ".join(map(str,line))+" |"
                     for line in (fields,["---"]*len(fields),*rows))

primary=[r for r in read("08_PAIRED_RESULTS") if r["panel"]=="S2/30" and r["mode"]=="quote_fill"]
comparison=table(
    ["Политика","Recovery","FLAT","Нарушения","Mean USD",
     "Парное Δ USD","95% скорр.","CVaR99 USD","Worst mark USD","Новые расходы с резервом"],
    [(r["policy"],r["recoveries"],r["flat"],r["risk_violations"],usd(r["mean_terminal"]),
      usd(r["paired_mean"]),f'{usd(r["paired_low"])} … {usd(r["paired_high"])}',
      usd(r["cvar99_realized"]),usd(r["worst_mark"]),usd(r["max_cost_reserve"])) for r in primary])
stress=table(["Политика","FLAT","Нарушения","Остаток","Pending","Худший mark USD"],
             [(r["policy"],r["flat"],r["violations"],r["residual"],r["pending"],usd(r["worst_mark"]))
              for r in read("09_STRESS_SUMMARY")])
src=Path("final_template.md").read_text()
Path("FINAL_REPORT_RU.md").write_text(src.replace("{{MAIN}}",comparison).replace("{{STRESS}}",stress))
