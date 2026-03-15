# ALE + ALC Architecture Specification (Implemented in this iteration)

## 1. Problem Statement

Классический ALE-only pipeline (`geometry -> positions -> exposure -> risk -> optimization -> FSM`) не имеет структурной компрессии книги, что ведёт к росту depth, exposure, margin pressure и риск-эскалации.

## 2. ALC Layer

Добавлен слой **ALC (Adaptive Lock Compression)** между `positions` и `exposure`.

Новый pipeline:

`geometry -> positions -> ALC compression -> exposure -> risk -> optimization -> FSM`

## 3. Compression Type

Используется **TYPE C — LOCK COMPRESSION**.

В рамках текущей stream-local реализации compression применяет коэффициентное сжатие лотов книги (`alpha=0.5`) c сохранением относительной геометрии уровней.

## 4. Trigger Conditions

Compression trigger активируется при любом из условий:

- `n > 8` (глубина структуры),
- `margin_level < 200%`, где `margin_level = Equity / Margin * 100`,
- `n >= max_levels` (`max_levels=30`),
- SAFE-rescue path (`safe_active == true`).

## 5. Compression Coefficient

- `alpha = 0.5`
- `effective_exposure = exposure * alpha`
- `delta_new = delta * alpha`
- `margin_new = margin * alpha`

## 6. PnL Policy

Compression не фиксирует PnL внешним close-all действием;
PnL перераспределяется структурно вместе с лотами (пропорционально сжатию объёма).

## 7. Max Levels Constraint

- `max_levels = 30`
- при достижении лимита новые уровни не добавляются,
- запускается compression.

## 8. SAFE Integration

В SAFE режиме включён **Rescue Compression**:

`SAFE -> ALC compression -> stabilization`

## 9. Harvest Modes

Поддерживаются:
- `HARVEST_FULL` — принудительный SAFE обоих потоков,
- `HARVEST_PARTIAL` — запуск stream compression без форсированного SAFE.

## 10. Compression History

Ведётся журнал событий компрессии:

- `timestamp`
- `levels_before`, `levels_after`
- `delta_before`, `delta_after`
- `margin_before`, `margin_after`

## 11. Adaptive k

`CALOptimalK` сохранён; в текущей итерации ALC интегрирован без изменения внешнего API `CALOptimalK`.
Функциональная цель: `k = f(volatility, exposure, depth)` оставлена как точка следующей итерации.

## 12. New Modules

Добавлен каталог: `ale/compression/`

- `CALCompressionEngine.mqh`
- `CALLockCompression.mqh`
- `CALCompressionHistory.mqh`
- `CALCompressionScheduler.mqh`

## 13. Main Compression API

Текущий API в коде:

```cpp
bool ProcessCompression(CALPositionBook &book,
                        CALStreamContext &ctx,
                        const double equity,
                        const bool safe_rescue);
```

## 14. LOCK Compression Algebra

Базовые формулы:

- `L_i = L0 * k^i`
- `V = Σ L_i`
- `Δ = Σ sign_i * L_i`
- `Δ_new = Δ * alpha`

Pair-lock reference form:

- `L_lock = min(B_i, S_j)`
- `B_i_new = B_i - L_lock`
- `S_j_new = S_j - L_lock`

## 15. Optimization Objective

Компрессия направлена на уменьшение

`F = |Δ| + λ * Margin`

## 16. Stability Intuition

- Без ALC: `Risk ~ k^n`
- С ALC: `Risk ~ alpha^m * k^n`

где `m` — число компрессий.

## 17. Bounded Exposure Guardrails

Система поддерживает bounded структуру при:

- `alpha <= 0.5`
- `n_max <= 30`
- фазовом контроле `k*g < 1` + SAFE.

## 18. FSM Extension

В FSM добавлены:

- состояние `ALE_STATE_COMPRESSION`
- сигнал `ALE_SIGNAL_COMPRESSION`

## 19. Unit Test Targets (added)

Добавлены новые unit-test файлы:

- `TestLockCompression.mqh`
- `TestALCStability.mqh`
- `TestCompressionMargin.mqh`
- `TestCompressionPnL.mqh`
- `TestCompressionTrigger.mqh`

## 20. Outcome

ALE расширен до **ALE + ALC**, где компрессия стала системным механизмом контроля depth/exposure/margin и стабилизации поведения при стрессовых состояниях.
