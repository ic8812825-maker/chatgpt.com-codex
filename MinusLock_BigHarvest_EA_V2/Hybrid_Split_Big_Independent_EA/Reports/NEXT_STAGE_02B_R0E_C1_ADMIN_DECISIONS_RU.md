# 02B-R0E-C1 — административные решения и уточнения

BASE_SHA=074165b38f1b6d6253a9629c7d2def988e8e286a

PROPOSED / AWAITING_ADMIN_APPROVAL. Audit/test-only; production/trading/dispatch запрещены.

Сохраняются16 прежних решений. C1 усиливает их технические критерии, не создаёт отдельное экономическое решение для каждого теста. Реального утверждения нет. Replay priority и batch netting — явно предложенные исполнимые fixture profiles, требуют выбора в D07/D05 до production.

## Contract: D-01

Recommendation: Сохранить прежнее PROPOSED решение до явного утверждения; C1 не меняет экономическую семантику; прежний scope/approval неизменён.
ExactProposedContract: См. C1 CONTRACT_ADDENDUM и исходный R0E sheet.
Alternatives: Для D05 net batch loss либо отдельно утверждённый peak/sticky cap; для D07 receipt-first либо conflict-first с явно заданной unavailable policy. Остальные альтернативы R0E сохранены.
MigrationImpact: Не выполняется; C1 store/schema/receipts только fixtures, не совместимый production migration codec.
UnprovenDependencies: broker authenticity, global funding/debit attribution, durable/CAS/recovery, MQL5 runtime и full NewFar integration.
R1Impact: Новое отдельное задание только после approved dependencies; production сейчас запрещён.
ApprovalStatus: AWAITING_ADMIN_APPROVAL
AdministratorDecision:

ApprovalDate:

ApprovalIdentifier:

## Contract: D-02

Recommendation: Сохранить прежнее PROPOSED решение до явного утверждения; Journal-aware AvailableReserve, unknown не known0.
ExactProposedContract: См. C1 CONTRACT_ADDENDUM и исходный R0E sheet.
Alternatives: Для D05 net batch loss либо отдельно утверждённый peak/sticky cap; для D07 receipt-first либо conflict-first с явно заданной unavailable policy. Остальные альтернативы R0E сохранены.
MigrationImpact: Не выполняется; C1 store/schema/receipts только fixtures, не совместимый production migration codec.
UnprovenDependencies: broker authenticity, global funding/debit attribution, durable/CAS/recovery, MQL5 runtime и full NewFar integration.
R1Impact: Новое отдельное задание только после approved dependencies; production сейчас запрещён.
ApprovalStatus: AWAITING_ADMIN_APPROVAL
AdministratorDecision:

ApprovalDate:

ApprovalIdentifier:

## Contract: D-03

Recommendation: Сохранить прежнее PROPOSED решение до явного утверждения; C1 не меняет экономическую семантику; прежний scope/approval неизменён.
ExactProposedContract: См. C1 CONTRACT_ADDENDUM и исходный R0E sheet.
Alternatives: Для D05 net batch loss либо отдельно утверждённый peak/sticky cap; для D07 receipt-first либо conflict-first с явно заданной unavailable policy. Остальные альтернативы R0E сохранены.
MigrationImpact: Не выполняется; C1 store/schema/receipts только fixtures, не совместимый production migration codec.
UnprovenDependencies: broker authenticity, global funding/debit attribution, durable/CAS/recovery, MQL5 runtime и full NewFar integration.
R1Impact: Новое отдельное задание только после approved dependencies; production сейчас запрещён.
ApprovalStatus: AWAITING_ADMIN_APPROVAL
AdministratorDecision:

ApprovalDate:

ApprovalIdentifier:

## Contract: D-04

