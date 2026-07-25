# Hybrid Split Big — решения Администратора, требуемые до нормативной MQL5-реализации

## ADM-MQL5-01 — конфликт default-геометрии третьего закона

**Фактический config:** `BigCoreRatio=1.60`, `BigTrendRatio=0.25`, `TargetNewFarRatio=0.60`, `MaximumNewBigToOldFarRatio=0.99`.

При постоянных коэффициентах нормативное ограничение NextBig имеет вид:

$$
(c+t)q < MaximumNewBigToOldFarRatio.
$$

Текущие defaults дают:

$$
(1.60+0.25)\times0.60=1.11\ge0.99.
$$

Максимально допустимый target при этих c/t:

$$
q_{max}=0.99/(1.60+0.25)=0.535135\ldots
$$

**Конфликт:** ТЗ требует не менять `TargetNewFarRatio` автоматически, но также требует, чтобы default q=0.60 корректно отклонялся; одновременно полноценный Future Small/NextBig implementation не может самостоятельно выбрать, является ли default режимом reject, новым approved profile либо допустимым исключением.

| Вариант Администратора | Последствие реализации |
|---|---|
| A. Сохранить default 0.60 | `OnInit`/pre-open Hybrid возвращает `HYBRID_CONFIG_INVALID`; hybrid не откроет basket с defaults. |
| B. Утвердить q ≤ 0.535135 | Изменить approved set/profile и parity vectors; legacy remains untouched. |
| C. Изменить c/t или cap | Требуется новый математический proof, vectors и Administrator approval. |

**Требуемое решение:** выбрать A/B/C до изменения MQL5 `Config.mqh`, `OnInit` validation и shipped `.set` profiles.

## ADM-MQL5-02 — rounding SmallBase

Нормативные материалы требуют безопасный all-down до решения Администратора, а текущий код использует `CalcSmallBaseLot` с `NormalizeLotUp`. Это изменяет Law 1/2, margin и parity. Нужно утвердить `EA_CURRENT` либо `ALL_DOWN` и обновлять MQL5, Oracle, formulas и vectors одной транзакцией.

## ADM-MQL5-03 — money allocation ratios

Полный MQL5 ledger требует утверждённые `α/β/γ`; текущие public inputs представляют старую двухдольную модель `CloseFarShare`/`ReserveShare`. Без явной политики carry нельзя внедрять `AllocateConfirmedHarvest` без самостоятельного бизнес-решения.

## ADM-MQL5-04 — terminal risk-reducing close policy

ТЗ разрешает risk-reducing closes в terminal state, но не утверждает, закрывать ли residual exposure автоматически, удерживать до Manual Admin Decision или использовать emergency loss cap. Это определяет торговое действие и не может быть выбрано программистом.

## Утверждено Администратором (2026-07-24)

* `TargetNewFarRatio=0.50`; при `(1.60+0.25)*0.50=0.925<0.99` Third Law проходит с запасом `0.065`.
* Rounding profile: Core DOWN, Trend DOWN, SmallBase UP, NewFar DOWN (`EA_CURRENT`).
* Harvest allocation (superseded 2026-07-25 by ADM-MQL5-05): `.20/.70/.10` больше не является MQL5 default; negative Harvest не кредитует Reserve/Partial, residual идёт в Carry, event idempotent.
* FinalReserveReal не является источником Partial Far или Small Transition.
* Terminal mode: no new positions/NewFar/reserve transfers; разрешены только доказанные worst-case risk-reducing closes, после каждого — Final Close recheck, иначе Manual Hold.

## ADM-MQL5-05 — согласование Hybrid allocation и Law 1

**Статус:** RESOLVED — выбран вариант A (2026-07-25).

Исторически был обнаружен обязательный математический конфликт этапа 2: прежние Hybrid-доли `α=0.20`, `β=0.70`, `γ=0.10` теперь отделены от legacy `WorkCloseFarShare`/`WorkReserveShare`, поэтому Law 1 обязан использовать именно `HybridFinalReserveShare=0.70`.

Текущая геометрия:

```text
BigCoreRatio = 1.60
BigTrendRatio = 0.25
SmallBaseToFarRatio = 0.60
MinimumReserveCatchUpRatio = 1.10
```

Даёт:

```text
K_R = 0.70 * (1.60 + 0.25 - 0.60) = 0.875 < 1.10
```

До решения конфигурация обязана была возвращать `HYBRID_REJECT_LAW1`; подмена legacy `WorkReserveShare` запрещалась и остаётся запрещённой. Решение ниже заменяет Hybrid inputs на `.10/.90/.00`.

### Вариант A — сохранить геометрию и увеличить β

Сохранить `Core=1.60`, `Trend=0.25`, `Small=0.60` и поднять `HybridFinalReserveShare` минимум до `β>=0.88`; пример допустимой суммы: `α=0.10`, `β=0.90`, `γ=0.00`.

### Вариант B — сохранить α/β/γ и изменить геометрию

Сохранить `α=0.20`, `β=0.70`, `γ=0.10`, но изменить геометрию так, чтобы `c+t-s >= 1.57142857`. При текущем `c+t-s=1.25` нужно увеличить `Core`/`Trend` или уменьшить `Small`.

### Вариант C — снизить порог Law 1

Сохранить геометрию и allocation, но снизить `MinimumReserveCatchUpRatio`. Этот вариант не устраняет базовый конфликт `K_R>1`, потому что текущее `K_R=0.875` меньше 1.

### Вариант D — разделить HarvestFinalReserveShare и CatchUpEffectiveReserveShare

Разрешается только при доказанном дополнительном источнике Reserve; фиктивная доля в Law 1 запрещена.

### Решение Администратора — ПРИНЯТО (этап 0)

Выбран вариант A: `HybridPartialFarShare=0.10`, `HybridFinalReserveShare=0.90`, `HybridCarryShare=0.00`. Для утверждённой геометрии `K_R=0.90*(1.60+0.25-0.60)=1.125>=1.10`; ADM-MQL5-05 закрыт. CarryBase равен нулю, но денежный residual округления продолжает кредитоваться в Carry. Защитные запреты FinalReserve остаются без изменений.
