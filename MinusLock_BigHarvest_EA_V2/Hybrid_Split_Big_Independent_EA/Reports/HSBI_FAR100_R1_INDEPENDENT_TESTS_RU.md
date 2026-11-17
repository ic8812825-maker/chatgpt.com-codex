# FAR100 — Реально выполненные независимые проверки и ограничения

SourceCommitSHA=8640bf464eda220d9096adb99bc8bcb390ed68e7
CheckedAtUTC=2026-11-17T13:31:04.086505+00:00
ExecutionMode=LOCAL_RESEARCH_GIT_PLUS_GITHUB_MCP_PUBLICATION
DocumentVersion=HSBI-FAR100-R1-V1
NormativeStatus=RESEARCH_AUDIT_ONLY_NOT_OWNER_APPROVAL
EvidenceClass=SYNTHETIC_MATH_ONLY; STATIC_SOURCE_REVIEW; EXECUTED_PYTHON_REFERENCE_ONLY
DocumentationAudit=UNPROVEN_NOT_PASS_EXHAUSTIVE_SEMANTICS_NOT_CERTIFIED
BrokerProof=UNAVAILABLE
NativeMQL5=NOT_RUN_METAEDITOR_NOT_FOUND
PRODUCTION_CHANGED=NO; IMPLEMENTATION_ALLOWED=NO; BROKER_DISPATCH_ALLOWED=NO; REAL_TRADING_ALLOWED=NO.

Нормативные предпосылки: сохраняются D06=A и NewFar=A/MINIMUM_SAFE_V1, исходные роли и order Small→OldFar→Trend→Core part→actual residual→promotion. CR09 не утверждён, новых owner selections/receipts нет. Старые evidence не изменены. PASS далее относится только к фактически выполненной независимой Python-проверке конкретного synthetic predicate; он не authorizes strategy/runtime.

Синтетические предпосылки: EURUSD/счёт USD, contract100000, tick0.00001, point0.00001, pip0.0001, tick value1USD/lot симметрично; lot min/step0.01,max100,origin0. Spread0.00020 уже в Bid/Ask; opening commission3.5USD/lot учтена в realized, closing3.5USD/lot, accrued swap−1USD/lot, fee0, projected slippage1tick=1USD/lot. Это НЕ сведения реального брокера. Research money использует exact Decimal и не округляет каждый posting до цента; реальный currency/posting/partial-commission profile UNAVAILABLE. QuoteDigits5 не currency digits.

R_all=Initial100−opening fees11.55=88.45USD; excluded Initial I100; RecoveryRealized_A=−11.55. Deposit100000; Balance100088.45 после openings. Исторического eligible harvest в главной fixture нет: TransitionBudget=FinalReserve=PartialFarBudget=0. StartingEquityMark99555.15 при SELL Bid1.10500/Ask1.10520. Все Position/Deal/Action IDs с MODEL — исследовательские символы, не брокерские tickets.

Основные формулы: NetLot=SELL−BUY; DealNet=Profit+Swap+signed Commission+Fee; projected net содержит только ещё не включённые costs; RecoveryPLCloseNow_A=R_all−I+ΣOpenCloseNowNet−H_in, здесь H_in0; Economic=R_all+ΣOpenCloseNowNet. Threshold=10+5+1=16. Allocations не прибавляются к результату. Slippage, реализованная в simulated fill price, второй раз не списывается.

Полные данные, exact decimals и actual command exit codes: [run metadata](../Tests/Evidence/FAR100_R1/run_metadata.json), [команды](../Tests/Evidence/FAR100_R1/commands.json), [test results](../Tests/Evidence/FAR100_R1/test_results.json). Фактические брокерские fills отсутствуют; native/broker/durable tests не запускались.

## Команды и фактический outcome

Рабочий каталог команд — разрешённый PROJECT_PATH в локальном checkout веткиwork на source SHA. Запущены:

