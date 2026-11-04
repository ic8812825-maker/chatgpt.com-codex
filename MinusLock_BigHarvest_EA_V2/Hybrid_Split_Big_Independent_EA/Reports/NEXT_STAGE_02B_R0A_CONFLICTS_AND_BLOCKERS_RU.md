# 02B-R0A — противоречия и оставшиеся блокировки

База `cb5e55cb38aa4f2eb5b58e5218462c6738f3097a`. Адресные доказательства R0 подтверждены без production remediation. Полные точные тексты: [кандидат](../Docs/NEXT_STAGE_02B_R0A_CONTRACT_FREEZE_CANDIDATE_RU.md), утверждение: [лист администратора](NEXT_STAGE_02B_R0A_ADMIN_APPROVAL_SHEET_RU.md).

## Подтверждённое в ограниченной области

- M-01: local Catch-Up допускает foreign source/allocation keys; amount/owner/event binding DTO неполон. Spent source при не-allocated ветке тоже может пройти. End-to-end реальный double spend не заявляется.
- M-02: точная assembly expected копирует submitted identity; independent expected tests отклоняют те же foreign fields. Полная NewFar selection NOT_RUN.
- L-01: changed Profit/Commission при том же Net/volume/price/key даёт NO_OP; record/key не содержат AccountLogin/server namespace.
- L-02: Reserve50/Partial0→Reserve0/Partial50 при той же сумме даёт NO_OP. PolicyVersion отсутствует в этом DTO.
- M-05: aggregate Small10 даёт metric10, но это не доказательство разрешённого actual Small→Reserve spend.
- ZERO-CORE: raw.001→Core0 при slope.19 locally valid. Не исправлено; отдельная geometry зависимость.
- CR-09: max TransitionLoss не тождествен min money margin; действующий критерий all-level не определён однозначно, поэтому DECISION_REQUIRED.
- Ограничение R0 oracle: PlanID/Revision999 не проверяются oracle_consumption; новый нормативный тест документирует ALLOW при ожидаемом REJECT, старый runner/evidence не менялись.

## Реестр решений и конфликтов

**D-01:** Docs/04,08 требуют equality; Docs/32 допускает <= и складывает consumed с неуточнёнными grants. Безопасный вариант: Полные immutable grants; отдельные balances; промежуточный Unallocated недоступен. Статус: AWAITING_ADMIN_APPROVAL. Источники: Docs/04:Allocation conservation; Docs/08:Allocation Ledger; Docs/32; CR-01/04/07/08.

**D-02:** Общее recoveryMoney может смешивать прогноз и доступный ресурс. Безопасный вариант: Раздельные DTO, без неявного projected→actual/available. Статус: AWAITING_ADMIN_APPROVAL. Источники: Docs/04:RecoveryPL; Docs/24; Docs/27; Docs/31; CR-02/05/10.

**D-03:** Aggregate Core+Trend+Small ошибочно выглядит разрешённым Big Reserve. Безопасный вариант: Small positive net — ResidualHeld, не BigReserve; Core/Trend только confirmed eligible источники. Статус: AWAITING_ADMIN_APPROVAL. Источники: Docs/08:Isolation; Docs/31; CR-10; M05-small-only.

**D-04:** Название increase не определяет baseline и может ослаблять gate. Безопасный вариант: Хранить оба, для рекомендуемого рабочего gate выбрать ABSOLUTE; incremental — diagnostic до отдельного разрешения. Статус: AWAITING_ADMIN_APPROVAL. Источники: Docs/04:Reserve Catch-Up; Docs/24; Docs/31; D-04 предыдущего пакета.

**D-05:** Одна семантическая область для плановой оценки и фактического accounting. Безопасный вариант: Раздельные типы и обязательная post-fill reconciliation. Статус: AWAITING_ADMIN_APPROVAL. Источники: Docs/04:Transition Loss; Docs/08; Docs/27; R12A per-ticket fill/batch atomicity.

**D-06:** Не определено пересечение per-leg и Catch-Up deductions. Безопасный вариант: Charge-once по документированным riskBasis/window, отдельные независимые risk budgets; unresolved overlap блокирует proof. Статус: AWAITING_ADMIN_APPROVAL. Источники: Docs/24; Docs/04:Reserve Catch-Up; Include/Money/HSBI_CostModel.mqh:18; D-06 предыдущего пакета.

