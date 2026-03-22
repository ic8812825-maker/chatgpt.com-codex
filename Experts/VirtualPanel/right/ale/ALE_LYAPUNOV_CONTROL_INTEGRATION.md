# ALE_LYAPUNOV_CONTROL_INTEGRATION

## 1) Где считается V и ΔV

Runtime-вычисление Lyapunov телеметрии встроено в `CALFlowEngine`:

- формирование состояния: `BuildLyapunovState(...)`
- расчет `V` и `ΔV`: `UpdateLyapunovTelemetry(...)`
- принятие управляющего действия: `ApplyLyapunovControl(...)`

## 2) Где используется в runtime

Lyapunov используется вне `/lyapunov/` в ядре:

- `CALFlowEngine::AddVirtual(...)` — запрет expansion при высоком Lyapunov-риске
- `CALFlowEngine::Process(...)` — Lyapunov guard/critical сигналы влияют на compression/SAFE
- `CALRiskEngine::Evaluate(...)` — Lyapunov критичность участвует в SAFE-триггере
- `CALCompressionEngine::ShouldTrigger(...)` — Lyapunov risk/delta ускоряют compression trigger
- `CALStateMachine` — новые сигналы `ALE_SIGNAL_LYAPUNOV_GUARD/CRITICAL`

## 3) Feedback loop

Замкнутый контур управления:

`state -> V/ΔV -> guard/critical action -> compression/SAFE/expansion gating -> new state`

Реакции:

- рост `V` / положительный `ΔV` -> усиление контроля
- Lyapunov critical -> SAFE + rescue compression
- снижение риска -> ослабление блокировок и восстановление активности

## 4) Согласование Python ↔ MQL

Слои приведены к общей концепции:

- единый набор факторов риска (drawdown, exposure, margin, depth, distance, loss)
- учет control/latency/compression в улучшенной формуле
- baseline vs improved сравнение в Python-аудите и отчетах

## 5) Телеметрия

В `CALStreamContext` добавлены поля:

- `lyapunov_v`
- `lyapunov_delta`
- `lyapunov_prev_v`
- `lyapunov_risk_level`
- `lyapunov_action_code`

Это позволяет трассировать, почему принято конкретное runtime-решение.
