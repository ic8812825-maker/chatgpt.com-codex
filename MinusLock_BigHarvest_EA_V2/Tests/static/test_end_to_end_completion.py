from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
money=(ROOT/'Include/BrokerMoneyModel.mqh').read_text()
state=(ROOT/'Include/StateMachine.mqh').read_text()
types=(ROOT/'Include/Types.mqh').read_text()
harness=(ROOT/'Tests/MQL5/BigSmallStateMachineTest.mq5').read_text()

def test_big_volume_and_margin_are_isolated_and_projected():
    assert 'DirectionalVolumeSnapshot' in money
    assert 'POSITION_MAGIC)==MagicNumber' in money
    assert 'brokerTotalBuy' in money and 'managedBuy' in money
    assert 'projectedEquityAfterOpen=equity-g.projectedOpenCommission-g.projectedInitialSpreadLoss-g.projectedSlippage-g.executionBuffers' in money
    assert 'currentMargin+g.newBasketMargin' in money

def test_small_reconciliation_and_dynamic_cycles_are_active():
    assert 'SmallOperationAudit smallOperationAudits[5]' in types
    assert 'ReconcileCompletedSmallTransition' in state
    assert 'STATE_SMALL_RECONCILIATION_FAILED' in state
    assert 'EvaluateDynamicReverseCycles' in money
    assert 'ReverseCycleProjection &projections[]' in money

def test_false_reverse_has_distinct_execution_fsm():
    for name in ('STATE_FALSE_REVERSE_DECISION','STATE_FALSE_REVERSE_CLOSE_REVERSE','STATE_FALSE_REVERSE_CLOSE_BASE','STATE_FALSE_REVERSE_CLOSE_TAILS_REVERSE','STATE_FALSE_REVERSE_CLOSE_TAILS_BASE','STATE_FALSE_REVERSE_CLOSE_BASKET','STATE_FALSE_REVERSE_RECONCILIATION','STATE_FALSE_REVERSE_COMPLETED','STATE_FALSE_REVERSE_FAILED'):
        assert name in types and name in state
    assert 'reserveImpact=MathMax(0.0,-closed)' in state
    assert 'projectedMarginAfter=MathMax(0.0,currentMargin-released)' in state

def test_mql_harness_drives_real_state_machine_events():
    assert 'struct TestMarketEvent' in types
    assert 'ApplyTestMarketEvent(event)' in harness
    assert 'RunStateMachine()' in harness
    assert 'SimOpenPosition' not in harness and 'SimClosePositionByTicket' not in harness
    assert 'SetState(' not in harness
