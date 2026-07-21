# План реализации Hybrid Split Big

1. `HybridGeometrySolver.mqh`: common money preview и выбор Big candidate.
2. `HybridTransitionPlanner.mqh`: persisted `HybridReversePlan`, preview next
   geometry и запрет закрытия OldFar без valid plan.
3. `Types.mqh`: explicit phase states/context; `StateMachine.mqh`: dispatch и
   phase actions через существующие pending/retry/actual-volume contracts.
4. `Config.mqh`: только необходимые opt-in inputs. `BrokerMoneyModel.mqh`:
   TargetNewFar только при Hybrid mode.
5. Документ/код таблица и Python mirror создаются после реализации; MetaEditor
   и Strategy Tester остаются внешними acceptance gates.
