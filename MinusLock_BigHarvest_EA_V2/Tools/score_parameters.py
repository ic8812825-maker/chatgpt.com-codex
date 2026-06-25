"""Scoring helpers for the MinusLock offline optimizer."""

from __future__ import annotations

from dataclasses import dataclass

REJECTED_SCORE_PENALTY = 1_000_000.0


@dataclass(frozen=True)
class ScoreWeights:
    recovery_pl: float = 1.0
    profit_factor: float = 100.0
    recovery_factor: float = 50.0
    max_equity_dd: float = 2.0
    max_margin_used: float = 0.5
    stop_max_levels_penalty: float = 500.0
    recovery_loss_penalty: float = 500.0
    integrity_risk_penalty: float = 1000.0
    compression_violation_penalty: float = 1000.0


def score_candidate(metrics: dict, weights: ScoreWeights = ScoreWeights()) -> float:
    """Score one aggregate metrics dictionary.

    Positive recovery and robust profit factor increase score; deep drawdown,
    margin load, STOP_MAX_LEVELS and recovery-loss outcomes are heavily
    penalized. The formula intentionally ranks stability above raw profit.
    """
    score = 0.0
    score += metrics.get("RecoveryPL_Mean", 0.0) * weights.recovery_pl
    score += metrics.get("ProfitFactorOffline", 0.0) * weights.profit_factor
    score += metrics.get("RecoveryFactorOffline", 0.0) * weights.recovery_factor
    score -= metrics.get("MaxDD_Max", 0.0) * weights.max_equity_dd
    score -= metrics.get("MaxMarginUsed", 0.0) * weights.max_margin_used
    score -= metrics.get("StopMaxLevelsCount", 0) * weights.stop_max_levels_penalty
    score -= metrics.get("ClosedRecoveryLossCount", 0) * weights.recovery_loss_penalty
    score -= metrics.get("IntegrityRiskCount", 0) * weights.integrity_risk_penalty
    score -= metrics.get("CompressionViolationCount", 0) * weights.compression_violation_penalty
    return round(score, 4)


def verdict(metrics: dict) -> str:
    if metrics.get("RejectedReason"):
        return "REJECTED_" + metrics["RejectedReason"]
    if metrics.get("CompressionViolationCount", 0) > 0:
        return "REJECTED_COMPRESSION"
    if metrics.get("StopMaxLevelsCount", 0) > 0:
        return "REJECTED_STOP_MAX_LEVELS"
    if metrics.get("ClosedRecoveryLossCount", 0) > 0:
        return "REJECTED_RECOVERY_LOSS"
    if metrics.get("RecoveryPL_Min", 0.0) <= 0.0:
        return "REJECTED_NON_POSITIVE_MIN_RECOVERY"
    if metrics.get("MaxDD_Max", 0.0) > metrics.get("MaxAllowedDD", 10**9):
        return "REJECTED_DRAWDOWN"
    if metrics.get("MaxMarginUsed", 0.0) > metrics.get("MaxAllowedMargin", 10**9):
        return "REJECTED_MARGIN"
    return "ACCEPT"
