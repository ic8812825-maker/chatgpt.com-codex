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
