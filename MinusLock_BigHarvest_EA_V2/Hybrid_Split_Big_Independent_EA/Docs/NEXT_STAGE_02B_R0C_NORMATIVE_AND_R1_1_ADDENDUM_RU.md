# 02B-R0C — дополнение к нормативному пакету и будущему R1.1

База `8903f7ba5d376dc642024ac8ab4400b884466c55`. Только новые test-only artifacts. Старый `NEXT_STAGE_02B_R1_1_IMPLEMENTATION_SPEC_RU.md` не изменён. Этот документ не утверждает D-01–D-08, CR-09 и не разрешает production.

| Уточнение | Характер | Решение администратора | Влияние на будущий R1.1 |
|---|---|---|---|
| R0C-ID: strict type/range, bool не ID, revision exhaustion | Уточнение D-07/D-08 и новая явная граничная семантика | AWAITING | Поля account/IDs/Magic и negative/mutation tests; не запускать R1.1 сейчас |
| R0C-SHAPE: Malformed→REJECT, missing fact→UNAVAILABLE, programmer error visible | Явное разделение прежней неоднозначной ошибки входа | AWAITING | Required immutable payload shape, без broad catch или silent defaults |
| R0C-SNAPSHOT: ID + независимый content receipt | Новое явное test fixture требование, уточняет D-08 | AWAITING | R1.1 хранит immutable source reference; trusted provider/current proof pipeline остаются последующими фазами |
| R0C-TIME: zero-skew fixture clock и inclusive endpoint | Новый тестовый профиль, не broker policy | AWAITING | Сохранять raw time/clock domain; не выводить UTC/freshness authority из числа |
| R0C-DECIMAL: adjusted<=64/exp[-64,64], context256 | Технический test-only domain, не экономический лимит счёта | AWAITING | Не переносить в MQL5 денежный DTO без отдельного выбора codec/domain |
| R0C-MONEY: causal digest/signed sum/posted-state/origin tests | Проверяемость существовавших требований D-01/D-08 | AWAITING; экономику не меняет | Independent expected tests; source raw64 не заменяет posted reconciliation |
| R0C-REPLAY/APPLY: current gates после known receipt, zero deltas | Уточнение D-07 | AWAITING | Economic duplicate NO_OP не повышает source до AVAILABLE; durable consumption не входит в R1.1 |
| R0C-CR09: ALL_LEVEL_POSITIVE / SINGLE_LEVEL_POSITIVE | Явное типизированное различие scope CR-09 | AWAITING | NewFar/geometry/FutureSmall production запрещены для R1.1; здесь не реализуются |

Четыре дополнительные мутации и authority-side snapshot counterexample показывают, что прежний R0B COMPLETE нельзя использовать как закрытие обязательного oracle-контракта. Исходные141/30 результаты достоверны для своих каталогов; новый review не переписывает их. После R0C принятие test-only пакета возможно только в его ограниченном домене.

Перед отдельным заданием R1.1 нужны явные утверждения D-01–D-08/CR-09 и применимых R0C clauses с версиями/идентификаторами. Предыдущий allowlist EconomicLedger/Namespace/CanonicalCodec автоматически не расширяется. Snapshot provider, consumption protocol, NewFar, Big/Small geometry, dispatch и persistent backend остаются вне R1.1.

Не переносить Python Decimal/JSON representation напрямую в MQL5 raw source codec. Пять raw64 vectors прежнего этапа не доказывают NFC/full codec correctness. Migration по-прежнему append-only, unknown namespace/schema/provenance =>UNAVAILABLE; не подставлять текущий AccountLogin в старую запись. Ни duplicate equality, ни fixture eligibility не подтверждают broker history.

Откат текущего этапа — отдельный reviewed revert собственного test-only commit при необходимости, без изменения денежных данных и без компенсирующих сделок. До нового baseline, approval и отдельного задания R1.1 не начинать.

Связанные источники: `Docs/NEXT_STAGE_02B_R0B_CONTRACT_FREEZE_PROPOSAL_RU.md` (D-01/D-07/D-08/CR-09), `Docs/NEXT_STAGE_02B_R1_1_IMPLEMENTATION_SPEC_RU.md` (§§3–14), `Docs/NEXT_STAGE_02B_R0C_ORACLE_CONTRACT_RU.md` (точные R0C ContractID). Исполнимые доказательства — verification matrix и R0C evidence.
