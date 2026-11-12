# DG01 — ballot владельца

Все поля AdministratorDecision пусты. ReadinessStatus — оценка подготовленности вопроса, не решение. Возможные действия: утвердить конкретную формулировку, отклонить, вернуть на доработку. Ни один выбор не выполнен Codex.

| Canonical ID | Display | Readiness | Approval |
|---|---|---|---|
|D-01|D-01|READY_FOR_ADMIN_DECISION|AWAITING_ADMIN_APPROVAL|
|D-02|D-02|READY_FOR_ADMIN_DECISION|AWAITING_ADMIN_APPROVAL|
|D-03|D-03|READY_FOR_ADMIN_DECISION|AWAITING_ADMIN_APPROVAL|
|D-04|D-04|READY_FOR_ADMIN_DECISION|AWAITING_ADMIN_APPROVAL|
|D-05|D-05|CONTRACT_CONFLICT|AWAITING_ADMIN_APPROVAL|
|D-06|D-06|INSUFFICIENT_EVIDENCE|AWAITING_ADMIN_APPROVAL|
|D-07|D-07|READY_FOR_ADMIN_DECISION|AWAITING_ADMIN_APPROVAL|
|D-08|D-08|READY_FOR_ADMIN_DECISION|AWAITING_ADMIN_APPROVAL|
|CR-09|D-09|BLOCKED_BY_DEPENDENCY|AWAITING_ADMIN_APPROVAL|
|NUM-EXACT-1|D-10|READY_FOR_ADMIN_DECISION|AWAITING_ADMIN_APPROVAL|
|NUM-DOMAIN-1|D-11|INSUFFICIENT_EVIDENCE|AWAITING_ADMIN_APPROVAL|
|NUM-CODEC|D-12|INSUFFICIENT_EVIDENCE|AWAITING_ADMIN_APPROVAL|
|SNAP-FIXTURE-1|D-13|READY_FOR_ADMIN_DECISION|AWAITING_ADMIN_APPROVAL|
|FUNDING-GLOBAL-ATTRIBUTION|D-14|BLOCKED_BY_DEPENDENCY|AWAITING_ADMIN_APPROVAL|
|MQL-DOMAIN|D-15|INSUFFICIENT_EVIDENCE|AWAITING_ADMIN_APPROVAL|
|BALANCE-SCHEMA-MAPPING|D-16|BLOCKED_BY_DEPENDENCY|AWAITING_ADMIN_APPROVAL|

## D-01
Утвердить/отклонить/вернуть на доработку: G=C+R+F; RemainingGross=R+F; Available=F только после complete reconciliation/journal.

AdministratorDecision: (не заполнено)

Required native/external evidence: MetaEditor compile + isolated script actual logs; codec/native integers goldens for relevant contracts. Backend/broker/durable/concurrent evidence separate.

## D-02
Утвердить/отклонить/вернуть на доработку: Шесть денежных типов не взаимозаменяемы; каждый переход требует independent source/posted/policy/journal boundary.

AdministratorDecision: (не заполнено)

Required native/external evidence: MetaEditor compile + isolated script actual logs; codec/native integers goldens for relevant contracts. Backend/broker/durable/concurrent evidence separate.

## D-03
Утвердить/отклонить/вернуть на доработку: Small-only positive → ResidualHeld; transfer только отдельным approved policy/event.

AdministratorDecision: (не заполнено)

Required native/external evidence: MetaEditor compile + isolated script actual logs; codec/native integers goldens for relevant contracts. Backend/broker/durable/concurrent evidence separate.

## D-04
Утвердить/отклонить/вернуть на доработку: AbsoluteFarLoss рабочий кандидат; Incremental только отдельная диагностика с независимым basis.

AdministratorDecision: (не заполнено)

Required native/external evidence: MetaEditor compile + isolated script actual logs; codec/native integers goldens for relevant contracts. Backend/broker/durable/concurrent evidence separate.

## D-05
Утвердить/отклонить/вернуть на доработку: Владелец выбирает current signed loss, sticky breach либо peak historical loss; выбор здесь не сделан.

AdministratorDecision: (не заполнено)

Required native/external evidence: Confirmed batch membership, ordered partial fills, component costs, restart preservation of selected metric and reset authority; no policy selected here.

