# HSBI-03G-R1 — спецификация квалификации и фиксированные vectors

DocumentVersion=HSBI-03G-R1-V1
SourceCommitSHA=e68e73e1b252d20e15588645004f9066c6ae88f0
Scope=QualificationVersion=HSBI_CR09_ALL_REQUIRED_QUAL_V1
EvidenceClass=TEST_SPECIFIED_NOT_RUN; MATH_DERIVED for independently checked arithmetic
NormativeStatus=PROPOSED_AWAITING_OWNER_APPROVAL
Dependencies=CR09 contract; all owner/provider/numeric gates

Репозиторий: `ic8812825-maker/chatgpt.com-codex`, ветка `work`. Все пути ниже находятся внутри `MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/`. Новый текст является проектом контракта, а не утверждением реализации. Выбор D-06 A и companion NewFar A сохраняется; полный CR-09 не утверждён. Формальных approval receipts нет.

PRODUCTION_CHANGED=NO; IMPLEMENTATION_ALLOWED=NO; R11_IMPLEMENTATION_ALLOWED=NO; BROKER_DISPATCH_ALLOWED=NO; REAL_TRADING_ALLOWED=NO; NATIVE_MQL5_TESTS=NOT_RUN.

UNAVAILABLE означает отсутствие обязательного доказательства; CONFLICT — противоречие данных; REJECT — доказанное нарушение. Каждый результат запрещает новый финансовый эффект, delta=0. NO_OP допустим только после проверки подлинного полного прежнего event body и receipt. Числа математических примеров не являются брокерскими константами.

## Статус и источники

Все записи ниже имеют ExecutionStatus=NOT_RUN и EvidenceClass=TEST_SPECIFIED_NOT_RUN. Expected — требование к будущей реализации/компоненту, а не наблюдённый production result. Математическая проверка сумм в памяти не является MQL5 test run. Полный broker-backed solver path, компиляция, crash/concurrency/native ещё не выполнялись.

