# Стратегия MQL5 и MT5 тестирования

Версия 1.0. Статус: нормативный план; тесты не реализованы.

## Unit MQL5

Lot/price rounding; dimensions/signs; broker money; identity/ownership; EventKey/ConsumptionKey; ledger conservation; catch-up; monotonic RecoveryPL; compression/finite sequence; NewFar solver; Final Close double-count guard.

## Integration MQL5

Initial BUY/SELL и rollback; basket staged opening; every retcode; partial/delayed/duplicate fill; Big Harvest and allocations; Partial Far reservation/consumption; Final Close; full Small Transition; restart in every FSM state; reconciliation outcomes and terminal-safe.

## Strategy Tester

Far BUY/Far SELL; trend without pullback; repeated reversals; two and many transitions; gaps; spread expansion; commission/swap/slippage; low margin; min/coarse lot step; multiple symbols; same Magic different symbols; disconnect/restart fixtures; altered/manual positions.

## Evidence

MetaEditor report 0 errors/0 warnings; tester HTML/XML, Experts/Journal, orders/deals/positions, snapshots, action/event/economic/allocation ledgers, reason traces and checksums.

- `HSBI-TEST-001`: compile PASS требует фактический MetaEditor artifact.
- `HSBI-TEST-002`: Strategy Tester PASS требует reproducible set/data/report.
- `HSBI-TEST-003`: Python PASS не заменяет MQL5/MT5 evidence.
- `HSBI-TEST-004`: Base и Worst Case тестируются независимо.
- `HSBI-TEST-005`: mutation tests должны ловить ownership, double-count, early FSM advance и second-Far defects.
- `HSBI-TEST-006`: restart matrix охватывает каждую pending phase.

Контракт: вход — implemented mapped requirements; выход — signed evidence index. Preconditions: deterministic build info. Postconditions: traceability matrix updated. Error route: missing evidence=UNPROVEN. Owner: Tests/* and Reports. Открытые вопросы: symbols/timeframes/history windows и demo duration.