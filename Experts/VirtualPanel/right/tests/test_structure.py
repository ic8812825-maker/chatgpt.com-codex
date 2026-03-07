from pathlib import Path

ROOT = Path("Experts/VirtualPanel/right")


def test_main_files_exist():
    assert (ROOT / "VirtualPanel.mq5").exists()
    assert (ROOT / "ALECore.mqh").exists()
    assert (ROOT / "tests/RunAllTests.mq5").exists()


def test_project_structure():
    assert ROOT.exists()
    assert (ROOT / "ale").exists()
    assert (ROOT / "tests").exists()
