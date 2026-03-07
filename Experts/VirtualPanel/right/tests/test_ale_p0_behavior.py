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
    assert "SetStrictRuntimeChecks" in text


def test_risk_config_contains_configurable_invariants():
    text = _read(ALE_ROOT / "config/CALRiskConfig.mqh")

    assert "MAX_POSITIONS" in text
    assert "MIN_LOT" in text
    assert "ENABLE_STRICT_RUNTIME_CHECKS" in text


def test_flow_engine_has_nan_inf_guards_per_stage():
    text = _read(ALE_ROOT / "core/CALFlowEngine.mqh")

    assert "GuardRuntimeValue" in text
    assert '"Geometry"' in text
    assert '"Exposure"' in text
    assert '"Risk"' in text
    assert '"Math"' in text
    assert "ForceSAFE()" in text


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


def test_vshape_trace_and_export_tests_registered():
    text = _read(RIGHT_TESTS / "RunAllTests.mqh")
    assert "TestALE_ReplayScenario_VShape" in text
    assert "TestALE_StateTraceMatcher" in text
    assert "TestALE_CSVExports" in text


def test_export_helper_supports_csv_and_junit_xml():
    text = _read(ALE_ROOT / "core/CALExportHelper.mqh")

    assert "BeginReplayContextCSV" in text
    assert "ExportPositionsCSV" in text
    assert "ExportJUnitXML" in text


def test_deterministic_runner_supports_vshape_and_state_trace_matcher():
    text = _read(ALE_ROOT / "core/CALDeterministicRunner.mqh")

    assert "ALE_REPLAY_VSHAPE" in text
    assert "ReplayWithExpectedTrace" in text
    assert "ExportAttachedVirtuals" in text


def test_separate_brain_modules_exist():
    assert (ALE_ROOT / "core/CALEngineBuy.mqh").exists()
    assert (ALE_ROOT / "core/CALEngineSell.mqh").exists()
    assert (ALE_ROOT / "core/CALEngineCommon.mqh").exists()


def test_common_state_and_metrics_are_exposed_via_interface():
    text = _read(ALE_ROOT / "interfaces/IALEngine.mqh")
    assert "StateCommon" in text
    assert "NetDeltaCommon" in text
    assert "PnLCommon" in text
    assert "SAFECommon" in text
