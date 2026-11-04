# 02B-R0A — сквозные денежные инварианты

Проверенная база: `cb5e55cb38aa4f2eb5b58e5218462c6738f3097a`, ветка `work`, UTC проверки `2026-11-04T01:18:36Z`. Режим `NORMATIVE_FREEZE_PREPARATION / AUDIT_AND_TEST_ONLY`. Все новые экономические формулировки — **PROPOSED**, не утверждённый production-норматив. `STAGE_02B_R1_IMPLEMENTATION_ALLOWED=NO`.

CurrentStatus относится к текущему production/source доказательству, а ProposedTestStatus — только к выполненным тестам кандидата. Прохождение test-only oracle не меняет CurrentStatus. Конфликты/неизвестный runtime не повышаются до PASS.

## INV-01

**InvariantID:** INV-01

**FormalDefinition:** ΣGrant=N; Remaining+Consumed=Grant; Available=Remaining-Reserved>=0

**NormativeSource:** D-01

**AffectedFunctions:** HSBI_ValidateAllocationConservation

**PositiveExample:** 50=40+10

**Counterexample:** 50!=50+10

**TestID:** D01-no-double-count

**CurrentStatus:** CONFLICT

**ApprovalRequired:** True

**ProposedTestStatus:** PASS

Источник теста: `Tests/Static/check_hsbi_02b_r0a_normative_contracts.py`; точные значения — `Tests/Evidence/NEXT_STAGE_02B_R0A_PROPOSED_TESTS.json`. Нормативный ID связан с точным текстом в [кандидате фиксации](NEXT_STAGE_02B_R0A_CONTRACT_FREEZE_CANDIDATE_RU.md).

## INV-02

**InvariantID:** INV-02

**FormalDefinition:** Один account-scoped DealTicket имеет один immutable economic payload

**NormativeSource:** D-08

**AffectedFunctions:** HSBI_BuildSourceDealKey / HSBI_ClassifyEconomicDuplicate

**PositiveExample:** same record =>same digest

**Counterexample:** Profit55/-5 vs60/-10 при Net50

**TestID:** L01-component-digest

**CurrentStatus:** FAIL

**ApprovalRequired:** True

**ProposedTestStatus:** PASS

Источник теста: `Tests/Static/check_hsbi_02b_r0a_normative_contracts.py`; точные значения — `Tests/Evidence/NEXT_STAGE_02B_R0A_PROPOSED_TESTS.json`. Нормативный ID связан с точным текстом в [кандидате фиксации](NEXT_STAGE_02B_R0A_CONTRACT_FREEZE_CANDIDATE_RU.md).

## INV-03

**InvariantID:** INV-03

**FormalDefinition:** Ни один debit не может потребить один остаток дважды

**NormativeSource:** D-07

**AffectedFunctions:** HSBI_EvaluateReserveCatchUp / consumption registry

**PositiveExample:** E1=10 из50 =>40

**Counterexample:** E2=41 при40

**TestID:** D07-next41

**CurrentStatus:** UNPROVEN

**ApprovalRequired:** True

**ProposedTestStatus:** PASS

Источник теста: `Tests/Static/check_hsbi_02b_r0a_normative_contracts.py`; точные значения — `Tests/Evidence/NEXT_STAGE_02B_R0A_PROPOSED_TESTS.json`. Нормативный ID связан с точным текстом в [кандидате фиксации](NEXT_STAGE_02B_R0A_CONTRACT_FREEZE_CANDIDATE_RU.md).

## INV-04

**InvariantID:** INV-04

**FormalDefinition:** ExpectedProof=AuthorityRecord+Context, а не SubmittedProof

**NormativeSource:** D-08

**AffectedFunctions:** HSBI_NewFarProofIdentity / HSBI_SolveNewFar assembly

**PositiveExample:** independent proof match

**Counterexample:** foreign identity + self-copy

**TestID:** D08-self-copy-position

