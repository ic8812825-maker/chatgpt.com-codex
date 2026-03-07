import re
from pathlib import Path


def test_ui_ids_unique():
    file = Path("Experts/VirtualPanel/right/VirtualPanel.mq5")
    text = file.read_text(encoding="utf-8")

    ids = re.findall(r'"VP_[A-Za-z0-9_]+"', text)
    assert len(ids) == len(set(ids)), "Duplicate UI IDs detected"