Recommendation: Сохранить прежнее PROPOSED решение до явного утверждения; C1 не меняет экономическую семантику; прежний scope/approval неизменён.
ExactProposedContract: См. C1 CONTRACT_ADDENDUM и исходный R0E sheet.
Alternatives: Для D05 net batch loss либо отдельно утверждённый peak/sticky cap; для D07 receipt-first либо conflict-first с явно заданной unavailable policy. Остальные альтернативы R0E сохранены.
MigrationImpact: Не выполняется; C1 store/schema/receipts только fixtures, не совместимый production migration codec.
UnprovenDependencies: broker authenticity, global funding/debit attribution, durable/CAS/recovery, MQL5 runtime и full NewFar integration.
R1Impact: Новое отдельное задание только после approved dependencies; production сейчас запрещён.
ApprovalStatus: AWAITING_ADMIN_APPROVAL
AdministratorDecision:

ApprovalDate:

ApprovalIdentifier:

## Contract: D-05

Recommendation: Сохранить прежнее PROPOSED решение до явного утверждения; Independent batch membership; предложенный signed-batch-net/cap-on-prefix; sticky historical breach/peak loss не решены.
ExactProposedContract: См. C1 CONTRACT_ADDENDUM и исходный R0E sheet.
Alternatives: Для D05 net batch loss либо отдельно утверждённый peak/sticky cap; для D07 receipt-first либо conflict-first с явно заданной unavailable policy. Остальные альтернативы R0E сохранены.
MigrationImpact: Не выполняется; C1 store/schema/receipts только fixtures, не совместимый production migration codec.
UnprovenDependencies: broker authenticity, global funding/debit attribution, durable/CAS/recovery, MQL5 runtime и full NewFar integration.
R1Impact: Новое отдельное задание только после approved dependencies; production сейчас запрещён.
ApprovalStatus: AWAITING_ADMIN_APPROVAL
AdministratorDecision:

ApprovalDate:

ApprovalIdentifier:

## Contract: D-06

Recommendation: Сохранить прежнее PROPOSED решение до явного утверждения; Полный applicable cost set; buffer gate, не actual Consumed; размеры из provider, не выбирались.
ExactProposedContract: См. C1 CONTRACT_ADDENDUM и исходный R0E sheet.
Alternatives: Для D05 net batch loss либо отдельно утверждённый peak/sticky cap; для D07 receipt-first либо conflict-first с явно заданной unavailable policy. Остальные альтернативы R0E сохранены.
MigrationImpact: Не выполняется; C1 store/schema/receipts только fixtures, не совместимый production migration codec.
UnprovenDependencies: broker authenticity, global funding/debit attribution, durable/CAS/recovery, MQL5 runtime и full NewFar integration.
R1Impact: Новое отдельное задание только после approved dependencies; production сейчас запрещён.
ApprovalStatus: AWAITING_ADMIN_APPROVAL
AdministratorDecision:

ApprovalDate:

ApprovalIdentifier:

## Contract: D-07

Recommendation: Сохранить прежнее PROPOSED решение до явного утверждения; Exact receipt versus immutable history conflict: C1 proposed conflict-first для economic source и unavailable при incomplete journals; current gates не повторяются для known receipt.
ExactProposedContract: См. C1 CONTRACT_ADDENDUM и исходный R0E sheet.
Alternatives: Для D05 net batch loss либо отдельно утверждённый peak/sticky cap; для D07 receipt-first либо conflict-first с явно заданной unavailable policy. Остальные альтернативы R0E сохранены.
MigrationImpact: Не выполняется; C1 store/schema/receipts только fixtures, не совместимый production migration codec.
UnprovenDependencies: broker authenticity, global funding/debit attribution, durable/CAS/recovery, MQL5 runtime и full NewFar integration.
R1Impact: Новое отдельное задание только после approved dependencies; production сейчас запрещён.
ApprovalStatus: AWAITING_ADMIN_APPROVAL
AdministratorDecision:

ApprovalDate:

ApprovalIdentifier:

## Contract: D-08

Recommendation: Сохранить прежнее PROPOSED решение до явного утверждения; Раздельные economic/allocation/consumption events, immutable vector binding, historical receipt context.
ExactProposedContract: См. C1 CONTRACT_ADDENDUM и исходный R0E sheet.
Alternatives: Для D05 net batch loss либо отдельно утверждённый peak/sticky cap; для D07 receipt-first либо conflict-first с явно заданной unavailable policy. Остальные альтернативы R0E сохранены.
MigrationImpact: Не выполняется; C1 store/schema/receipts только fixtures, не совместимый production migration codec.
UnprovenDependencies: broker authenticity, global funding/debit attribution, durable/CAS/recovery, MQL5 runtime и full NewFar integration.
R1Impact: Новое отдельное задание только после approved dependencies; production сейчас запрещён.
ApprovalStatus: AWAITING_ADMIN_APPROVAL
AdministratorDecision:

