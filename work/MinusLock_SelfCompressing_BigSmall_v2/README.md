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
