# HSBI-03E — Numeric test vectors

Версия: **HSBI-03E-R1**. SOURCE_COMMIT_SHA=`b5ca9d377d454dfbec63ece76dd1c759abc3656d`.
Репозиторий `ic8812825-maker/chatgpt.com-codex`, ветка `work`, все относительные source paths внутри `MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/`.
Статус: **PROPOSED / AWAITING_OWNER_DECISION**. Ни один текст не APPROVED. Нормативный выбор, architecture/provider и implementation evidence — разные gates.
STATIC_REVIEWED означает чтение исходного текста; MATH_DERIVED — вывод при указанных предпосылках; COUNTEREXAMPLE_CONFIRMED — опровержение утверждения, не runtime PASS; HISTORICAL_TEST_RESULT — старый artifact; все новые vectors TEST_SPECIFIED_NOT_RUN; NATIVE_NOT_RUN. Новых compile/runtime/mutation/native tests не выполнялось.
UNAVAILABLE — обязательное evidence отсутствует; CONFLICT — доказательства противоречат; REJECT — доказанное нарушение домена/предусловия. Все три запрещают новый effect; финансовая delta=0. NO_OP возможен только по валидному полному старому receipt.
Публикация отчёта не утверждает контракт, не закрывает P0 и не разрешает production/R1.1/dispatch/trading.

VectorSetId=HSBI_03E_NUMERIC_VECTORS_V1;Revision=HSBI-03E-R1;Status=TEST_SPECIFIED_NOT_RUN.
Все expected ниже заданы математически/литерально; runner/production/native не исполнялись.
Источники: Docs08:6–24;Docs25:3–7;R0F NUMERIC_CODEC_OPTIONS17–35;R0G CODEC_DECISION9–34;Include/Money/HSBI_CostModel.mqh:11–18;Include/Planning/HSBI_BrokerGrid.mqh:8–36;EconomicLedgerTypes:6–12.
Manifest:[HSBI_NUMERIC_CONTRACT_MANIFEST_V1](HSBI_03E_NUMERIC_CONTRACT_MANIFEST_V1_RU.md).
Native golden source: Tests/Evidence/NEXT_STAGE_02B_R0F_CODEC_GOLDENS.json blob e506b9f3867dc98936f025603871653e72dd0620;MQL5Compile=NOT_RUN.

## Fixture profiles и проверяемая граница

M2: CurrencyCode=XTEST2,CurrencyDigits2,S100,ExactMoney signed64,verified aggregate HALF_EVEN только в явно указанных conversion vectors. Это synthetic profile,не реальная валюта/брокерский default. Положительные settled acceptance cases предполагают independent expected posted receipt;без него тот же amount UNAVAILABLE.
G0: O_v0,min0.03,max1.00,step0.02;price origin0,tick0.25,point0.01. GMIN: тот же min/step,origin0.03. Их различие не выбор production grid.
MIN=−9223372036854775808;MAX=9223372036854775807 minor. Тесты domain helper отдельно от source/funding authorization;accepted number не grant.

## Exact/range/rounding vectors

| ID | Fixed input | Expected | Formula/invariant |
|---|---|---|---|
| N01 | M2,minor0 | numeric0;zero consume reject | balances≥0;consume a>0 |
| N02 | M2,signed minorMIN | signed fact representable;eligible positive grant0;abs/neg separate reject | MIN≤x≤MAX;negative source not funds |
| N03 | M2,minorMAX | exactMAX;main92233720368547758.07 | main=minor/100 |
| N04 | minorMAX+1 lexeme9223372036854775808 | REJECT(OVERFLOW) before cast | x≤MAX |
| N05 | minorMIN−1 lexeme−9223372036854775809 | REJECT(OVERFLOW) | x≥MIN |
| N06 | add(MAX,1) | REJECT,no mutation | checked upper bound |
| N07 | sub(MIN,1) | REJECT | checked lower bound |
| N08 | abs(MIN),neg(MIN),mul(MIN,−1),div(MIN,−1) | all REJECT | positive2^63 unrepresentable |
| N09 | add sequenceMAX+MAX−MAX−MAX | naive sequence REJECT at second term;no false PASS from final0 | every intermediate bounded |
| N10 | scale main exact92233720368547758.08 by100 | REJECT | scaled9223372036854775808>MAX |
| N11 | exactdecimal1.005,M2 aggregateHALF_EVEN |100 minor |100.5 tie→even100 |
| N12 | exactdecimal1.015,same |102 minor |101.5 tie→even102 |
| N13 | exactdecimal−1.005,same |−100 minor | symmetric ties,not truncation |
| N14 | exactdecimal−1.015,same |−102 minor |−101.5 tie→even−102 |
| N15 | components0.005,0.005 | component posting0+0=0;aggregate posting1 | stage explicit,not interchangeable |
| N16 | components−0.005,−0.005 | component0;aggregate−1 | signed stage distinction |
| N17 | posted profileD9 (outside proposed adapter0…8),wellformed | UNAVAILABLE(UNSUPPORTED_PRECISION) | no guessed downgrade to8/2 |
| N18 | D unknown / booltrue instead integer | unknown→UNAVAILABLE;bool→REJECT | exact type/domain |
| N19 | CurrencyCode missing or foreign profile ID | REJECT missing;CONFLICT receipt mismatch | currency/profile binding |
| N20 | projectedLoss exact0.004 atM2 | stays positive preview;not proved zero;gate needs error bound | preview≠posted rounding |
| N21 | preview rawNaN,+Inf,−Inf | REJECT | finite-only |
| N22 | floating preview helper ADD(1e308,1e308) | overflow output→ERROR/UNAVAILABLE,no permit | finite inputs not sufficient |
| N23 | rational share MAX×2/3 with naivei64 product | checked reject unless approved safe reduced/wide method | product overflow despite final fit |
| N24 | G101,shares1/4,1/4,1/4,1/4 | first4=(25,25,25,25),Residual1 | floor grants;Σ=101 |
| N25 | G100,C30,R20,F50,reserve20 | C30,R40,F30 | conservation100 |
| N26 | same sourceFree50,concurrent30+30,same revision | at most one commit,Free20;second conflict | atomic balance+receipt+revision |
| N27 | actual components60,−2,−7,−1 | net50 exactly in declared posted basis | signed component sum,each once |

