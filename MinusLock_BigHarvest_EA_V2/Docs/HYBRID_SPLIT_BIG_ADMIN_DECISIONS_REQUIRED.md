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