**D-07:** Bool prior и key без amount не доказывают exactly-once. Безопасный вариант: Typed outcomes; eligibility отдельно от commit, durable registry как prerequisite. Статус: AWAITING_ADMIN_APPROVAL. Источники: Docs/08:Keys/exactly-once; Docs/16; Docs/32; R10 replay binding.

**D-08:** Флаги и self-copy expected не подтверждают existence/provenance. Безопасный вариант: История брокера плюс durable журнал и независимая reconciliation; fixture только для тестов. Статус: AWAITING_ADMIN_APPROVAL. Источники: Docs/08; Docs/16; Docs/31; Docs/32; R10 proofBoundary; R12A scope boundary.

**CR-09:** Maximum TransitionLoss не обязан совпадать с minimum Catch-Up margin. Безопасный вариант: A; B допустим только явно ограниченным альтернативным решением. Статус: AWAITING_ADMIN_APPROVAL. Источники: Docs/30; Docs/27; Include/Planning/HSBI_FutureSmallProofAggregator.mqh:50; CR-09 предыдущего пакета.


## UNPROVEN / NOT_RUN

| Область | Статус | Что необходимо для закрытия |
|---|---|---|
| Confirmed broker history и role/plan reconciliation | NOT_RUN / UNPROVEN | read-only provider в целевом account namespace; fixture не заменяет terminal |
| Durable consumption registry/CAS/commit/restart | UNPROVEN | approved backend и crash/concurrency injection; in-memory модель не является IO |
| Полная NewFar integration и обязательность всех authority callers | UNPROVEN / NOT_RUN | отдельный integration этап; локальные validators не доказывают невозможность обхода |
| MQL5 main/harness compile и tests | NOT_RUN | MetaEditor/MT5 отсутствуют; template компилируемость не заявляется |
| Strategy Tester и broker money/margin modes | NOT_RUN | безопасная terminal environment и реальные logs; без dispatch |
| Currency/precision posting и cost overlap | DECISION_REQUIRED / NOT_RUN | D-01/D-06 утверждение и broker validation; decimal fixture не доказывает currency conversion |
| WORST_CASE all-level future funding | UNPROVEN | proof каждого required уровня и cumulative balance evolution; не отфильтровывать отрицательные/missing уровни |
| Экономическая конечность recovery | UNPROVEN | feasible execution path; slope/positive local margin недостаточны |

## Независимость новых проверок

128 новых checks — executable tests предложенных правил. Decimal math использует USD/2-digit профиль и unit-price linear инструмент для иллюстрации Bid/Ask; не вызывает broker APIs. Authority/complete/fresh в этих тестах являются предпосылками независимо заданных fixtures, а не реальными broker-confirmation flags. In-memory state evolution показывает арифметическую идемпотентность, но не durable exactly-once. Source-sensitive guard проверяет извлечённый unchanged runtime policy; MQL5 runtime NOT_RUN.

## Вопросы администратора

1. Утвердить D-01 full committed grants, отдельный Unallocated/ResidualHeld и precision policy либо точную альтернативу, включая совместимость broker posting.
2. Утвердить D-02 DTO/conversion boundaries и разделение projected planning / actual resource authorization.
3. Утвердить D-03 Small→ResidualHeld либо иной явно описанный bucket без потери и повторного учёта.
4. Выбрать D-04 immutable working loss metric; рекомендация ABSOLUTE, incremental diagnostic.
5. Утвердить D-05 actual partial/completed/over-cap accounting outcomes без торговых переходов.
6. Утвердить D-06 coverage map, risk independence/overlap handling и неизменность buffers до реализации.
7. Утвердить D-07 typed NO_OP/CONFLICT/ELIGIBLE_FOR_COMMIT и durable prerequisites.
8. Утвердить D-08 account namespace, authoritative providers, role mapping/canonicalization/migration.
9. Выбрать CR-09 A (рекомендуется) либо B с явным SINGLE_LEVEL_ONLY; определить scope и version.
10. Отдельно разрешить фазу R1 и её allowlist после решений; geometry/durable/selector/runtime не входят автоматически.

До этих решений R1 запрещён. Готовность пакета к рассмотрению не означает утверждённую модель, readiness EA или торговое разрешение.
