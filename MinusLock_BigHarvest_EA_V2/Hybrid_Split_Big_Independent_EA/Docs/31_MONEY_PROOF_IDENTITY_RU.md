# 31. Identity broker-money proof

`HSBI_MoneyProofIdentity` связывает proof с account, Symbol, Magic, CycleID, PositionIdentifier, role, direction, source deal/event, snapshot, PlanID и StateRevision. Reserve и Far proofs проверяются независимо.

Reserve source обязан иметь положительный finite net, runtime-confirmed projected PASS и роль BigCore/BigTrend. Far-loss source обязан иметь роль FAR, направление старого Far и отдельную identity. Basket recovery, общий gross profit и transition loss не заменяют эти proofs.

Identity mismatch отклоняет Catch-Up fail-closed; comment не является identity source.
