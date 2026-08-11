# HSB.1V — аудит identity и ownership

Полный source-of-truth tuple: `AccountLogin + Symbol + Magic + CycleID + PositionIdentifier + Role`.

- `HSBI_SamePositionOwner` сравнивает все элементы tuple; comment и ticket не участвуют.
- `HSBI_EvaluateOwnership` отклоняет foreign identity, changed role, changed direction, changed actual volume и revision mismatch, направляя результат в reconciliation.
- Stale/reused ticket не меняет ownership: ticket не заменяет `PositionIdentifier`.
- `BIG_CORE` допускается к promotion только как фактически наблюдаемый ненулевой residual с исходным identifier; произвольная role promotion запрещена.
- `HSBI_ExactlyOneFarOrZero` отклоняет два Far.

Тестовый script содержит проверки foreign tuple, stale/reused ticket, changed volume, changed role, duplicate Far и actual residual. До фактического запуска MT5 результаты остаются `UNVERIFIED`.