ApprovalDate:

ApprovalIdentifier:

## Contract: CR-09

Recommendation: Сохранить прежнее PROPOSED решение до явного утверждения; C1 не меняет экономическую семантику; прежний scope/approval неизменён.
ExactProposedContract: См. C1 CONTRACT_ADDENDUM и исходный R0E sheet.
Alternatives: Для D05 net batch loss либо отдельно утверждённый peak/sticky cap; для D07 receipt-first либо conflict-first с явно заданной unavailable policy. Остальные альтернативы R0E сохранены.
MigrationImpact: Не выполняется; C1 store/schema/receipts только fixtures, не совместимый production migration codec.
UnprovenDependencies: broker authenticity, global funding/debit attribution, durable/CAS/recovery, MQL5 runtime и full NewFar integration.
R1Impact: Новое отдельное задание только после approved dependencies; production сейчас запрещён.
ApprovalStatus: AWAITING_ADMIN_APPROVAL
AdministratorDecision:

ApprovalDate:

ApprovalIdentifier:

## Contract: NUM-EXACT-1

Recommendation: Сохранить прежнее PROPOSED решение до явного утверждения; C1 не меняет экономическую семантику; прежний scope/approval неизменён.
ExactProposedContract: См. C1 CONTRACT_ADDENDUM и исходный R0E sheet.
Alternatives: Для D05 net batch loss либо отдельно утверждённый peak/sticky cap; для D07 receipt-first либо conflict-first с явно заданной unavailable policy. Остальные альтернативы R0E сохранены.
MigrationImpact: Не выполняется; C1 store/schema/receipts только fixtures, не совместимый production migration codec.
UnprovenDependencies: broker authenticity, global funding/debit attribution, durable/CAS/recovery, MQL5 runtime и full NewFar integration.
R1Impact: Новое отдельное задание только после approved dependencies; production сейчас запрещён.
ApprovalStatus: AWAITING_ADMIN_APPROVAL
AdministratorDecision:

ApprovalDate:

ApprovalIdentifier:

## Contract: NUM-DOMAIN-1

Recommendation: Сохранить прежнее PROPOSED решение до явного утверждения; C1 не меняет экономическую семантику; прежний scope/approval неизменён.
ExactProposedContract: См. C1 CONTRACT_ADDENDUM и исходный R0E sheet.
Alternatives: Для D05 net batch loss либо отдельно утверждённый peak/sticky cap; для D07 receipt-first либо conflict-first с явно заданной unavailable policy. Остальные альтернативы R0E сохранены.
MigrationImpact: Не выполняется; C1 store/schema/receipts только fixtures, не совместимый production migration codec.
UnprovenDependencies: broker authenticity, global funding/debit attribution, durable/CAS/recovery, MQL5 runtime и full NewFar integration.
R1Impact: Новое отдельное задание только после approved dependencies; production сейчас запрещён.
ApprovalStatus: AWAITING_ADMIN_APPROVAL
AdministratorDecision:

ApprovalDate:

ApprovalIdentifier:

## Contract: NUM-CODEC

Recommendation: Сохранить прежнее PROPOSED решение до явного утверждения; C1 не меняет экономическую семантику; прежний scope/approval неизменён.
ExactProposedContract: См. C1 CONTRACT_ADDENDUM и исходный R0E sheet.
Alternatives: Для D05 net batch loss либо отдельно утверждённый peak/sticky cap; для D07 receipt-first либо conflict-first с явно заданной unavailable policy. Остальные альтернативы R0E сохранены.
MigrationImpact: Не выполняется; C1 store/schema/receipts только fixtures, не совместимый production migration codec.
UnprovenDependencies: broker authenticity, global funding/debit attribution, durable/CAS/recovery, MQL5 runtime и full NewFar integration.
R1Impact: Новое отдельное задание только после approved dependencies; production сейчас запрещён.
ApprovalStatus: AWAITING_ADMIN_APPROVAL
AdministratorDecision:

