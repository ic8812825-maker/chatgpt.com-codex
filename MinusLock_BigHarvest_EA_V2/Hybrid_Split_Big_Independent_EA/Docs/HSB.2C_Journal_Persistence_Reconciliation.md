# HSB.2C — Journal, persistence и reconciliation

Journal append-only связывает записи previous/current/payload digest. Идентичный повтор — NO_OP, тот же ключ с другим payload — CONFLICT. Scope CycleID/PlanID/StateRevision обязателен.

Execution snapshot проверяет schema/version, identity, monotonic revision, chain, digest, freshness и единственность active/completed intents. Ошибка восстановления даёт RECOVERY_REJECTED/UNAVAILABLE и fail-closed.

External outcome завершает intent только при runtime terminal source, свежем EventID, прочитанных Deal/Position, ownership, полном volume, допустимой price и полном identity match. Simulated/injected/proxy outcome не завершает production intent.
