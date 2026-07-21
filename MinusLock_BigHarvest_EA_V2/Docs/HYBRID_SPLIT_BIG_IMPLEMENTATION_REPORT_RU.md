# Отчёт реализации Hybrid Split Big

| Требование дизайна | Реализация | Статус |
|---|---|---|
| Target-first NewFar | `CalcTargetNewFarLot`, `BuildHybridReversePlan` | PASS |
| Денежный TransitionPlan | `HybridTransitionPlanner.mqh` + broker money API | PASS |
| Next geometry preview | `PreviewNextSplitGeometry` до и после Core close | PASS |
| Recovery/Catch-up gate | `SolveHybridGeometry` + plan preview | PASS |
| OldFar без плана запрещён | `ProcessSplitSmallCloseOldFar` | PASS |
| Фактический остаток Core | `ProcessSplitSmallCloseCorePart` | PASS |
| Persisted core plan identity/target | `SaveState`/`RecoverState` | PASS |
| Реальные MT5 deal/fill/restart | Strategy Tester | PENDING |

`UseHybridSplitBigGeometry` — новый единственный opt-in switch. Старый
`UseHybridGeometrySolver` сохранён только для backward-compatible set-файлов
и не активирует новый путь. Final Reserve не используется в plan transition.