ApprovalDate:

ApprovalIdentifier:

## Contract: SNAP-FIXTURE-1

Recommendation: Сохранить прежнее PROPOSED решение до явного утверждения; C1 не меняет экономическую семантику; прежний scope/approval неизменён.
ExactProposedContract: См. C1 CONTRACT_ADDENDUM и исходный R0E sheet.
Alternatives: Для D05 net batch loss либо отдельно утверждённый peak/sticky cap; для D07 receipt-first либо conflict-first с явно заданной unavailable policy. Остальные альтернативы R0E сохранены.
MigrationImpact: Не выполняется; C1 store/schema/receipts только fixtures, не совместимый production migration codec.
UnprovenDependencies: broker authenticity, global funding/debit attribution, durable/CAS/recovery, MQL5 runtime и full NewFar integration.
R1Impact: Новое отдельное задание только после approved dependencies; production сейчас запрещён.
ApprovalStatus: AWAITING_ADMIN_APPROVAL
AdministratorDecision:

ApprovalDate:

ApprovalIdentifier:

## Contract: FUNDING-GLOBAL-ATTRIBUTION

Recommendation: Сохранить прежнее PROPOSED решение до явного утверждения; C1 не меняет экономическую семантику; прежний scope/approval неизменён.
ExactProposedContract: См. C1 CONTRACT_ADDENDUM и исходный R0E sheet.
Alternatives: Для D05 net batch loss либо отдельно утверждённый peak/sticky cap; для D07 receipt-first либо conflict-first с явно заданной unavailable policy. Остальные альтернативы R0E сохранены.
MigrationImpact: Не выполняется; C1 store/schema/receipts только fixtures, не совместимый production migration codec.
UnprovenDependencies: broker authenticity, global funding/debit attribution, durable/CAS/recovery, MQL5 runtime и full NewFar integration.
R1Impact: Новое отдельное задание только после approved dependencies; production сейчас запрещён.
ApprovalStatus: AWAITING_ADMIN_APPROVAL
AdministratorDecision:

ApprovalDate:

ApprovalIdentifier:

## Contract: MQL-DOMAIN

Recommendation: Сохранить прежнее PROPOSED решение до явного утверждения; C1 не меняет экономическую семантику; прежний scope/approval неизменён.
ExactProposedContract: См. C1 CONTRACT_ADDENDUM и исходный R0E sheet.
Alternatives: Для D05 net batch loss либо отдельно утверждённый peak/sticky cap; для D07 receipt-first либо conflict-first с явно заданной unavailable policy. Остальные альтернативы R0E сохранены.
MigrationImpact: Не выполняется; C1 store/schema/receipts только fixtures, не совместимый production migration codec.
UnprovenDependencies: broker authenticity, global funding/debit attribution, durable/CAS/recovery, MQL5 runtime и full NewFar integration.
R1Impact: Новое отдельное задание только после approved dependencies; production сейчас запрещён.
ApprovalStatus: AWAITING_ADMIN_APPROVAL
AdministratorDecision:

ApprovalDate:

ApprovalIdentifier:

## Contract: BALANCE-SCHEMA-MAPPING

Recommendation: Сохранить прежнее PROPOSED решение до явного утверждения; C1 не меняет экономическую семантику; прежний scope/approval неизменён.
ExactProposedContract: См. C1 CONTRACT_ADDENDUM и исходный R0E sheet.
Alternatives: Для D05 net batch loss либо отдельно утверждённый peak/sticky cap; для D07 receipt-first либо conflict-first с явно заданной unavailable policy. Остальные альтернативы R0E сохранены.
MigrationImpact: Не выполняется; C1 store/schema/receipts только fixtures, не совместимый production migration codec.
UnprovenDependencies: broker authenticity, global funding/debit attribution, durable/CAS/recovery, MQL5 runtime и full NewFar integration.
R1Impact: Новое отдельное задание только после approved dependencies; production сейчас запрещён.
ApprovalStatus: AWAITING_ADMIN_APPROVAL
AdministratorDecision:

ApprovalDate:

ApprovalIdentifier:
