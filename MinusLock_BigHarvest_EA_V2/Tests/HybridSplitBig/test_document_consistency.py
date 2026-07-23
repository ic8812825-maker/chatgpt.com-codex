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
