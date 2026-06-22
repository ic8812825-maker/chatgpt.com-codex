from pathlib import Path
import re
root = Path(__file__).resolve().parents[1]
text = (root / 'Include' / 'PositionResolutionEngine.mqh').read_text() + '\n' + (root / 'Include' / 'StateMachine.mqh').read_text()
assert not re.search(r'\((?:[^)]*,\s*)?PositionResolutionResult\s+(?!&)', text), 'PositionResolutionResult must not be passed by value'
assert not re.search(r'\((?:[^)]*,\s*)?PositionSnapshot\s+(?!&)', text), 'PositionSnapshot must not be passed by value'
assert 'bool ResolveOpenedPosition(' in text and 'PositionResolutionResult &result' in text
assert 'bool ResolveOpenedPositionAfterOpen(' in text and 'PositionResolutionResult &result' in text
print('position_resolution_reference_only_check PASS')
