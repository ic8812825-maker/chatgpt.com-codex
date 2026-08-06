# HSBI-DEC-006 — Emergency Policy

Статус: `RESOLVED`.

Recovery Final Close и Emergency Liquidation являются разными authorities, reason codes, отчётами и terminal states. Recovery Final Close требует положительного RecoveryPL gate. Emergency допускает убыток только по MARGIN_EMERGENCY, DRAWDOWN_EMERGENCY, IDENTITY_CONFLICT, PERSISTENCE_CORRUPTION, UNKNOWN_POSITION, DUPLICATE_FAR, BROKER_EXECUTION_FAILURE либо MANUAL_KILL_SWITCH.

Emergency не называется успешным recovery; Reserve не прибавляется к результату; после запуска запрещены новые открытия и auto-resume. Закрытия проходят ownership guard, persist-before-action и transaction confirmation. Неоднозначная ownership переводит систему в TERMINAL_SAFE без угадывания позиции; manual review обязателен.

Owner: `Risk/EmergencyPolicy` совместно с `Execution/TransactionEngine`. Tests: every trigger, no-open-after-trigger, loss reporting, duplicate Far, restart during liquidation.