## Replay/identity vectors

B0 — полный RecordFields/RecordBinaryHex source golden,не сокращённый DTO. LogicalK=(B1,S1,1,11),cycle1,position13,Action1,Event31;profit60,swap−2,commission−7,fee−1,net50. Original authenticated receipt/store frozen до mutations.

| ID | Fixed input | Expected | Invariant |
|---|---|---|---|
| R01 | exactB0 existing key/body/receipt,even after source exhausted | NO_OP,delta0;no new funds | validate old receipt before current new-event gates |
| R02 | B0 profit61,commission−8,net50,rest same;caller recomputes hash | CONFLICT | same K/altered components not equal |
| R03 | B0 position14 orroleBigTrend | CONFLICT | full body compare |
| R04 | B0 new ObservationID99,immutable Event31/body unchanged | same source,NO_OP economic effect | observation not source |
| R05 | B0 AccountLogin2 with properly different source association | distinct K,but NEW_IDENTITY not funding | namespace |
| R06 | B0 codec alternate known mapping,decoded body same | same K;no newgrant | codec-independent source |
| R07 | changed codec/profile without approved mapping | UNAVAILABLE | no silent legacy/coercion |
| R08 | old record lacks broker/server/consumed/posting profile | quarantine/spendable0 | unknown not default |

## Codec/frame/UTF8 vectors

C0=полный literal RecordBinaryHex из source golden в указанном blob;T0=RecordTextHex оттуда. Они fixed by source SHA+blob+JSON key. Строки ниже задают однозначную mutation specific field bytes,не повторный subject encoder как oracle.

| ID | Input | Expected | Invariant |
|---|---|---|---|
| C01 | C0/T0 unchanged known fixture profiles | match literal golden;semanticB0 | full field/name order |
| C02 | C0 remove final one byte | REJECT(TRUNCATED) | exact lengths/complete record |
| C03 | C0 append00 | REJECT(TRAILING_BYTES) | no extra data |
| C04 | C0 Broker value bytes4231 replaceC0AF,len stays2 | REJECT(INVALID_UTF8) | overlong sequence forbidden |
| C05 | C0 Broker value replaceEDA080,len3 with correctly updated field length | REJECT(INVALID_UTF8_SURROGATE) | no UTF8 surrogate |
| C06 | C0 Broker valueF4908080,len4 | REJECT(CODEPOINT_RANGE) | ≤U+10FFFF |
| C07 | C0 Broker length4097 before allocation | REJECT(RESOURCE_CAP) | ≤4096 proposed limit |
| C08 | C0 с00 padding до total65537 bytes | REJECT(RESOURCE_CAP) before allocation | ≤65536 including framing |
| C09 | C0 SchemaVersion value2 exactwellformedu64 | UNAVAILABLE(SCHEMA_VERSION) | no semantic reinterpretation/newincome |
| C10 | headerHSBI-F64Z-2+00,rest C0 payload | UNAVAILABLE(CODEC_VERSION) | known grammar unsupported version |
| C11 | C0 duplicate Broker name/value before Server | REJECT(FIELD_ORDER/DUPLICATE) | exact29 fields |
| C12 | integeru64Account=9223372036854775808 | REJECT(FIELD_DOMAIN) | account signedMAX,wireu64 not permission |
| C13 | u64DealTicket=18446744073709551615 | integer exact roundtrip;other domain gates separately | no double cast |
| C14 | value d8000000000000000 on Z strict wire | REJECT(NONCANONICAL_ZERO);encoder raw−0 emits+0 | canonical Z |
| C15 | d7ff0000000000000,dfff0000000000000,d7ff8000000000000 | REJECT(NONFINITE) | ±Inf/NaN |
| C16 | T17 integeri2:01 or i2:+1 or i2:−0 | REJECT(NONCANONICAL_INTEGER) | no leadingzero/plus/negativezero |
| C17 | T17 one token1.0e+000 instead fixed scientific17 | REJECT(NONCANONICAL_FLOAT) | exact formatter profile,not any roundtrip |
| C18 | string content U+00E9 vs U+0065 U+0301 (UTF8C3A9 vs65CC81) | distinct strings/bodies,no NFC folding | exact UTF8 identity |
| C19 | embedded00 in string value | REJECT(NUL_POLICY) | zero terminator not string content |
| C20 | nativeUTF16 unpaired high surrogateD800 before encode | REJECT(INVALID_UNICODE) | no lossy replacement |

