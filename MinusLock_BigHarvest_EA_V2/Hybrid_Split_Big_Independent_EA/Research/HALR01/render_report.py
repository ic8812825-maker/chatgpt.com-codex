"""Render the narrative report tables from numeric artifacts."""
from csv import DictReader
from pathlib import Path
import json


def read(name):
    with open(name + ".csv") as file:
        return list(DictReader(file))


def fmt(row, key):
    return f'{float(row[key]):.2f}'


def percent(row, key):
    return f'{100*float(row[key]):.2f}%'


def table(fields, rows):
    def line(f):
        return "| " + " | ".join(map(str, f)) + " |"
    return "\n".join([line(fields), line(["---"]*len(fields)), *(line(r) for r in rows)])


budget = read("BUDGET_FRONTIER")
comparison = [r for r in read("COMPARISON_RESULTS") if r["budget"] == "180"]
exact = {r["variant"]: r for r in comparison if r["split"] == "exhaustive_6"}
test = [r for r in comparison if r["split"] == "independent_test"]
stress = [r for r in comparison if r["split"] == "adversarial_holdout"]
bud = table(["Лимит", "Доп. бюджет", "Вариант", "Восстановления", "Wilson 95%",
             "Худший PnL (test)", "Макс. внутрисценарный убыток (D⁶)", "Нарушения stress"],
            ((r["budget"], r["additional_budget"], r["variant"],
              f'{r["recoveries"]}/{r["n"]} ({percent(r,"rate")})',
              f'{percent(r,"wilson_low")}–{percent(r,"wilson_high")}', fmt(r,"worst"),
              fmt(r,"exhaustive_intracycle_loss"), r["stress_violations"]) for r in budget))
comp = table(["Вариант", "Recovery test", "Среднее test", "Худший test", "CVaR95 test",
              "Recovery D⁶", "Худший D⁶", "Нарушения D⁶"],
             ((r["variant"], percent(r,"rate"), fmt(r,"mean"), fmt(r,"worst"), fmt(r,"cvar95"),
               percent(exact[r["variant"]],"rate"), fmt(exact[r["variant"]],"worst"),
               exact[r["variant"]]["violations"]) for r in test))
st = table(["Вариант", "Худший PnL", "Нарушения", "Сбои", "Остаток", "StopOut"],
           ((r["variant"], fmt(r,"worst"), r["violations"], r["failures"],
             r["residual"], r["stopouts"]) for r in stress))
settings = []
for row in budget:
    p = json.loads(row["params"])
    if row["variant"] == "K":
        settings.append((row["budget"], "K", "—", "—", "—", "—", "—", "—", "—"))
        continue
    settings.append((row["budget"], row["variant"], p["net"]/100,
                     p["core"]/100 if row["variant"].startswith("A") else "—",
                     p["trigger"] if not row["variant"].startswith("M") else "—",
                     p["switches"] if row["variant"].startswith("A") else "—",
                     p["horizon"], p["reserve"], int(row["gross_limit"])/100))
parameters = table(["Лимит", "Вариант", "Net (лот)", "Порог Core (лот)",
                    "Триггер (пунктов)", "Переключения", "Горизонт", "Резерв", "Gross (лот)"],
                   settings)
template = Path("report_template.md").read_text()
report = template.replace("{{BUDGET}}",bud).replace("{{COMPARISON}}",comp).replace("{{STRESS}}",st).replace("{{PARAMS}}",parameters)
Path("FINAL_REPORT_RU.md").write_text(report)
