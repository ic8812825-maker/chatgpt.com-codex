"""Insert computed comparison tables and immutable provenance into the report."""
from csv import DictReader
import json
from pathlib import Path


def table(header,rows):
    return "\n".join("| "+" | ".join(map(str,row))+" |"
                     for row in (header,["---"]*len(header),*rows))


def p(s):
    return f"{100*float(s):.2f}%" if s else "—"


def f(s):
    return f"{float(s):.2f}" if s else "—"


with open("08_ROBUSTNESS_MATRIX.csv") as file:
    rows=[r for r in DictReader(file)
          if r["profile"] in ("E0","E1","E2") and r["horizon"]=="12"
          and r["generator"]=="markov"]
main=table(["Контракт","Политика","Recovery","Wilson 95%","FLAT","Mean","Worst","CVaR99","Нарушения"],
           [(r["profile"],r["policy"],p(r["recovery_rate"]),
             f'{p(r["wilson_lo"])}–{p(r["wilson_hi"])}',r["flat"],
             f(r["mean_pnl"]),f(r["worst_pnl"]),f(r["cvar99"]),r["risk_violations"])
            for r in rows])
stages=json.loads(Path("STAGE_COMMITS.json").read_text())
commits="\n".join(f'- {x["subject"]} [`{x["sha"][:12]}`](https://github.com/ic8812825-maker/chatgpt.com-codex/commit/{x["sha"]})'
                 for x in stages)
commits+="\n- HALR03-10 — итоговый отчёт и экономическое сравнение. Точный SHA опубликован в PR."
text=Path("final_template.md").read_text().replace("{{MAIN}}",main).replace("{{COMMITS}}",commits)
Path("FINAL_REPORT_RU.md").write_text(text)
