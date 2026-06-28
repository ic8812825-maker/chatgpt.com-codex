from pathlib import Path
root = Path(__file__).resolve().parents[1]
sets = root / 'Sets'
for set_path in sets.glob('*.set'):
    text = set_path.read_text()
    for token in ['GeometryMode=0', 'InitialRoundStep=10', 'BigStartRoundStep=10', 'BigStepRoundStep=5', 'FarDistanceRoundStep=50']:
        assert token in text, (set_path.name, token)
print('ADAPTIVE_GEOMETRY_SET_FILES_CHECK PASS')
