# 3.1.6.3.11 — Small Transition и NewFar

## Hybrid sequence found

При Hybrid trigger строится `hybridReversePlan` и вызывается `SaveState()`. Фактические phases используют Split states:

```text
SmallBase full close
→ OldFar full close
→ BigTrend full close
→ BigCore partial close
→ actual remaining BigCore read from position
→ promote BigCore ticket/identifier as sole Far
→ clear BigCore role
→ history P/L check
→ ReconcileCompletedSmallTransition
```

Это близко к целевой роли NewFar. `ReconcileCompletedSmallTransition()` требует закрытия OldFar/BigTrend/SmallBase, положительный compressed Far, один managed position и Reserve consistency.

## Критические проблемы

- Each close handler advances on synchronous wrapper; actual transaction event is absent.
- `ClosePositionByTicketWithComment()` accepts `PLACED` and `DONE_PARTIAL`; `VerifyFullClose()` polling immediately after request may race terminal update.
- BigCore target в Hybrid берётся из `hybridReversePlan`, но close lot вычисляется заново как `bigCoreLot-target`.
- Actual residual проверяется, что является сильной частью mapping.
- Minimum transition condition uses `smallScenarioRealAfter-smallScenarioRealBefore < MinimumTransitionProfitMoney`; relation to normative `MaximumTransitionLossMoney`/TransitionBudget contract is not unified.
- Non-Hybrid Split branch keeps DynamicReverseSmall/legacy alternative roles; same functions contain both paths.

## Замечания

- `SMALL-001 P1`: Correct target order exists, but no transaction-confirmed barrier between phases.
- `SMALL-002 P1`: Hybrid and non-Hybrid Split execute in shared functions/states.
- `SMALL-003 P1`: Transition money gate differs from normative signed TransitionNet/budget model.
- `SMALL-004 P1`: Full-close verification may occur before asynchronous settlement.
- `SMALL-005 P2`: Plan target is persisted, but full immutable per-phase StateRevision binding is absent.

NewFar source: `MAPPED_AND_ACTIVE` only inside Hybrid-modified Split route; lifecycle safety: `PARTIAL/UNSAFE`.
