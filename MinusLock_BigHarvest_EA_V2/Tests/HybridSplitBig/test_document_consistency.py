import json
from pathlib import Path
from hybrid_split_big_reference import DECISION_CODES
ROOT=Path(__file__).resolve().parents[2];D=ROOT/'Docs';V=json.loads((Path(__file__).parent/'test_vectors.json').read_text())
def test_documents_formula_and_corrected_arithmetic():
 files=['HYBRID_SPLIT_BIG_THREE_LAWS_MATH_MANUAL_RU.md','HYBRID_SPLIT_BIG_FORMULA_REFERENCE.md','HYBRID_SPLIT_BIG_TEST_VECTORS.md','HYBRID_SPLIT_BIG_PROGRAMMER_CHECKLIST.md','HYBRID_SPLIT_BIG_OPEN_QUESTIONS.md','HYBRID_SPLIT_BIG_CODE_MAPPING.md','HYBRID_SPLIT_BIG_IMPLEMENTATION_GAPS.md','HYBRID_SPLIT_BIG_ORACLE_COVERAGE.md']
 for f in files:assert (D/f).is_file()
 text='\n'.join((D/f).read_text() for f in files)
 for n in range(1,31):assert f'## Глава {n}.' in (D/files[0]).read_text()
 for good in ('43.00','13.20','8.60','30.10','4.30','EA_CURRENT','ProjectedFinalRecoveryPL','ActualFinalRecoveryPL'):assert good in text
 for bad in ('44.20','14.40','8.84','30.94','4.42'):assert bad not in text
 for n in range(1,11):assert f'ADMIN-Q{n:02d}' in text
def test_vectors_are_unique_executable_and_documented():
 assert len(V)==20 and len({x['id'] for x in V})==20
 docs='\n'.join(p.read_text() for p in D.glob('HYBRID_SPLIT_BIG*.md'))
 for x in V:assert x['expected']['code'] in DECISION_CODES and x['id'] in docs and x['expected']['code'] in docs

def test_stage0_normative_contract_and_resolved_allocation():
 config=(ROOT/'Include'/'Config.mqh').read_text()
 admin=(D/'HYBRID_SPLIT_BIG_ADMIN_DECISIONS_REQUIRED.md').read_text()
 normative=(D/'HYBRID_SPLIT_BIG_MQL5_NORMATIVE_ALGORITHMS_RU.md').read_text()
 coverage=(D/'HYBRID_SPLIT_BIG_ORACLE_COVERAGE.md').read_text()
 assert 'HybridPartialFarShare = 0.10' in config
 assert 'HybridFinalReserveShare = 0.90' in config
 assert 'HybridCarryShare = 0.00' in config
 assert 'Статус:** RESOLVED' in admin and '1.125>=1.10' in admin
 for chapter in range(1,9): assert f'## {chapter}.' in normative
 for term in ('PositionFingerprint','FarCloseCost_n=max(-FarCloseNet_n,0)',
              'nextRisk=oldRisk*q','TargetNewFarRatio','ManagedPositions==0',
              'PREPARED → EVENT_WRITTEN → CACHE_UPDATED → RECONCILED → COMPLETED'):
  assert term in normative
 assert '| FULLY_COVERED |' not in coverage

def test_strategy_tester_plan_is_administrator_owned():
 plan=(D/'HYBRID_SPLIT_BIG_STRATEGY_TESTER_ADMIN_PLAN_RU.md').read_text()
 for n in range(1,17): assert f'ST-{n:02d}' in plan
 assert 'Администратор' in plan and 'Every tick based on real ticks' in plan

def test_stage0_safety_contract_documents():
 names=('HYBRID_SPLIT_BIG_SYSTEM_INVARIANTS.md',
        'HYBRID_SPLIT_BIG_STATE_TRANSITION_TABLE.md',
        'HYBRID_SPLIT_BIG_GATE_GRAPH.md',
        'HYBRID_SPLIT_BIG_MONEY_FLOW.md',
        'HYBRID_SPLIT_BIG_TRACE_SPEC.md')
 texts={name:(D/name).read_text() for name in names}
 assert all((D/name).is_file() for name in names)
 assert all(key in texts[names[0]] for key in ('GEO-01','MONEY-01','LOGIC-01','REC-01'))
 assert '| Current | Event | Condition |' in texts[names[1]]
 assert 'IDENTITY' in texts[names[2]] and 'FINAL_CLOSE_PREVIEW' in texts[names[2]]
 assert 'FinalReserve -X-> Transition' in texts[names[3]]
 assert 'HYBRID_CATCHUP_LEVEL' in texts[names[4]] and 'DurationMicros=' in texts[names[4]]

def test_temporal_catchup_contract_is_unambiguous():
 temporal=(D/'HYBRID_SPLIT_BIG_CATCHUP_TEMPORAL_MODEL_RU.md').read_text()
 invariants=(D/'HYBRID_SPLIT_BIG_SYSTEM_INVARIANTS.md').read_text()
 trace=(D/'HYBRID_SPLIT_BIG_TRACE_SPEC.md').read_text()
 for term in ('HybridCatchUpState','StateBefore[n+1] = Transition','Open[k]→Close[k]',
              'PartialBudgetGross','requiresFinalCloseCheck','SteadyStateUpper',
              'BaseState[n]','WorstState[n]'):
  assert term in temporal
 for code in ('TIME-01','TIME-02','TIME-03','TIME-04','FAR-01','FAR-02','FAR-03','FAR-04','FAR-05'):
  assert code in invariants
 for field in ('StateBeforeFingerprint','StateAfterFingerprint','FarLotClosed',
               'PartialBudgetConsumed','RealizedPLAfterPartial','MarginReleased','CoverageAfter'):
  assert field in trace

