# AUDIT03 CLOSE — Event × State × Partial × Timeout × Restart

База `398da88424f3fb7b30e5315fbc3bf89219dd9ad2`; ветка `work`. Все новые изменения контрактов — **PROPOSED**. Owner approval отсутствует.

`Tests/Close/fsm_matrix.csv`: 37 union states (33 production + documentary aliases) × 8 events × 3 fill states × 3 outcome states × 2 restart states = 5328 obligation rows. Каждая строка содержит expected и причину; ProductionVerification=NOT_VERIFIED. Это полный Cartesian obligation grid для объявленных enum, а не проверенная full FSM.

Docs/06:6 дополнительно называет ACTION_REQUEST_SENT, ACTION_ORDER_PENDING, ACTION_PARTIAL_FILL, ACTION_RETRY_PENDING; production enum вместо них содержит RETRY_PENDING. Эти четыре documentary aliases включены отдельными строками полного Cartesian grid; их mapping к production enum NOT_VERIFIED. Ни одна неприсутствующая роль не считается покрытой автоматически.

StateMachine:5 разрешает часть графа и self-transition, :6 не проверяет event/actual settlement и increment overflow, :7 не сохраняет journal. Поэтому topology не является execution authorization. Main:19–44 остаётся DISABLED + stub.

При COMPLETE fill нужны независимые confirmed deals, exact volume, fresh positions, ownership, ledger, persisted result и expected revision. Partial/timeout/unknown не разрешают следующий шаг; restart блокирует resume до reconciliation. Terminal/manual/emergency safety conditions отдельно от recovery success.

FULL_FSM_VERIFIED=NO. Full documentary state alias mapping и реализация обязательных callers остаются gap.