```text
python3 Tests/Reference/hsbi_far100_r1_documentation.py
exit_code=0
python3 Tests/Reference/hsbi_far100_r1_oracle.py > Tests/Evidence/FAR100_R1/oracle_stdout.txt
exit_code=0
python3 Tests/Reference/hsbi_far100_r1_tests.py > Tests/Evidence/FAR100_R1/tests_stdout.txt
exit_code=0
```

Final reference run: assertions=1191,PASS=1191,FAIL=0;causal mutations12,KILLED12,SURVIVED0. Это1191 assertion rows, а не1191 независимых торговых сценариев. Между ранним exploratory run1176 и final1191 добавлены полноценные source inventory/admission negative controls; окончательное evidence содержит1191. Native tests0. UNPROVEN5 и NOT_RUN4 — отдельные obligations, не прибавляются кчислу executed assertions.

Documentation bytesread545,semantic exhaustiveness not certified. Python3.12.14; exact Decimal и отдельный Fraction tick-count oracle. Expected hand constants−275.50/−306.60/−153.30/+112.25,full−623.15,N.4closed−520.95/residual−102.20,opening11.55,threshold16 не генерируются из actual outputs. Fraction oracle не вызывает Decimal money functions; production modules не импортируются.

## Классы проверок

| Class | Executed assertion rows |
|---|---|
| ALLOCATION | 12 |
| CATCHUP | 5 |
| COST | 1 |
| FINALCLOSE | 6 |
| FUTURESMALL | 1 |
| IDENTITY | 11 |
| MARGIN | 4 |
| MONEY | 453 |
| NEGATIVE | 29 |
| NEWFAR | 20 |
| PRICE | 409 |
| RESTART | 18 |
| RISK | 3 |
| TRANSITION | 17 |
| VOLUME | 202 |


VOLUME проверяет99N/rounding/grid/coarse/min;PRICE close-side/tick/pip/mirror;MONEY literal legs/Fraction101snapshots/conservation;COST opening/closing/duplicate charges;ALLOCATION source replay/Free/reservations;CATCHUP necessary-vs-money;TRANSITION staged partial/delayed/unknown;NEWFAR complete grid/actual mismatch;FUTURESMALL local2501tick monotonicity only;RISK/MARGIN synthetic boundedstress/profile distinction;FINALCLOSE equality/priority/emergency;IDENTITY fullbody/corelineage;RESTART18 metadata roundtrips;NEGATIVE malformed inputs/admission/mutations.

Зелёная reference assertion «model rejects unknown» не означает, что current MQL5 validator делает то же. Ни успешная production branch151, ни full native all-required route не запускались.

## Causal mutations (исследовательский artifact, production не мутировал)

| Mutation | ChangedField | KillingInvariant | Outcome |
|---|---|---|---|
| CLOSE_COMPRESSION | farclosed | FarClosed=1 | KILLED |
| CLOSE_FULL_CORE | coreclosed | CoreClosed+N=C | KILLED |
| OMIT_SMALL | closing | closing+residual=full | KILLED |
| DOUBLE_RESERVE | closing | allocations not income | KILLED |
| DOUBLE_FEE | closing | cost counted once | KILLED |
| WRONG_SIDE | closing | executable side PnL | KILLED |
| NEW_POSITION | identity | same Core identifier | KILLED |
| DIRECTION_TEMPLATE | direction | promoted Core direction | KILLED |
| INITIAL_DOUBLE | initial_count | unique initial posting | KILLED |
| REUSE_FREE | consumed | Grant=C+Free | KILLED |
| PARTIAL_ADVANCE | pending | no advance pending | KILLED |
| TWO_FAR | second_far | unique managed Far | KILLED |


Base valid artifact проходит независимые volume/closing+residual/source/cash/pending инварианты. Каждая одна повреждённая field-model нарушает конкретное условие. Это фиксированная causal mutation matrix, не полный mutation coverage production.

## НЕ выполнено / НЕ доказано