**CurrentStatus:** FAIL

**ApprovalRequired:** True

**ProposedTestStatus:** PASS

Источник теста: `Tests/Static/check_hsbi_02b_r0a_normative_contracts.py`; точные значения — `Tests/Evidence/NEXT_STAGE_02B_R0A_PROPOSED_TESTS.json`. Нормативный ID связан с точным текстом в [кандидате фиксации](NEXT_STAGE_02B_R0A_CONTRACT_FREEZE_CANDIDATE_RU.md).

## INV-05

**InvariantID:** INV-05

**FormalDefinition:** ActualDealNetRaw=Profit+Swap+Commission+Fee со знаками брокера

**NormativeSource:** D-01

**AffectedFunctions:** HSBI_ValidateEconomicRecord / HSBI_TryActualDealNet

**PositiveExample:** 55-5=50

**Counterexample:** 56-5 != recorded50

**TestID:** D01-components-sum-mismatch

**CurrentStatus:** FAIL

**ApprovalRequired:** True

**ProposedTestStatus:** PASS

Источник теста: `Tests/Static/check_hsbi_02b_r0a_normative_contracts.py`; точные значения — `Tests/Evidence/NEXT_STAGE_02B_R0A_PROPOSED_TESTS.json`. Нормативный ID связан с точным текстом в [кандидате фиксации](NEXT_STAGE_02B_R0A_CONTRACT_FREEZE_CANDIDATE_RU.md).

## INV-06

**InvariantID:** INV-06

**FormalDefinition:** Projected не конвертируется непосредственно в actual/grant/available

**NormativeSource:** D-02

**AffectedFunctions:** HSBI_EvaluateBasketMoney / MoneyState conversion

**PositiveExample:** actual0=>available0

**Counterexample:** projected100 без close

**TestID:** D02-no-implicit-ProjectedBasketNet

**CurrentStatus:** UNPROVEN

**ApprovalRequired:** True

**ProposedTestStatus:** PASS

Источник теста: `Tests/Static/check_hsbi_02b_r0a_normative_contracts.py`; точные значения — `Tests/Evidence/NEXT_STAGE_02B_R0A_PROPOSED_TESTS.json`. Нормативный ID связан с точным текстом в [кандидате фиксации](NEXT_STAGE_02B_R0A_CONTRACT_FREEZE_CANDIDATE_RU.md).

## INV-07

**InvariantID:** INV-07

**FormalDefinition:** Source namespace включает broker/server/account

**NormativeSource:** D-08

**AffectedFunctions:** HSBI_BuildSourceDealKey

**PositiveExample:** same namespace/deal same source

**Counterexample:** Account1 vs Account2 deal11

**TestID:** D08-namespace-account

**CurrentStatus:** FAIL

**ApprovalRequired:** True

**ProposedTestStatus:** PASS

Источник теста: `Tests/Static/check_hsbi_02b_r0a_normative_contracts.py`; точные значения — `Tests/Evidence/NEXT_STAGE_02B_R0A_PROPOSED_TESTS.json`. Нормативный ID связан с точным текстом в [кандидате фиксации](NEXT_STAGE_02B_R0A_CONTRACT_FREEZE_CANDIDATE_RU.md).

## INV-08

**InvariantID:** INV-08

**FormalDefinition:** 0<=Reserved<=Remaining; Available>=0

**NormativeSource:** D-01

**AffectedFunctions:** HSBI_ValidateMoneyState / HSBI_CanConsumeAmount

**PositiveExample:** remaining50 reserved10 =>40

**Counterexample:** reserved51 приremaining50

**TestID:** D01-negative-available

**CurrentStatus:** FAIL

**ApprovalRequired:** True

**ProposedTestStatus:** PASS

