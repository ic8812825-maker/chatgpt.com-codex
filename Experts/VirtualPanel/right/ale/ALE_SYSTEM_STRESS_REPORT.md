# ALE_SYSTEM_STRESS_REPORT

## Monte Carlo baseline (latest reproducible run)

- random: `p_collapse = 0.7874`
- trend: `p_collapse = 0.8328`
- shock: `p_collapse = 0.8968`

## Adversarial A/B

- monotonic: no-control `0.0089`, control `0.0000`
- regime shift: no-control `0.9967`, control `0.0233`
- jump cluster: no-control `1.0000`, control `0.3022`
- liquidity gap: no-control `0.9156`, control `0.0000`

## Stress V2 (liquidity freeze + spread x10 + delay + slippage)

- no-control: `0.9992`
- control: `0.0242`
- activity ratio: `0.8207`

## Extreme stress probe

- `k -> 2.0` + adverse trend remains a documented failure mode in prior truth audit.

## Conclusion

System-level control materially reduces collapse risk, but residual adversarial risk remains non-zero in hardest modes.
