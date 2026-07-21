# Валидация Hybrid Split Big

## Выполнено

* Python invariant suite и независимая deterministic search.
* `git diff --check`.
* Проверка документа/кода через static pytest assertions.

## Не выполнено (блокер FINAL_APPROVED)

MetaEditor compile и MT5 Strategy Tester с real ticks отсутствуют в контейнере.
До этих проверок статус только `MQL5_IMPLEMENTED`/`PYTHON_TESTED`; включение
hybrid режима для реальных денег запрещено.