## D-06
Утвердить/отклонить/вернуть на доработку: Каждый обязательный cost покрывается ровно один раз по independent basis/window; unknown overlap не безопасный0.

AdministratorDecision: (не заполнено)

Required native/external evidence: MetaEditor compile + isolated script actual logs; codec/native integers goldens for relevant contracts. Backend/broker/durable/concurrent evidence separate.

## D-07
Утвердить/отклонить/вернуть на доработку: Global source funding journal + immutable replay + atomic durable commit/CAS; локальная idempotency не exactly-once backend.

AdministratorDecision: (не заполнено)

Required native/external evidence: MetaEditor compile + isolated script actual logs; codec/native integers goldens for relevant contracts. Backend/broker/durable/concurrent evidence separate.

## D-08
Утвердить/отклонить/вернуть на доработку: SourceKey=(Broker,Server,Account,Deal), full immutable body; NEW identity не funding; unknown facts UNAVAILABLE.

AdministratorDecision: (не заполнено)

Required native/external evidence: MetaEditor compile + isolated script actual logs; codec/native integers goldens for relevant contracts. Backend/broker/durable/concurrent evidence separate.

## CR-09
Утвердить/отклонить/вернуть на доработку: Явно выбрать ALL_LEVEL либо SINGLE_LEVEL scope; all-level требует minMargin>0 по каждому required level.

AdministratorDecision: (не заполнено)

Required native/external evidence: MetaEditor compile + isolated script actual logs; codec/native integers goldens for relevant contracts. Backend/broker/durable/concurrent evidence separate.

## NUM-EXACT-1
Утвердить/отклонить/вернуть на доработку: Exact settled money representation; projected risk не округляется до безопасного0.

AdministratorDecision: (не заполнено)

Required native/external evidence: MetaEditor compile + isolated script actual logs; codec/native integers goldens for relevant contracts. Backend/broker/durable/concurrent evidence separate.

## NUM-DOMAIN-1
Утвердить/отклонить/вернуть на доработку: Явный supported currency/precision/range и отказ за domain; unlimited Fraction не MQL domain.

AdministratorDecision: (не заполнено)

Required native/external evidence: MetaEditor compile + isolated script actual logs; codec/native integers goldens for relevant contracts. Backend/broker/durable/concurrent evidence separate.

## NUM-CODEC
Утвердить/отклонить/вернуть на доработку: F64Z рекомендуется как candidate raw captured codec; T17Z — альтернатива; native compatibility не подтверждена.

AdministratorDecision: (не заполнено)

Required native/external evidence: MetaEditor compile + isolated script actual logs; codec/native integers goldens for relevant contracts. Backend/broker/durable/concurrent evidence separate.

## SNAP-FIXTURE-1
Утвердить/отклонить/вернуть на доработку: Versioned strict schema+typed content+независимый receipt; fixture receipt не broker authenticity.

AdministratorDecision: (не заполнено)

Required native/external evidence: MetaEditor compile + isolated script actual logs; codec/native integers goldens for relevant contracts. Backend/broker/durable/concurrent evidence separate.

## FUNDING-GLOBAL-ATTRIBUTION
Утвердить/отклонить/вернуть на доработку: Единый source-level inventory across allocations, roles и restarts; transfer/reversal отдельными событиями.

AdministratorDecision: (не заполнено)

Required native/external evidence: MetaEditor compile + isolated script actual logs; codec/native integers goldens for relevant contracts. Backend/broker/durable/concurrent evidence separate.

## MQL-DOMAIN
Утвердить/отклонить/вернуть на доработку: Native long/ulong/double/UTF8, overflow, finite-only и codec goldens обязательны до acceptance.

AdministratorDecision: (не заполнено)

Required native/external evidence: MetaEditor compile + isolated script actual logs; codec/native integers goldens for relevant contracts. Backend/broker/durable/concurrent evidence separate.

## BALANCE-SCHEMA-MAPPING
Утвердить/отклонить/вернуть на доработку: Legacy Remaining мигрирует только при известном gross/free/consumed/reserved/owner/currency mapping.

AdministratorDecision: (не заполнено)

Required native/external evidence: MetaEditor compile + isolated script actual logs; codec/native integers goldens for relevant contracts. Backend/broker/durable/concurrent evidence separate.
