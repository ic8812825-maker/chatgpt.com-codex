# MinusLock Self Compressing BigSmall v2

## Краткое описание

Самосжимающаяся система разруливания минусового замка.

```text
BIG_SIDE:
    Close Big = 100%
    Close Small = 100%
    20% NetProfit на хвост
    80% NetProfit в резерв

SMALL_SIDE:
    Close Small = 100%
    Close Big = 22%
    RemainBig = 78%
    Новый хвост = RemainBig
```

Основной режим закрытия хвоста — денежный: 20% означает бюджет от `NetProfit`, а не автоматическое закрытие 20% лота хвоста.

## Состав проекта

```text
MinusLock_SelfCompressing_BigSmall_v2/
├── MinusLock_SelfCompressing_BigSmall_v2.xlsx
├── README.md
├── MANUAL_v2.md
├── TEST_REPORT_MinusLock_SelfCompressing_BigSmall_v2.md
├── requirements.txt
├── tests/
│   └── excel/
│       └── test_minuslock_bigsmall_v2.py
├── docs/
│   └── README.md
└── examples/
    └── README.md
```

## Файлы

- `MinusLock_SelfCompressing_BigSmall_v2.xlsx` — Excel-калькулятор v2 с листами `Settings`, `Calculator`, `Trend_UP`, `Trend_DOWN`, `Risk_Analysis`, `Tests`, `Manual`, `Examples`.
- `MANUAL_v2.md` — актуальный v2-мануал системы.
- `TEST_REPORT_MinusLock_SelfCompressing_BigSmall_v2.md` — подробный отчёт тестирования калькулятора.
- `tests/excel/test_minuslock_bigsmall_v2.py` — pytest-набор для проверки структуры workbook, формул и v2-логики.
- `requirements.txt` — минимальные Python-зависимости для тестирования.
- `docs/` — папка для дополнительной документации проекта.
- `examples/` — папка для дополнительных примеров проекта.


## v3 исправления

- корректный баланс после закрытия дальнего хвоста;
- `RealizedFarLoss`;
- `Risk_Analysis` учитывает закрытый убыток хвоста;
- `DUAL_TAIL` блокирует следующий уровень;
- `Costs` считаются на закрываемый лот: `Costs = ClosedLotsForCosts × CostPerLot`.


## v4 исправления

- `DUAL_TAIL` теперь хранит оба хвоста;
- `BLOCKED` строки не теряют старый хвост;
- `OpenLotsAfter` и `MarginAfter` считаются от двух хвостов;
- добавлены поля ручного закрытия хвостов: `ManualOldFarCloseLot`, `ManualNewFarCloseLot`, `ManualClosePL`;
- новый уровень после `DUAL_TAIL` невозможен без `ManualAllowNewLevel = YES`.


## v5 fixes

- true `DUAL_TAIL` state persistence;
- `BLOCKED` rows keep both tails;
- `Risk_Analysis` counts `BLOCKED` and `DUAL_TAIL` exposure;
- active tails cannot disappear without manual close;
- `ManualAllowNewLevel` required to resume after `DUAL_TAIL`.

## Результаты тестирования

```text
32 теста PASS
37 pytest PASS
0 критических ошибок
```

Подробности см. в `TEST_REPORT_MinusLock_SelfCompressing_BigSmall_v2.md`.

## Быстрая проверка

Из корня репозитория:

```bash
python -m pytest work/MinusLock_SelfCompressing_BigSmall_v2/tests/excel/test_minuslock_bigsmall_v2.py -q
```

Из папки проекта:

```bash
python -m pytest tests/excel/test_minuslock_bigsmall_v2.py -q
```

## v6 sync fixes

- all calculation sheets share identical headers;
- all formulas generated from one source;
- Trend_UP and Trend_DOWN synchronized;
- Risk_Analysis includes Global Risk Summary;
- DUAL_TAIL/BLOCKED/STOP counted globally;
- workbook auto-calculation enabled.

## v7 fixes

- removed Excel circular references;
- fixed Trend_DOWN DUAL_TAIL persistence;
- populated Global Total Closed Profit / Loss;
- ensured BLOCKED rows have no blank key fields;
- verified workbook formulas with a no-direct-self-reference scan; desktop Excel manual warning check is noted as requiring Microsoft Excel.

## v8 fixes

