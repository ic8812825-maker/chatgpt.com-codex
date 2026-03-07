from pathlib import Path

ALE_ROOT = Path("Experts/VirtualPanel/right/ale")
RIGHT_TESTS = Path("Experts/VirtualPanel/right/tests")


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_unified_runner_exists_in_ale_tree():
    assert (ALE_ROOT / "tests/RunAllTests.mqh").exists()
    assert (ALE_ROOT / "tests/RunAllTests.mq5").exists()


def test_unified_runner_calls_required_suites_in_order():
    text = _read(ALE_ROOT / "tests/RunAllTests.mqh")

    i_ale = text.index("TestALE_DualFlowIntegration")
    i_geom = text.index("TestGeometry_BuySellGrids")
    i_risk = text.index("TestRisk_WorstDDMargin")

    assert i_ale < i_geom < i_risk


def test_buy_sell_isolation_tests_are_wired():
    text = _read(RIGHT_TESTS / "RunAllTests.mqh")
    assert "TestALE_BuyFlowIsolation" in text
    assert "TestALE_SellFlowIsolation" in text



def test_position_book_has_runtime_invariants_and_rollback_api():
    text = _read(ALE_ROOT / "positions/CALPositionBook.mqh")

    assert "CheckInvariants" in text
    assert "bool Edit(" in text
    assert "bool Remove(" in text
    assert "safe rollback" in text



def test_global_safe_strict_inequality_documented():
    text = _read(ALE_ROOT / "core/CALEngine.mqh")
    assert "Strict inequality (>) is intentional" in text



def test_debug_macro_present():
    text = _read(ALE_ROOT / "core/CALDebug.mqh")
    assert "#define VP_DEBUG" in text
    assert "VP_DEBUG_LOG" in text



def test_risk_boundary_test_registered():
    text = _read(RIGHT_TESTS / "RunAllTests.mqh")
    assert "TestRisk_GlobalSafeThresholdBoundaries" in text
