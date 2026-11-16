# HSBI-03D — Numeric и native qualification

Версия HSBI-03D-REMOTE-R1; source SHA6543bc2c0d125f5f7e02f78a092b0412a2e34626.
NATIVE_MQL5_TESTS=NOT_RUN. Этот файл задаёт испытания, не содержит новых PASS.
Ballot D10–D12,D15 и source catalog: [review](HSBI_03D_INDEPENDENT_CONTRACT_REVIEW_RU.md), [ballot](HSBI_03D_OWNER_APPROVAL_BALLOT_RU.md).

## Evidence discipline

STATIC_REVIEWED исходный код; MATH_DERIVED условная арифметика; COUNTEREXAMPLE_CONFIRMED опровержение утверждения без production runtime; HISTORICAL_TEST_RESULT старый artifact; TEST_SPECIFIED_NOT_RUN новые vectors; NATIVE_NOT_RUN нет MQL5 исполнения; UNVERIFIED missing facts.
Reference/C++ PASS не native PASS. Compile не economic correctness. Все новые vectors ниже TEST_SPECIFIED_NOT_RUN.

Исторический Tests/Close/production_subset_results.json blob192fe577764407499c6334d8e07c55ad78afeed7: 7 PASS/16 FAIL,exit1. Expected неизменны. COMMITTED-UNDERALLOCATION-PROPOSED и P0-03-EXHAUSTED-PROPOSED contract-dependent и хранятся отдельно; ни один не перезапущен.

## Fixed positive/negative vectors

| ID | Вход | Expected |
|---|---|---|
| T01+ | G100; grants20×5; bucket C7,R3,F10 | both identities true |
| T01− | committed G100 grants90 | REJECT,no mutation |
| T02+ | confirmed50,grant40,C10,R5 | bookFree25 только с authority |
| T02− | projected50/runtimeConfirmed=true,no actual receipt | spendable0/UNAVAILABLE |
| T03+ | Core40,Trend10,Small100 | Big basis50 |
| T03− | Core−10,Trend0,Small100 | Big0,economic90 |
| T04+ | gain40,absoluteLoss20,buffer1 | preview margin19 |
| T04− | baseline40,absolute50,reserve30 | coverage REJECT |
| T05+ | fill−12,cap12 | current12,stickyfalse |
| T05− | fills−15,+100,cap12 | net85,current0,peak15,stickytrue |
| T06+ | gross100,commission−2,swap−1,fee−1 | net96,not92 |
| T06− | Initial50,other−10,open−5,policyA | Economic35,Recovery−15 |
| T07+ | exact committed replay after restart | NOOP,same balances/revision |
| T07− | UNKNOWN resend/release | BLOCKED |
| T08+ | same K/body,new ObservationID | same source,no grant |
| T08− | same K,changed components/same net | CONFLICT |
| T09+ | losses10,5,margins9,2,valid proofs | all finite required levels feasible |
| T09− | losses10,5,margins9,−11 | REJECT regardless max-loss level |
| T10+ | minorG10000,C3000,R2000,F5000 | exact equality |
| T10− | MAX+1,abs(MIN),MIN×−1 | checked overflow reject |
| T11+ | aggregate HALF_EVEN scale100,0.005+0.005 | posted1 minor |
| T11− | component result0 under aggregate receipt | profile conflict |
| T12+ | same fact through two qualified codecs | one logical source |
| T12− | truncated/unknown schema/trailing bytes | strict decoder REJECT |
| T13+ | exact clock now100,ts95,TTL10 | fresh |
| T13− | ts101 or89 | future/stale reject |
| T14+ | Free50,first consume30 commit | Free20 |
| T14− | second30 at old revision | conflict,no second debit |
| T15+ | ulong18446744073709551615 roundtrip | exact,no double cast |
| T15− | nonfinite money/invalid enum/subminimum volume | REJECT |
| T16+ | complete mappingG100,C20,R10,F70 | preserve balances,replayNOOP |
| T16− | available100,no namespace/consumed | quarantine,spendable0 |

T14 специфицирует serializable runtime, не считается выполненным concurrency test.

## Обязательная native matrix

| Группа | Fixed inputs и expected |
|---|---|
| I64 | MIN=−9223372036854775808,MIN+1,−1,0,1,MAX−1,MAX=9223372036854775807; MAX+1,MIN−1,abs/negateMIN,MIN×−1 reject before operation |
| Intermediates | MAX+MAX−MAX−MAX math0, unsafe sequence forbidden; alternative algorithm proof separately |
| U64/Revision | 0,9223372036854775807,9223372036854775808,18446744073709551615 exact encode/decode; MAX revision increment unavailable |
| Currency | explicit scales1/100/1000/10^8 fixture profiles; ±0.005,±0.015 component/aggregate HALF_EVEN; compare independently posted receipt |
| Binary64 | ±0,smallest positive subnormal,smallest normal,largest finite,NaN,±Inf; finite values roundtrip in declared profile,nonfinite reject,Z maps −0 to0 |
| Underflow | positive preview loss0.004 at cents scale remains nonzero preview obligation; smaller subnormal cases record actual native behaviour,not guessed support |
| Volume | min0.01/step0.01:0.009 reject;raw0.256→floor0.25/ceil0.26; min0.03/step0.02 distinguishes origin profile |
| Price | tick0.25:100.25 valid,100.10 offgrid; priceDigits separate from money precision |
| Codec | max IDs,negativezero,subnormal,UTF8 multibyte byte lengths; embedded NUL policy; truncation,unknownschema,extra bytes,oversize,duplicate fields reject |
| Journal | same receipt changed body; crash before/after each stage;torn snapshot; replay no second debit |
| Registry | concurrent30+30 from50;source alias/import replay;multi-source transfer;restart during reserve/consume/release |
| D05 | −15,+100 vs+100,−15 cap12;restart every prefix;incomplete/corrupt order;unauthorized/stale/duplicate reset;no autoresume |

F64Z arithmetic reconstruction/byte shifts/string framing, T17Z formatting/exponent/roundtrip и u64 conversions проверяются на конкретном MQL5 build. Ни один candidate не утверждён автоматически. R0F candidate caps4096 UTF8 bytes/string,65536 record не являются доказанной decoder qualification; профиль лимитов должен войти в frozen manifest до tests.

## Требования к артефакту исполнения

Каждый результат: source SHA,test version,compiler/terminal build,broker/fixture profile,exact input,expected,actual,status/exit,полный log. Test harness dispatch disabled; production trading не разрешается. Native test implementation/runner этим audit-only этапом не создаётся и не запускается.

Numeric approval bundle D10+D11+D12+D15 включает profile/scale/posting/rounding/range/intermediates/zero/subnormal/schema/codec/UTF8/caps и native goldens. Evidence gaps D11/D12 остаются BLOCKED_BY_EVIDENCE; D15 ready только как qualification requirement.
