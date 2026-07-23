from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
DOCS=ROOT/'Docs'
FILES=['HYBRID_SPLIT_BIG_THREE_LAWS_MATH_MANUAL_RU.md','HYBRID_SPLIT_BIG_FORMULA_REFERENCE.md','HYBRID_SPLIT_BIG_TEST_VECTORS.md','HYBRID_SPLIT_BIG_PROGRAMMER_CHECKLIST.md','HYBRID_SPLIT_BIG_OPEN_QUESTIONS.md','HYBRID_SPLIT_BIG_CODE_MAPPING.md','HYBRID_SPLIT_BIG_IMPLEMENTATION_GAPS.md']
def test_required_documents_and_chapters():
    for f in FILES: assert (DOCS/f).is_file() and (DOCS/f).stat().st_size>400
    main=(DOCS/FILES[0]).read_text()
    for n in range(1,31): assert f'## Глава {n}.' in main
    for token in ('ProjectedFinalRecoveryPL','ActualFinalRecoveryPL','CumulativeTransitionLoss','TERMINAL_SAFE_STATE','MarginConservativeUpperBound'):
        assert token in main
def test_admin_questions_and_twenty_vectors():
    q=(DOCS/'HYBRID_SPLIT_BIG_OPEN_QUESTIONS.md').read_text()
    for n in range(1,11): assert f'ADMIN-Q{n:02d}' in q
    v=(DOCS/'HYBRID_SPLIT_BIG_TEST_VECTORS.md').read_text()
    for n in range(1,21): assert f'TV-{n:02d}' in v
def test_shared_definitions_are_synchronised():
    texts=[(DOCS/f).read_text() for f in FILES[:3]]
    for token in ('TransitionNet','FinalReserveReal','CoverageDeficit'):
        assert all(token in t for t in texts), token
    main=(DOCS/FILES[0]).read_text(); ref=(DOCS/FILES[1]).read_text()
    for token in ('ProjectedFinalRecoveryPL','ActualFinalRecoveryPL','CumulativeTransitionLoss','MarginConservativeUpperBound'):
        assert token in main and token in ref, token