C05/C06 mutations reconstruct only required length/value of Broker;remaining names/values byte-for-byte C0. C07 no actual4097-byte allocation required to reject declared oversized length. C16−0 uses ASCII minus0 bytes2D30,not Unicode minus;typography in table semantic notation. Valid UTF8 byte lengths include UTF8 multibyte values,не count of MQL characters.

### Literal scalar goldens

| ID | Raw binary64 input | F64Z expected bits | T17Z expected token |
|---|---|---|---|
| zero | 0x0.0p+0 | 0000000000000000 | 0.0000000000000000e+000 |
| negative-zero | -0x0.0p+0 | 0000000000000000 | 0.0000000000000000e+000 |
| one | 0x1.0000000000000p+0 | 3ff0000000000000 | 1.0000000000000000e+000 |
| negative-five | -0x1.4000000000000p+2 | c014000000000000 | -5.0000000000000000e+000 |
| one-tenth | 0x1.999999999999ap-4 | 3fb999999999999a | 1.0000000000000001e-001 |
| min-normal | 0x1.0000000000000p-1022 | 0010000000000000 | 2.2250738585072014e-308 |
| min-subnormal | 0x0.0000000000001p-1022 | 0000000000000001 | 4.9406564584124654e-324 |
| max-finite | 0x1.fffffffffffffp+1023 | 7fefffffffffffff | 1.7976931348623157e+308 |

Для finite inputs Decode(Encode(x))=x в Z semantic domain;raw negativezero sign не preserved. Source golden MQL5Compile NOT_RUN. Все8 scalar native roundtrip должны быть исполнены отдельно,включая min subnormal и max finite. Не объявлять арифметическое bit-reconstruction нативно корректным по Python result.

## Price/volume grid vectors

| ID | Input | Expected | Formula/invariant |
|---|---|---|---|
| G01 | G0 volume0.04 | valid | (0.04−0)/0.02=2,bounds |
| G02 | G0 volume0.03 | offgridREJECT |1.5 not integer |
| G03 | GMIN volume0.03 | valid | (0.03−0.03)/0.02=0 |
| G04 | GMIN volume0.04 | offgridREJECT |0.5 not integer |
| G05 | G0 volume0.02 | subminimumREJECT despite grid |0.02<0.03 |
| G06 | volume0.256,min0.01,max1,origin0,step0.01 | floor0.25/ceil0.26 thenrevalidate | purpose rounding |
| G07 | price100.25/tick0.25/origin0 | valid |401 ticks |
| G08 | price100.10/tick0.25 | REJECT |400.4 ticks |
| G09 | price Digits2,tick0.25,price100.10 | stillREJECT | price digits not tick grid |
| G10 | CurrencyDigits from symbolDigits5 without account profile | UNAVAILABLE | money precision authority |
| G11 | inactive optional Trend tagged0 | allowed only explicit inactive policy | not active below-min lot |
| G12 | active mandatory Core0 or negative volume | REJECT | active>0 andbounds |
| G13 | step0/NaN/Inf ororigin unknown | REJECT invalid;UNAVAILABLE unknown | no divide/normalize by invalid grid |

## Acceptance evidence и unresolved

Нужен test artifact на конкретном source/compiler/terminal build с exact inputs,expected/actual,status,full log и provider/profile IDs;native tests,hostile decoder,concurrency и crash отдельно. Compare full body and scalar goldens независимо от subject codec. Native unsupported subnormal/precision→domain unavailable,не исключить failing vector молча.
Исторические R0F116PASS/R0G128PASS и C++7PASS/16FAIL сохранены,не rerun;contract-dependent two old scenarios не переписаны.
Unresolved: final codec,actual profile/mapping,error bounds,provider/durability,native evidence. См.[snapshot cases](HSBI_03E_SNAPSHOT_AUTHORITY_CONTRACT_RU.md),[R11 gates](HSBI_03E_R11_GATE_MATRIX_RU.md),[ballot](HSBI_03E_OWNER_FINAL_DECISION_BALLOT_RU.md).
