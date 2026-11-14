# R1.1 — независимые expected / результаты / обязательства

BASE_SHA=`398da88424f3fb7b30e5315fbc3bf89219dd9ad2`. Все новые acceptance требования PROPOSED. Literal expected в `Tests/Close/test_reference.py` и `production_subset.cpp`; subject не вычисляет expected. Точный input C++ воспроизводится harness source; Python — фиксированные record и параметры. Хэши subject/harness/results сохранены рядом.

| ID | Независимый input / ожидаемый результат | Выполненный scope | Остаточное обязательство |
|---|---|---|---|
| P0-01 | P60,C−10 против P50,C0, Net50, same key → CONFLICT | C++ FAIL; Python PASS | все поля, provider receipt и native |
| P0-02 | Rsv50/PF0 против Rsv0/PF50, total50 → CONFLICT | C++ FAIL; Python PASS | полный vector/schema и native |
| P0-03 | Grant50, Consumed50, Free0, новый debit.01 → REJECT | Python PASS; C++ PROPOSED exhausted case FAIL | production lifecycle semantics, source registry |
| P0-04 | fresh risk с NaN worstCaseLoss → REJECT | C++ FAIL; Python PASS | все inputs И limits отдельно в native |
| P0-05 | finalReserve=+Infinity → REJECT | C++ FAIL; Python PASS | все money fields/intermediate overflow |
| P0-06 | lot.005,min.01,step.01 → REJECT | Python PASS | actual BrokerGrid/native |
| P0-07 | partial.5/request1 unconfirmed → REJECT; NaN accumulated → REJECT | Python PASS; C++ NaN FAIL | actual deals completeness, delayed complete |
| P0-08 | same event amount5000→4999 → CONFLICT | Python PASS (receipt simulation) | actual journal altered body со старым digest, native NOT_RUN |
| P0-09 | state revision0 при expected1 → REJECT | C++ PASS; Python PASS | stale request при available funds; atomic CAS |
| P0-10 | UNKNOWN prior execution → BLOCK/RECONCILE, no redispatch | C++ retry predicate FAIL; Python PASS | actual unknown broker outcome, mandatory caller |
| P0-11 | Far в far и candidate слотах → REJECT | Python topology PASS; current Context static partial | all slots actual/native; duplicate physical identifier |
| P0-12 | Reserve без independent source → REJECT/UNAVAILABLE, no permit | Python UNAVAILABLE PASS | actual source proof, allocation key, receipt provider |
| P0-13 | applied event после trusted restore → NO_OP, consumed не увеличивается | Python PASS; historical DG01 PASS | durable restart, crash point, actual journal reconstruction |
| P0-14 | Harvest50, open−60, remaining1 → CyclePnL−11, NO FINAL CLOSE | Python PASS | full FinalClose coverage/risk/actual-zero conjunction |

## Дополнительные независимые сценарии