- [Reports/HSBI_03F_R2_TEST_VECTOR_SPECIFICATION_RU.md:21–157](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/e68e73e1b252d20e15588645004f9066c6ae88f0/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_03F_R2_TEST_VECTOR_SPECIFICATION_RU.md#L21-L157). SourceBlobSHA=`0b74240e22fe0248977bb7448baac5039383452e`; EvidenceClass=STATIC_REVIEWED.
- [Reports/HSBI_03F_R2_TRANSITION_CATCHUP_MATH_PROOFS_RU.md:21–153](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/e68e73e1b252d20e15588645004f9066c6ae88f0/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_03F_R2_TRANSITION_CATCHUP_MATH_PROOFS_RU.md#L21-L153). SourceBlobSHA=`427f90083629a8e5207952e509a0e4fcefedc377`; EvidenceClass=STATIC_REVIEWED.
- [Include/Planning/HSBI_NewFarSolver.mqh:94–151](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/e68e73e1b252d20e15588645004f9066c6ae88f0/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Include/Planning/HSBI_NewFarSolver.mqh#L94-L151) — HSBI_SolveNewFar. SourceBlobSHA=`3d19eccd6cd318b9b4591e2bc0ccaa95f661930d`; EvidenceClass=STATIC_REVIEWED.
- [Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:35–75](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/e68e73e1b252d20e15588645004f9066c6ae88f0/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Include/Money/HSBI_ReserveCatchUpEvaluator.mqh#L35-L75) — legacy component behavior. SourceBlobSHA=`87a8b7e97727ce6e47c2a2f0abc3e237f6203204`; EvidenceClass=STATIC_REVIEWED.
- [Tests/Close/production_subset_results.json:1–161](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/e68e73e1b252d20e15588645004f9066c6ae88f0/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Tests/Close/production_subset_results.json#L1-L161) — HISTORICAL_TEST_RESULT only. SourceBlobSHA=`192fe577764407499c6334d8e07c55ad78afeed7`; EvidenceClass=STATIC_REVIEWED.

Нормативные проекты expected: [required set](HSBI_03G_R1_CR09_REQUIRED_LEVEL_CONTRACT_RU.md), [quantity](HSBI_03G_R1_PER_LEVEL_FAR_VOLUME_BINDING_RU.md), [metrics](HSBI_03G_R1_TRANSITION_CATCHUP_METRIC_SCHEMA_RU.md), [feasibility](HSBI_03G_R1_ALL_LEVEL_FEASIBILITY_PROOF_RU.md), [funding](HSBI_03G_R1_RESERVE_FUNDING_AUTHORITY_RU.md), [objective](HSBI_03G_R1_MINIMUM_SAFE_COMPATIBILITY_RU.md). Они ещё PROPOSED. Test rule не создаёт owner approval.

## Полные fixtures через immutable inheritance

Полный исходный body каждого R2 fixture берётся исключительно из pinned blob `0b74240e22fe0248977bb7448baac5039383452e` (R2 vectors), а денежные формулы из `427f90083629a8e5207952e509a0e4fcefedc377` (R2 math). Inheritance означает все поля исходной fixture плюс явно перечисленные overrides, не «любые подходящие значения». Если fixture missing/unsupported — fixture setup UNAVAILABLE, не успешный отказ target branch. Ни один исходный файл или expected не изменяется.

R2-F-PROJECTION: XTEST3,digits3,scale1000,MODEL_LINEAR_1,point/tick1,tick value1,grid min/step0.05,max10,origin0. BUYgross=v(P−open),SELLgross=v(open−P);Far/SmallSELL,Core/TrendBUY;CoreRatio3,TrendRatio1,SmallRatio1;allopens100. F_before0.4/0.2/0.1,F_after0.2/0.1/0.05;quotes125/125/150 (Bid=Ask). B_leg=B_CU=1, прочие costs0 кроме Far/Small commissions. Initial recovery−20,risk100/tolerance1→90/80/70,allowedmargin100,syntheticmargin10/lot→24/12/6,gross initial10,priorBig10,q0.5,minimumcompression0.05/ratio0.5,maxratio0.5,maxDepth3,counts3,futurecap20,outer4caps12. IDs/snapshot/time/shape flags и nominal source tuple наследуются из pinned R2. Account1,cycle7,magic7,plan9,revision5,market1001/1002/1003,cost2001/2002/2003,risk3001/3002/3003,ticktime100,TTL10,epochE1. Real broker/provider receipts NONE. Legacy expectedPlanDigest="" не даёт integrity authority.

M_MINUS Far commission magnitude(2.2,8.2,2.2),Small(25.8,4.8,6.8),margins(9,−4,2). M_PLUS меняет только L2 f3.2,s9.8 →margins9/1/2. M_ZERO L2 f4.2,s8.8 →9/0/2. Все обновления content требуют новых fixture receipts; сохранять старый ID с новым content — отдельный негативный case. Эти fixtures projected и не являются физической sequential history; нужны direction/position lineage и реальная authority.

R_AUTH: independently stipulated reference source (B_MODEL,S_MODEL,account1,deal101),actual posting18.125,share0.8,ReserveGrant14.5,residual3.625,C0/R0/F14.5,revision5,allocationA101; real provider NONE. V1 — quantity-only fixture с указанными inputs; не money authority. NF_A_B/NF_TIE — tuple-level fixtures с полными rows в каждом case; неподанные gates считаются математическими premises только для component, а финансовое разрешение всегда NO. INT64_EXACT — generic signed64 boundary, не утверждённый реальный currency manifest.

## Наследуемые TL/CU — точная новая expected group без переписывания R2

Каждая следующая запись имеет ContractVersion=HSBI_CR09_ALL_REQUIRED_V1,FixtureVersion=HSBI-03G-FIXTURE-1,ExecutionStatus=NOT_RUN,EvidenceClass=TEST_SPECIFIED_NOT_RUN. Input — полный одноимённый R2 test из pinned blob с его fixture/overrides; изменён только versioned target contract. RequiredSourceEvidence — R2 frozen mathematical receipts для component; настоящие source/provider/clock/profile receipts для native integration. ExpectedFailureReason указан в таблице; для успешного predicate — NONE, финансовое разрешение всё равно NO. Native successful route не доказан ни для одного case.

| TestID | Фиксированный input / expected нового контракта | Invariant / failure reason | Независимый компонент / native dependency |
|---|---|---|---|
| TL-01 | R2 TL_BASE1,cap12,Tmax12,A_control3; output хранит12 и3 | METRIC_KIND_MISMATCH если смешаны | typed DTO / successful return path |
| TL-02 | R2 TL_BASE2,cap5,Tmax3,A_control12; cap сравнивает3 | Far loss не basket maximum | typed cap / broker money |
| TL-03 | M_PLUS,explicit controlL2,Tmax12@L1,A9.2@L2,minM1 | LEVEL_SCOPE_MISMATCH | aggregate binding / native candidate |
| TL-04 | M_MINUS,controlL1 M9,requiredL2 M−4 →REJECT | REQUIRED_MARGIN_NEGATIVE | all-level minimum / native integration |
| TL-05 | TL_BASE1,Small commission L1=37,T13,cap12 →REJECT | TRANSITION_CAP_EXCEEDED до safe[] | cap guard / native rejected branch |
| CU-01 | M_PLUS,required3 →Mmin1,all-CatchUp predicate true | NONE; другие gates отдельно | margin model / real authority |
| CU-02 | M_ZERO,required3 →Mmin0,REJECT | NONPOSITIVE_CATCHUP_MARGIN | exact zero / native rounding |
| CU-03 | M_MINUS →Mmin−4,REJECT | REQUIRED_MARGIN_NEGATIVE | exact model / integration |
| CU-04 | M_MINUS,argmaxT=L1,argminM=L2 | Independent extrema | maths/aggregate / native source path |
| CU-05 | M_PLUS,L2money missing →UNAVAILABLE | REQUIRED_MONEY_PROOF_MISSING | completeness / caller propagation |
| CU-06 | R_AUTH, sequential9+9 from14.5 →second REJECT | INSUFFICIENT_FREE | inventory / atomic journal |
| CU-07 | M_PLUS,Snapshot1002→2002,no replacement receipt →UNAVAILABLE | SNAPSHOT_AUTHORITY_MISSING; при empty expectedDigest старый code не обязан дать digest mismatch | receipt validator / native authority |
| CU-08 | CurrentRevision6,proof/plan5 →CONFLICT | STATE_REVISION_MISMATCH | revision binding / restart |
| CU-09 | Positive projected reserve,actual receiptsNONE →BLOCKED funding | SOURCE_AUTHORITY_MISSING | authority separation / provider |
| CU-10 | min/step0.025,prefix3,required4,L4unknown →UNAVAILABLE | TAIL_MONEY_NOT_PROVEN | required scope / native bound |

TL_BASE1/2 полные leg/open/cost inputs наследуются из R2 §1. TL03 не подменяется невозможным genuine producer примером T3/7/12. Два разных формата evidence — mathematical scenario и executed branch — сохраняются раздельно.

## Новые конкретные test records

Во всех случаях non-success financial delta=0. Для positive component expected не создаётся consumption/reservation/dispatch. JSON суммы даны decimal strings, чтобы test harness не менял входы через случайный binary64 parse. Выбор int/floating/codec harness требует отдельного утверждённого profile.

### LEVEL-01

```json
{
  "TestID": "LEVEL-01",
  "ContractVersion": "HSBI_CR09_ALL_REQUIRED_V1",
  "FixtureVersion": "HSBI-03G-FIXTURE-1",
  "Input": {
    "Fixture": "R2-F-PROJECTION/M_PLUS",
    "R": [
      "L1",
      "L2",
      "L3"
    ],
    "P": [
      "L1",
      "L2",
      "L3"
    ],
    "semantics": "ALTERNATIVE_SCENARIOS",
    "terminal": "approved fixture guard at L3"
  },
  "Expected": {
    "completeness": "COMPLETE_FOR_DECLARED_FIXTURE_SCOPE",
    "financialPermission": "NO"
  },
  "Invariant": "R subset P; no retroactive required count",
  "RequiredSourceEvidence": "Frozen level manifest + independent per-level original receipts",
  "ExpectedFailureReason": "NONE_FOR_COMPONENT_PREDICATE; FINANCIAL_AUTHORITY_NOT_GRANTED",
  "EvidenceClass": "TEST_SPECIFIED_NOT_RUN",
  "ExecutionStatus": "NOT_RUN",
  "IndependentComponent": "set coverage component",
  "NativeIntegrationRequired": "owner-selected model + real provider/native"
}
```

### LEVEL-02

```json
{
  "TestID": "LEVEL-02",
  "ContractVersion": "HSBI_CR09_ALL_REQUIRED_V1",
  "FixtureVersion": "HSBI-03G-FIXTURE-1",
  "Input": {
    "Fixture": "R2-F-PROJECTION/M_PLUS",
    "R": [
      "L1",
      "L2",
      "L3",
      "L4"
    ],
    "P": [
      "L1",
      "L2",
      "L3"
    ],
    "L4": "MISSING"
  },
  "Expected": {
    "completeness": "INCOMPLETE",
    "reason": "REQUIRED_LEVEL_MISSING",
    "delta": 0
  },
  "Invariant": "Missing required ID not zero",
  "RequiredSourceEvidence": "External frozen R, no L4 receipt",
  "ExpectedFailureReason": "REQUIRED_LEVEL_MISSING",
  "EvidenceClass": "TEST_SPECIFIED_NOT_RUN",
  "ExecutionStatus": "NOT_RUN",
  "IndependentComponent": "set coverage component",
  "NativeIntegrationRequired": "native missing-level propagation"
}
```

### LEVEL-03

```json
{
  "TestID": "LEVEL-03",
  "ContractVersion": "HSBI_CR09_ALL_REQUIRED_V1",
  "FixtureVersion": "HSBI-03G-FIXTURE-1",
  "Input": {
    "Fixture": "R2-F-PROJECTION/M_PLUS",
    "IDs": [
      "L1",
      "L2",
      "L2"
    ],
    "bodies": [
      "body1",
      "body2",
      "alteredBody2"
    ]
  },
  "Expected": {
    "status": "CONFLICT",
    "reason": "DUPLICATE_LEVEL_ALTERED_BODY",
    "delta": 0
  },
  "Invariant": "One ID one immutable body",
  "RequiredSourceEvidence": "Original receipts for L2 and altered body",
  "ExpectedFailureReason": "DUPLICATE_LEVEL_ALTERED_BODY",
  "EvidenceClass": "TEST_SPECIFIED_NOT_RUN",
  "ExecutionStatus": "NOT_RUN",
  "IndependentComponent": "manifest/receipt comparison",
  "NativeIntegrationRequired": "authority-backed content validation"
}
```

### LEVEL-04

```json
{
  "TestID": "LEVEL-04",
  "ContractVersion": "HSBI_CR09_ALL_REQUIRED_V1",
  "FixtureVersion": "HSBI-03G-FIXTURE-1",
  "Input": {
    "Fixture": "R2-F-PROJECTION/M_PLUS",
    "requiredOrder": [
      "L1",
      "L2",
      "L3"
    ],
    "providedOrder": [
      "L2",
      "L1",
      "L3"
    ],
    "semantics": "SEQUENTIAL_TRANSITIONS",
    "edges": [
      [
        "L1",
        "L2"
      ],
      [
        "L2",
        "L3"
      ]
    ]
  },
  "Expected": {
    "status": "REJECT",
    "reason": "STATE_CHAIN_ORDER_MISMATCH",
    "delta": 0
  },
  "Invariant": "Sequential edges preserve causation",
  "RequiredSourceEvidence": "Ordered state before/after receipts",
  "ExpectedFailureReason": "STATE_CHAIN_ORDER_MISMATCH",
  "EvidenceClass": "TEST_SPECIFIED_NOT_RUN",
  "ExecutionStatus": "NOT_RUN",
  "IndependentComponent": "graph validator",
  "NativeIntegrationRequired": "native execution-prefix/restart"
}
```

### LEVEL-05

```json
{
  "TestID": "LEVEL-05",
  "ContractVersion": "HSBI_CR09_ALL_REQUIRED_V1",
  "FixtureVersion": "HSBI-03G-FIXTURE-1",
  "Input": {
    "Fixture": "R2-F-PROJECTION/M_PLUS",
    "volumeMin": "0.025",
    "volumeStep": "0.025",
    "maximumDepth": 3,
    "FarAfter": [
      "0.2",
      "0.1",
      "0.05"
    ],
    "R": [
      "L1",
      "L2",
      "L3",
      "L4"
    ],
    "tail": "EXACT_REQUIRED_4",
    "L4": "UNKNOWN"
  },
  "Expected": {
    "status": "UNAVAILABLE",
    "reason": "TAIL_MONEY_NOT_PROVEN",
    "delta": 0
  },
  "Invariant": "Volume bound not all-safety tail theorem",
  "RequiredSourceEvidence": "Tail manifest; L4 money proof absent",
  "ExpectedFailureReason": "TAIL_MONEY_NOT_PROVEN",
  "EvidenceClass": "TEST_SPECIFIED_NOT_RUN",
  "ExecutionStatus": "NOT_RUN",
  "IndependentComponent": "bound versus coverage component",
  "NativeIntegrationRequired": "native producer with conservative prefix"
}
```

### LEVEL-06

```json
{
  "TestID": "LEVEL-06",
  "ContractVersion": "HSBI_CR09_ALL_REQUIRED_V1",
  "FixtureVersion": "HSBI-03G-FIXTURE-1",
  "Input": {
    "Fixture": "R2-F-PROJECTION/M_PLUS",
    "LevelSemantics": "UNKNOWN_SCHEMA_V99"
  },
  "Expected": {
    "status": "UNSUPPORTED",
    "reason": "LEVEL_SEMANTICS_UNSUPPORTED",
    "delta": 0
  },
  "Invariant": "Unknown version not guessed",
  "RequiredSourceEvidence": "Version allowlist receipt",
  "ExpectedFailureReason": "LEVEL_SEMANTICS_UNSUPPORTED",
  "EvidenceClass": "TEST_SPECIFIED_NOT_RUN",
  "ExecutionStatus": "NOT_RUN",
  "IndependentComponent": "schema validator",
  "NativeIntegrationRequired": "native codec/restart"
}
```

### VOLUME-01

```json
{
  "TestID": "VOLUME-01",
  "ContractVersion": "HSBI_CR09_ALL_REQUIRED_V1",
  "FixtureVersion": "HSBI-03G-FIXTURE-1",
  "Input": {
    "Fixture": "V1",
    "share": "0.5",
    "NetBig": "1.2",
    "FarBefore": "1",
    "FarAfter": "0.4",
    "OriginalCandidate": "0.8",
    "mode": "SAME_POSITION_PARTIAL",
    "FarClosed": "0.6"
  },
  "Expected": {
    "lhs": "0.6",
    "FarBefore": false,
    "FarAfter": true,
    "FarClosed": false,
    "OriginalCandidate": false
  },
  "Invariant": "Strict comparison, purpose-specific outcomes",
  "RequiredSourceEvidence": "One position/action partial-fill lineage",
  "ExpectedFailureReason": "NONE_FOR_COMPONENT_PREDICATE; FINANCIAL_AUTHORITY_NOT_GRANTED",
  "EvidenceClass": "TEST_SPECIFIED_NOT_RUN",
  "ExecutionStatus": "NOT_RUN",
  "IndependentComponent": "exact quantity predicates",
  "NativeIntegrationRequired": "native grid + fills"
}
```

### VOLUME-02

```json
{
  "TestID": "VOLUME-02",
  "ContractVersion": "HSBI_CR09_ALL_REQUIRED_V1",
  "FixtureVersion": "HSBI-03G-FIXTURE-1",
  "Input": {
    "Fixture": "V1",
    "share": "0.5",
    "NetBig": "1.2",
    "FarBefore": "1",
    "FarAfter": "0.4",
    "oldPosition": "SELL:P1",
    "newPosition": "BUY:P2",
    "mode": "PROMOTION",
    "FarClosed": "1"
  },
  "Expected": {
    "compression": "0.6",
    "physicalClosed": "1",
    "reason": "COMPRESSION_NOT_PHYSICAL_CLOSED"
  },
  "Invariant": "Closed volume not Before-After across identifiers",
  "RequiredSourceEvidence": "OldFar full-close and originalCore residual receipts",
  "ExpectedFailureReason": "COMPRESSION_NOT_PHYSICAL_CLOSED",
  "EvidenceClass": "TEST_SPECIFIED_NOT_RUN",
  "ExecutionStatus": "NOT_RUN",
  "IndependentComponent": "lineage semantics",
  "NativeIntegrationRequired": "actual-fill integration, no dispatch in qualification"
}
```

### VOLUME-03

```json
{
  "TestID": "VOLUME-03",
  "ContractVersion": "HSBI_CR09_ALL_REQUIRED_V1",
  "FixtureVersion": "HSBI-03G-FIXTURE-1",
  "Input": {
    "Fixture": "R2-F-PROJECTION/M_PLUS",
    "policy": "FarBefore",
    "share": "0.8",
    "NetBig": [
      "1.2",
      "0.6",
      "0.3"
    ],
    "FarBefore": [
      "0.4",
      "0.2",
      "0.1"
    ],
    "legacyN": "0.4"
  },
  "Expected": {
    "lhs": [
      "0.96",
      "0.48",
      "0.24"
    ],
    "perLevel": [
      true,
      true,
      true
    ],
    "legacy": [
      true,
      true,
      false
    ]
  },
  "Invariant": "Lot scope bound to corresponding level",
  "RequiredSourceEvidence": "Volume proof and frozen obligation policy",
  "ExpectedFailureReason": "NONE_FOR_COMPONENT_PREDICATE; FINANCIAL_AUTHORITY_NOT_GRANTED",
  "EvidenceClass": "TEST_SPECIFIED_NOT_RUN",
  "ExecutionStatus": "NOT_RUN",
  "IndependentComponent": "quantity model",
  "NativeIntegrationRequired": "owner policy + native producer"
}
```

### VOLUME-04

```json
{
  "TestID": "VOLUME-04",
  "ContractVersion": "HSBI_CR09_ALL_REQUIRED_V1",
  "FixtureVersion": "HSBI-03G-FIXTURE-1",
  "Input": {
    "Fixture": "V1",
    "share": "0.5",
    "NetBig": "1.2",
    "FarBefore": "1",
    "FarLossProofVolume": "0.4",
    "Obligation": "FULL_CLOSE_OLD_FAR"
  },
  "Expected": {
    "status": "CONFLICT",
    "reason": "LOSS_VOLUME_SCOPE_MISMATCH",
    "delta": 0
  },
  "Invariant": "Cannot price small volume and claim full coverage",
  "RequiredSourceEvidence": "Far money receipt with volume+identifier",
  "ExpectedFailureReason": "LOSS_VOLUME_SCOPE_MISMATCH",
  "EvidenceClass": "TEST_SPECIFIED_NOT_RUN",
  "ExecutionStatus": "NOT_RUN",
  "IndependentComponent": "typed binding validator",
  "NativeIntegrationRequired": "real broker money wrapper"
}
```

### VOLUME-05

```json
{
  "TestID": "VOLUME-05",
  "ContractVersion": "HSBI_CR09_ALL_REQUIRED_V1",
  "FixtureVersion": "HSBI-03G-FIXTURE-1",
  "Input": {
    "Fixture": "V1",
    "VolumeMin": "0.05",
    "VolumeMax": "10",
    "VolumeStep": "0.05",
    "GridOrigin": "0",
    "FarBefore": "0.43"
  },
  "Expected": {
    "status": "REJECT",
    "reason": "OFF_GRID_VOLUME",
    "delta": 0
  },
  "Invariant": "No hidden rounding of immutable evidence",
  "RequiredSourceEvidence": "Broker grid receipt version",
  "ExpectedFailureReason": "OFF_GRID_VOLUME",
  "EvidenceClass": "TEST_SPECIFIED_NOT_RUN",
  "ExecutionStatus": "NOT_RUN",
  "IndependentComponent": "grid validator",
  "NativeIntegrationRequired": "native boundary/grid qualification"
}
```

### MONEY-01

```json
{
  "TestID": "MONEY-01",
  "ContractVersion": "HSBI_CR09_ALL_REQUIRED_V1",
  "FixtureVersion": "HSBI-03G-FIXTURE-1",
  "Input": {
    "Fixture": "R2-F-PROJECTION/M_PLUS",
    "G": "12",
    "A": "11",
    "B": "1",
    "profile": "M3_EXACT"
  },
  "Expected": {
    "M": "0",
    "feasible": false,
    "reason": "NONPOSITIVE_CATCHUP_MARGIN",
    "delta": 0
  },
  "Invariant": "Strict >0",
  "RequiredSourceEvidence": "Cost/source amount receipts",
  "ExpectedFailureReason": "NONPOSITIVE_CATCHUP_MARGIN",
  "EvidenceClass": "TEST_SPECIFIED_NOT_RUN",
  "ExecutionStatus": "NOT_RUN",
  "IndependentComponent": "exact margin component",
  "NativeIntegrationRequired": "native strict boundary"
}
```

### MONEY-02

```json
{
  "TestID": "MONEY-02",
  "ContractVersion": "HSBI_CR09_ALL_REQUIRED_V1",
  "FixtureVersion": "HSBI-03G-FIXTURE-1",
  "Input": {
    "Fixture": "R2-F-PROJECTION/M_PLUS",
    "G": "12.001",
    "A": "11",
    "B": "1",
    "Ginterval": [
      "11.999",
      "12.003"
    ],
    "Ainterval": [
      "10.999",
      "11.001"
    ],
    "Binterval": [
      "1",
      "1.001"
    ]
  },
  "Expected": {
    "nominal": "0.001",
    "lower": "-0.003",
    "feasible": false,
    "reason": "LOWER_BOUND_NOT_POSITIVE",
    "delta": 0
  },
  "Invariant": "Nominal sign not certified lower bound",
  "RequiredSourceEvidence": "Approved independent error-bound profile",
  "ExpectedFailureReason": "LOWER_BOUND_NOT_POSITIVE",
  "EvidenceClass": "TEST_SPECIFIED_NOT_RUN",
  "ExecutionStatus": "NOT_RUN",
  "IndependentComponent": "interval arithmetic",
  "NativeIntegrationRequired": "native rounding/error qualification"
}
```

### MONEY-03

```json
{
  "TestID": "MONEY-03",
  "ContractVersion": "HSBI_CR09_ALL_REQUIRED_V1",
  "FixtureVersion": "HSBI-03G-FIXTURE-1",
  "Input": {
    "Fixture": "R2-F-PROJECTION/M_PLUS",
    "G": "NaN",
    "A": "1",
    "B": "1"
  },
  "Expected": {
    "status": "REJECT",
    "reason": "NONFINITE_MONEY",
    "delta": 0
  },
  "Invariant": "NaN not admissible",
  "RequiredSourceEvidence": "Numeric profile finite-domain rule",
  "ExpectedFailureReason": "NONFINITE_MONEY",
  "EvidenceClass": "TEST_SPECIFIED_NOT_RUN",
  "ExecutionStatus": "NOT_RUN",
  "IndependentComponent": "domain guard",
  "NativeIntegrationRequired": "native NaN/Infinity representation"
}
```

### MONEY-04

```json
{
  "TestID": "MONEY-04",
  "ContractVersion": "HSBI_CR09_ALL_REQUIRED_V1",
  "FixtureVersion": "HSBI-03G-FIXTURE-1",
  "Input": {
    "Fixture": "INT64_EXACT",
    "currency": "XTEST3",
    "scale": 1000,
    "postedMinor": "-9223372036854775808",
    "operation": "max(0,-postedMinor)"
  },
  "Expected": {
    "status": "UNAVAILABLE",
    "reason": "INT64_NEGATION_OVERFLOW",
    "delta": 0
  },
  "Invariant": "No abs(INT64_MIN) wrap/clamp",
  "RequiredSourceEvidence": "Approved exact type/range profile",
  "ExpectedFailureReason": "INT64_NEGATION_OVERFLOW",
  "EvidenceClass": "TEST_SPECIFIED_NOT_RUN",
  "ExecutionStatus": "NOT_RUN",
  "IndependentComponent": "checked arithmetic boundary",
  "NativeIntegrationRequired": "native signed64 boundary"
}
```

### MONEY-05

```json
{
  "TestID": "MONEY-05",
  "ContractVersion": "HSBI_CR09_ALL_REQUIRED_V1",
  "FixtureVersion": "HSBI-03G-FIXTURE-1",
  "Input": {
    "Fixture": "INT64_EXACT",
    "left": "9223372036854775807",
    "right": "1",
    "operation": "add"
  },
  "Expected": {
    "status": "UNAVAILABLE",
    "reason": "INT64_ADDITION_OVERFLOW",
    "delta": 0
  },
  "Invariant": "Check before add",
  "RequiredSourceEvidence": "Exact numeric manifest",
  "ExpectedFailureReason": "INT64_ADDITION_OVERFLOW",
  "EvidenceClass": "TEST_SPECIFIED_NOT_RUN",
  "ExecutionStatus": "NOT_RUN",
  "IndependentComponent": "checked arithmetic",
  "NativeIntegrationRequired": "native overflow/cast qualification"
}
```

### COST-01

```json
{
  "TestID": "COST-01",
  "ContractVersion": "HSBI_CR09_ALL_REQUIRED_V1",
  "FixtureVersion": "HSBI-03G-FIXTURE-1",
  "Input": {
    "Fixture": "R2-F-PROJECTION/M_PLUS",
    "ActualDeal": {
      "profit": "10",
      "commission": "-1",
      "swap": "-2",
      "fee": "-0.5"
    },
    "duplicateDeduction": false
  },
  "Expected": {
    "actualNet": "6.5",
    "inclusionCountPerFact": 1
  },
  "Invariant": "Signed components once",
  "RequiredSourceEvidence": "Actual deal and cost coverage receipts",
  "ExpectedFailureReason": "NONE_FOR_COMPONENT_PREDICATE; FINANCIAL_AUTHORITY_NOT_GRANTED",
  "EvidenceClass": "TEST_SPECIFIED_NOT_RUN",
  "ExecutionStatus": "NOT_RUN",
  "IndependentComponent": "cost inclusion component",
  "NativeIntegrationRequired": "broker association+native"
}
```

### COST-02

```json
{
  "TestID": "COST-02",
  "ContractVersion": "HSBI_CR09_ALL_REQUIRED_V1",
  "FixtureVersion": "HSBI-03G-FIXTURE-1",
  "Input": {
    "Fixture": "R2-F-PROJECTION/M_PLUS",
    "actualNet": "6.5",
    "CommissionIncludedInNet": "-1",
    "requestedExtraCommissionDeduction": "1",
    "sameCostFactID": "CF1"
  },
  "Expected": {
    "status": "CONFLICT",
    "reason": "DUPLICATE_COST_FACT",
    "delta": 0
  },
  "Invariant": "No double deduction",
  "RequiredSourceEvidence": "CF1 includedIn mapping",
  "ExpectedFailureReason": "DUPLICATE_COST_FACT",
  "EvidenceClass": "TEST_SPECIFIED_NOT_RUN",
  "ExecutionStatus": "NOT_RUN",
  "IndependentComponent": "cost coverage validator",
  "NativeIntegrationRequired": "provider-backed facts"
}
```

### COST-03

```json
{
  "TestID": "COST-03",
  "ContractVersion": "HSBI_CR09_ALL_REQUIRED_V1",
  "FixtureVersion": "HSBI-03G-FIXTURE-1",
  "Input": {
    "Fixture": "R2-F-PROJECTION/M_PLUS",
    "legBuffer": [
      "1",
      "1",
      "1",
      "1"
    ],
    "extraCatchUpBuffer": "1",
    "extraPurpose": "UNKNOWN"
  },
  "Expected": {
    "status": "UNAVAILABLE",
    "reason": "COST_BASIS_UNBOUND",
    "delta": 0
  },
  "Invariant": "No guessed disjoint headroom",
  "RequiredSourceEvidence": "CostBasisManifest missing buffer purpose",
  "ExpectedFailureReason": "COST_BASIS_UNBOUND",
  "EvidenceClass": "TEST_SPECIFIED_NOT_RUN",
  "ExecutionStatus": "NOT_RUN",
  "IndependentComponent": "coverage completeness",
  "NativeIntegrationRequired": "authority/native cost integration"
}
```

### COST-04

```json
{
  "TestID": "COST-04",
  "ContractVersion": "HSBI_CR09_ALL_REQUIRED_V1",
  "FixtureVersion": "HSBI-03G-FIXTURE-1",
  "Input": {
    "Fixture": "R2-F-PROJECTION/M_PLUS",
    "quoteSpreadAlreadyInCloseSide": true,
    "additionalSpreadSameWindow": "0.2"
  },
  "Expected": {
    "status": "CONFLICT",
    "reason": "SPREAD_ALREADY_INCLUDED",
    "delta": 0
  },
  "Invariant": "Bid/Ask spread counted once",
  "RequiredSourceEvidence": "Price/cost window receipt",
  "ExpectedFailureReason": "SPREAD_ALREADY_INCLUDED",
  "EvidenceClass": "TEST_SPECIFIED_NOT_RUN",
  "ExecutionStatus": "NOT_RUN",
  "IndependentComponent": "cost ownership",
  "NativeIntegrationRequired": "native BUY/SELL bid/ask"
}
```

### SOURCE-01

```json
{
  "TestID": "SOURCE-01",
  "ContractVersion": "HSBI_CR09_ALL_REQUIRED_V1",
  "FixtureVersion": "HSBI-03G-FIXTURE-1",
  "Input": {
    "Fixture": "R_AUTH",
    "physicalK": [
      "B_MODEL",
      "S_MODEL",
      "1",
      "101",
      "DEAL_NET"
    ],
    "deliveryEvents": [
      "501",
      "999"
    ],
    "body": "same full body"
  },
  "Expected": {
    "physicalSources": 1,
    "newGrant": "0",
    "reason": "REIMPORT_SAME_ECONOMIC_FACT"
  },
  "Invariant": "Delivery event not source",
  "RequiredSourceEvidence": "Independent broker/server/account/deal mapping",
  "ExpectedFailureReason": "REIMPORT_SAME_ECONOMIC_FACT",
  "EvidenceClass": "TEST_SPECIFIED_NOT_RUN",
  "ExecutionStatus": "NOT_RUN",
  "IndependentComponent": "source dedup",
  "NativeIntegrationRequired": "provider reconciliation"
}
```

### SOURCE-02

```json
{
  "TestID": "SOURCE-02",
  "ContractVersion": "HSBI_CR09_ALL_REQUIRED_V1",
  "FixtureVersion": "HSBI-03G-FIXTURE-1",
  "Input": {
    "Fixture": "R_AUTH",
    "event": "501",
    "oldComponents": {
      "profit": "20",
      "commission": "-1.875"
    },
    "newComponents": {
      "profit": "21",
      "commission": "-2.875"
    },
    "sameNet": "18.125"
  },
  "Expected": {
    "status": "CONFLICT",
    "reason": "ALTERED_COMPONENT_SAME_NET",
    "delta": 0
  },
  "Invariant": "Net equality not immutable identity",
  "RequiredSourceEvidence": "Original full component receipt",
  "ExpectedFailureReason": "ALTERED_COMPONENT_SAME_NET",
  "EvidenceClass": "TEST_SPECIFIED_NOT_RUN",
  "ExecutionStatus": "NOT_RUN",
  "IndependentComponent": "body comparison",
  "NativeIntegrationRequired": "real source provider"
}
```

### SOURCE-03

```json
{
  "TestID": "SOURCE-03",
  "ContractVersion": "HSBI_CR09_ALL_REQUIRED_V1",
  "FixtureVersion": "HSBI-03G-FIXTURE-1",
  "Input": {
    "Fixture": "R_AUTH",
    "oldK": [
      "B_MODEL",
      "S_MODEL",
      "1",
      "101"
    ],
    "newK": [
      "B_MODEL",
      "S_MODEL",
      "2",
      "101"
    ],
    "ConsumerAccount": "1"
  },
  "Expected": {
    "status": "REJECT",
    "reason": "WRONG_ACCOUNT_SOURCE",
    "delta": 0
  },
  "Invariant": "Same ticket not same account source",
  "RequiredSourceEvidence": "Account/server receipt",
  "ExpectedFailureReason": "WRONG_ACCOUNT_SOURCE",
  "EvidenceClass": "TEST_SPECIFIED_NOT_RUN",
  "ExecutionStatus": "NOT_RUN",
  "IndependentComponent": "identity validator",
  "NativeIntegrationRequired": "broker multi-account negative qualification"
}
```

### SOURCE-04

```json
{
  "TestID": "SOURCE-04",
  "ContractVersion": "HSBI_CR09_ALL_REQUIRED_V1",
  "FixtureVersion": "HSBI-03G-FIXTURE-1",
  "Input": {
    "Fixture": "R_AUTH",
    "SourceHistory": "MISSING",
    "net": "18.125",
    "runtimeConfirmed": true
  },
  "Expected": {
    "status": "UNAVAILABLE",
    "reason": "SOURCE_AUTHORITY_MISSING",
    "delta": 0
  },
  "Invariant": "Boolean not authority",
  "RequiredSourceEvidence": "History/association receipt absent",
  "ExpectedFailureReason": "SOURCE_AUTHORITY_MISSING",
  "EvidenceClass": "TEST_SPECIFIED_NOT_RUN",
  "ExecutionStatus": "NOT_RUN",
  "IndependentComponent": "authority validator",
  "NativeIntegrationRequired": "provider unavailable path"
}
```

### FUNDING-01

```json
{
  "TestID": "FUNDING-01",
  "ContractVersion": "HSBI_CR09_ALL_REQUIRED_V1",
  "FixtureVersion": "HSBI-03G-FIXTURE-1",
  "Input": {
    "Fixture": "R_AUTH",
    "semantics": "SEQUENTIAL_TRANSITIONS",
    "Free": "14.5",
    "events": [
      {
        "id": "7001",
        "debit": "9",
        "expectedRevision": 5
      },
      {
        "id": "7002",
        "debit": "9",
        "expectedRevision": 6
      }
    ]
  },
  "Expected": {
    "afterFirst": {
      "C": "9",
      "R": "0",
      "F": "5.5",
      "revision": 6
    },
    "second": "REJECT",
    "reason": "INSUFFICIENT_FREE",
    "secondDelta": "0"
  },
  "Invariant": "No refresh of same Free",
  "RequiredSourceEvidence": "Registry initial receipt and durable first outcome",
  "ExpectedFailureReason": "INSUFFICIENT_FREE",
  "EvidenceClass": "TEST_SPECIFIED_NOT_RUN",
  "ExecutionStatus": "NOT_RUN",
  "IndependentComponent": "reference inventory component",
  "NativeIntegrationRequired": "atomic provider+journal/crash"
}
```

### FUNDING-02

```json
{
  "TestID": "FUNDING-02",
  "ContractVersion": "HSBI_CR09_ALL_REQUIRED_V1",
  "FixtureVersion": "HSBI-03G-FIXTURE-1",
  "Input": {
    "Fixture": "R_AUTH",
    "Grant": "14.5",
    "C": "0",
    "R": "0",
    "F": "14.5",
    "reserve": "9",
    "commitReserved": "4",
    "releaseRemaining": "5"
  },
  "Expected": {
    "C": "4",
    "R": "0",
    "F": "10.5",
    "sum": "14.5"
  },
  "Invariant": "Reservation then consume/release conserves grant",
  "RequiredSourceEvidence": "Reservation/action/outcome receipts",
  "ExpectedFailureReason": "NONE_FOR_COMPONENT_PREDICATE; FINANCIAL_AUTHORITY_NOT_GRANTED",
  "EvidenceClass": "TEST_SPECIFIED_NOT_RUN",
  "ExecutionStatus": "NOT_RUN",
  "IndependentComponent": "exact lifecycle component",
  "NativeIntegrationRequired": "durable concurrency/crash"
}
```

### FUNDING-03

```json
{
  "TestID": "FUNDING-03",
  "ContractVersion": "HSBI_CR09_ALL_REQUIRED_V1",
  "FixtureVersion": "HSBI-03G-FIXTURE-1",
  "Input": {
    "Fixture": "R_AUTH",
    "sameSource": true,
    "oldAllocation": "A101",
    "newAllocation": "A999",
    "newGrantRequest": "14.5"
  },
  "Expected": {
    "status": "CONFLICT",
    "reason": "ALLOCATION_ALIAS_NOT_NEW_SOURCE",
    "delta": 0
  },
  "Invariant": "Source uniqueness across allocation keys",
  "RequiredSourceEvidence": "Registry physical-source index",
  "ExpectedFailureReason": "ALLOCATION_ALIAS_NOT_NEW_SOURCE",
  "EvidenceClass": "TEST_SPECIFIED_NOT_RUN",
  "ExecutionStatus": "NOT_RUN",
  "IndependentComponent": "source/global allocation model",
  "NativeIntegrationRequired": "atomic multi-consumer integration"
}
```

### FUNDING-04

```json
{
  "TestID": "FUNDING-04",
  "ContractVersion": "HSBI_CR09_ALL_REQUIRED_V1",
  "FixtureVersion": "HSBI-03G-FIXTURE-1",
  "Input": {
    "Fixture": "R_AUTH",
    "e1": {
      "amount": "9",
      "expectedRevision": 5
    },
    "e2": {
      "amount": "9",
      "expectedRevision": 5
    },
    "interleaving": "both read Free14.5 before commit"
  },
  "Expected": {
    "committedCount": 1,
    "loser": "REVISION_CONFLICT",
    "maxConsumed": "9"
  },
  "Invariant": "CAS serializes concurrent spending",
  "RequiredSourceEvidence": "Two durable registry outcomes",
  "ExpectedFailureReason": "NONE_FOR_COMPONENT_PREDICATE; FINANCIAL_AUTHORITY_NOT_GRANTED",
  "EvidenceClass": "TEST_SPECIFIED_NOT_RUN",
  "ExecutionStatus": "NOT_RUN",
  "IndependentComponent": "reference interleaving model",
  "NativeIntegrationRequired": "native provider concurrency stress"
}
```

### FUNDING-05

```json
{
  "TestID": "FUNDING-05",
  "ContractVersion": "HSBI_CR09_ALL_REQUIRED_V1",
  "FixtureVersion": "HSBI-03G-FIXTURE-1",
  "Input": {
    "Fixture": "R_AUTH",
    "oldEvent": "7001",
    "oldBody": {
      "amount": "9",
      "source": "K1"
    },
    "replayBody": {
      "amount": "9",
      "source": "K1"
    },
    "oldOutcome": "COMMITTED"
  },
  "Expected": {
    "status": "NO_OP",
    "delta": "0"
  },
  "Invariant": "Verified exact replay not debit",
  "RequiredSourceEvidence": "Authentic original body+outcome",
  "ExpectedFailureReason": "NONE_FOR_COMPONENT_PREDICATE; FINANCIAL_AUTHORITY_NOT_GRANTED",
  "EvidenceClass": "TEST_SPECIFIED_NOT_RUN",
  "ExecutionStatus": "NOT_RUN",
  "IndependentComponent": "idempotency comparison",
  "NativeIntegrationRequired": "journal replay/restart"
}
```

### FUNDING-06

```json
{
  "TestID": "FUNDING-06",
  "ContractVersion": "HSBI_CR09_ALL_REQUIRED_V1",
  "FixtureVersion": "HSBI-03G-FIXTURE-1",
  "Input": {
    "Fixture": "R_AUTH",
    "oldEvent": "7001",
    "oldAmount": "9",
    "newAmount": "8.999"
  },
  "Expected": {
    "status": "CONFLICT",
    "reason": "EVENT_BODY_CHANGED",
    "delta": 0
  },
  "Invariant": "Same event different body no effect",
  "RequiredSourceEvidence": "Original full event receipt",
  "ExpectedFailureReason": "EVENT_BODY_CHANGED",
  "EvidenceClass": "TEST_SPECIFIED_NOT_RUN",
  "ExecutionStatus": "NOT_RUN",
  "IndependentComponent": "idempotency comparison",
  "NativeIntegrationRequired": "native codec/body binding"
}
```

### FUNDING-07

```json
{
  "TestID": "FUNDING-07",
  "ContractVersion": "HSBI_CR09_ALL_REQUIRED_V1",
  "FixtureVersion": "HSBI-03G-FIXTURE-1",
  "Input": {
    "Fixture": "R_AUTH",
    "Grant": "14.5",
    "Consumed": "9",
    "correction": "-10",
    "newGrant": "4.5"
  },
  "Expected": {
    "status": "CONFLICT",
    "reason": "CORRECTION_BELOW_COMMITTED_OBLIGATION",
    "Free": "NOT_NEGATIVE_RECOMPUTED",
    "delta": 0
  },
  "Invariant": "Correction not silent rollback of consumption",
  "RequiredSourceEvidence": "Append-only correction causation",
  "ExpectedFailureReason": "CORRECTION_BELOW_COMMITTED_OBLIGATION",
  "EvidenceClass": "TEST_SPECIFIED_NOT_RUN",
  "ExecutionStatus": "NOT_RUN",
  "IndependentComponent": "reconciliation model",
  "NativeIntegrationRequired": "provider/journal recovery"
}
```

### FUNDING-08

```json
{
  "TestID": "FUNDING-08",
  "ContractVersion": "HSBI_CR09_ALL_REQUIRED_V1",
  "FixtureVersion": "HSBI-03G-FIXTURE-1",
  "Input": {
    "Fixture": "R_AUTH",
    "journalOutcome": "UNKNOWN_AFTER_CRASH",
    "registryRevision": "UNRECONCILED",
    "retryDebit": "9"
  },
  "Expected": {
    "status": "UNAVAILABLE",
    "reason": "RESTART_RECONCILIATION_REQUIRED",
    "delta": 0
  },
  "Invariant": "No blind re-consume after unknown outcome",
  "RequiredSourceEvidence": "Durable intent/outcome and broker reconciliation",
  "ExpectedFailureReason": "RESTART_RECONCILIATION_REQUIRED",
  "EvidenceClass": "TEST_SPECIFIED_NOT_RUN",
  "ExecutionStatus": "NOT_RUN",
  "IndependentComponent": "recovery state validator",
  "NativeIntegrationRequired": "crash at every commit boundary"
}
```

### SNAPSHOT-01

```json
{
  "TestID": "SNAPSHOT-01",
  "ContractVersion": "HSBI_CR09_ALL_REQUIRED_V1",
  "FixtureVersion": "HSBI-03G-FIXTURE-1",
  "Input": {
    "Fixture": "R2-F-PROJECTION/M_PLUS",
    "fresh": true,
    "AuthorityReceipt": "NONE"
  },
  "Expected": {
    "status": "UNAVAILABLE",
    "reason": "SNAPSHOT_AUTHORITY_MISSING",
    "delta": 0
  },
  "Invariant": "Fresh flag insufficient",
  "RequiredSourceEvidence": "Independent authority receipt absent",
  "ExpectedFailureReason": "SNAPSHOT_AUTHORITY_MISSING",
  "EvidenceClass": "TEST_SPECIFIED_NOT_RUN",
  "ExecutionStatus": "NOT_RUN",
  "IndependentComponent": "receipt validator",
  "NativeIntegrationRequired": "provider qualification"
}
```

### SNAPSHOT-02

```json
{
  "TestID": "SNAPSHOT-02",
  "ContractVersion": "HSBI_CR09_ALL_REQUIRED_V1",
  "FixtureVersion": "HSBI-03G-FIXTURE-1",
  "Input": {
    "Fixture": "R2-F-PROJECTION/M_PLUS",
    "SnapshotId": 1002,
    "oldContent": "M_MINUS L2",
    "newContent": "M_PLUS L2",
    "oldReceipt": "UNCHANGED"
  },
  "Expected": {
    "status": "CONFLICT",
    "reason": "SNAPSHOT_CONTENT_CHANGED",
    "delta": 0
  },
  "Invariant": "Same basket total not same content",
  "RequiredSourceEvidence": "Full original cost/quote receipt",
  "ExpectedFailureReason": "SNAPSHOT_CONTENT_CHANGED",
  "EvidenceClass": "TEST_SPECIFIED_NOT_RUN",
  "ExecutionStatus": "NOT_RUN",
  "IndependentComponent": "content binding",
  "NativeIntegrationRequired": "native serialization+authority"
}
```

### SNAPSHOT-03

```json
{
  "TestID": "SNAPSHOT-03",
  "ContractVersion": "HSBI_CR09_ALL_REQUIRED_V1",
  "FixtureVersion": "HSBI-03G-FIXTURE-1",
  "Input": {
    "Fixture": "R2-F-PROJECTION/M_PLUS",
    "clockEpoch": "E1",
    "now": 100,
    "issued": 120,
    "skewMax": 2,
    "expiry": 130
  },
  "Expected": {
    "status": "REJECT",
    "reason": "FUTURE_TIMESTAMP_OUTSIDE_SKEW",
    "delta": 0
  },
  "Invariant": "Authority time not caller time",
  "RequiredSourceEvidence": "Trusted monotonic epoch+skew policy",
  "ExpectedFailureReason": "FUTURE_TIMESTAMP_OUTSIDE_SKEW",
  "EvidenceClass": "TEST_SPECIFIED_NOT_RUN",
  "ExecutionStatus": "NOT_RUN",
  "IndependentComponent": "freshness component",
  "NativeIntegrationRequired": "native clock/restart/skew"
}
```

### SNAPSHOT-04

```json
{
  "TestID": "SNAPSHOT-04",
  "ContractVersion": "HSBI_CR09_ALL_REQUIRED_V1",
  "FixtureVersion": "HSBI-03G-FIXTURE-1",
  "Input": {
    "Fixture": "R2-F-PROJECTION/M_PLUS",
    "currentAccount": "1",
    "snapshotAccount": "2",
    "snapshotPosition": "MISSING"
  },
  "Expected": {
    "status": "REJECT",
    "reason": "SNAPSHOT_ACCOUNT_POSITION_MISMATCH",
    "delta": 0
  },
  "Invariant": "Correct account and position required",
  "RequiredSourceEvidence": "Position membership receipt",
  "ExpectedFailureReason": "SNAPSHOT_ACCOUNT_POSITION_MISMATCH",
  "EvidenceClass": "TEST_SPECIFIED_NOT_RUN",
  "ExecutionStatus": "NOT_RUN",
  "IndependentComponent": "identity validator",
  "NativeIntegrationRequired": "provider actual inventory"
}
```

### SNAPSHOT-05

```json
{
  "TestID": "SNAPSHOT-05",
  "ContractVersion": "HSBI_CR09_ALL_REQUIRED_V1",
  "FixtureVersion": "HSBI-03G-FIXTURE-1",
  "Input": {
    "Fixture": "R2-F-PROJECTION/M_PLUS",
    "restart": true,
    "oldEpoch": "E1",
    "newEpoch": "E2",
    "reconciliation": "NONE"
  },
  "Expected": {
    "status": "UNAVAILABLE",
    "reason": "SNAPSHOT_RESTART_UNRECONCILED",
    "delta": 0
  },
  "Invariant": "Old monotonic timestamp not fresh in new epoch",
  "RequiredSourceEvidence": "Restart/reconciliation receipt",
  "ExpectedFailureReason": "SNAPSHOT_RESTART_UNRECONCILED",
  "EvidenceClass": "TEST_SPECIFIED_NOT_RUN",
  "ExecutionStatus": "NOT_RUN",
  "IndependentComponent": "epoch validator",
  "NativeIntegrationRequired": "native terminal restart"
}
```

### OBJECTIVE-01

```json
{
  "TestID": "OBJECTIVE-01",
  "ContractVersion": "HSBI_CR09_ALL_REQUIRED_V1",
  "FixtureVersion": "HSBI-03G-FIXTURE-1",
  "Input": {
    "Fixture": "NF_A_B",
    "candidates": [
      [
        "a",
        "0.2",
        18,
        40,
        2,
        [
          2,
          2
        ]
      ],
      [
        "b",
        "0.3",
        12,
        50,
        3,
        [
          4,
          4
        ]
      ]
    ],
    "allOtherGates": "MODEL_VALID"
  },
  "Expected": {
    "MINIMUM_SAFE_V1": "a",
    "legacyRiskFirst": "b"
  },
  "Invariant": "N precedes Risk after feasibility",
  "RequiredSourceEvidence": "Frozen candidates+required proofs",
  "ExpectedFailureReason": "NONE_FOR_COMPONENT_PREDICATE; FINANCIAL_AUTHORITY_NOT_GRANTED",
  "EvidenceClass": "TEST_SPECIFIED_NOT_RUN",
  "ExecutionStatus": "NOT_RUN",
  "IndependentComponent": "tuple comparator model",
  "NativeIntegrationRequired": "native qualified candidates"
}
```

### OBJECTIVE-02

```json
{
  "TestID": "OBJECTIVE-02",
  "ContractVersion": "HSBI_CR09_ALL_REQUIRED_V1",
  "FixtureVersion": "HSBI-03G-FIXTURE-1",
  "Input": {
    "Fixture": "NF_A_B",
    "candidates": [
      [
        "x",
        "0.1",
        1,
        20,
        1,
        [
          4,
          -1
        ]
      ],
      [
        "a",
        "0.2",
        18,
        40,
        2,
        [
          2,
          2
        ]
      ]
    ],
    "cap": 12
  },
  "Expected": {
    "selected": "a",
    "excluded": "x",
    "reason": "REQUIRED_MARGIN_NEGATIVE"
  },
  "Invariant": "Unsafe low N cannot win",
  "RequiredSourceEvidence": "All level margin receipts",
  "ExpectedFailureReason": "REQUIRED_MARGIN_NEGATIVE",
  "EvidenceClass": "TEST_SPECIFIED_NOT_RUN",
  "ExecutionStatus": "NOT_RUN",
  "IndependentComponent": "feasibility before rank",
  "NativeIntegrationRequired": "native full path"
}
```

### OBJECTIVE-03

```json
{
  "TestID": "OBJECTIVE-03",
  "ContractVersion": "HSBI_CR09_ALL_REQUIRED_V1",
  "FixtureVersion": "HSBI-03G-FIXTURE-1",
  "Input": {
    "Fixture": "NF_TIE",
    "N": "0.2",
    "Risk": 10,
    "Margin": 40,
    "Transitions": 2,
    "candidates": {
      "d": [
        10,
        1
      ],
      "e": [
        4,
        3
      ]
    }
  },
  "Expected": {
    "selected": "e",
    "minimumMargins": {
      "d": 1,
      "e": 3
    }
  },
  "Invariant": "Tie uses minAll, not control",
  "RequiredSourceEvidence": "Frozen R and exact margins",
  "ExpectedFailureReason": "NONE_FOR_COMPONENT_PREDICATE; FINANCIAL_AUTHORITY_NOT_GRANTED",
  "EvidenceClass": "TEST_SPECIFIED_NOT_RUN",
  "ExecutionStatus": "NOT_RUN",
  "IndependentComponent": "min/tuple model",
  "NativeIntegrationRequired": "native aggregator/output binding"
}
```

### OBJECTIVE-04

```json
{
  "TestID": "OBJECTIVE-04",
  "ContractVersion": "HSBI_CR09_ALL_REQUIRED_V1",
  "FixtureVersion": "HSBI-03G-FIXTURE-1",
  "Input": {
    "Fixture": "NF_TIE",
    "numericTuplesEqual": true,
    "tieProfile": "MODEL_ASCII_TOTAL_1",
    "TieIDs": [
      "a",
      "b"
    ],
    "orders": [
      [
        "a",
        "b"
      ],
      [
        "b",
        "a"
      ]
    ]
  },
  "Expected": {
    "selectedEachOrder": [
      "a",
      "a"
    ]
  },
  "Invariant": "Permutation-invariant deterministic total order",
  "RequiredSourceEvidence": "Fixture-only total order; real codec pending",
  "ExpectedFailureReason": "NONE_FOR_COMPONENT_PREDICATE; FINANCIAL_AUTHORITY_NOT_GRANTED",
  "EvidenceClass": "TEST_SPECIFIED_NOT_RUN",
  "ExecutionStatus": "NOT_RUN",
  "IndependentComponent": "tie comparator component",
  "NativeIntegrationRequired": "native UTF-8/roundtrip/version"
}
```

### OBJECTIVE-05

```json
{
  "TestID": "OBJECTIVE-05",
  "ContractVersion": "HSBI_CR09_ALL_REQUIRED_V1",
  "FixtureVersion": "HSBI-03G-FIXTURE-1",
  "Input": {
    "Fixture": "NF_A_B",
    "smallerCandidate": {
      "N": "0.1",
      "evidence": "MISSING"
    },
    "largerCandidate": {
      "N": "0.2",
      "feasible": "MODEL_TRUE"
    }
  },
  "Expected": {
    "qualifiedMinimum": "UNAVAILABLE",
    "reason": "SMALLER_CANDIDATE_UNPROVEN",
    "delta": 0
  },
  "Invariant": "Best-known not proven minimum",
  "RequiredSourceEvidence": "Complete candidate-set receipt",
  "ExpectedFailureReason": "SMALLER_CANDIDATE_UNPROVEN",
  "EvidenceClass": "TEST_SPECIFIED_NOT_RUN",
  "ExecutionStatus": "NOT_RUN",
  "IndependentComponent": "search completeness",
  "NativeIntegrationRequired": "native candidate enumeration"
}
```

### OBJECTIVE-06

```json
{
  "TestID": "OBJECTIVE-06",
  "ContractVersion": "HSBI_CR09_ALL_REQUIRED_V1",
  "FixtureVersion": "HSBI-03G-FIXTURE-1",
  "Input": {
    "Fixture": "NF_A_B",
    "allCandidates": "NO_PROVEN_FEASIBLE",
    "requiredProofs": "COMPLETE_REJECTED"
  },
  "Expected": {
    "status": "NO_SAFE_CANDIDATE",
    "delta": 0
  },
  "Invariant": "No unsafe fallback",
  "RequiredSourceEvidence": "Complete rejection proofs",
  "ExpectedFailureReason": "NONE_FOR_COMPONENT_PREDICATE; FINANCIAL_AUTHORITY_NOT_GRANTED",
  "EvidenceClass": "TEST_SPECIFIED_NOT_RUN",
  "ExecutionStatus": "NOT_RUN",
  "IndependentComponent": "selection component",
  "NativeIntegrationRequired": "native reject propagation"
}
```

### OBJECTIVE-07

```json
{
  "TestID": "OBJECTIVE-07",
  "ContractVersion": "HSBI_CR09_ALL_REQUIRED_V1",
  "FixtureVersion": "HSBI-03G-FIXTURE-1",
  "Input": {
    "Fixture": "R2-F-PROJECTION/M_PLUS",
    "margins": [
      "9",
      "0",
      "2"
    ],
    "allOtherNumericPredicates": true
  },
  "Expected": {
    "status": "REJECT",
    "reason": "NONPOSITIVE_CATCHUP_MARGIN",
    "delta": 0
  },
  "Invariant": "Zero not feasible",
  "RequiredSourceEvidence": "Exact per-level margin fixture",
  "ExpectedFailureReason": "NONPOSITIVE_CATCHUP_MARGIN",
  "EvidenceClass": "TEST_SPECIFIED_NOT_RUN",
  "ExecutionStatus": "NOT_RUN",
  "IndependentComponent": "feasibility component",
  "NativeIntegrationRequired": "native boundary"
}
```

### OBJECTIVE-08

```json
{
  "TestID": "OBJECTIVE-08",
  "ContractVersion": "HSBI_CR09_ALL_REQUIRED_V1",
  "FixtureVersion": "HSBI-03G-FIXTURE-1",
  "Input": {
    "Fixture": "R2-F-PROJECTION/M_PLUS",
    "margins": [
      "9",
      "UNKNOWN",
      "2"
    ],
    "providedMinimum": "2"
  },
  "Expected": {
    "status": "UNAVAILABLE",
    "reason": "MARGIN_SET_INCOMPLETE",
    "delta": 0
  },
  "Invariant": "No minimum over remaining levels",
  "RequiredSourceEvidence": "Frozen R and missing receipt",
  "ExpectedFailureReason": "MARGIN_SET_INCOMPLETE",
  "EvidenceClass": "TEST_SPECIFIED_NOT_RUN",
  "ExecutionStatus": "NOT_RUN",
  "IndependentComponent": "completeness before minimum",
  "NativeIntegrationRequired": "native output contract"
}
```

### COMPATIBILITY-01

```json
{
  "TestID": "COMPATIBILITY-01",
  "ContractVersion": "HSBI_CR09_ALL_REQUIRED_V1",
  "FixtureVersion": "HSBI-03G-FIXTURE-1",
  "Input": {
    "Fixture": "LEGACY_RESULT",
    "legacySchema": "HSBI_BASE_e68",
    "returnTransitionLoss": "3",
    "aggregateMaximum": "12",
    "kindDeclared": false
  },
  "Expected": {
    "qualifiedWorst": "UNAVAILABLE",
    "reason": "LEGACY_METRIC_KIND_UNBOUND"
  },
  "Invariant": "No relabel legacy Far as basket loss",
  "RequiredSourceEvidence": "Pinned source/schema proof",
  "ExpectedFailureReason": "LEGACY_METRIC_KIND_UNBOUND",
  "EvidenceClass": "TEST_SPECIFIED_NOT_RUN",
  "ExecutionStatus": "NOT_RUN",
  "IndependentComponent": "adapter validation",
  "NativeIntegrationRequired": "native persistence/adapters"
}
```

### COMPATIBILITY-02

```json
{
  "TestID": "COMPATIBILITY-02",
  "ContractVersion": "HSBI_CR09_ALL_REQUIRED_V1",
  "FixtureVersion": "HSBI-03G-FIXTURE-1",
  "Input": {
    "Fixture": "LEGACY_PLAN",
    "oldObjective": "RISK_FIRST",
    "requestedObjective": "MINIMUM_SAFE_V1",
    "planReceipt": "OLD_UNCHANGED"
  },
  "Expected": {
    "status": "UNSUPPORTED",
    "reason": "PLAN_OBJECTIVE_VERSION_MISMATCH",
    "delta": 0
  },
  "Invariant": "No silent plan migration",
  "RequiredSourceEvidence": "Old immutable plan receipt",
  "ExpectedFailureReason": "PLAN_OBJECTIVE_VERSION_MISMATCH",
  "EvidenceClass": "TEST_SPECIFIED_NOT_RUN",
  "ExecutionStatus": "NOT_RUN",
  "IndependentComponent": "version gate",
  "NativeIntegrationRequired": "native restart/migration"
}
```

### COMPATIBILITY-03

```json
{
  "TestID": "COMPATIBILITY-03",
  "ContractVersion": "HSBI_CR09_ALL_REQUIRED_V1",
  "FixtureVersion": "HSBI-03G-FIXTURE-1",
  "Input": {
    "Fixture": "R2-F-PROJECTION/M_PLUS",
    "ResultSchemaVersion": "V99",
    "ProofSchemaVersion": "CR09_PROOF_V1"
  },
  "Expected": {
    "status": "UNSUPPORTED",
    "reason": "UNKNOWN_RESULT_SCHEMA",
    "delta": 0
  },
  "Invariant": "Unknown schema fail-closed",
  "RequiredSourceEvidence": "Approved version manifest",
  "ExpectedFailureReason": "UNKNOWN_RESULT_SCHEMA",
  "EvidenceClass": "TEST_SPECIFIED_NOT_RUN",
  "ExecutionStatus": "NOT_RUN",
  "IndependentComponent": "schema decoder",
  "NativeIntegrationRequired": "native codec compatibility"
}
```

### SAFETY-01

```json
{
  "TestID": "SAFETY-01",
  "ContractVersion": "HSBI_CR09_ALL_REQUIRED_V1",
  "FixtureVersion": "HSBI-03G-FIXTURE-1",
  "Input": {
    "Fixture": "D06_A",
    "R_all": "40",
    "O_phys": "-4",
    "C_rem": "1",
    "I": "50",
    "H_in": "4",
    "MinimumProfit": "10",
    "H_gate": "5",
    "Tolerance": "1"
  },
  "Expected": {
    "E": "35",
    "RecoveryResultA": "-19",
    "threshold": "16",
    "ordinaryFinalClose": false,
    "reason": "RECOVERY_RESULT_BELOW_THRESHOLD"
  },
  "Invariant": "Positive E not positive recovery",
  "RequiredSourceEvidence": "Initial group/cost/headroom receipts",
  "ExpectedFailureReason": "RECOVERY_RESULT_BELOW_THRESHOLD",
  "EvidenceClass": "TEST_SPECIFIED_NOT_RUN",
  "ExecutionStatus": "NOT_RUN",
  "IndependentComponent": "exact formula model",
  "NativeIntegrationRequired": "native FinalClose/source integration"
}
```

### SAFETY-02

```json
{
  "TestID": "SAFETY-02",
  "ContractVersion": "HSBI_CR09_ALL_REQUIRED_V1",
  "FixtureVersion": "HSBI-03G-FIXTURE-1",
  "Input": {
    "Fixture": "D05",
    "orderedFills": [
      "-15",
      "100"
    ],
    "cap": "12",
    "priorSticky": false,
    "reset": "NONE"
  },
  "Expected": {
    "currentNet": "85",
    "currentLoss": "0",
    "historicalBreach": true,
    "sticky": true,
    "continuation": "BLOCKED"
  },
  "Invariant": "Positive final net not reset",
  "RequiredSourceEvidence": "Independent ordered history; reset authority unbound",
  "ExpectedFailureReason": "NONE_FOR_COMPONENT_PREDICATE; FINANCIAL_AUTHORITY_NOT_GRANTED",
  "EvidenceClass": "TEST_SPECIFIED_NOT_RUN",
  "ExecutionStatus": "NOT_RUN",
  "IndependentComponent": "sticky history reference model",
  "NativeIntegrationRequired": "journal/restart authority/native"
}
```

### SAFETY-03

```json
{
  "TestID": "SAFETY-03",
  "ContractVersion": "HSBI_CR09_ALL_REQUIRED_V1",
  "FixtureVersion": "HSBI-03G-FIXTURE-1",
  "Input": {
    "Fixture": "ERR038",
    "shortLots": "0.1",
    "multiplier": "1",
    "priceMoveAdverse": "UNBOUNDED",
    "positions": 1
  },
  "Expected": {
    "moneyLossBound": "NOT_PROVEN",
    "reason": "UNBOUNDED_PRICE_MOVE"
  },
  "Invariant": "Bounded lots not bounded monetary loss",
  "RequiredSourceEvidence": "Explicit bounded-market/execution assumptions absent",
  "ExpectedFailureReason": "UNBOUNDED_PRICE_MOVE",
  "EvidenceClass": "TEST_SPECIFIED_NOT_RUN",
  "ExecutionStatus": "NOT_RUN",
  "IndependentComponent": "symbolic loss formula",
  "NativeIntegrationRequired": "separate risk proof, not native sufficient"
}
```

### SAFETY-04

```json
{
  "TestID": "SAFETY-04",
  "ContractVersion": "HSBI_CR09_ALL_REQUIRED_V1",
  "FixtureVersion": "HSBI-03G-FIXTURE-1",
  "Input": {
    "Fixture": "R2-F-PROJECTION/M_PLUS",
    "allMarginsPositive": true,
    "Tmax": "13",
    "cap": "12",
    "controlFarLoss": "3"
  },
  "Expected": {
    "status": "REJECT",
    "reason": "TRANSITION_CAP_EXCEEDED",
    "delta": 0
  },
  "Invariant": "Far loss cannot bypass basket cap",
  "RequiredSourceEvidence": "Complete basket maximum proof",
  "ExpectedFailureReason": "TRANSITION_CAP_EXCEEDED",
  "EvidenceClass": "TEST_SPECIFIED_NOT_RUN",
  "ExecutionStatus": "NOT_RUN",
  "IndependentComponent": "gate component",
  "NativeIntegrationRequired": "native rejection before safe array"
}
```

## Будущая нативная квалификация

Нужны compiler/terminal build, pinned source SHA, exact fixture/vector IDs, actual instrument properties, source/market/cost/risk/margin authority receipts, numeric/codec versions, expected/actual/status/log, reached branch, состояние before/after и financial delta. Calculation-only broker wrappers не означают dispatch. Top solver отвергает injection: ранний reject fake symbol/unit-test режима нельзя выдать за проверку успешной ветви151.

Компонентные проверки set/tuple/money/identity могут выполняться отдельно после разрешения подходящей среды; положительный результат reference модели не переносится на production. Полная интеграция требует реального provider и durable journal; crash/concurrency обязательны для funding authority. Исторические 7 PASS/16 FAIL, включая два contract-dependent сценария, не редактируются.

OpenQuestions: owner-selected semantics/obligation/eligibility; actual receipts/profiles; где и кем будет выполнен native stage.
AcceptanceCriteria: все inherited и новые vectors имеют fixed inputs/expected/invariant/evidence; независимый oracle; отрицательные/unknown cases delta0; published artifact отличает NOT_RUN от PASS/FAIL.
