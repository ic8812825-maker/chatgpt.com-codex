# Этап 3.1.6.3.15 — реестр смешения Legacy, Split и Hybrid

| MIX-ID | Область | Legacy element | Split element | Hybrid element | Фактическое поведение | Критичность |
|---|---|---|---|---|---|---|
| MIX-001 | Runtime mode | `UseLegacySingleBigGeometry` | `UseSplitBigGeometry` | `UseHybridSplitBigGeometry` | Hybrid не отдельный mode, а modifier Split | P1 |
| MIX-002 | Config | BigRatio/SmallRatio/CloseBigOnSmall | BigCore/Trend/Base ratios | Hybrid allocation/target inputs | все inputs живут одновременно в одном Config | P1 |
| MIX-003 | FSM | STATE_FAR_ACTIVE/legacy Big states | STATE_SPLIT_* | Hybrid conditions внутри Split handlers | единый switch обслуживает три поколения | P1 |
| MIX-004 | Initial→Far | compatibility transition | общий Far context | Hybrid использует тот же Far | legacy bridge является входом Hybrid | P2 |
| MIX-005 | Geometry | `GeometryEngine` legacy lots | Split preparation | `HybridGeometrySolver` | два/три источника geometry | P1 |
| MIX-006 | Open path | generic `OpenPosition` comments | SPLIT role states/comments | Hybrid plan lots | Hybrid execution остаётся Split | P1 |
| MIX-007 | Small | Legacy CloseBigOnSmall semantics | DynamicReverseSmall | Hybrid NewFar from BigCore | общие functions ветвятся bool-флагом | P1 |
| MIX-008 | Final Close | Reserve>=loss historical rule | Split final safety | Hybrid preview | competing gate authorities | P1 |
| MIX-009 | Money | WorkCloseFarShare/WorkReserveShare | Split Reserve ledger | Hybrid shares | разные allocations сосуществуют | P1 |
| MIX-010 | Risk | legacy policy flags | Split terminal states | Hybrid risk preview | terminal behavior не унифицирован | P1 |
| MIX-011 | Persistence | legacy Big/Small fields | split roles | hybridReversePlan | один GlobalVariables schema без единой versioned topology | P1 |
| MIX-012 | Reconciliation | legacy topology | split topology | Hybrid expected topology | shared resolver/integrity engine | P1 |
| MIX-013 | Simulation | legacy virtual positions | split states | hybrid previews | `AllowRealTrading=false` выбирает simulation semantics | P1 |
| MIX-014 | Identity | generic ticket | role identifiers | CycleID/fingerprint | TradeEngine atomарно проверяет только Symbol+Magic | P0 |
| MIX-015 | Events | synchronous return | pending contracts | normative EventKey | OnTradeTransaction отсутствует | P1 |

## Итог

Hybrid Split Big реально присутствует, но не является изолированной основной production-системой. Он частично подключён как набор solver/gates и conditional branches внутри активной Split архитектуры. Legacy остаётся default mode и продолжает определять общий lifecycle Initial Lock/Far и часть shared parameters/functions.

Production MQL5 не изменялся.
