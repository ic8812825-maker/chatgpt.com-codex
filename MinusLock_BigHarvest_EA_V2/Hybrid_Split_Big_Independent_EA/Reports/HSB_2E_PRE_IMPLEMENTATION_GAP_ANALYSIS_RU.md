# HSB.2E pre-implementation gap analysis

| Компонент | Сейчас | Требуется | Блокер | Этап |
|---|---|---|---|---|
| Context/FSM | static/pure | production orchestration | MT5 proof | 2E |
| Broker money | wrapper/unverified | runtime-confirmed | V2 | 2E.2 |
| Persistence | contracts | backend | implementation | 2E.1 |
| Reconciliation | validators | engine | implementation | 2E.4 |
| Transaction | intent/barrier | lifecycle | implementation | 2E.5 |
| Initial Lock | interface | production scenario | implementation | 2E.6 |
| Big | calculations/contracts | production scenario | implementation | 2E.7 |
| Partial Far | allocation contract | production scenario | implementation | 2E.8 |
| Final Close | gate/contracts | production scenario | implementation | 2E.9 |
| Small | interface/solver | production scenario | implementation | 2E.10 |
| Broker dispatch | absent | demo-only initially | approval | 2E.13 |

```text
OWNERLESS_COMPONENTS=0
UNSPECIFIED_INTERFACES=0
UNMAPPED_REQUIREMENTS=0
IMPLEMENTATION_ORDER_DEFINED=YES
TEST_ORDER_DEFINED=YES
HSB_2E_PREP_READY=YES
TRADING_LOGIC_IMPLEMENTATION=NOT_STARTED
REAL_TRADING_ALLOWED=NO
```
