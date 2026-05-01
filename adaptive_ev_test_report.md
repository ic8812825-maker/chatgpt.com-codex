# Отчет тестирования системы Adaptive EV

- Итог: **PASS (все сценарии)**
- Использованные оптимизированные параметры:
  - alpha=0.3
  - delta_step=0.28
  - gamma=0.12
  - ls_min=0.25

## Результаты по сценариям
- **FLAT_LOW_VOL**: verdict=PASS, equity=0.345454, max_dd=0.000461, survival_violations=0, cycles=68
- **TREND_UP_MODERATE**: verdict=PASS, equity=0.042487, max_dd=0.0, survival_violations=0, cycles=6
- **TREND_DOWN_MODERATE**: verdict=PASS, equity=0.085153, max_dd=0.004289, survival_violations=0, cycles=7
- **VOLATILE_MEAN_ZERO**: verdict=PASS, equity=0.0222, max_dd=0.0, survival_violations=0, cycles=1
- **SHOCK_REGIME**: verdict=PASS, equity=0.023102, max_dd=0.01509, survival_violations=0, cycles=6

## JSON (results)
```json
[
  {
    "scenario": "FLAT_LOW_VOL",
    "steps": 700,
    "cycles": 68,
    "equity": 0.345454,
    "max_drawdown": 0.000461,
    "survival_violations": 0,
    "verdict": "PASS"
  },
  {
    "scenario": "TREND_UP_MODERATE",
    "steps": 700,
    "cycles": 6,
    "equity": 0.042487,
    "max_drawdown": 0.0,
    "survival_violations": 0,
    "verdict": "PASS"
  },
  {
    "scenario": "TREND_DOWN_MODERATE",
    "steps": 700,
    "cycles": 7,
    "equity": 0.085153,
    "max_drawdown": 0.004289,
    "survival_violations": 0,
    "verdict": "PASS"
  },
  {
    "scenario": "VOLATILE_MEAN_ZERO",
    "steps": 700,
    "cycles": 1,
    "equity": 0.0222,
    "max_drawdown": 0.0,
    "survival_violations": 0,
    "verdict": "PASS"
  },
  {
    "scenario": "SHOCK_REGIME",
    "steps": 700,
    "cycles": 6,
    "equity": 0.023102,
    "max_drawdown": 0.01509,
    "survival_violations": 0,
    "verdict": "PASS"
  }
]
```

## JSON (improvement_log, last 20 entries)
```json
[
  {
    "round": 1,
    "params": {
      "lb0": 1.0,
      "ls0": 1.0,
      "pb": 100.0,
      "ps": 101.0,
      "spread": 0.2,
      "atr": 0.8,
      "alpha": 0.3,
      "delta_step": 0.28,
      "gamma": 0.12,
      "d_max": 2.0,
      "ls_min": 0.25
    },
    "all_pass": true,
    "failed_scenarios": []
  }
]
```