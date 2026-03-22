# ALE_CONTROL_AUDIT

## Measured metrics

From current PCRCV run:
- `trades_executed`: active
- `expansions_allowed`: active
- `expansions_blocked`: active
- `compressions_triggered`: active
- `time_in_CRITICAL`: non-zero under stress

Detailed normal profile (`TestProfitConstrainedControl`):
- `activity_ratio = 0.4572`
- `trade_rate = 0.1064`
- `control_intensity = 0.5428`
- `fake_safety = False`

## Overcontrol criterion

Rule: blocked >> allowed implies overcontrol.
- Normal control profile: **NOT overcontrolled**.
- Overkill thresholds profile: **OVERCONTROL detected** (expected fail-mode).

## Control effectiveness

- In normal profile: improves risk while keeping activity.
- In overkill profile: safety can become degenerate no-trade behavior.
