"""Render exact primary evidence into the report."""
from csv import DictReader
from pathlib import Path

with open("07_PRIMARY_RESULTS.csv") as f:
    r=list(DictReader(f))
def money(s):
    return f"{float(s):.2f}" if s else "—"
header="| Политика | Recovery | FLAT | Mean USD | Median USD | CVaR95 | CVaR99 | Worst USD | Нарушения |"
sep="| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |"
lines=[header,sep]
for x in r:
    v=(x["policy"],f'{x["recovered"]}/{x["n"]}',x["flat"],
       *(money(x[k]) for k in ("mean_realized","median_realized","cvar95_realized","cvar99_realized","worst_mark")),
       x["violations"])
    lines.append("| "+" | ".join(v)+" |")
text=Path("report_template.md").read_text().replace("{{PRIMARY}}","\n".join(lines))
Path("FINAL_REPORT_RU.md").write_text(text)
