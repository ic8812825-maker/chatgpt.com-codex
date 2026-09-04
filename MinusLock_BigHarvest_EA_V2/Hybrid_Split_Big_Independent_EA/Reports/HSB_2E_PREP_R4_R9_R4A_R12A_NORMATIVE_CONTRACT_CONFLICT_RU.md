# NORMATIVE_CONTRACT_CONFLICT — R12A

## Статус

`R12A=BLOCKED_ON_NORMATIVE_CONTRACT_CONFLICT`.

Работа остановлена до реализации source-mutation suite predicates 8–14, потому что действующий Registry/Contract не задаёт каноническое представление authoritative ledger и допустимую semantics batch/fill. Следовательно, нельзя независимо реализовать требуемую проверку `PERSISTED_LEDGER_REVALIDATION` без молчаливого изобретения экономической/ledger-политики.

## Локализация

| Predicate | File/path | Registry expectation | Contract/evaluator actual | Conflict |
|---|---|---|---|---|
| `PERSISTED_LEDGER_REVALIDATION` | `HSB_2E_R4_R9_R4A_R12_PREDICATE_REGISTRY.json`, `exactInputPaths` | `consumedDealIds`, `authoritativeLedgerRoot` | R12 evaluator проверяет только уникальность IDs, форму root и subset в REPLAY | Нет формулы `canonicalLedger → authoritativeLedgerRoot`; 64-hex string не даёт независимой revalidation. |
| `BATCH_ATOMICITY` | тот же Registry, `scenarioInput.deals[*]` | batch atomicity | R12 evaluator сравнивает set intentId и set deal intentId, PRE_COMMIT возвращает PASS | Не определены batch identity, commit/rollback/partial semantics и applicability PRE_COMMIT. |
| `PER_TICKET_FILL` | Registry requestedVolume/deal.volume | per-ticket fill | R12 evaluator допускает любой cumulative fill `<= requestedVolume` | Не определено, допускается ли partial fill и когда требуется exact settlement. |

## Воспроизводимое наблюдение

В committed positive fixture `consumedDealIds=[]`, но `authoritativeLedgerRoot` непустой 64-hex. SHA-256 от единственного очевидного candidate — canonical sorted consumed IDs — не совпадает с опубликованным root. Поэтому этот candidate не может быть принят как нормативная формула без административного решения.

## Запрошенное административное решение

Нужны явные нормативные ответы:

1. canonical ledger body, ordering и serialization для `authoritativeLedgerRoot`;
2. rules inclusion actual deals, consumed IDs, deal-event bindings и accumulated history;
3. applicability `BATCH_ATOMICITY` по фазам PRE_COMMIT/COMMITTED/REPLAY и допустимость partial/rollback;
4. per-ticket fill policy: partial, exact settlement, multiple fills, grid/tolerance.

До ответа запрещено объявлять `ACTUAL_EVALUATOR_COVERAGE=PASS`, `SECOND_BLOCK_SOURCE_MUTATIONS=ALL_CAUGHT` или полноценный PASS R12A.

## Сохранённые ограничения

```text
QUALIFICATION_CORE_READY=NO
ORACLE_V3_FINAL_ACCEPTANCE=NOT_GRANTED
FULL_ECONOMIC_CORRECTNESS=NOT_PROVEN
LIFECYCLE_EXECUTED_BY_NATIVE_MODEL=NO
MODEL_CHANGES_ALLOWED=NO
TRADING_LOGIC_START_ALLOWED=NO
TRADE_REQUESTS_ALLOWED=NO
REAL_TRADING_ALLOWED=NO
METAEDITOR=NOT_RUN
MT5=NOT_RUN
```
