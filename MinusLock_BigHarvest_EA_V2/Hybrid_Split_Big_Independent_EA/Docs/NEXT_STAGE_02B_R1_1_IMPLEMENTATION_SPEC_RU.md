# 02B-R1.1 — спецификация ограниченного Economic Ledger этапа

Статус документа READY_FOR_REVIEW, не допуск реализации. База подготовки: `9b43c38afdb89c6b3b514b654c7fb9a936f9bf2b`. `STAGE_02B_R1_IMPLEMENTATION_ALLOWED=NO`. Никакой production-файл этим документом сейчас не разрешён к изменению. Нужны явное нормативное утверждение администратора и отдельное задание R1.1 с новым проверенным baseline.

## 1. Точный предполагаемый allowlist после approval

- `Include/Money/HSBI_EconomicLedgerTypes.mqh` — Economic DTO, source key, shape validation, immutable equality/duplicate/serialization.
- Новый `Include/Money/HSBI_EconomicSourceNamespace.mqh` — typed namespace helpers только для Economic Record.
- Новый `Include/Money/HSBI_EconomicCanonicalCodec.mqh` — approved versioned codec, finite/bounds checks; никаких money credits.
- Новые scoped tests/fixtures/evidence в `Tests/`, новые R1.1 отчёты. Точные test filenames фиксируются отдельным заданием. Нельзя менять старые tests/evidence ради зелёного результата.

## 2. Запрещённые файлы и поведение

Все остальные production-файлы, включая весь `Include/Planning/`, `Include/Execution/`, `Include/Runtime/`, `Include/Persistence/`, Allocation/Reserve/CatchUp/Big/Small money functions и главный `.mq5`. Не менять NewFar assembly/solver, geometry, formulas, dispatch или OnTradeTransaction. Никаких реальных/демо ордеров, automatic close/hedge, auto-resume или production migration IO. Разрешение R1.1 не включает R1.2–R1.5.

## 3. Нормативные зависимости

Администратор явно фиксирует D-01–D-08 и CR-09 либо отдельное письменное scoped deferral, не придуманное исполнителем. Для R1.1 особенно обязательны D-01 precision/source accounting, D-02 raw/actual distinction, D-07 duplicate outcomes, D-08 namespace/codec/identity/migration. Выбранные версии текста, codec и precision modes записываются в задании. При любой неоднозначности STOP, не выбирать более удобный вариант. Все поля approval сейчас пусты.

## 4. Предлагаемая структура Economic Record

SchemaVersion и CanonicalizationVersion; BrokerIdentity, ServerIdentity, AccountLogin; Symbol, Magic; SourceCycleID, SourcePlanID, SourceActionID, SourceEventID; DealTicket, OrderTicket, PositionIdentifier; Role, Direction, EntryType; raw Volume/Price/Profit/Swap/Commission/Fee/DeclaredNet и исходные timestamp/clock domain; AccountCurrency/CurrencyDigits/PrecisionPolicyVersion; SourceSnapshotID/ReceiptReference; ReconciliationState и payload digest.

AccountLogin — positive signed long; Deal/Order/Position/Event/Plan/Action/Cycle IDs — bounded positive ulong; Magic — configured signed long, nonzero, без bool/string coercion. Broker/Server не выводятся из Symbol/Magic. Для trade-record сохраняется действующий Volume>0 и требуется finite raw Volume/Price/components; instrument-specific price/grid validation принадлежит независимому provider, неизвестный domain не угадывается. Source timestamp/clock domain сохраняются с исходной точностью, UTC conversion не выдумывается. Source origin fields неизменны; current consumption plan/revision/snapshot принадлежат отдельному DTO будущего этапа.

R1.1 не реализует trusted history provider: допускается только OBSERVED_RAW/UNAVAILABLE reconciliation state. Shape validity и canonical integrity не означают подтверждённый денежный источник. `actual=true` либо `valid=true` не переводят record в AvailableReserve. Opening commissions/fees сохраняются в economic accounting; opening entry не становится harvest source.

## 5. Immutable identity и payload

В equality входят все economic origin identifiers, namespace, role/direction/entry, volume/price, каждый signed component, net, source time/clock domain, source snapshot/schema/currency/precision и approved provenance reference. Mutable diagnostics/reconciliation-processing flags не заменяют identity и не должны приводить к silent payload replacement.

Один SourceDealKey может иметь только один immutable payload. Изменение любой компоненты при той же общей Net — CONFLICT. Broker correction оформляется отдельным versioned reconciliation/correction record по утверждённой процедуре, не переписыванием old exact duplicate.

ReceiptReference разделяется: immutable OriginHistoryObservationReference относится к исходным фактам; последующий ReconciliationReceipt — отдельный append-only envelope, привязанный к immutable record digest. Его появление не переписывает raw source payload. Mutable ReconciliationState/processing metadata не входят в EconomicSourceIdentity; downstream authority проверяет и record digest, и новый receipt отдельно.

## 6. Duplicate classification

- Другой source key — NEW, после полной shape/namespace проверки.
- Тот же source key и exact canonical immutable payload — NO_OP, zero money/state/revision/action changes.
- Тот же source key и иной immutable payload — CONFLICT, no mutation, reconciliation required.
- Неизвестная schema/codec/namespace — UNAVAILABLE, не NO_OP и не arbitrary fallback.

Нельзя использовать MathAbs(NetA-NetB)<epsilon как доказательство полной идентичности. Сравнение только Net/price/volume запрещено. DealID>0 не доказывает existence; local duplicate classifier не является authority lookup.

## 7. Account namespace

