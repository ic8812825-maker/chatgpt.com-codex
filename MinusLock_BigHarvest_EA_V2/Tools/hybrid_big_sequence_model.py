"""Recursive L1--L7 ledger used by the independent Hybrid proof."""
from __future__ import annotations
from dataclasses import asdict, dataclass
from hybrid_geometry_model import Broker, Candidate, evaluate, floor_step

@dataclass
class HybridBigSequenceState:
    sequence_id:int; level:int; direction:str; far_before_lot:float; far_after_lot:float
    far_loss_before:float; far_loss_after:float; reserve_before:float; reserve_added:float
    reserve_after:float; partial_far_budget:float; partial_far_close_lot:float; partial_far_carry:float
    coverage_before:float; coverage_after:float; coverage_deficit_before:float; coverage_deficit_after:float
    recovery_pl_before:float; recovery_pl_after:float; accepted:bool; reject_reason:str
    def row(self): return asdict(self)

def simulate_sequence(sequence_id:int, direction:str, candidate:Candidate, broker:Broker, far_lot:float, levels:int=7):
    """Apply each harvest to the actual remainder from the preceding level."""
    reserve=carry=0.0; far=far_lot; result=[]
    for level in range(1, levels+1):
        e=evaluate(candidate, broker, far, 200.0)
        far_loss_before=far*200.0*broker.point_value
        coverage_before=reserve+carry
        deficit_before=max(0.0, far_loss_before-coverage_before)
        harvest=max(0.0, (e.core_lot+e.trend_lot-e.small_lot)*200.0-e.transition_costs)
        # Allocation is performed as two independent operations, not derived
        # from the residual equation: reserve share is credited first and the
        # remaining harvest pays a rounded partial Far close.
        reserve_add=harvest*candidate.reserve_share
        partial_budget=harvest-reserve_add
        close_lot=floor_step(min(far, partial_budget/(200.0*broker.point_value)), broker)
        used=close_lot*200.0*broker.point_value
        carry_after=partial_budget-used
        far_after=max(0.0, far-close_lot)
        far_loss_after=far_after*200.0*broker.point_value
        reserve_after=reserve+reserve_add
        coverage_after=reserve_after+carry_after
        deficit_after=max(0.0, far_loss_after-coverage_after)
        # Once the deficit is already zero, preserving zero coverage deficit is
        # the valid terminal invariant; otherwise an actual improvement is
        # required before the recursive state is passed onward.
        accepted=(deficit_before <= 1e-9) or (e.accepted and deficit_after < deficit_before-1e-9)
        result.append(HybridBigSequenceState(sequence_id,level,direction,far,far_after,far_loss_before,far_loss_after,reserve,reserve_add,reserve_after,partial_budget,close_lot,carry_after,coverage_before,coverage_after,deficit_before,deficit_after,e.recovery_slope*200,e.recovery_slope*200+harvest,accepted,"" if accepted else (e.reject_reason if not e.accepted else "COVERAGE_DEFICIT")))
        far,reserve,carry=far_after,reserve_after,carry_after
    return result
