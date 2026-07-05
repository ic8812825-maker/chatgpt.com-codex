# ATR Set Files Audit

## Standard

- Основной стандарт Adaptive Geometry: `ATRTimeframe=0` (`PERIOD_CURRENT`) и `ATRPeriod=14`.
- `ATRPeriod=14` выбран как классический стандарт ATR: он быстрее реагирует на изменение волатильности и лучше подходит для адаптивной геометрии на текущем графике.
- Ранее массовый `ATRPeriod=20` появился из офлайн-оптимизационного recommended anchor и был слишком консервативным для основных ATR-пресетов.
- `ATRPeriod=20` оставлен только для Conservative / Ultra_Conservative / ATR_Conservative: это более сглаженная, медленная и осторожная геометрия.

## Audit table

| SET файл | GeometryMode | ATRTimeframe | ATRPeriod | Статус | Комментарий |
|---|---|---|---:|---|---|
| ATR_Conservative.set | GEOMETRY_ATR_SAFE | PERIOD_CURRENT | 20 | PASS | консервативный сглаженный режим; ATRPeriod=20 разрешён только здесь |
| Adaptive_ATR_BALANCED.set | GEOMETRY_ATR_BALANCED | PERIOD_CURRENT | 14 | PASS | основной BALANCED ATR-пресет |
| Adaptive_ATR_PROFIT.set | GEOMETRY_ATR_PROFIT | PERIOD_CURRENT | 14 | PASS | быстрый Recovery ATR-пресет |
| Adaptive_ATR_SAFE.set | GEOMETRY_ATR_SAFE | PERIOD_CURRENT | 14 | PASS | SAFE с классическим ATR 14 |
| Aggressive_Recovery.set | GEOMETRY_ATR_PROFIT | PERIOD_CURRENT | 14 | PASS | агрессивный Recovery без H1 override |
| Anti_Trend.set | GEOMETRY_ATR_SAFE | PERIOD_CURRENT | 14 | PASS | анти-трендовый основной стандарт |
| Conservative.set | GEOMETRY_ATR_SAFE | PERIOD_CURRENT | 20 | PASS | консервативный сглаженный режим; ATRPeriod=20 разрешён только здесь |
| High_Volatility.set | GEOMETRY_ATR_SAFE | PERIOD_CURRENT | 14 | PASS | высокая волатильность, текущий график |
| Low_Volatility.set | GEOMETRY_ATR_BALANCED | PERIOD_CURRENT | 14 | PASS | низкая волатильность, текущий график |
| Maximum_Recovery.set | GEOMETRY_ATR_PROFIT | PERIOD_CURRENT | 14 | PASS | максимальный Recovery основной стандарт |
| Minimum_Big_Levels.set | GEOMETRY_ATR_BALANCED | PERIOD_CURRENT | 14 | PASS | главный пресет минимизации Big уровней |
| Multi_Symbol.set | GEOMETRY_ATR_BALANCED | PERIOD_CURRENT | 14 | PASS | мультисимвольный основной стандарт |
| Recommended.set | GEOMETRY_ATR_BALANCED | PERIOD_CURRENT | 14 | PASS | основной рабочий стандарт |
| Trend.set | GEOMETRY_ATR_PROFIT | PERIOD_CURRENT | 14 | PASS | трендовый основной стандарт |
| Ultra_Conservative.set | GEOMETRY_ATR_SAFE | PERIOD_CURRENT | 20 | PASS | консервативный сглаженный режим; ATRPeriod=20 разрешён только здесь |
| Universal.set | GEOMETRY_ATR_BALANCED | PERIOD_CURRENT | 14 | PASS | универсальный основной стандарт |

## ATRPeriod 14 vs 20

| ATRPeriod | Назначение | Реакция | Риск | Где используется |
|---:|---|---|---|---|
| 14 | Основной рабочий стандарт | Быстрее реагирует на изменение волатильности | Меньше инерции, геометрия ближе к текущему рынку | Recommended, Universal, Minimum Big Levels, SAFE/BALANCED/PROFIT, Trend/AntiTrend, Multi Symbol, Low/High Volatility |
| 20 | Консервативное сглаживание | Медленнее реагирует | Может расширять уровни и замедлять Recovery | Только Conservative, Ultra_Conservative, ATR_Conservative |

## MT5 comparison placeholder

| Mode | ATRPeriod | ATRTimeframe | ATRPoints | WorkInitial | WorkBigStart | WorkBigStep | WorkFar | FinalState | MaxBigLevel | RecoveryPL | NetProfit | OnTester | MaxDD |
|---|---:|---|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|
| MANUAL | - | - | - | 190 | 200 | 75 | 275 | MT5 required | MT5 required | MT5 required | MT5 required | MT5 required | MT5 required |
| ATR_SAFE | 14 | PERIOD_CURRENT | MT5 required | MT5 required | MT5 required | MT5 required | MT5 required | MT5 required | MT5 required | MT5 required | MT5 required | MT5 required | MT5 required |
| ATR_BALANCED | 14 | PERIOD_CURRENT | MT5 required | MT5 required | MT5 required | MT5 required | MT5 required | MT5 required | MT5 required | MT5 required | MT5 required | MT5 required | MT5 required |
| ATR_PROFIT | 14 | PERIOD_CURRENT | MT5 required | MT5 required | MT5 required | MT5 required | MT5 required | MT5 required | MT5 required | MT5 required | MT5 required | MT5 required | MT5 required |
| ATR_SAFE_CONSERVATIVE | 20 | PERIOD_CURRENT | MT5 required | MT5 required | MT5 required | MT5 required | MT5 required | MT5 required | MT5 required | MT5 required | MT5 required | MT5 required | MT5 required |

MT5 Strategy Tester cannot be executed in this container; this audit locks the `.set` standard and documents the exact comparison table that must be filled from MetaTester logs/reports.
