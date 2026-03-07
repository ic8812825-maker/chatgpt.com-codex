import re
from pathlib import Path


def test_event_handlers_exist():
    file = Path("Experts/VirtualPanel/right/VirtualPanel.mq5")
    text = file.read_text(encoding="utf-8")

    assert re.search(r"int\s+OnInit\s*\(", text)
    assert re.search(r"void\s+OnDeinit\s*\(", text)
    assert re.search(r"void\s+OnTick\s*\(", text)
