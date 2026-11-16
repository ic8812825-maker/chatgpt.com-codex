# HSBI-03D — P0 remediation crosswalk

Source SHA 6543bc2c0d125f5f7e02f78a092b0412a2e34626; версия HSBI-03D-REMOTE-R1; audit-only.
14 P0 рассмотрены; 0 закрыто. ERR-ID сохранены. Статусы STATIC_REVIEWED/MATH_DERIVED, не runtime PASS.
S01–S20: [точный source catalog](HSBI_03D_INDEPENDENT_CONTRACT_REVIEW_RU.md#зафиксированные-источники).
Historical register: Reports/HSBI_AUDIT03_CLOSE_FINDINGS_RECONCILIATION_RU.md, исходные R11 dependency/test/unapplied plans остаются неизменными.

Пакеты этого crosswalk описывают требуемую работу, не новое разрешение implementation:
A identity/provider; B exact ledger/registry; C finite/domain guards; D reserve/all-level proofs; E journal/restart/context.
G=local guard; P=independent provider; J=durable atomic journal; M=отдельное математическое доказательство.

| ERR | Причина и source location | Минимальный контрпример | Контракт; минимальный пакет | Guard/provider/journal/proof и критерий закрытия |
|---|---|---|---|---|
| ERR-001 | S01:9–10 incomplete economic body compare | equal net, different profit/commission/role | D08/D10/D12; A+C | G full body/enums/finite; P association; J old receipt. Production negative cases/native domain и обязательность caller paths |
| ERR-002 | S01:6–7 key без broker/server/account | same ticket two accounts | D08/D16; A | P stable namespace; G key/body binding; J registration. Cross-account isolation и legacy quarantine |
| ERR-004 | S02:8 duplicate по total | vector20,20,20,20,20 против0,40,20,20,20 | D01/D07; B | G immutable full manifest; J full old receipt. Changed-vector conflict, exact replay NOOP |
| ERR-005 | S02:7 incomplete components/phase | buckets−1,101,0,0,0 source100 | D01/D10/D11; B+C | G finite/nonnegative/phase; M both identities; J atomic commit. Draft/committed cases, no changed historical expected |
| ERR-007 | S04:44–50/S05:25–30 source/allocation/consumption binding missing | valid consumption belongs to another allocation | D02/D07/D08/D14; A+B+D | G full tuple; P registry; J receipt. Cross-source/cross-allocation rejection |
| ERR-008 | S04:63–70 exhausted source reuse, unallocated branch | source50 consumed50 eligible50→gain40 at share0.8 | D01/D02/D14; B+D+E | G lifecycle; P+J global inventory. Exhaustion,races,restart replay; local guard alone not global proof |
| ERR-009 | S09:6 no complete finite/range guard input+limits | NaN limit/input evades ordered checks | D11/D15; C | G all inputs/limits; prove mandatory caller integration; native NaN/Inf and valid control |
| ERR-010 | S10:9–22 barrier finite/retry outcome | NaN fill; UNKNOWN locally retryable | D07/D11/D15; C+E | G finite/outcome/volume; P actual fills; J reconciliation. No resend/release on unknown, crash/retry tests |
| ERR-011 | S03:4–5 incomplete money state validation | Inf bucket; unvalidated valid/revision fields | D01/D10/D11; B+C | G complete domain; exact schema; J revision/state consistency. Nonfinite/control cases |
| ERR-012 | S11:19–25,45–53; S20:5–6 incomplete slot uniqueness | FAR in far and candidate not counted together | D07/D08; E | G all slots/physical positions; P ownership; mandatory call sites, promotion/restart tests |
| ERR-013 | S07:60–72,119–124 caller provenance/self-built identity | internally consistent DTO without actual origin | D02/D08/D13/D14; A+D+E | P actual source+association; J receipt. Equality guard alone cannot close; authentic/forged causal pair |
| ERR-033 | Docs/08:12–24; S04:44–70,S13:5–7 missing global funding authority | same deal consumed through two allocation/event IDs | D01/D02/D07/D08/D14; B+D+E | P+J serializable global inventory; M conservation; real concurrency/crash/restart qualification |
| ERR-038 | Docs/04:33–36 unproven monetary bound | fixed SELL volume1,unbounded price M→lossM | CR09/D11; separate M | Explicit bounded market/execution/cost model and proof; no guard/provider/journal alone closes it; OPEN |
| ERR-048 | S04:24–76 scalar/proof value binding missing | proof10,scalar100 yields false positive margin | D02/D04/D08/D13; A+D | G amount/basis/identity; P receipt. Direct evaluator negative tests. S07:121–122 derives scalars: do not automatically claim solver exploit |

## Общий критерий приёмки исправления

Closed только после нормативного выбора, конкретного production change отдельного разрешённого этапа, positive/negative evidence на production path, доказанной обязательности guard, provider evidence там где нужно и native/crash/concurrency evidence соответствующего свойства. Наличие helper или reference-model PASS недостаточно. В этом этапе production не изменялся.

## Исторические тесты

Tests/Close/production_subset_results.json, blob192fe577764407499c6334d8e07c55ad78afeed7: 7 PASS / 16 FAIL; exit1. HISTORICAL_TEST_RESULT, не rerun.
COMMITTED-UNDERALLOCATION-PROPOSED и P0-03-EXHAUSTED-PROPOSED — два contract-dependent сценария; их expected не изменять и не выдавать за доказанные нарушения любого возможного legacy representation до D01/D16. Независимая необходимость исключить повторное расходование сохраняется.

Новый compile/test/mutation/native запуск отсутствует. Все предложенные closure tests TEST_SPECIFIED_NOT_RUN. P0_CLOSED=0.
