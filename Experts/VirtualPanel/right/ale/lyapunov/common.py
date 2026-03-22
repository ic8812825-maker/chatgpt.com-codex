from __future__ import annotations
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
RUNNER_PATH = ROOT / "Experts/VirtualPanel/right/tests/run_unit_tests.py"
ALE_ROOT = ROOT / "Experts/VirtualPanel/right/ale"


def load_runner_module():
    spec = importlib.util.spec_from_file_location("ale_runner", RUNNER_PATH)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod
