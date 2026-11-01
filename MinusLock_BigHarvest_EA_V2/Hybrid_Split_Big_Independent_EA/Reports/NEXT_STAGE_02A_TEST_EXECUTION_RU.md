# HSBI NEXT STAGE 02A — журнал выполнения тестов

## Паспорт

- UTC: `2026-11-01T00:15:25Z`
- mode: local Git checkout plus read-only GitHub remote verification
- baseline: `6bb6a2f75f8fb0d5d51b1259476ddc47477eaaa3`
- Python: `3.12.14`
- MetaEditor/MetaTrader 5/Wine: отсутствуют
- production mutation: не выполнялась

## Свежие результаты

| Проверка | Exit | Статус | Область доказательства |
|---|---:|---|---|
| `verify_hsb_2e_prep_r4_r8.py --root <project>` | 0 | PASS | Python reference R8: 104 historical vectors, price authority, certificate/fill/economic matrices, 30 invariants |
| `verify_hsb_2e_r4_r9_r4a_r10.py` | 0 | PASS | 28 fixtures, 11 lifecycle steps |
| `verify_hsb_2e_r4_r9_r4a_r12_alignment.py` | 0 | PASS | 14 predicate contracts aligned with Python evaluator |
| `accept_hsb_2e_r4_r9_r4a_r12_second_block.py` | 0 | PASS | R10=67, second-block fixtures=15, sensitivity=7/7 |
| `audit_hsb_2e_r4_r9_r4a_r12a_actual_coverage.py` | 0 | PASS | AST/read coverage Python evaluator ownership matrix |
| `check_hsb_2e_r4_r9_r4a_r12a_fix_01.py` | 0 | PASS with blocker | 13 causal cases pass; script reports `SECOND_BLOCK_SOURCE_MUTATIONS=NOT_STARTED`, `SECOND_BLOCK_ACCEPTANCE=NOT_GRANTED` |
| `verify_hsb_2e_r4_r9_r4a_r12a_normative_contract.py` | 0 | LIMITED | Printed SHA-256 of empty ledger; does not read MQL5 money production source |
| `verify_hsb_2d_v1_r7.py --root <project> --skip-seal` | 1 | FAIL | 57/62 current-tree static checks; five failures are stale status/manifest/marker expectations and missing historical artifacts |
| no-trade production scan | 0 | PASS | 74 files; zero `OrderSend`, `CTrade`, `PositionOpen`, `PositionClose`, `TRADE_ACTION_`, `OnTradeTransaction` |

Первый вызов R7/R8 без обязательного `--root` завершился argparse exit 2 и не считается выполнением теста. После диагностики оба запуска повторены с корректным root; R8 прошёл, R7 дал описанный FAIL.

## NOT_RUN

| Проверка | Причина |
|---|---|
| MetaEditor main compile | executable отсутствует |
| MetaEditor MQL5 harness compile | executable отсутствует |
| MQL5 tests | MetaTrader 5 отсутствует |
| Strategy Tester | MetaTrader 5 отсутствует |
| Broker `OrderCalcProfit/OrderCalcMargin` | нет terminal/account/symbol runtime |
| Real deal/ledger/restart | production transaction and persistence pipeline отсутствует |
| Stage-02A production source mutations | production-код нельзя менять; отдельный disposable MQL5 compilation environment отсутствует |

## Интерпретация

PASS reference-тестов доказывает только поведение Python specification и отдельных static contracts. Он не повышает `FULL_ECONOMIC_CORRECTNESS` до PASS и не заменяет MQL5/broker execution. Frozen R7 FAIL не означает торговую регрессию: verifier ожидает исторический sealed set, который не соответствует текущему более позднему дереву.
