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
