from __future__ import annotations

import csv
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

CYCLE_COLUMNS = [
    "Level", "Scenario", "FarLotBefore", "BigLot", "SmallLot", "ProfitBig", "LossSmall",
    "SmallPL", "OldFarPL", "ClosedBigPL", "NetProfit", "CloseFarBudget", "ReserveAdd",
    "TotalReserveBefore", "TotalReserveAfter", "CloseFarLotRaw", "CloseFarLotRounded",
    "FarRemainLot", "FarRemainLoss", "FinalCloseAllowed", "ReverseStrength",
    "ProjectedReserveCoverage", "State", "Action", "StopReason", "CycleFinalPL",
    "MaxOpenLots", "MaxFarLot", "InitialIgnoredProfit",
]

@dataclass
class CycleMathRow:
    Level: int
    Scenario: str
    FarLotBefore: float
    BigLot: float = 0.0
    SmallLot: float = 0.0
    ProfitBig: float = 0.0
    LossSmall: float = 0.0
    SmallPL: float = 0.0
    OldFarPL: float = 0.0
    ClosedBigPL: float = 0.0
    NetProfit: float = 0.0
    CloseFarBudget: float = 0.0
    ReserveAdd: float = 0.0
    TotalReserveBefore: float = 0.0
    TotalReserveAfter: float = 0.0
    CloseFarLotRaw: float = 0.0
    CloseFarLotRounded: float = 0.0
    FarRemainLot: float = 0.0
    FarRemainLoss: float = 0.0
    FinalCloseAllowed: bool = False
    ReverseStrength: float = 0.0
    ProjectedReserveCoverage: float = 0.0
    State: str = "RUNNING"
    Action: str = ""
    StopReason: str = ""
    CycleFinalPL: float = 0.0
    MaxOpenLots: float = 0.0
    MaxFarLot: float = 0.0
    InitialIgnoredProfit: float = 0.0

    def to_dict(self) -> dict[str, object]:
        d = asdict(self)
        d["FinalCloseAllowed"] = "YES" if self.FinalCloseAllowed else "NO"
        return d


def write_cycle_csv(rows: Iterable[CycleMathRow], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CYCLE_COLUMNS, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(row.to_dict())


def write_cycle_markdown(rows: list[CycleMathRow], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    headers = ["Level", "Scenario", "FarLotBefore", "BigLot", "SmallLot", "NetProfit", "Reserve", "FarRemainLoss", "FinalClose", "State", "Action"]
    lines = ["# AI Cycle Math", "", "| " + " | ".join(headers) + " |", "|" + "|".join(["---"] * len(headers)) + "|"]
    for r in rows:
        values = [
            r.Level, r.Scenario, f"{r.FarLotBefore:.2f}", f"{r.BigLot:.2f}", f"{r.SmallLot:.2f}",
            f"{r.NetProfit:.2f}", f"{r.TotalReserveAfter:.2f}", f"{r.FarRemainLoss:.2f}",
            "YES" if r.FinalCloseAllowed else "NO", r.State, r.Action,
        ]
        lines.append("| " + " | ".join(map(str, values)) + " |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
