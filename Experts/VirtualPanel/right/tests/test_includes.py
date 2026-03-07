from pathlib import Path

ROOT = Path("Experts/VirtualPanel/right")


def _normalize_include(inc: str) -> str:
    return inc.replace("\\", "/")


def test_no_missing_includes():
    for file in ROOT.rglob("*.mq*"):
        text = file.read_text(encoding="utf-8")
        for line in text.splitlines():
            if "#include" in line and '"' in line:
                inc = line.split('"')[1]
                include_path = (file.parent / _normalize_include(inc)).resolve()
                assert include_path.exists(), f"Missing include {inc} in {file}"
