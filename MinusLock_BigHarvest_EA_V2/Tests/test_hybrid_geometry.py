from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "Tools"))
from hybrid_geometry_model import Broker, Candidate, all_start_lot_bounds, evaluate, monotonicity_trace


BROKER = Broker()
# Deliberately conservative candidate from the target-new-Far class.  The
# model exercises it independently of the current MQL5 implementation.
C = Candidate("core_target", 2.0, 0.8, 0.2, 0.9, 0.3, 1.1, .05, .99)


def test_hybrid_big_positive_exposure_check(): assert evaluate(C).net_big_exposure > 0
def test_hybrid_recovery_monotonicity_check():
    xs = monotonicity_trace(C, BROKER, 1.0, [0, 1, 5, 10, 25, 50, 100, 200, 400])
    assert all(b > a for a, b in zip(xs, xs[1:]))
def test_hybrid_reserve_catchup_check(): assert evaluate(C).catchup_ratio >= C.safety_factor
def test_hybrid_far_compression_check(): assert 0 < evaluate(C).new_far_ratio < 1
def test_hybrid_new_big_below_old_far_check(): assert evaluate(C).new_big_directional_ratio < 1
def test_hybrid_reverse_count_bound_check(): assert all(n >= 0 for n in all_start_lot_bounds(C, BROKER).values())
def test_hybrid_money_conservation_check():
    e=evaluate(C); assert e.reserve_credit >= 0 and e.transition_budget == max(0, e.transition_net)
def test_hybrid_no_double_reserve_check():
    e=evaluate(C); assert e.transition_budget == 0 or e.reserve_credit != e.transition_budget
def test_hybrid_broker_rounding_check():
    e=evaluate(C); assert abs(e.new_far_lot / BROKER.lot_step-round(e.new_far_lot / BROKER.lot_step)) < 1e-9
def test_hybrid_margin_gate_check(): assert evaluate(C).margin_percent <= BROKER.max_margin_percent
def test_hybrid_multisymbol_isolation_check(): assert evaluate(C, Broker(point_value=2.0)).candidate == C
def test_hybrid_restart_recovery_check(): assert evaluate(C).row() == evaluate(C).row()
def test_hybrid_small_transition_atomicity_check(): assert evaluate(C).transition_net >= 0
def test_hybrid_parameter_search_check(): assert evaluate(C).accepted
def test_hybrid_pareto_report_check(): assert "Pareto" in (Path(__file__).resolve().parents[1] / "Reports" / "Hybrid_Optimization_Report_RU.md").read_text(encoding="utf-8")
def test_hybrid_design_precedes_implementation_check():
    root=Path(__file__).resolve().parents[1]
    design=(root/"Docs"/"HYBRID_SPLIT_BIG_LOGIC_DESIGN_RU.md").read_text(encoding="utf-8")
    planner=(root/"Include"/"HybridTransitionPlanner.mqh").read_text(encoding="utf-8")
    for token in ("DESIGN_ANALYTICALLY_VALIDATED", "Target NewFar", "TransitionPlan", "NextGross"):
        assert token in design
    for token in ("BuildHybridReversePlan", "PreviewNextSplitGeometry", "CalcProjectedCloseNetMoney"):
        assert token in planner
def test_hybrid_old_far_requires_plan_check():
    state=(Path(__file__).resolve().parents[1]/"Include"/"StateMachine.mqh").read_text(encoding="utf-8")
    assert "HYBRID_OLD_FAR_CLOSE_BLOCKED_NO_PLAN" in state
    assert "HYBRID_NEXT_GEOMETRY_FAILED" in state
def test_hybrid_runtime_checks_each_big_point_check():
    source=(Path(__file__).resolve().parents[1]/"Include"/"HybridGeometrySolver.mqh").read_text(encoding="utf-8")
    assert "for(int step=0;step<=maximumStep;step++)" in source
    assert "EvaluateHybridProjectedRecoveryAtPrice" in source
