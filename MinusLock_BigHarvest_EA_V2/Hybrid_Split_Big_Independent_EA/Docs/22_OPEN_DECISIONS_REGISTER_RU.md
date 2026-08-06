# Реестр нормативных решений после HSB.0R

Версия 2.0. Статус: CLOSED_FOR_HSB1_ARCHITECTURE.

| ID | Принятое решение | Статус |
|---|---|---|
| HSBI-DEC-001 | Формулы и broker-normalized диапазоны фиксированы; research ratios не являются production default | DEFERRED_WITH_SAFE_CONTRACT |
| HSBI-DEC-002 | Allocation profile конфигурируемый; conservation/source ownership/bucket isolation обязательны | DEFERRED_WITH_SAFE_CONTRACT |
| HSBI-DEC-003 | Typed fresh control prices, Bid/Ask и broker tick proof range | RESOLVED |
| HSBI-DEC-004 | Exact recursive Future Small до terminal/depth/bound; depth 1 недостаточен | RESOLVED |
| HSBI-DEC-005 | Minimum broker-valid safe residual с deterministic tie-break | RESOLVED |
| HSBI-DEC-006 | Emergency Liquidation отделена от Recovery Final Close | RESOLVED |
| HSBI-DEC-007 | Minimum из absolute/equity/OldFarRisk/cumulative caps; значения конфигурационные | DEFERRED_WITH_SAFE_CONTRACT |
| HSBI-DEC-008 | Money threshold + execution buffer + tolerance; значение конфигурационное | DEFERRED_WITH_SAFE_CONTRACT |
| HSBI-DEC-009 | Обязательные fail-closed gates; research limits не real defaults | DEFERRED_WITH_SAFE_CONTRACT |
| HSBI-DEC-010 | Identity включает Account+Symbol+Magic+CycleID+identifier+role; one cycle/symbol | RESOLVED |
| HSBI-DEC-011 | Versioned file snapshot + SHA-256 + append-only journal; GV markers only | RESOLVED |
| HSBI-DEC-012 | REAL_LIMITED contract с explicit approval; торговля сейчас запрещена | RESOLVED |
| HSBI-DEC-013 | Confirmed Small touch, fresh repeated snapshots, debounce key | RESOLVED |
| HSBI-DEC-014 | Same ActionID retry only after reconciliation; timeout→RECONCILING | RESOLVED |

`DEFERRED_WITH_SAFE_CONTRACT` не требует изменения основных типов HSB.1: интерфейсы, диапазоны, validation, owners и тесты определены; меняются только validated configuration values после MQL5/MT5 evidence.

```text
OPEN_P0=0
OPEN_P1=0
OPEN_P2=0
REAL_TRADING_ALLOWED=NO
```