def test_stage_11_normative_temporal_contract():
 temporal=(D/'HYBRID_SPLIT_BIG_CATCHUP_TEMPORAL_MODEL_RU.md').read_text()
 inv=(D/'HYBRID_SPLIT_BIG_SYSTEM_INVARIANTS.md').read_text()
 gate=(D/'HYBRID_SPLIT_BIG_GATE_GRAPH.md').read_text()
 coverage=(D/'HYBRID_SPLIT_BIG_ORACLE_COVERAGE.md').read_text()
 assert '`NORMATIVE`' in temporal
 for term in ('BuildProjectedReopenPrices','openCommissionAlreadyRealized',
              'CATCHUP_REQUIRES_FINAL_CLOSE_PREVIEW','Worst per-leg adverse policy',
              'OverlapUpper'):
  assert term in temporal
 for code in [*(f'TIME-{n:02d}' for n in range(1,7)),
              *(f'FAR-{n:02d}' for n in range(1,8)),
              *(f'ACC-{n:02d}' for n in range(1,6))]:
  assert code in inv
 assert 'STATE_VALIDATION → TRIGGER_PRICE → CURRENT_LEG_MONEY' in gate
 assert 'Stage 1.1 sequential temporal Catch-Up' in coverage and 'PARTIALLY_COVERED' in coverage


def test_stage_11_audit_status_and_companion_links():
 docs=('HYBRID_SPLIT_BIG_MQL5_NORMATIVE_ALGORITHMS_RU.md','HYBRID_SPLIT_BIG_SYSTEM_INVARIANTS.md',
       'HYBRID_SPLIT_BIG_STATE_TRANSITION_TABLE.md','HYBRID_SPLIT_BIG_GATE_GRAPH.md',
       'HYBRID_SPLIT_BIG_MONEY_FLOW.md','HYBRID_SPLIT_BIG_TRACE_SPEC.md',
       'HYBRID_SPLIT_BIG_FORMULA_REFERENCE.md','HYBRID_SPLIT_BIG_THREE_LAWS_MATH_MANUAL_RU.md',
       'HYBRID_SPLIT_BIG_IMPLEMENTATION_GAPS.md','HYBRID_SPLIT_BIG_MQL5_MAPPING.md',
       'HYBRID_SPLIT_BIG_IMPLEMENTATION_REPORT_RU.md','MANUAL.md')
 for name in docs:
  assert 'HYBRID_SPLIT_BIG_CATCHUP_TEMPORAL_MODEL_RU' in (D/name).read_text(), name
 report=(D/'HYBRID_SPLIT_BIG_FINITE_CATCHUP_REPORT_RU.md').read_text()
 assert 'HYBRID_FINITE_CATCHUP_SOURCE_READY' in report
 assert 'explicitly not claimed' in report
 assert not (Path(__file__).parent/'test_catchup_level_model.py').exists()
 fixture=(ROOT/'Tests'/'MQL5'/'HybridSplitBig'/'HybridCatchUpFixtures.mqh').read_text()
 assert 'SUPERSEDED_TEMPORAL_MODEL' in fixture
 temporal=(Path(__file__).parent/'test_catchup_temporal_model.py').read_text()
 for n in range(1,48): assert f'FT-{n:02d}' in temporal or 'range(1,48)' in temporal

def test_stage12_outcome_contract_documents():
 truth=(D/'HYBRID_SPLIT_BIG_CATCHUP_OUTCOME_TRUTH_TABLE.md').read_text()
 inv=(D/'HYBRID_SPLIT_BIG_SYSTEM_INVARIANTS.md').read_text()
 temporal=(D/'HYBRID_SPLIT_BIG_CATCHUP_TEMPORAL_MODEL_RU.md').read_text()
 trace=(D/'HYBRID_SPLIT_BIG_TRACE_SPEC.md').read_text()
 for term in ('ERROR > TERMINAL > REJECT','FINAL_ROUTE | FINAL_ROUTE','FINITE_PASS | FINITE_PASS'):
  assert term in truth
 for prefix,count in (('OUTCOME',4),('WORST',3),('MARGIN',4)):
  for n in range(1,count+1): assert f'{prefix}-{n:02d}' in inv
 assert 'cumulativeSpreadStress=false' in temporal and 'BUY→Ask' in temporal
 for field in ('OutcomeClass','BaseTriggerBid/Ask','EstimatedReleasedMarginUpper','SteadyStateMarginUpper'):
  assert field in trace

def test_stage121_route_state_contract():
 temporal=(D/'HYBRID_SPLIT_BIG_CATCHUP_TEMPORAL_MODEL_RU.md').read_text()
 truth=(D/'HYBRID_SPLIT_BIG_CATCHUP_OUTCOME_TRUTH_TABLE.md').read_text()
 inv=(D/'HYBRID_SPLIT_BIG_SYSTEM_INVARIANTS.md').read_text()
 gate=(D/'HYBRID_SPLIT_BIG_GATE_GRAPH.md').read_text()
 trace=(D/'HYBRID_SPLIT_BIG_TRACE_SPEC.md').read_text()
 assert 'HybridFinalCloseRouteState' in temporal and 'до Partial scan' in gate
 assert '| FINAL_ROUTE | CONTINUE | REJECT_DIVERGENCE | no |' in truth
 for n in range(1,11): assert f'ROUTE-INV-{n:02d}' in inv
 for field in ('FullFarAffordabilityEvaluated','FarLotForFinalClosePreview','RouteStateFingerprint'):
  assert field in trace
