"""Draw the budget surface (optional Matplotlib)."""
from csv import DictReader
import math
import matplotlib.pyplot as plt

plt.rcParams["svg.hashsalt"]="halr02"
with open("COST_BUDGET_FRONTIER.csv") as f:
    rows=list(DictReader(f))
loss=sorted({int(r["loss_budget"]) for r in rows})
cost=sorted({int(r["cost_budget"]) for r in rows})
lookup={(int(r["loss_budget"]),int(r["cost_budget"])):r for r in rows}
z=[[100*float(lookup[b,c]["recovery_rate"]) if lookup[b,c]["policy"] else math.nan
    for c in cost] for b in loss]
fig,ax=plt.subplots(figsize=(7,5),layout="constrained")
fig.colorbar(ax.imshow(z,aspect="auto",cmap="Blues",vmin=0,vmax=100),ax=ax,label="Восстановление, %")
ax.set(xticks=range(len(cost)),xticklabels=cost,yticks=range(len(loss)),yticklabels=loss,
       xlabel="Лимит новых расходов, USD",ylabel="Лимит полного убытка, USD")
for i,row in enumerate(z):
    for j,x in enumerate(row):
        ax.text(j,i,"—" if math.isnan(x) else f"{x:.1f}",ha="center",va="center",
                color="white" if x>62 else "#1a2740")
fig.savefig("BUDGET_SURFACE.svg",metadata={"Date":None})
