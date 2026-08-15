# HSB.2C-R1-P2 — implementation report

Реально удалена старая структура/builder из RuntimeMode, основной EA и ReserveCatchUp подключены к canonical policy, проверен include graph и добавлены T401–T430.

Поиск implementation symbols:

```text
Include/Core/HSBI_RuntimePolicy.mqh:5:struct HSBI_RuntimePolicy
Include/Core/HSBI_RuntimePolicy.mqh:12:HSBI_RuntimePolicy HSBI_BuildRuntimePolicy(...)
```

Остальные совпадения `HSBI_BuildRuntimePolicy(` являются вызовами canonical функции. Документальные упоминания не входят в MQL5 definition count.

```text
RUNTIME_POLICY_CANONICAL=PASS
DUPLICATE_RUNTIME_POLICY_DEFINITIONS=0
DUPLICATE_RUNTIME_POLICY_FUNCTIONS=0
INCLUDE_GRAPH_AUDIT=PASS
TESTS_T01_T430=DECLARED_STATIC
BROKER_TRANSACTION_ENGINE=NOT_IMPLEMENTED
TRADING_IMPLEMENTED=NO
REAL_TRADING_ALLOWED=NO
HSB.2D=NOT_STARTED
```