Native compile,MQL5,broker OrderCalcProfit/OrderCalcMargin,настоящие crash/concurrency не запускались: MetaEditor/terminal/wine не найден в PATH/проверенных установках; read-only broker/provider отсутствует. Reference JSON restart не disk durability. Исторические67 TL/CU/03G specs по-прежнему NOT_RUN, старые7PASS/16FAIL не изменены.
Пять unproven obligations: whole-document semantic review,actual broker proof,full CR09binding,safe first SmallTransition,profitable multi-transition reachability. Результат full strategy=MATH_AUDIT_UNPROVEN, а не1191PASS торговой модели.

Protected92 SHA256 parity before/after подтверждена,656 original historical evidence hashes неизменны. Final remote diff отдельно проверяется после публикации; self-referential будущий commit hash не выдумывается.

## Точные исходные опоры и влияние на торговлю

- [Docs/04_MATHEMATICAL_MODEL_RU.md:9](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/8640bf464eda220d9096adb99bc8bcb390ed68e7/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Docs/04_MATHEMATICAL_MODEL_RU.md#L9)
- [Docs/05_GEOMETRY_MODEL_RU.md:21](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/8640bf464eda220d9096adb99bc8bcb390ed68e7/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Docs/05_GEOMETRY_MODEL_RU.md#L21)
- [Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md:5](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/8640bf464eda220d9096adb99bc8bcb390ed68e7/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md#L5)
- [Docs/12_FINAL_CLOSE_SPECIFICATION_RU.md:7](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/8640bf464eda220d9096adb99bc8bcb390ed68e7/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Docs/12_FINAL_CLOSE_SPECIFICATION_RU.md#L7)
- [Docs/13_SMALL_TRANSITION_SPECIFICATION_RU.md:12](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/8640bf464eda220d9096adb99bc8bcb390ed68e7/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Docs/13_SMALL_TRANSITION_SPECIFICATION_RU.md#L12)
- [Docs/14_NEW_FAR_SOLVER_SPECIFICATION_RU.md:25](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/8640bf464eda220d9096adb99bc8bcb390ed68e7/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Docs/14_NEW_FAR_SOLVER_SPECIFICATION_RU.md#L25)
- [Docs/15_RISK_AND_MARGIN_CONTRACT_RU.md:12](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/8640bf464eda220d9096adb99bc8bcb390ed68e7/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Docs/15_RISK_AND_MARGIN_CONTRACT_RU.md#L12)
- [Docs/24_BROKER_MONEY_MODEL_RU.md:5](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/8640bf464eda220d9096adb99bc8bcb390ed68e7/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Docs/24_BROKER_MONEY_MODEL_RU.md#L5)
- [Docs/29_CANDIDATE_OBJECTIVE_AND_TIEBREAK_RU.md:3](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/8640bf464eda220d9096adb99bc8bcb390ed68e7/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Docs/29_CANDIDATE_OBJECTIVE_AND_TIEBREAK_RU.md#L3)
- [Docs/30_FUTURE_SMALL_AGGREGATE_PROOF_RU.md:5](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/8640bf464eda220d9096adb99bc8bcb390ed68e7/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Docs/30_FUTURE_SMALL_AGGREGATE_PROOF_RU.md#L5)
- [Reports/HSBI_03F_R2_D06_A_NORMATIVE_LOCK_RU.md:30](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/8640bf464eda220d9096adb99bc8bcb390ed68e7/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_03F_R2_D06_A_NORMATIVE_LOCK_RU.md#L30)
- [Reports/HSBI_03F_R2_NEWFAR_MINIMUM_SAFE_NORMATIVE_LOCK_RU.md:30](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/8640bf464eda220d9096adb99bc8bcb390ed68e7/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_03F_R2_NEWFAR_MINIMUM_SAFE_NORMATIVE_LOCK_RU.md#L30)

Source blob SHA всех документов — в documentation_inventory.json, SHA25692 protected до/после — в protected_before/after.json. Конфликты source/Docs по full Core/closed Core, fixed template lineage, selective/minAll и objective не исправлены. Реальные risk/margin/provider/profile и full future proof UNAVAILABLE/UNPROVEN. Влияние: implementation, broker dispatch, real trading запрещены независимо от числа Python PASS.