Источник теста: `Tests/Static/check_hsbi_02b_r0a_normative_contracts.py`; точные значения — `Tests/Evidence/NEXT_STAGE_02B_R0A_PROPOSED_TESTS.json`. Нормативный ID связан с точным текстом в [кандидате фиксации](NEXT_STAGE_02B_R0A_CONTRACT_FREEZE_CANDIDATE_RU.md).

## INV-09

**InvariantID:** INV-09

**FormalDefinition:** Все money finite и валюта/precision известны

**NormativeSource:** D-01

**AffectedFunctions:** HSBI_ValidateMoneyState / allocation validators

**PositiveExample:** finite50

**Counterexample:** Infinity/NaN

**TestID:** FINITE-Infinity

**CurrentStatus:** FAIL

**ApprovalRequired:** True

**ProposedTestStatus:** PASS

Источник теста: `Tests/Static/check_hsbi_02b_r0a_normative_contracts.py`; точные значения — `Tests/Evidence/NEXT_STAGE_02B_R0A_PROPOSED_TESTS.json`. Нормативный ID связан с точным текстом в [кандидате фиксации](NEXT_STAGE_02B_R0A_CONTRACT_FREEZE_CANDIDATE_RU.md).

## INV-10

**InvariantID:** INV-10

**FormalDefinition:** Approved money rounding conserves source; mandatory Core on broker grid >=Vmin

**NormativeSource:** D-01

**AffectedFunctions:** HSBI_SolveBigGeometry / allocation rounding

**PositiveExample:** Core.2 valid

**Counterexample:** raw.001 ->Core0

**TestID:** ZERO-raw-to-rounded

**CurrentStatus:** FAIL

**ApprovalRequired:** True

**ProposedTestStatus:** PASS

Источник теста: `Tests/Static/check_hsbi_02b_r0a_normative_contracts.py`; точные значения — `Tests/Evidence/NEXT_STAGE_02B_R0A_PROPOSED_TESTS.json`. Нормативный ID связан с точным текстом в [кандидате фиксации](NEXT_STAGE_02B_R0A_CONTRACT_FREEZE_CANDIDATE_RU.md).

## INV-11

**InvariantID:** INV-11

**FormalDefinition:** Exact replay: delta money/revision/actions=0

**NormativeSource:** D-07

**AffectedFunctions:** HSBI_IsDuplicateReserveConsumption / restart

**PositiveExample:** exact E1 returnsNO_OP

**Counterexample:** altered E1=11

**TestID:** D07-exact-noop

**CurrentStatus:** UNPROVEN

**ApprovalRequired:** True

**ProposedTestStatus:** PASS

Источник теста: `Tests/Static/check_hsbi_02b_r0a_normative_contracts.py`; точные значения — `Tests/Evidence/NEXT_STAGE_02B_R0A_PROPOSED_TESTS.json`. Нормативный ID связан с точным текстом в [кандидате фиксации](NEXT_STAGE_02B_R0A_CONTRACT_FREEZE_CANDIDATE_RU.md).

## INV-12

**InvariantID:** INV-12

**FormalDefinition:** Missing authority=>UNAVAILABLE, no authorization

**NormativeSource:** D-08

**AffectedFunctions:** HSBI_EvaluateReserveCatchUp / provenance lookup

**PositiveExample:** verified source

**Counterexample:** hasPrior=false без history

**TestID:** D08-missing-history

**CurrentStatus:** FAIL

**ApprovalRequired:** True

**ProposedTestStatus:** PASS

Источник теста: `Tests/Static/check_hsbi_02b_r0a_normative_contracts.py`; точные значения — `Tests/Evidence/NEXT_STAGE_02B_R0A_PROPOSED_TESTS.json`. Нормативный ID связан с точным текстом в [кандидате фиксации](NEXT_STAGE_02B_R0A_CONTRACT_FREEZE_CANDIDATE_RU.md).

## INV-13

**InvariantID:** INV-13

**FormalDefinition:** Новые события связаны с текущими Cycle/Plan/Revision

**NormativeSource:** D-07