| Scenario | Literal expected | Текущий scope |
|---|---|---|
| BUY/SELL symmetry | local coefficient1, price move+2/−2 с зеркальным sign → 2/2 | Python algebra PASS; asymmetric broker money NOT_RUN |
| Optional Trend0 | C3+T0−S1−F1=1 | Python algebra PASS; actual GeometrySolver pending |
| Price grid |100.03 с tick.05 off-grid → REJECT | Python Decimal PASS |
| Volume grid |.015 при step.01 → REJECT; max1 разрешён | Python Decimal PASS |
| Currency precision |1.005→100 cents,1.015→102 HALF_EVEN;1.2345→1234 mills | PROPOSED posting fixture PASS; broker rounding not approved |
| Negative zero |−0.0 →0 financial units | model PASS; raw codec still owner pending |
| Component signs |6000−100−200−50=5650 | Python signed accounting PASS |
| Gap | realized5000,open−7000,remaining100 → no close | model PASS, market provider pending |
| Spread expansion | realized5000,open−4500,remaining600 → no close | model PASS, disjoint basis pending |
| Margin shortage |positive accounting but risk_ok=false → no close | model PASS; real margin provider pending |
| Adverse trend |realized5000,open−20000,remaining100 → no close | model PASS; no loss/time bound implied |
| Competing consumers |free5000,r1; A4000 applies→free1000,r2; B same old r1 rejects, zero delta | serialized model PASS; true concurrency NOT_RUN |
| Snapshot mismatch |positive PnL, stale positions → no close | model PASS; content receipt provider pending |
| Invalid enum |direction99 → REJECT | Python PASS; C++ economic enum FAIL |
| Altered replay |same event/body changed → CONFLICT | Python PASS; durable journal pending |
| New allocation event |source already funded, event99 → CONFLICT | Python PASS; actual source registry pending |
| Public Reserve scalar |source proof1000,eligible10000 → REJECT | model PASS; production static gap ERR-048 |
| Public Far scalar |Far proof−5000,loss0 → REJECT | model PASS; production static gap ERR-048 |
| Exhausted Reserve |eligible5000,available0 → REJECT | model PASS; provider state pending |
| Projected money |projected gain5000,available0 → PREVIEW_ONLY, no funding | model PASS; production type separation pending |
| Worst level |catchup margins9/−11, transition10/5 → all-level REJECT | algebra PASS; production semantics CR-09 pending |
| Distinct account/server/deal |не один physical source | abstract tuple PASS; wire codec unresolved |
| Equal volume, changed price/position/role |same source changed immutable body → CONFLICT | C++ price PASS; role/position FAIL; Python PASS |
| Nonfinite limits |NaN/Infinity limits → REJECT | C++ NaN FAIL; model PASS |
| Overflow |1e100 minor conversion → REJECT | Decimal fixture PASS; native intermediates pending |

## Интерпретация результатов

- `reference_results.json`: 63 PASS / 0 FAIL, **новая test-only модель**.
- `production_subset_results.json`: 7 PASS / 16 FAIL, 23 checks **неизменённых MQL headers через C++17 shim**. Exit1 сохранён; это не MetaEditor/native execution. Два ожидания explicitly PROPOSED: committed underallocation и exhausted-source representation.
- `historical_TEST_RESULTS.json`: DG01 runner 62 reference PASS / 0 FAIL + 3 formatting PASS, новые результаты перенаправлены, старые evidence не тронуты. Эти числа не складываются с новой моделью как независимые production guards.
- `mutation_initial_results.json`: первый прогон 4 killed / 4 survived. Недостающие causal tests добавлены, старые expected не изменены.
- `mutation_results.json`: 8 реальных source mutations proposed Python model killed / 0 survived. Guard-free mutant запускает ту же suite в временном test-only каталоге. Не все guards проекта мутированы; полнота не заявляется.
- `patch_initial_checks.json`: два первоначально некорректных diff из-за отсутствующего newline; исправлен generator. `patch_checks.json`: все пять `git apply --check` PASS; patches **не применялись**. Это проверка синтаксиса diff, не correctness/native compile.

## Воспроизведение

Из корня репозитория:

```bash
PYTHONDONTWRITEBYTECODE=1 python MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Tests/Close/test_reference.py
PYTHONDONTWRITEBYTECODE=1 python MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Tests/Close/run_mutations.py
PYTHONDONTWRITEBYTECODE=1 python MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Tests/Close/run_historical.py
python MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Tests/Close/run_production_subset.py
```

Последняя команда ожидаемо возвращает1 из-за сохранённых FAIL; CI не должен объявлять её зелёной. Re-run меняет только новые close evidence, не frozen historical records. Для новых sealed runs сохранять отдельный новый evidence каталог. Windows/native: `Tests/Close/NATIVE_WINDOWS_RU.md` и `native_close.mq5`.

MQL5_COMPILE=NOT_RUN; MQL5_NATIVE_TESTS=NOT_RUN; NATIVE_VERIFIED=NO. Broker authority, actual execution, crash durability, concurrent consumers backend и full FSM native acceptance NOT_RUN. Любой model PASS ограничен указанным fixture scope.
