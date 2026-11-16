# HSBI-03D — R1.1 readiness gates

Версия HSBI-03D-REMOTE-R1; source SHA6543bc2c0d125f5f7e02f78a092b0412a2e34626.
Это publication audit package, не implementation authorisation.
Исходные Reports/HSBI_R11_P0_DEPENDENCY_PLAN_RU.md,HSBI_R11_P0_TEST_MATRIX_RU.md,HSBI_R11_P0_UNAPPLIED_PATCH_PLAN_RU.md не переписаны.
Детали16 решений: [review](HSBI_03D_INDEPENDENT_CONTRACT_REVIEW_RU.md),[ballot](HSBI_03D_OWNER_APPROVAL_BALLOT_RU.md); [P0 crosswalk](HSBI_03D_P0_REMEDIATION_CROSSWALK_RU.md).

## Разделить три разных разрешения

1. Нормативное owner approval: какое поведение должно быть.
2. Architecture approval: какие authoritative providers,registry,durable transaction обеспечивают его.
3. Implementation qualification: фактические production paths/native/crash/concurrency evidence.
Ни один пункт не следует автоматически из публикации или предыдущего пункта. Отчёт не делает missing authority существующей.

## Что готово к голосованию сейчас

12 principles/policy decisions: D01,D02,D03,D04,D05,D07,D08,CR09,NUM-EXACT-1,FUNDING-GLOBAL-ATTRIBUTION,MQL-DOMAIN,BALANCE-SCHEMA-MAPPING.
D05 включает предложенный reset protocol; утвердить current formula без reset недостаточно.
D10/D15 можно утвердить как exact-accounting/qualification requirements, но concrete numeric bundle не frozen.

Остальные4:
D06 CONFLICTING — выбрать Initial-excluding A либо явное нормативное изменение B;
D11 BLOCKED_BY_EVIDENCE — currency/posting/grid profile;
D12 BLOCKED_BY_EVIDENCE — native codec goldens/decoder qualification;
D13 REQUIRES_CLARIFICATION — actual provider/clock/unit/uncertainty profile.

## Обязательные gates

| Gate | Требуется | Текущий статус/ограничение |
|---|---|---|
| OWNER-VERSION | Canonical ID,variant,exact text version/blob,owner identity/date/scope | AWAITING;0 approved |
| INITIAL-POLICY | D06 A/B; EconomicCyclePnL отдельно RecoveryResult | CONFLICTING Docs/09:20 |
| OBJECTIVE | Docs/14:22–23 minimum-safe-first vs Docs/29:3 risk-first | unresolved; CR09 не выбирает |
| MONEY-PROFILE | currency,scale,posting stage,rounding,range | missing qualified evidence |
| GRID-PROFILE | price tick,volume step,min,max,origin,optional leg policy | origin conflict/profile not frozen |
| SNAPSHOT-AUTHORITY | provider,clock domain,unit,TTL/skew,original content receipt | clarification/evidence required |
| SOURCE-AUTHORITY | broker source namespace,actual records,independent EA association | DTO flags не authority |
| REGISTRY | complete global inventory,serializable balance+receipt+revision | not implemented/qualified here |
| DURABILITY | crash-consistent journal/state,UNKNOWN reconciliation,restart | production persistence stub S13 |
| NUMERIC-BUNDLE | D10+D11+D12+D15 single manifest | no final F64Z/native freeze |
| NATIVE | build-bound fixed vectors,codec/domain/grids evidence | NATIVE_NOT_RUN |
| CONCURRENCY/CRASH | true consumer races,multi-source transaction,power-loss stages | TEST_SPECIFIED_NOT_RUN |
| LEGACY | proven mappings,quarantine unknown,no resets | corpus not qualified |
| PRODUCTION-PATH | minimal explicit future allowlist,mandatory guards,causal tests | not changed or tested here |
| ERR038 | explicit bounded market/execution/cost model+proof | OPEN,separate proof |

## Минимальные remediation interfaces

A identity/provider: logical source K + complete body + actual association; no caller-self authentication.
B ledger/registry: immutable grant manifest,exact C/R/F,source inventory,atomic effects.
C domain guards: finite/range/enum/overflow validation на обязательных caller paths.
D reserve/all-level: scalar/proof binding,eligibility,absolute Far loss,min margin каждого required level.
E journal/restart/context: durable receipts,full-body replay validation,UNKNOWN barrier,all-slot ownership.
Это категории требований crosswalk, не самовольное изменение existing patch plan и не разрешение писать production.

## Риски и непринятые предположения

Bounded lots не global money-loss bound; finite proven levels не tail theorem; positive BigHarvest не positive CyclePnL; preview PASS не funds; reset не erase history; schema change не new source; published report не evidence-qualified implementation.

Прежде чем разрешать R1.1, владелец должен отдельно утвердить строго ограниченный change scope и достаточные qualification gates. Если отдельный guard можно внедрить независимо, его допустимость всё равно требует отдельного разрешения и proof mandatory integration; это задание такого разрешения не даёт.
BROKER_DISPATCH_ALLOWED=NO; REAL_TRADING_ALLOWED=NO; R11_IMPLEMENTATION_ALLOWED=NO.