**AffectedFunctions:** HSBI_ValidateReserveConsumption / NewFar assembly

**PositiveExample:** plan1rev1

**Counterexample:** plan999/rev999

**TestID:** D07-binding-revision

**CurrentStatus:** FAIL

**ApprovalRequired:** True

**ProposedTestStatus:** PASS

Источник теста: `Tests/Static/check_hsbi_02b_r0a_normative_contracts.py`; точные значения — `Tests/Evidence/NEXT_STAGE_02B_R0A_PROPOSED_TESTS.json`. Нормативный ID связан с точным текстом в [кандидате фиксации](NEXT_STAGE_02B_R0A_CONTRACT_FREEZE_CANDIDATE_RU.md).

## INV-14

**InvariantID:** INV-14

**FormalDefinition:** All-level margin=min RequiredLevels, missing proof blocks guarantee

**NormativeSource:** CR-09

**AffectedFunctions:** HSBI_AggregateFutureSmallProof

**PositiveExample:** fixedR/B,F=T antitone

**Counterexample:** maxT L1+29, L2-16

**TestID:** CR09-A-negative-level

**CurrentStatus:** DECISION_REQUIRED

**ApprovalRequired:** True

**ProposedTestStatus:** PASS

Источник теста: `Tests/Static/check_hsbi_02b_r0a_normative_contracts.py`; точные значения — `Tests/Evidence/NEXT_STAGE_02B_R0A_PROPOSED_TESTS.json`. Нормативный ID связан с точным текстом в [кандидате фиксации](NEXT_STAGE_02B_R0A_CONTRACT_FREEZE_CANDIDATE_RU.md).

## INV-15

**InvariantID:** INV-15

**FormalDefinition:** Small gain/projected gain не создаёт скрытый BigReserve

**NormativeSource:** D-03

**AffectedFunctions:** HSBI_EvaluateBasketMoney / allocation role gate

**PositiveExample:** Core10 ->eligible10

**Counterexample:** Small10 ->BigReserve0 Residual10

**TestID:** D03-small-not-reserve

**CurrentStatus:** FAIL

**ApprovalRequired:** True

**ProposedTestStatus:** PASS

Источник теста: `Tests/Static/check_hsbi_02b_r0a_normative_contracts.py`; точные значения — `Tests/Evidence/NEXT_STAGE_02B_R0A_PROPOSED_TESTS.json`. Нормативный ID связан с точным текстом в [кандидате фиксации](NEXT_STAGE_02B_R0A_CONTRACT_FREEZE_CANDIDATE_RU.md).

## INV-16

**InvariantID:** INV-16

**FormalDefinition:** BrokerDispatchAllowed=false во всех разрешённых режимах

**NormativeSource:** NO-TRADE

**AffectedFunctions:** HSBI_IsBrokerDispatchAllowed / HSBI_NoTradeExecution

**PositiveExample:** all static modes dispatchfalse

**Counterexample:** any allowed dispatch forbidden

**TestID:** guard-1

**CurrentStatus:** PASS

**ApprovalRequired:** False

**ProposedTestStatus:** PASS

Источник теста: `Tests/Static/check_hsbi_02b_r0a_normative_contracts.py`; точные значения — `Tests/Evidence/NEXT_STAGE_02B_R0A_PROPOSED_TESTS.json`. Нормативный ID связан с точным текстом в [кандидате фиксации](NEXT_STAGE_02B_R0A_CONTRACT_FREEZE_CANDIDATE_RU.md).

## Ограничения статусов

INV-03/11 durable exactly-once остаются UNPROVEN. INV-05: локальная формула signed net верна, но record validation/immutable comparator не доказывают сохранность компонентов, broker reconciliation NOT_RUN. INV-10 сочетает выявленный zero-Core defect с proposed precision policy, которая отдельно требует администратора. INV-16 PASS — static scan/извлечённая policy на baseline, не MQL5 runtime acceptance.