SourceDealKey — canonical typed `(SchemaVersion,BrokerIdentity,ServerIdentity,AccountLogin,DealTicket)` с однозначным encoding. Symbol/Magic/Cycle — связанные immutable поля, но их изменение не создаёт второй разрешённый источник для того же deal. Два accounts/servers с Deal11 различаются. Не использовать неэкранированный `|` concat как универсальный codec.

## 8. Currency, precision и codec

Приоритетная рекомендуемая precision policy — independently confirmed broker-posted amounts/posted components. HALF_EVEN допускается лишь как отдельно approved local mode после verification. Неизвестные CurrencyDigits, receipt/policy или mismatch =>UNAVAILABLE. Нет implicit currency conversion и automatic rounding historical source.

Предложение отдельного codec `HSBI-ECON-RAW64-1`: canonical UTF-8 JSON с фиксированной схемой и sorted unique keys; identity strings NFC по явно проверенному codec; integer IDs — typed base-10 strings; raw finite binary64 source values — 16 hex big-endian с нормализацией -0 в +0. NaN/Infinity/overflow reject. Posted minor-unit integers с currency/digits/receipt хранятся отдельно. Raw64 не является финансовым rounding и не конвертируется напрямую в доступные деньги.

Five Python raw64 golden vectors (0,-0,1,-5,.1) проверены в R0B; MQL5 codec и NFC adapter не реализованы/не скомпилированы. Выбор этого codec вместо прежних decimal proposals требует approval D-08. Не переинтерпретировать R10/R12A historical roots под новой версией.

Raw components сохраняются точно как наблюдённый источник. DeclaredNet — предъявленное finite поле, не автоматически verified ActualDealNetRaw. Независимое signed-sum/posted reconciliation и trusted provider — последующие этапы. До них economic record не разрешает allocation/consumption, даже если shape validation прошла. Реализация не должна скрыть эту недоступность tolerance/DoubleToString(8).

## 9. Negative tests

Foreign Broker/Server/Account/Symbol/Magic/Deal/Order/Position/Cycle/SourcePlan/Action/Event/Snapshot; нулевые/unknown/overflow IDs и bool coercion; missing namespace; NaN/Infinity; source raw components mismatch при Net50; разные Fee/Swap; altered volume/price/time/role/direction/entry; unknown schema/codec; currency/digits mismatch; broker-posted/local mismatch; corrupted digest; duplicate with changed payload; unknown source after migration. Положительный полный valid-shape/control record обязателен для каждой группы. Никакого faux actual-source approval без provider.

## 10. Mutation tests

В isolated test copies production target после отдельного допуска: убрать account namespace; сравнивать только total Net; игнорировать Profit/Swap/Commission/Fee по отдельности; стереть Order/Position/Role/Direction/Plan/Event/time; ослабить schema/codec/precision/finite checks; подменить payload digest self-copy; разрешить неизвестный legacy namespace. Каждую mutation ловит нужный причинный vector, а не parser error или иной не связанный guard. Все initial survivors сохраняются в evidence, затем расширяется coverage. R0B mutations Python reference не заменяют эту будущую MQL5 source проверку.

## 11. Миграция

Не изменять исторические записи. Читать legacy schema как legacy; сохранять исходные bytes/hash и schema. Нужны independent storage ownership и broker history receipts, связывающие старую запись с account/server и всем payload. Просто подставить текущий ACCOUNT_LOGIN или найти похожий Deal11 недостаточно: такие tickets могут совпасть у разных accounts.

Если происхождение неоднозначно/неполно — UNAVAILABLE/manual reconciliation, no funding. Approved migration создаёт новую append-only versioned запись с ссылкой на legacy hash и migration receipt; не переписывает old key/evidence. Persistent backend не реализовывать в R1.1; проверять только fixtures/read-only migration contract.

## 12. Откат

Остановить зависимых consumers, сохранить snapshots/evidence read-only. Только отдельным reviewed git revert собственного phase commit по решению администратора; без reset/rebase/force/amend. Нельзя запускать старую schema поверх новых records без approved reverse migration; unknown schema fail-closed. Не создавать compensating trades. R1.1 не выполняет persistent migration/dispatch, поэтому rollback не должен иметь денежных side effects.

## 13. Критерии остановки

Baseline/remote/worktree mismatch; неоднозначный approval или raw/posted semantics; файл вне allowlist; unexpected production diff; недоступный codec либо отсутствующий namespace/provider; невозможность доказать source; mutation survivor/infrastructure error; неожиданная regression. Не угадывать currency, origin или amount. При unavailable MetaEditor записать NOT_RUN, не объявлять native readiness.

## 14. Критерии завершения

Только approved scope; fresh independent exact/changed duplicate tests и source mutations; schema/namespace/codec golden vectors; изменения source действительно обнаруживаются hash и behavior; known legacy effects классифицированы. MetaEditor main/harness и MQL5 assertions требуют реального инструмента; иначе native acceptance остаётся BLOCKED/NOT_RUN.

Frozen R0/R0A source-extraction anchors могут стать несовместимы при согласованном DTO change: нельзя переписать их history или скрыть infrastructure error как PASS. Нужен новый versioned scoped harness с новыми schema inputs. Остальные M-01/M-02/L-02/zero-Core defects остаются открытыми. Один атомарный commit R1.1 после separate review; не объединять с другими production фазами.

## 15. Неизменяемый запрет dispatch

Ни duplicate PASS/NO_OP, ни raw record shape validity не разрешают trading. BrokerDispatchAllowed=false, real trading=false, OnTradeTransaction trading не реализуется. Этот документ — specification для будущего задания, а не исполнение R1.1.
