"""Synthetic offline scenarios for MinusLock BigHarvest EA V2.

The scenarios are intentionally deterministic and conservative. They do not
replace MT5 Strategy Tester; they provide fast mathematical screening so bad
parameter zones can be rejected before manual MT5 runs.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List


@dataclass(frozen=True)
class Scenario:
    name: str
    events: tuple[str, ...]
    stress_multiplier: float = 1.0
    description: str = ""


def build_scenarios(max_levels: int = 10) -> List[Scenario]:
    """Return the required Big/Small/Reverse/MaxLevels stress scenarios."""
    big = tuple("B" for _ in range(max_levels))
    small = tuple("S" for _ in range(max_levels))
    alternating = tuple(("B" if i % 2 == 0 else "S") for i in range(max_levels))
    false_reverse = tuple(("S", "S", "B", "S", "B", "S", "B", "S", "B", "S")[:max_levels])
    adverse = tuple(("S", "S", "S", "B", "S", "S", "B", "S", "S", "B")[:max_levels])
    max_levels_stress = tuple(("B", "S", "S", "B", "S", "B", "S", "S", "B", "S")[:max_levels])
    worst_case = tuple(("S", "B", "S", "S", "B", "S", "S", "S", "B", "S")[:max_levels])

    return [
        Scenario("A_BIG_WINS", big, 0.90, "Big wins every level; checks how quickly Far is reduced."),
        Scenario("B_SMALL_WINS", small, 1.10, "Small wins every level; checks compression and reserve stress."),
        Scenario("C_ALTERNATING", alternating, 1.00, "Alternating Big/Small sequence."),
        Scenario("D_FALSE_REVERSE", false_reverse, 1.08, "Small, Small, Big, Small, Big false-reversal pattern."),
        Scenario("E_ADVERSE_TREND", adverse, 1.20, "Strong adverse trend against Far; frequent Small and reverse pressure."),
        Scenario("F_MAX_LEVELS", max_levels_stress, 1.15, "Forces deep level usage and max-level decision pressure."),
        Scenario("G_WORST_CASE", worst_case, 1.30, "Worst-case synthetic ordering for Far loss and margin load."),
    ]


def scenario_names(scenarios: Iterable[Scenario]) -> str:
    return ", ".join(s.name for s in scenarios)
