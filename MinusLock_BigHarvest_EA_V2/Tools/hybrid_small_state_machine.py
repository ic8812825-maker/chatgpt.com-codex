"""Executable, phase-by-phase model of the Hybrid reverse transition."""
from __future__ import annotations
from dataclasses import dataclass, field

@dataclass
class PositionState:
    role:str; direction:str; lot:float; open_price:float=0.; current_price:float=0.; floating_net:float=0.; realized_net:float=0.; active:bool=True
@dataclass
class HybridSmallState:
    scenario_id:int; direction:str; old_far:PositionState|None; big_core:PositionState|None; big_trend:PositionState|None; small_base:PositionState|None
    target_new_far_lot:float; transition_budget_before:float=0.; final_reserve:float=0.; new_far:PositionState|None=None; phase:str="NEW"; actual_new_far_lot:float=0.; transition_budget_after:float=0.; transition_net:float=0.; realized_cycle_pl:float=0.; costs:float=0.; plan_valid:bool=False; next_geometry_valid:bool=False; completed:bool=False; phase_history:list[str]=field(default_factory=list); errors:list[str]=field(default_factory=list)
    def step(self, action): self.phase_history.append(action)
    def fail(self, reason): self.errors.append(reason); self.phase="FAIL"; return self
def create_hybrid_reverse_plan(s): s.phase="PLAN_CREATED";s.step(s.phase);return s
def validate_hybrid_reverse_plan(s):
    if s.phase!="PLAN_CREATED" or s.target_new_far_lot<=0:return s.fail("INVALID_PHASE_TRANSITION")
    s.plan_valid=True;s.phase="PLAN_VALIDATED";s.step(s.phase);return s
def _close(s,name,phase):
    p=getattr(s,name)
    if not s.plan_valid or p is None:return s.fail("INVALID_PHASE_TRANSITION")
    s.realized_cycle_pl+=p.floating_net-p.realized_net;s.costs+=abs(p.lot)*.1;setattr(s,name,None);s.phase=phase;s.step(phase);return s
def close_small_base(s): return _close(s,"small_base","SMALLBASE_CLOSED")
def close_old_far(s):
    if s.small_base is not None:return s.fail("INVALID_PHASE_TRANSITION")
    return _close(s,"old_far","OLDFAR_CLOSED")
def close_big_trend(s):
    if s.old_far is not None:return s.fail("INVALID_PHASE_TRANSITION")
    return _close(s,"big_trend","BIGTREND_CLOSED")
def close_big_core_stage(s):
    if s.big_trend is not None or s.big_core is None:return s.fail("INVALID_PHASE_TRANSITION")
    close=max(0.,s.big_core.lot-s.target_new_far_lot);s.transition_net=s.realized_cycle_pl-s.costs;s.transition_budget_after=max(0.,s.transition_budget_before+s.transition_net);s.big_core.lot-=close;s.phase="BIGCORE_COMPRESSED";s.step(s.phase);return s
def verify_big_core_remainder(s):
    if s.phase!="BIGCORE_COMPRESSED" or s.big_core is None or abs(s.big_core.lot-s.target_new_far_lot)>1e-9:return s.fail("UNACCOUNTED_BIGCORE")
    s.big_core.lot=s.target_new_far_lot;s.actual_new_far_lot=s.big_core.lot;s.phase="ACTUAL_REMAIN_VERIFIED";s.step(s.phase);return s
def preview_next_split_geometry(s):
    if s.phase!="ACTUAL_REMAIN_VERIFIED":return s.fail("INVALID_PHASE_TRANSITION")
    s.next_geometry_valid=s.actual_new_far_lot>0;s.phase="NEXT_GEOMETRY_PREVIEWED";s.step(s.phase);return s
def promote_big_core_remainder_to_new_far(s):
    if not s.next_geometry_valid or s.new_far is not None:return s.fail("DUPLICATE_NEW_FAR" if s.new_far else "INVALID_PHASE_TRANSITION")
    s.big_core.role="NewFar";s.new_far=s.big_core;s.big_core=None;s.phase="NEWFAR_PROMOTED";s.step(s.phase);return s
def evaluate_final_close(s):
    if any((s.old_far,s.big_trend,s.small_base)) or s.new_far is None:return s.fail("ORPHAN_POSITION")
    s.phase="FINAL_GATE_CHECKED";s.step(s.phase);return s
def create_next_cycle(s):
    if s.phase!="FINAL_GATE_CHECKED":return s.fail("INVALID_PHASE_TRANSITION")
    s.completed=True;s.phase="VALID_SMALLER_NEXT_CYCLE";s.step("NEXT_CYCLE_CREATED");return s
def run_small_scenario(i,direction,old,core,trend,small,target):
    s=HybridSmallState(i,direction,PositionState("OldFar",direction,old,floating_net=-old*200),PositionState("BigCore",direction,core,floating_net=core*200),PositionState("BigTrend",direction,trend,floating_net=trend*100),PositionState("SmallBase",direction,small,floating_net=small*50),target)
    for fn in (create_hybrid_reverse_plan,validate_hybrid_reverse_plan,close_small_base,close_old_far,close_big_trend,close_big_core_stage,verify_big_core_remainder,preview_next_split_geometry,promote_big_core_remainder_to_new_far,evaluate_final_close,create_next_cycle): s=fn(s)
    return s
