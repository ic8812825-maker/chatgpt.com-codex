"""Generate the optional static figure (requires Matplotlib)."""
from csv import DictReader
import matplotlib.pyplot as plt

plt.rcParams["svg.hashsalt"] = "halr01"

with open("BUDGET_FRONTIER.csv") as f:
    rows = list(DictReader(f))
x = [int(row["additional_budget"]) for row in rows]
p = [100*float(row["rate"]) for row in rows]
lo = [100*float(row["wilson_low"]) for row in rows]
hi = [100*float(row["wilson_high"]) for row in rows]
fig, ax = plt.subplots(figsize=(8.5, 4.4), layout="constrained")
ax.errorbar(x, p, yerr=([max(0,a-b) for a,b in zip(p,lo)],
                       [max(0,a-b) for a,b in zip(hi,p)]),
            fmt="o", color="#154b78", capsize=4)
ax.plot(x, p, alpha=.45, color="#154b78")
ax.set(xlabel="Допустимый дополнительный убыток относительно K, USD",
       ylabel="Восстановление, %",
       title="Синтетическая модель · независимые испытания")
ax.set_xticks(x)
ax.set_ylim(bottom=0)
ax.grid(axis="y", alpha=.25)
fig.savefig("BUDGET_CURVE.svg", metadata={"Date": None})
