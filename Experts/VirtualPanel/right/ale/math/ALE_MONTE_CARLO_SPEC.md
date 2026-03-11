# ALE_MONTE_CARLO_SPEC.md
## Спецификация стохастического стресс-тестирования ALE

Версия: 1.0

---

## 1. Назначение

Документ задаёт единый протокол Monte Carlo стресс-тестов для ALE.

Цели:
1. оценка частоты SAFE,
2. оценка распределений DD/PnL,
3. выявление неустойчивых конфигураций,
4. подтверждение инвариантов I1–I8 на случайных траекториях.

---

## 2. Стохастическая модель

Используется GBM-дискретизация:

\[
S_{t+\Delta t}=S_t\exp\left((\mu-\sigma^2/2)\Delta t+\sigma\sqrt{\Delta t}Z_t\right),
\quad Z_t\sim\mathcal N(0,1).
\]

Параметры:
- \(S_0\) — начальная цена,
- \(\mu\) — drift,
- \(\sigma\) — volatility,
- \(\Delta t\) — шаг,
- \(T\) — горизонт,
- \(N=T/\Delta t\) — число шагов,
- \(M\) — число траекторий.

---

## 3. Входной профиль тестирования

Минимальный набор сценариев по параметрам:

1. Низкая волатильность: \(\sigma\in[0.05,0.15]\)
2. Средняя: \(\sigma\in[0.15,0.30]\)
3. Высокая: \(\sigma\in[0.30,0.60]\)
4. Кризисная: \(\sigma>0.60\)

Для каждого профиля прогоняются стабильные, пограничные и эксплозивные пары \((k,g)\).

---

## 4. Фазовые группы конфигураций

Определяется \(\theta=kg\):
- STABLE: \(\theta<0.9\)
- MARGINAL: \(0.9\le\theta<1\)
- EXPLOSIVE: \(\theta\ge1\)

Требования:
- STABLE не должен иметь массовых мгновенных SAFE.
- EXPLOSIVE должен отклоняться/переводиться в SAFE.

---

## 5. Метрики, обязательные к сбору

Для каждой траектории j:
- \(PnL_j(T)\)
- \(DD_j^{max}\)
- \(M_j^{max}\)
- индикатор SAFE: \(I_j^{SAFE}\in\{0,1\}\)
- время первого SAFE: \(\tau_j^{SAFE}\)

Агрегаты:
- \(\mathbb E[PnL(T)]\)
- \(\mathbb E[DD^{max}]\)
- квантиль \(q_{0.95}(DD^{max})\)
- SAFE-rate:

\[
\text{SAFE\_rate}=\frac{1}{M}\sum_{j=1}^M I_j^{SAFE}.
\]

---

## 6. Критерии приёмки Monte Carlo

Для STABLE-конфигураций:
1. отсутствует систематическое нарушение I1–I8,
2. SAFE-rate ниже заданного лимита \(\alpha_{stable}\),
3. tail-DD ниже лимита \(DD_{95}^{max}\).

Для MARGINAL:
- допускается рост SAFE-rate, но без нарушения hard-контрактов SAFE.

Для EXPLOSIVE:
- конфигурация должна быть отклонена guardrail-валидацией **или**
- должен наблюдаться near-immediate SAFE.

---

## 7. Проверка инвариантов на траекториях

Для каждого шага t и траектории j проверяются:
- I1, I2: bounded exposure/margin,
- I3: SAFE non-bypass,
- I5: additivity BUY+SELL,
- I7: monotonic risk,
- I8: \(\theta<1\) либо SAFE.

Любое нарушение = fail сценария.

---

## 8. Требования к воспроизводимости

Monte Carlo должен быть воспроизводим:
- фиксированный seed генератора,
- фиксированный набор параметров,
- протокол сериализации результатов.

Рекомендация:

\[
seed = hash(config\_id, scenario\_id).
\]

---

## 9. Псевдокод прогона

```text
for each scenario in ScenarioSet:
  set (mu, sigma, dt, T, M)
  for each config in ConfigSet:
    if invalid(config): mark REJECTED; continue
    safe_count = 0
    for j in 1..M:
      S <- generate_gbm_path(seed_j)
      state <- reset(config)
      for t in 1..N:
        state <- step_ALE(state, S[t])
        check_invariants(state)
      collect_metrics(j, state)
      if state.safe_ever: safe_count++
    aggregate_metrics(config)
    evaluate_acceptance(config)
```

---

## 10. Набор отчётных графиков

Обязательные графики по каждому профилю:
1. Гистограмма \(DD^{max}\)
2. Гистограмма итогового \(PnL(T)\)
3. SAFE-rate vs \(\theta\)
4. SAFE-rate vs \(\sigma\)
5. Heatmap по \((k,g)\) с фазовыми зонами.

---

## 11. Связь с фазовой теорией

Monte Carlo должен подтверждать:
- с ростом \(\theta\) растёт SAFE-rate,
- при \(\theta\ge1\) система входит в SAFE существенно чаще/раньше,
- с ростом \(\sigma\) стабильная область по \((k,g)\) сужается, согласуясь с

\[
kg<e^{-\sigma^2/2}.
\]

---

## 12. Связь с документацией

Этот документ связан с:
- `ALE_FORMAL_SPEC.md` (общая формальная модель),
- `ALE_INVARIANTS.md` (контракты I1–I8),
- `ALE_RISK_PROOF.md` (доказательная часть),
- `ALE_PHASE_MODEL.md` (фазовый контракт).

---

## 13. Нормативный статус

Monte Carlo стресс-тестирование является обязательным для любых изменений:
- risk/,
- optimization/,
- math/,
- core/ (если затрагиваются SAFE и фазовые правила).

