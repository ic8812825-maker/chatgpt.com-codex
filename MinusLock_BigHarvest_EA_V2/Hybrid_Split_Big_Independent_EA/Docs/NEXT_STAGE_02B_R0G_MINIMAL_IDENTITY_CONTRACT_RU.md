# R0G — минимальный identity contract

BASE_SHA=bcaa766568b9fe7eec0781a8c6efbb288cf16dae

PROPOSED / AWAITING_ADMIN_APPROVAL. Только подготовка Minimal R1.1; ни одного production изменения или утверждения.

Источники: `Include/Money/HSBI_EconomicLedgerTypes.mqh:6` struct, `:7` BuildSourceDealKey, `:8` ValidateEconomicRecord, `:9` SameEconomicRecord, `:10` ClassifyEconomicDuplicate, `:11` SerializeEconomicRecord, `:12` IsHarvestSourceEntry. R0F ECONOMIC_IDENTITY_SPEC/NUMERIC_CODEC_OPTIONS/R1_IMPLEMENTATION_SPEC; frozen `hsbi_02b_r0f_contract_candidate.py:record_shape/encode_record`; новые TestID в TEST_RESULTS.json.

## R0G-ID-KEY-1 / R0G-ID-BODY-1

SourceKey=(Broker,Server,AccountLogin,DealTicket), без Symbol/Magic/Cycle/codec/schema в logical key. Broker — устойчивый provider namespace, НЕ автоматически ACCOUNT_COMPANY; Server exact identity без casefold/NFC. Не подставлять текущий terminal account в historical record. Account positive signed long; DealTicket positive ulong. Key tuple сериализуется typed lengths, не через неоднозначные delimiters.

Полный одинаковый supported payload при независимо подтверждённом source и complete registry =>NO_OP. Изменённый immutable body при прежнем key =>CONFLICT. Нет независимого source/ownership/complete registry =>UNAVAILABLE. NEW только когда independently confirmed body и complete logical registry доказывают отсутствие key; это NEW_IDENTITY, не money authorization. Неизвестный legacy не NEW. Codec/schema version никогда не новый доход. Изменение Magic/Cycle/Symbol/Role при прежнем key — conflict даже при согласованном новом proof.

Тесты IDENTITY-FIELD-*/REGISTRY-* меняют каждый field отдельно и согласованно request+authority при frozen ledger. Компоненты Profit50 Commission0 vs Profit60 Commission-10 (остальные0) оба Net50 =>CONFLICT (IDENTITY-LITERAL-50-VS-60). Float equality exact captured finite64; epsilon запрещена. +/-0 эквивалентны только в proposed Z profile; NaN/Infinity отвергаются. Нет raw round->posted и нет проверенного broker DECIMAL net в этой API.

## 29-field минимальный attributed envelope

R0G сознательно сохраняет все29 fields: удаление уже обязательных R0F origin/units/time фактов позволило бы молча ослабить equality или выдать unknown legacy за complete. Это минимальный безопасный envelope ДАННОГО HSBI-EA-ECON-1, не утверждение математической минимальности для всех брокерских сделок. При другой явно approved schema можно уменьшить набор, но нужны новый ballot и cross-schema mapping. SourcePlan/Policy имеют explicit applicability, unknown не FALSE. Ни один field не deferred; deferred именно provider/backend implementation, не типизированные факты.

| Field | Identity | Attribution | Reconcile | Serialize | Minimal | Authority |
|---|---|---|---|---|---|---|
|SchemaVersion|yes|False|False|yes|yes|Versioned approved schema registry|
|Broker|yes|True|False|yes|yes|Independent namespace binding/account currency+precision policy|
|Server|yes|True|False|yes|yes|Independent namespace binding/account currency+precision policy|
|AccountLogin|yes|True|False|yes|yes|Independent namespace binding/account currency+precision policy|
|Symbol|yes|True|False|yes|yes|Broker history DEAL_* observation (scope BUY/SELL only)|
|Magic|yes|True|False|yes|yes|Broker history DEAL_* observation (scope BUY/SELL only)|
|CycleID|yes|True|False|yes|yes|Independent EA-origin association journal|
|DealTicket|yes|True|True|yes|yes|Broker history DEAL_* observation (scope BUY/SELL only)|
|OrderTicket|yes|False|True|yes|yes|Broker history DEAL_* observation (scope BUY/SELL only)|
|PositionIdentifier|yes|False|True|yes|yes|Broker history DEAL_* observation (scope BUY/SELL only)|
|ActionID|yes|True|False|yes|yes|Independent EA-origin association journal|
|EventID|yes|True|False|yes|yes|Independent EA-origin association journal|
|Role|yes|True|False|yes|yes|Independent EA-origin association journal|
|EntryType|yes|False|True|yes|yes|Broker history DEAL_* observation (scope BUY/SELL only)|
|DealType|yes|False|True|yes|yes|Broker history DEAL_* observation (scope BUY/SELL only)|
|TimestampMsc|yes|False|True|yes|yes|Broker history DEAL_* observation (scope BUY/SELL only)|
|Volume|yes|False|True|yes|yes|Broker history DEAL_* observation (scope BUY/SELL only)|
|Price|yes|False|True|yes|yes|Broker history DEAL_* observation (scope BUY/SELL only)|
|Profit|yes|False|True|yes|yes|Broker history DEAL_* observation (scope BUY/SELL only)|
|Swap|yes|False|True|yes|yes|Broker history DEAL_* observation (scope BUY/SELL only)|
|Commission|yes|False|True|yes|yes|Broker history DEAL_* observation (scope BUY/SELL only)|
|Fee|yes|False|True|yes|yes|Broker history DEAL_* observation (scope BUY/SELL only)|
|DealNet|yes|False|True|yes|yes|Derived captured aggregate: not a broker DEAL_NET field; independent reconciliation boundary|
|Currency|yes|False|True|yes|yes|Independent namespace binding/account currency+precision policy|
|Precision|yes|False|True|yes|yes|Independent namespace binding/account currency+precision policy|
|SourcePlanApplicable|yes|True|False|yes|yes|Independent EA-origin association journal|
|SourcePlan|yes|True|False|yes|yes|Independent EA-origin association journal|
|SourcePolicyApplicable|yes|True|False|yes|yes|Independent EA-origin association journal|
|SourcePolicyVersion|yes|True|False|yes|yes|Independent EA-origin association journal|

Broker history даёт DEAL_TICKET/ORDER/POSITION_ID/SYMBOL/MAGIC/ENTRY/TYPE/TIME_MSC/VOLUME/PRICE/PROFIT/SWAP/COMMISSION/FEE. Не содержит HSBI Cycle/Action/EconomicEvent/Role/SourcePlan/Policy. Эти поля нужны из независимого EA-origin journal. DEAL_MAGIC сам по себе не доказывает association. DealNet — производный captured aggregate, не самостоятельный MQL5 DEAL_NET; его signed-components/posted reconciliation обязательно отдельно и не подменяется equal Net. Currency/precision из independent account/provider policy, не SYMBOL_DIGITS. Broker/server стабильность и receipt authenticity остаются UNPROVEN. Manual magic0/nontrade account events вне attributed BUY/SELL profile, но не исчезают из future global economic ledger.

Публичные identity helpers принимают записи, не ходят в History*/AccountInfo*, не создают origin journal и не признают fixture authority брокерским доказательством. Полнота/подтверждение задаются test fixtures, не реализованы в production.
