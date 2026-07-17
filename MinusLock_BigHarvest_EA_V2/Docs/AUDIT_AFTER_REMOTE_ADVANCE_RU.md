# Аудит после продвижения origin/work

Исходная точка аудита: `ef2d427bfd8783fa454ffbc3e5b8ec3d06441b7e`. Проверенный HEAD: `07b05714161e9d4979e2da42967ed62841c3ff13`.

## Десять опубликованных коммитов

| SHA | Подпись | Файлы | Закрываемый пункт | Реализация и найденные ошибки | Тесты | Статус |
|---|---|---|---|---|---|---|
| `ebf0a68498740cb92dbb78f78eacfb6ffaf78e07` | Добавлены замечания по завершению денежной модели Big Small | журнал замечаний | REM-039—047 | Дефекты зарегистрированы, исправлений нет. | Нет | PARTIAL |
| `f97fce18b8bfed3007979f58add812b10d0df4b9` | Исправлены signed swap календарь и раздельные комиссии | `BrokerMoneyModel.mqh` | signed/triple swap, commission | Знак сохранён, rollover разбит по дням, open/close API разделён. Ошибки: worst-case cost вычислен, но не включён отдельно; календарь не имеет детерминированного pure-helper для MQL5 тестов. | Только Python-модель | PARTIAL |
| `31d782fa3c9ef658be7a45ce45b15b8b4b4e5a67` | Добавлены атомарный Big gate и пятикомпонентный Small контракт | money model, FSM, evaluator | Big atomic gate, Small contract | Gate вызывается до открытия core. Ошибки: directional volume суммируется повторно для legs одного направления; Reserve projection не входит в общий atomic decision. Small contract индексирует массив по enum вместо поиска роли. | evaluator без MetaEditor | PARTIAL |
| `1532ce9f318cddc9039e38933e9c1a73c340dca7` | Добавлены persisted Harvest и фактическая сверка Reserve | FSM, types | Harvest/reconciliation | Поля сохраняются. Ошибки: фазы `LEDGER_WRITTEN`, `DISTRIBUTED`, `CONSUMED` не управляют side effects; restart не продолжает транзакцию по фазе; harness лишь присваивает фазу. | Python не проверяет MQL persistence | FAIL |
| `8cd0b7e684e9e5dbb51833239e550cb34b318667` | Добавлен MQL5 State Machine harness Big Small | MQL5 harnesses, compile script | State Machine harness | Подключает FSM, но вызывает произвольный `SetState(from,to)` вместо событий/handlers; rejected operations и margin rejection заменены локальными присваиваниями. | MetaEditor NOT_RUN | FAIL |
| `e5b2786d8e76cb582866bb07f21261dd7e797573` | Расширен воспроизводимый preset Split Big Small | `.set` | reproducible preset | Критические параметры и checksum присутствуют, real trading выключен. | checksum | PASS |
| `a589f684da612bb0c02e89c67d73666ae2cf06cf` | Добавлены поведенческие тесты swap комиссии и конечности | Python tests | money tests | Числовые Python-тесты есть, но не вызывают MQL5 и не моделируют margin в reverse cycles. | pytest | PARTIAL |
| `a2dcfe965bd8da94f662ab651da6ac62b7d1d45b` | Добавлены денежные шлюзы Small и ложного разворота | money model | Small pretrade/false reverse | Pure evaluators добавлены, но не подключены к FSM до закрытия BigTrend; finite model не использует signed swap/commission/spread/slippage/margin как отдельные входы. | Нет runtime | FAIL |
| `0e5ea03ad9bd59c806f0ea25b0d348e6117c47c6` | Добавлен отчёт готовности денежной модели Big Small | reports/journal | readiness | Статусы честно оставлены NOT_RUN/UNKNOWN. | Документ | PASS |
| `07b05714161e9d4979e2da42967ed62841c3ff13` | Уточнены базы notional и turnover комиссии | money/config/preset/test | commission bases | Ветви различены и open/close не делятся пополам. Требуется числовой MQL5 тест и документирование валютной конверсии. | pytest | PARTIAL |

## Матрица требований

| Требование | Реализовано | Файл/функция | Тест | Статус | Что осталось |
|---|---|---|---|---|---|
| Signed swap | Да | `CalcSignedBrokerSwap` | Python числа | PARTIAL | MQL5 deterministic test |
| Triple swap | Да | `CalcSignedBrokerSwap` | Python calendar | PARTIAL | broker-server calendar MQL5 test |
| Notional/turnover | Да | `CalcPercentCommissionSide` | Python | PARTIAL | MQL5 numeric checks |
| Open/close commission | Да | отдельные functions | Python | PARTIAL | conversion/minimum/rounding |
| Big atomic gate | Частично | `EvaluateBigBasketGate` | evaluator | PARTIAL | устранить duplicate directional count; включить recovery/coverage в единый decision |
| Harvest phases | Поля есть | `HarvestPhase`, `SaveState` | формальный restart loop | FAIL | idempotent phase executor и crash tests |
| Reserve actual reconciliation | Да | `ProcessSplitBigHarvestFinalCheck` | нет runtime | PARTIAL | projected-vs-actual assertion |
| Small five legs | Частично | `EvaluateSmallTransition` | evaluator | PARTIAL | role lookup, FSM pre-trade integration |
| Small pre-trade | Pure helper | `EvaluateSmallPreTradeGate` | нет FSM test | FAIL | вызвать до close BigTrend |
| Finite reverse money | Частично | `EvaluateRequiredReverseCyclesMoney` | Python analogue | FAIL | swap/commission/spread/slippage/margin per cycle |
| False reverse | Pure helper | `EvaluateFalseReverseMoney` | нет FSM integration | FAIL | построить candidates из реальных positions и применить state |
| State Machine harness | Файл есть | `BigSmallStateMachineTest.mq5` | NOT_RUN | FAIL | события, positions, ledger, operations вместо прямых присваиваний |
| Preset | Да | `SPLIT_BIG_SMALL_TEST_SAFE.set` | checksum | PASS | MetaEditor/MT5 |
| Readiness report | Да | production report | review | PASS | runtime results |

`METAEDITOR_COMPILE=NOT_RUN`, `MT5_STRATEGY_TESTER=NOT_RUN`, `REAL_TRADING_ALLOWED=NO`.
