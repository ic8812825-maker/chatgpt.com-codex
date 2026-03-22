# ALE TRUTH VALIDATION REPORT

## 1. Adversarial Results
- adv_monotonic no/control: 1.0000 / 0.0000
- adv_regime_shift no/control: 0.9917 / 0.0000
- adv_jump_cluster no/control: 1.0000 / 0.0000
- adv_liquidity_gap no/control: 0.9258 / 0.0050

## 2. Control Behavior
- trades_executed: 480.36
- expansions_allowed: 1.76
- expansions_blocked: 478.60
- compressions_triggered: 2.00
- time_in_CRITICAL: 0.01

## 3. Profitability
- PnL no control: -14.0557
- PnL with control: -0.0982
- collapse no control: 0.0310
- collapse with control: 0.0000

## 4. Estimator Accuracy
- bias: 0.1221
- underestimation_rate: 0.0000
- false_safe_signals: 0

## 5. Failure Cases
- stress beyond training (k=2.0,R=50): p_collapse=1.0000, avg_depth=12.00

## 6. Final Verdict
[ ] Truly robust
[x] Overfitted / unstable
[ ] Stable but non-profitable
