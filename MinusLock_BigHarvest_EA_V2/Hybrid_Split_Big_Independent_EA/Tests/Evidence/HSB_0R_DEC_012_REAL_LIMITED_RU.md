# HSBI-DEC-012 — future REAL_LIMITED contract

Статус: `RESOLVED`.

Режим `REAL_LIMITED` не разрешён данным этапом. Его будущая активация требует одновременно ExplicitUserApproval, ProductionReadiness PASS и DemoForward PASS.

Обязательные controls: ApprovedSymbolList, validated minimum/start/max lot, one cycle per symbol, MaximumDailyLoss, MaximumCycleLoss, MaximumAccountDrawdown, MaximumMarginPercent, ManualKillSwitch, AutomaticTerminalSafe, full immutable logging, daily reconciliation, no auto-resume after critical error. Любой unset/invalid control блокирует запуск.

После critical error требуется manual review и новый explicit approval token. Owner: `Core/RuntimeMode`, `Risk/EmergencyPolicy`, `Diagnostics/EvidenceWriter`. Tests: absent approval, unapproved symbol, daily limit, kill switch, restart-after-critical.

Текущий статус неизменен: REAL_TRADING_ALLOWED=NO.
