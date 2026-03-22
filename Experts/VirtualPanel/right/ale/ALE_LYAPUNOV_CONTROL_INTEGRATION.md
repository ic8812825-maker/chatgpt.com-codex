# ALE_LYAPUNOV_CONTROL_INTEGRATION

## 1) Где считается V и ΔV

Runtime-вычисление Lyapunov телеметрии встроено в `CALFlowEngine`:

- `BuildLyapunovState(...)`
- `UpdateLyapunovTelemetry(...)`

Там же рассчитывается непрерывная сила управления:

- `lyapunov_control_strength = f(V, ΔV)`

## 2) Где выбирается действие, минимизирующее ΔV (КЛЮЧЕВОЕ)

**Файл:** `Experts/VirtualPanel/right/ale/core/CALFlowEngine.mqh`  
**Функция:** `SelectLyapunovAction(...)`

Логика:

1. Генерируются кандидаты действий:
   - `HOLD`, `EXPAND`, `COMPRESS`, `PARTIAL_CLOSE`, `SAFE`
2. Для каждого кандидата вычисляется прогноз:
   - `PredictDeltaVForAction(...)` -> `ΔV_pred = V_next - V_now`
3. В runtime выбирается действие с минимальным `ΔV_pred`.

Это не пороговый `if(flag)`, а selection через objective `min ΔV`.

## 3) Небинарное управление

В `CALFlowEngine` используется **небинарная** интенсивность:

- `lyapunov_control_strength` (0..1)
- compression alpha масштабируется непрерывно: `alpha = 1 - k*strength`
- expansion damping масштабируется непрерывно: `lyap_guard = 1 - strength`

Связь:

- `ΔV` растет -> `control_strength` растет
- `ΔV` снижается -> контроль ослабевает

## 4) Feedback loop

Замкнутый контур:

`state -> V/ΔV -> action selection(min ΔV) -> runtime action -> new state`

Где action влияет на:

- expansion gating
- compression/partial close
- SAFE
- FSM transitions (`ALE_SIGNAL_LYAPUNOV_GUARD/CRITICAL`)

## 5) Где Lyapunov влияет вне `/lyapunov/`

- `CALFlowEngine::AddVirtual(...)`
- `CALFlowEngine::ApplyLyapunovControl(...)`
- `CALFlowEngine::Process(...)`
- `CALRiskEngine::Evaluate(...)`
- `CALCompressionEngine::ShouldTrigger(...)`
- `CALStateMachine::TransitionBySignal(...)`

## 6) Проверка доминирования Lyapunov

В тестах добавлены сценарии поведения (не только формулы):

- `TestLyapunovOptimization`
- `TestLyapunovConvergence`
- `TestLyapunovDominance`

Их цель: показать, что режим с Lyapunov-control меняет поведение и метрики (E[ΔV], collapse risk, recovery).


## 7) Multi-step objective (Level 2)

Добавлено multi-step прогнозирование:

- `PredictDeltaVTrajectory(action, horizon=3)`

Итоговая целевая функция выбора действия:

- `objective = cumulative_ΔV + 0.6*ΔV_next + λ*V_next + penalty(V_next > threshold)`

Это устраняет жадность одношагового выбора и вводит bounded-V constraint.
