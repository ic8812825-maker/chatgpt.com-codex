"""Generate MT5 .set files from selected offline optimizer rows."""

from __future__ import annotations

from pathlib import Path

SET_KEYS = [
    "StartLot", "BigRatio", "SmallRatio", "CloseBigOnSmall", "RemainBigOnSmall",
    "CloseFarShare", "ReserveShare", "SmallReserveShare", "UseRecommended5050Preset",
    "InitialTriggerPoints", "BigMoveStartPoints", "BigMoveStepPoints", "FarDistancePoints",
    "FarDistanceMode", "GeometryMode", "ATRTimeframe", "ATRPeriod", "ATRInitialMultiplier", "ATRBigStartMultiplier", "ATRStepMultiplier", "ATRFarMultiplier", "MinInitialTriggerPoints", "MaxInitialTriggerPoints", "MinBigMoveStartPoints", "MaxBigMoveStartPoints", "MinBigMoveStepPoints", "MaxBigMoveStepPoints", "MinFarDistancePoints", "MaxFarDistancePoints", "GeometryRoundStep", "InitialRoundStep", "BigStartRoundStep", "BigStepRoundStep", "FarDistanceRoundStep", "FreezeGeometryPerCycle", "PrintAdaptiveGeometryLog", "AllowATRManualFallback", "ShowATRIndicatorOnChart", "MaxHarvestLevels", "SmallFarTouchOffsetPoints", "MaxReverseCycles",
    "MinReverseStrength", "WarningReverseStrength", "StrongReverseStrength", "MinProjectedReserveCoverage",
    "StopOnInvalidReverseGeometry", "StopOnReverseLimit", "AllowNegativeSmallReverseNet", "LotStep",
    "MaxSpreadPoints", "MaxMarginPercent", "MaxDrawdownPercent", "MaxManagedPositions", "MaxAccountMarginPercent", "MaxActiveSymbols",
    "StopOnRiskGateBlocked", "RiskGateLogIntervalSeconds", "MaxCloseRetryAttempts", "RetryLogIntervalSeconds",
    "MaxSlippagePoints", "CloseAllOnInvalidGeometry", "CloseFarOnMaxLevels", "ReserveMismatchTolerance",
    "VolumeMismatchToleranceLots", "ReconciliationIntervalSeconds", "PositionResolutionLookbackSeconds",
    "MagicNumber", "AllowRealTrading", "UseInternalSimulation", "UseMarketOrders", "EnableCycleMathCsv", "VerboseTickLogs",
]

DEFAULTS = {
    "UseRecommended5050Preset": "false",
    "FarDistanceMode": "3",
    "GeometryMode": "0",
    "ATRTimeframe": "30",
    "ATRPeriod": "14",
    "ATRInitialMultiplier": "1.00",
    "ATRBigStartMultiplier": "1.00",
    "ATRStepMultiplier": "0.40",
    "ATRFarMultiplier": "1.30",
    "MinInitialTriggerPoints": "100",
    "MaxInitialTriggerPoints": "250",
    "MinBigMoveStartPoints": "100",
    "MaxBigMoveStartPoints": "260",
    "MinBigMoveStepPoints": "50",
    "MaxBigMoveStepPoints": "125",
    "MinFarDistancePoints": "200",
    "MaxFarDistancePoints": "400",
    "GeometryRoundStep": "5",
    "InitialRoundStep": "10",
    "BigStartRoundStep": "10",
    "BigStepRoundStep": "5",
    "FarDistanceRoundStep": "50",
    "FreezeGeometryPerCycle": "true",
    "PrintAdaptiveGeometryLog": "true",
    "AllowATRManualFallback": "false",
    "ShowATRIndicatorOnChart": "true",
    "SmallFarTouchOffsetPoints": "0",
    "MinReverseStrength": "0.10",
    "WarningReverseStrength": "0.15",
    "StrongReverseStrength": "0.25",
    "MinProjectedReserveCoverage": "1.00",
    "StopOnInvalidReverseGeometry": "true",
    "StopOnReverseLimit": "true",
    "AllowNegativeSmallReverseNet": "false",
    "LotStep": "0.01",
    "MaxManagedPositions": "10",
    "MaxAccountMarginPercent": "60",
    "MaxActiveSymbols": "10",
    "StopOnRiskGateBlocked": "true",
    "RiskGateLogIntervalSeconds": "60",
    "MaxCloseRetryAttempts": "20",
    "RetryLogIntervalSeconds": "30",
    "MaxSlippagePoints": "30",
    "CloseAllOnInvalidGeometry": "true",
    "CloseFarOnMaxLevels": "true",
    "ReserveMismatchTolerance": "0.01",
    "VolumeMismatchToleranceLots": "0.001",
    "ReconciliationIntervalSeconds": "300",
    "PositionResolutionLookbackSeconds": "10",
    "MagicNumber": "20260609",
    "AllowRealTrading": "true",
    "UseInternalSimulation": "false",
    "UseMarketOrders": "true",
    "EnableCycleMathCsv": "true",
    "VerboseTickLogs": "false",
}


def write_set_file(path: Path, row: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    values = dict(DEFAULTS)
    values.update({k: str(row[k]) for k in row if k in SET_KEYS})
    with path.open("w", encoding="utf-8", newline="\n") as f:
        for key in SET_KEYS:
            if key in values:
                f.write(f"{key}={values[key]}\n")
