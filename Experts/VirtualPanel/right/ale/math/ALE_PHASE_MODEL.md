# ALE Mathematical Stability Specification
## Phase Diagram Contract

**Path:** `Experts/VirtualPanel/right/ale/math/ALE_PHASE_MODEL.md`

Этот документ фиксирует математический контракт устойчивости ALE и обязателен для модулей:
- `math/`
- `risk/`
- `optimization/`
- `tests/`

Изменение формул в этом документе допускается только через отдельное архитектурное решение.

## 1) Назначение
Phase Diagram делит пространство параметров ALE на три фазы:
- `STABLE`
- `MARGINAL`
- `EXPLOSIVE`

Классификация используется в:
- `CALPhaseDiagram`
- `CALRiskEngine`
- `CALGridOptimizer`
- `CALLotOptimizer`
- контрактных тестах.

## 2) Параметры модели
Ключевые параметры:
- `k` — grid step coefficient
- `g` — lot growth coefficient
- `μ` — drift
- `σ` — volatility

## 3) Индекс устойчивости
Определение:

`θ = k × g`

Это ключевой параметр сходимости/расходимости риска.

## 4) Геометрическая интерпретация PnL
Для сеточной модели:

- `Li = L0 × g^i`
- `ΔPi = k^i`
- `PnL ≈ Σ (Li × ΔPi) = L0 × Σ (gk)^i`

Следовательно, устойчивость определяется геометрическим рядом `Σ(gk)^i`.

## 5) Условие сходимости
- Сходимость: `gk < 1`
- Критическая граница: `gk = 1`
- Расходимость: `gk > 1`

## 6) Фазовая классификация
Через `θ = g × k`:

- `STABLE`: `θ < 0.9`
- `MARGINAL`: `0.9 ≤ θ < 1`
- `EXPLOSIVE`: `θ ≥ 1`

## 7) Стохастическая модель
Рынок моделируется GBM:

`dS = μSdt + σSdW`

## 8) Волатильностная коррекция
С учётом волатильности:

`gk < exp(-σ²/2)`

При росте `σ` допустимая область стабильности сужается.

## 9) Интеграционные правила
1. **Risk:** если фаза `EXPLOSIVE`, SAFE обязан активироваться.
2. **Optimization:** параметры из `EXPLOSIVE` области исключаются.
3. **Config Guardrail:** конфиг невалиден, если `k * growth_g >= 1`.
4. **I8 (stability invariant):** `θ < 1`, иначе SAFE must activate.

## 10) Двухпоточная архитектура
Phase Diagram применяется независимо по потокам BUY/SELL с отдельными параметрами `(k_buy, g_buy)` и `(k_sell, g_sell)`.

## 11) Чистота слоя
`CALPhaseDiagram` — чистый математический слой и не зависит от:
- `positions`
- `exposure`
- `geometry`