- fixed Global Max DualTail Exposure formula;
- added Settings geometry table Big-N / Small-N / Close-N;
- geometry table is linked to Settings parameters;
- Close-N is reference lot geometry, not the money-mode close rule.

## Big-harvest model update

- BigRatio = 1.30, SmallRatio = 0.36, CloseFarShare = 0.90, ReserveShare = 0.10;
- CloseBigOnSmall = 0.30 and RemainBigOnSmall = 0.70;
- CloseFarShare = 90% is a money budget from NetProfit, not 90% of the Far lot;
- example: Far = 1.00, Big = 1.30, Small ≈ 0.47, BigMove = 100, FarDistance = 200, NetProfit ≈ 83, CloseFarBudget ≈ 74.7, CloseFarLot ≈ 0.3735, FarRemain ≈ 0.6265.

## v9 LotStep rounding

- CloseFarShare = 90% remains a money budget from NetProfit, not a Far-lot percentage;
- CloseFarLotRaw is calculated from `CloseFarBudget / FarDistancePoints`;
- CloseFarLotRounded is the real tradable lot after `FLOOR(CloseFarLotRaw, LotStep)` and cannot exceed FarStartLot;
- if `CloseFarLotRaw < LotStep`, Far is not closed and `CannotCloseBelowLotStep = YES`;
- final close is allowed only when reserve covers `FarRemainLoss`.

## Big-Harvest Full Cycle Close

- When `FinalCloseAllowed = YES`, the remaining Far is considered fully covered by reserve and the Big-harvest cycle is closed.
- The closing row receives `Status = CLOSED_PROFIT`; `CycleClosed`, `CycleCloseLevel`, and `CycleFinalPL` record the closing event.
- All following levels are stopped: `FarStartLot`, `BigLot`, `SmallLot`, `CloseFarLotRaw`, `CloseFarLotRounded`, `FarRemainAfterRounded`, and `FarRemainLoss` become `0`.
- New Big/Small levels are not opened after full close; balance and reserve are carried forward unchanged.
- `CycleFinalPL = TotalReserve - FarRemainLoss` shows the final profitable result available after the reserve covers the remaining Far loss.

## Big-Harvest EA

- [MinusLock_BigHarvest_EA](MinusLock_BigHarvest_EA/) — MQL5-советник Big-Harvest, перенесённый в рабочую папку проекта.
- [Big-Harvest EA final local verification](reports/tests/big_harvest_ea_final_report.md) — локальный отчёт проверок; MetaEditor Compile и Strategy Tester требуют запуска в Windows/MetaTrader.

## Small-at-Far Scenario

Small-сценарий больше не исполняется сразу при первом движении в сторону Small. Если Small достиг защитного движения, советник переводит цикл в `STATE_WAIT_SMALL_TO_FAR` и ждёт, пока текущая цена дойдёт до цены открытия старого `Far` с учётом `SmallFarTouchOffsetPoints`. Для `Small=BUY` условие касания: `CurrentPrice >= OldFarOpenPrice + offset`; для `Small=SELL`: `CurrentPrice <= OldFarOpenPrice - offset`.

После касания старого Far выполняется `ProcessSmallAtFarTouch`: Small закрывается на 100%, старый Far закрывается на 100%, Big закрывается только на `CloseBigOnSmall`, а остаток Big становится новым Far. Затем обязательно сначала проверяется `FinalCloseAllowed` для нового Far. Если резерва хватает, новый Far закрывается полностью и состояние становится `STATE_CLOSED_PROFIT`; если резерва не хватает, только тогда открывается новый Big/Small от нового Far. В нормальном Small-at-Far сценарии `DUAL_TAIL` не должен появляться, потому что старый Far ликвидируется до назначения нового Far.

## Reverse Geometry Protection

`MinusLock_BigHarvest_EA` теперь защищает Small-at-Far rebuild перед открытием новой пары Big/Small:

- `NewFarLot` должен быть меньше `OldFarLot`.
- `NewBigLot` должен быть больше `NewFarLot`.
- `ReverseStrength` / `ReverseQualityScore` показывает качество переворота.
- `MaxReverseCycles` ограничивает бесконечные reverse-циклы.
- `ProjectedReserveCoverage` показывает, хватит ли резерва на следующий этап.
- `FinalCloseAllowed` проверяется до открытия нового Big/Small.
