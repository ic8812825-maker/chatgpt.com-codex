# AUDIT03 — полный индекс production sources и функций

## Текущий срез R2

199 деклараций имеют индивидуальные карточки:43 прежние20-field карты сохранены и дополнены FunctionID/Signature/authority/boundary;156 новых карт по18 обязательных R2 полей.198 различных имён: NormalizePriceToTick имеет2перегрузки с разными source/signature/FunctionID, обе без production callers. Card count199 не означает199 финансовых proof. Полный guard/caller нормативный inventory и оставшиеся contracts ещё не закрыты. Статические callers/dependencies перечислены для каждого body по74 production sources; native/dynamic reachability NOT_RUN.

Условное дополнительное доказательство nonprogress NewFar enumeration — ERR051, IMP023. Предложения не реализованы. Signature/source quotations — Markdown, не новый executable artifact. Текстовое чтение/парсинг не запускает функцию.


## Исторический срез FINAL-CLOSURE до R2

199 исходных объявлений сохранены;43 функции имеют новые индивидуальные карточки по20 полей с полным source body и static callsites. Для156 функций индивидуальный semantic crosswalk ещё не завершён. Все74 production sources ранее прочитаны, но это не199 доказанных mandatory financial callers. Новые карточки различают local shape/coherence от independent authority. [Guard crosswalk](HSBI_AUDIT03_GUARD_CALLER_CROSSWALK_RU.md) содержит15 групп и10 локальных TX clause rows, не глобальный atomic guard denominator. [FSM relation](HSBI_AUDIT03_FSM_COMPLETE_MATRIX_RU.md) отдельно раскрывает topology и отсутствующие lifecycle handlers.


74 production sources прочитаны целиком в совокупности исходного AUDIT03 и продолжения:73 Include headers и один main mq5. Их контрольная идентичность — неизменённый baseline4761c66edc3343f353ca774df835eedb1787b818. Восемь .gitkeep не production. Ни тесты, ни компиляция не запускались.

Индекс ниже извлекает имена **объявлений** и номера строк из прочитанных файлов. Это навигация, не автоматическое доказательство каждого caller/guard. Тематические связи являются набором применимых контрактов, не утверждением, что каждая функция реализует все перечисленные формулы. Точная индивидуальная clause→mandatory caller→proof матрица остаётся незавершённой; такой пробел не скрывается полным textual reading. Строки относятся к baseline, который совпадает с рабочими production bytes.

| Source | SHA256 / Git blob | Full range read | Declared function:line / structures | Applicable contracts | Formula families | Finding / improvement | Review scope |
|---|---|---|---|---|---|---|---|
| `Include/Core/HSBI_Context.mqh` | `7ae314b8f7e4183419943297885a6291afbf449a5d63490ca35757f737eb80ef` / `382be9e46dfc00a95393b79c2e2215cf0c0e62b4` | 1–60 | HSBI_InitializeContext:8; HSBI_ResetContext:9; HSBI_ContextPositionValid:10; HSBI_ContextRolesConflict:19; HSBI_ContextPositionInScope:27; HSBI_ValidateContext:33 | Docs/02_SYSTEM_ROLES_AND_IDENTITY_RU.md; Docs/06_STATE_MACHINE_SPECIFICATION_RU.md | F036/F057/F060/F061/F065 | ERR-012/016/025/028; IMP-006/008/017 | Namespace, roles, topology и runtime disable; topology не authorization; INDIVIDUAL_GUARD_MAPPING_PARTIAL |
| `Include/Core/HSBI_Enums.mqh` | `69b0ded8187af3f69a4058188c206f11b881e4f7d9c092d7bafe1bb9111d29f6` / `23ffdbc865932e8161d2f0eddd3627ca01640ef4` | 1–11 | DTO/enums/config declarations; no matched function | Docs/02_SYSTEM_ROLES_AND_IDENTITY_RU.md; Docs/06_STATE_MACHINE_SPECIFICATION_RU.md | F036/F057/F060/F061/F065 | ERR-012/016/025/028; IMP-006/008/017 | Namespace, roles, topology и runtime disable; topology не authorization; INDIVIDUAL_GUARD_MAPPING_PARTIAL |
| `Include/Core/HSBI_Identifiers.mqh` | `a6421afab5dc291df0d17cfa4e1d39f5cc96bd87aa9cd9602129e240d0a8dd9e` / `d05a05147f7641040dbf7261ebdd04832d643997` | 1–24 | HSBI_IsValidIdentity:6; HSBI_SameCycle:7; HSBI_SamePositionOwner:8; HSBI_SameSymbolScope:9; HSBI_UlongToString:10; HSBI_SerializeIdentity:23 | Docs/02_SYSTEM_ROLES_AND_IDENTITY_RU.md; Docs/06_STATE_MACHINE_SPECIFICATION_RU.md | F036/F057/F060/F061/F065 | ERR-012/016/025/028; IMP-006/008/017 | Namespace, roles, topology и runtime disable; topology не authorization; INDIVIDUAL_GUARD_MAPPING_PARTIAL |
| `Include/Core/HSBI_Invariants.mqh` | `4c4a742a62a60361fb63e907888f4bc936591c00326ebe2812ba2fa668133981` / `0c03a908e2887a4c19bf24829ba39769e05606b6` | 1–14 | HSBI_ExactlyOneFarOrZero:5; HSBI_NoDualTail:6; HSBI_NoUnknownRole:7; HSBI_ContextIdentityComplete:8; HSBI_StateRevisionMonotonic:9; HSBI_NoPendingActionConflict:10; HSBI_NoFinalReserveForPartialFar:11; HSBI_AllocationConservation:12; HSBI_RealTradingForbiddenAtHSB1:13 | Docs/02_SYSTEM_ROLES_AND_IDENTITY_RU.md; Docs/06_STATE_MACHINE_SPECIFICATION_RU.md | F036/F057/F060/F061/F065 | ERR-012/016/025/028; IMP-006/008/017 | Namespace, roles, topology и runtime disable; topology не authorization; INDIVIDUAL_GUARD_MAPPING_PARTIAL |
| `Include/Core/HSBI_ReasonCodes.mqh` | `62aef3906bc933cee98a136fd8ed983be36f23ef01da50a6c2572551bce2abe2` / `3ffbe6a053ee574f607ca11161c049c990ef8128` | 1–5 | HSBI_ReasonToString:4 | Docs/02_SYSTEM_ROLES_AND_IDENTITY_RU.md; Docs/06_STATE_MACHINE_SPECIFICATION_RU.md | F036/F057/F060/F061/F065 | ERR-012/016/025/028; IMP-006/008/017 | Namespace, roles, topology и runtime disable; topology не authorization; INDIVIDUAL_GUARD_MAPPING_PARTIAL |
| `Include/Core/HSBI_Roles.mqh` | `836970966be820261b031717bab2f81482ab76c57e06ee63269c368012a3399d` / `23d0bedac6e8852342638d7f16d121ad19124a11` | 1–11 | HSBI_IsKnownRole:6; HSBI_ValidatePositionDescriptor:7; HSBI_CanPromoteToFar:8; HSBI_ValidateRoleTransition:9; HSBI_CountFarRoles:10 | Docs/02_SYSTEM_ROLES_AND_IDENTITY_RU.md; Docs/06_STATE_MACHINE_SPECIFICATION_RU.md | F036/F057/F060/F061/F065 | ERR-012/016/025/028; IMP-006/008/017 | Namespace, roles, topology и runtime disable; topology не authorization; INDIVIDUAL_GUARD_MAPPING_PARTIAL |
| `Include/Core/HSBI_RuntimeMode.mqh` | `f47526eddac1c7007ebddfd5c32d95848600ba6751086442e8032ed6ce9878f2` / `3c5eb19440572cae78eb2d042907ae13ffb10a44` | 1–7 | HSBI_IsRuntimeModeAllowedAtStage1:5 | Docs/02_SYSTEM_ROLES_AND_IDENTITY_RU.md; Docs/06_STATE_MACHINE_SPECIFICATION_RU.md | F036/F057/F060/F061/F065 | ERR-012/016/025/028; IMP-006/008/017 | Namespace, roles, topology и runtime disable; topology не authorization; INDIVIDUAL_GUARD_MAPPING_PARTIAL |
| `Include/Core/HSBI_RuntimePolicy.mqh` | `1fa087dda8d81f182c8c6d8fd2dab4c4712b973c8f95ad15c0bfdf115b01d337` / `657fe730c1a3df306848d1de00af87aa589be449` | 1–30 | HSBI_BuildRuntimePolicy:12; HSBI_IsInjectedProofAllowed:23; HSBI_IsProductionPreflightAllowed:24; HSBI_IsBrokerDispatchAllowed:25; HSBI_IsStaticCalculationAllowed:26; HSBI_IsCompletionSourceAllowed:28 | Docs/02_SYSTEM_ROLES_AND_IDENTITY_RU.md; Docs/06_STATE_MACHINE_SPECIFICATION_RU.md | F036/F057/F060/F061/F065 | ERR-012/016/025/028; IMP-006/008/017 | Namespace, roles, topology и runtime disable; topology не authorization; INDIVIDUAL_GUARD_MAPPING_PARTIAL |
| `Include/Core/HSBI_StateMachine.mqh` | `7ec9f9860ce9d72c7f7c119377c1b2bedda25001921b92ef3aa9c7d95a32e403` / `836c2dcbe983caf7127cfcd2442dc0b740bf8479` | 1–11 | HSBI_IsTransitionAllowed:5; HSBI_ProposeStateTransition:6; HSBI_ApplyPureStateTransition:7; HSBI_ConflictTargetState:8; HSBI_CriticalErrorTargetState:9; HSBI_TransactionConflictTargetState:10 | Docs/02_SYSTEM_ROLES_AND_IDENTITY_RU.md; Docs/06_STATE_MACHINE_SPECIFICATION_RU.md | F036/F057/F060/F061/F065 | ERR-012/016/025/028; IMP-006/008/017 | Namespace, roles, topology и runtime disable; topology не authorization; INDIVIDUAL_GUARD_MAPPING_PARTIAL |
| `Include/Core/HSBI_StateValidator.mqh` | `145d73d6d69baf1ef58958237b6c375bef23e2cd9004d1f50c9fe694c24077f6` / `b4c6ba061c33a6514f9eef9db2e8e885ff09008f` | 1–6 | HSBI_ValidateStateTopology:4; HSBI_OutcomeCompletesAction:5 | Docs/02_SYSTEM_ROLES_AND_IDENTITY_RU.md; Docs/06_STATE_MACHINE_SPECIFICATION_RU.md | F036/F057/F060/F061/F065 | ERR-012/016/025/028; IMP-006/008/017 | Namespace, roles, topology и runtime disable; topology не authorization; INDIVIDUAL_GUARD_MAPPING_PARTIAL |
| `Include/Core/HSBI_Types.mqh` | `61e08fbfc9e97df1931ae6c825a5ff64e25f1fd4502f90e71f8b2a4c2857c3cc` / `9fd1c4bdf531665b50ba5ca6db38daba8f0d70d0` | 1–8 | HSBI_Result:7 | Docs/02_SYSTEM_ROLES_AND_IDENTITY_RU.md; Docs/06_STATE_MACHINE_SPECIFICATION_RU.md | F036/F057/F060/F061/F065 | ERR-012/016/025/028; IMP-006/008/017 | Namespace, roles, topology и runtime disable; topology не authorization; INDIVIDUAL_GUARD_MAPPING_PARTIAL |
| `Include/Core/HSBI_Version.mqh` | `b9432e5d966e99a8383ea9d6308e48c62725e431dd80e4a070020e9aa63359a9` / `d0eefae130ed96720b3f1962842d2a9c30168a00` | 1–12 | DTO/enums/config declarations; no matched function | Docs/02_SYSTEM_ROLES_AND_IDENTITY_RU.md; Docs/06_STATE_MACHINE_SPECIFICATION_RU.md | F036/F057/F060/F061/F065 | ERR-012/016/025/028; IMP-006/008/017 | Namespace, roles, topology и runtime disable; topology не authorization; INDIVIDUAL_GUARD_MAPPING_PARTIAL |
| `Include/Diagnostics/HSBI_Diagnostics.mqh` | `ca3590969d6b9392a5c69dc3b95878c439d316505a7e08647523a5d69e425c46` / `6bde810e9fc5fe577744381a7ce0d52c3d6718ed` | 1–7 | HSBI_BuildDiagnosticSnapshot:5; HSBI_UpdateDiagnosticSnapshot:6 | Docs/18_MQL5_ARCHITECTURE_SPECIFICATION_RU.md | NOT_APPLICABLE непосредственно к денежной арифметике | ERR-028; IMP-017 | Отображение/логирование не независимый provider; INDIVIDUAL_GUARD_MAPPING_PARTIAL |
| `Include/Diagnostics/HSBI_Logger.mqh` | `dc56e40d37909411f11dba454ec893e66315c92c68c85c1b4a9e3234daddc388` / `61471e52a9a98d465cb7ced3f6744ccd7678782e` | 1–7 | HSBI_Log:6 | Docs/18_MQL5_ARCHITECTURE_SPECIFICATION_RU.md | NOT_APPLICABLE непосредственно к денежной арифметике | ERR-028; IMP-017 | Отображение/логирование не независимый provider; INDIVIDUAL_GUARD_MAPPING_PARTIAL |
| `Include/Diagnostics/HSBI_PanelModel.mqh` | `ba0d4470c5ba0dd0f39ab6fe47e026efac4808fc74a7c2e2bc0e658726ee560c` / `2c878424c053e8c2b316c7e850c9df600dbdbc2d` | 1–6 | HSBI_BuildPanelModel:5 | Docs/18_MQL5_ARCHITECTURE_SPECIFICATION_RU.md | NOT_APPLICABLE непосредственно к денежной арифметике | ERR-028; IMP-017 | Отображение/логирование не независимый provider; INDIVIDUAL_GUARD_MAPPING_PARTIAL |
| `Include/Execution/HSBI_ActionTypes.mqh` | `f8c4c8238052aa2999b797de7cee3e39c39435bf7e42068b4d6d76994d505f01` / `b592dac8bb8e862336e0a8da371ba76445c4da68` | 1–8 | HSBI_ValidateActionRecord:6; HSBI_SerializeActionIds:7 | Docs/07_TRANSACTION_EXECUTION_CONTRACT_RU.md; Docs/HSB.2C_Execution_Intent_Spec.md | F036/F046/F057/F062/F063 | ERR-010/024/030/049; IMP-005/008/016 | Request, expected/actual ownership, finite/grid/enum/partial boundaries; INDIVIDUAL_GUARD_MAPPING_PARTIAL |
| `Include/Execution/HSBI_EventTypes.mqh` | `d588c6721e7a5af9e48bad54bdbe3cf3fc90688956353c3a04380ae0181f7c13` / `7dbdbb34a1e2eab4a3bf3bc0d649dbf30e45a13d` | 1–8 | HSBI_ValidateEventRecord:6; HSBI_SerializeEventIds:7 | Docs/07_TRANSACTION_EXECUTION_CONTRACT_RU.md; Docs/HSB.2C_Execution_Intent_Spec.md | F036/F046/F057/F062/F063 | ERR-010/024/030/049; IMP-005/008/016 | Request, expected/actual ownership, finite/grid/enum/partial boundaries; INDIVIDUAL_GUARD_MAPPING_PARTIAL |
| `Include/Execution/HSBI_ExecutionIntent.mqh` | `67d9381fd0f2d170efc22a07bf4b391c9e86b1685d697d1e6201b713adb4d4f2` / `026b7c6d44b9dad83eb7d8de9bd0c567094a13ca` | 1–45 | HSBI_ExecutionIntentDigest:15; HSBI_ValidateExecutionIntentDigest:26; HSBI_IsValidIntentStatus:27; HSBI_ValidateExecutionIntentStructure:28; HSBI_IntentIdempotencyKey:42; HSBI_IsSameIntentRetry:43; HSBI_IsIntentConflict:44 | Docs/07_TRANSACTION_EXECUTION_CONTRACT_RU.md; Docs/HSB.2C_Execution_Intent_Spec.md | F036/F046/F057/F062/F063 | ERR-010/024/030/049; IMP-005/008/016 | Request, expected/actual ownership, finite/grid/enum/partial boundaries; INDIVIDUAL_GUARD_MAPPING_PARTIAL |
| `Include/Execution/HSBI_ExecutionPreflight.mqh` | `7af97449654913e8488e8dccc44c3fcf2f08b79c14ec3aea5d0388604fb5c9c0` / `2889fe50eb4690681f370d7be8613a887a81a05d` | 1–49 | HSBI_ValidateExecutionPreflight:17; HSBI_IsIntentLifecycleTransitionAllowed:35; HSBI_IntentRetryAllowed:47 | Docs/07_TRANSACTION_EXECUTION_CONTRACT_RU.md; Docs/HSB.2C_Execution_Intent_Spec.md | F036/F046/F057/F062/F063 | ERR-010/024/030/049; IMP-005/008/016 | Request, expected/actual ownership, finite/grid/enum/partial boundaries; INDIVIDUAL_GUARD_MAPPING_PARTIAL |
| `Include/Execution/HSBI_ExternalOutcome.mqh` | `01eb91c904e73d2f3973c21c37e3973b2c72cb73e295621939e132b965b65c88` / `409e85b37268c2b7f4785a1b0d614423592b5ba7` | 1–33 | HSBI_ExternalOutcomeDigest:13; HSBI_ReconcileExecutionOutcome:22 | Docs/07_TRANSACTION_EXECUTION_CONTRACT_RU.md; Docs/HSB.2C_Execution_Intent_Spec.md | F036/F046/F057/F062/F063 | ERR-010/024/030/049; IMP-005/008/016 | Request, expected/actual ownership, finite/grid/enum/partial boundaries; INDIVIDUAL_GUARD_MAPPING_PARTIAL |
| `Include/Execution/HSBI_NoTradeExecution.mqh` | `d3264d4a3a8a6aef1a0cc69420f6d26b6aa16f25ec19e43f46151e6cbb242084` / `5c29fece82fe03a954fb345bf006de6a281705f9` | 1–9 | HSBI_SubmitActionStub:5; HSBI_OpenPositionStub:6; HSBI_ClosePositionStub:7; HSBI_PartialCloseStub:8 | Docs/07_TRANSACTION_EXECUTION_CONTRACT_RU.md; Docs/HSB.2C_Execution_Intent_Spec.md | F036/F046/F057/F062/F063 | ERR-010/024/030/049; IMP-005/008/016 | Request, expected/actual ownership, finite/grid/enum/partial boundaries; INDIVIDUAL_GUARD_MAPPING_PARTIAL |
| `Include/Execution/HSBI_OwnershipGuardTypes.mqh` | `842a28c0fa460d00c443dc9ddda2a1d5314300e3adbfb155f1876457a38f4ac7` / `4e6ca9ad75ef5ad37da4555feea44d451a6cb4c2` | 1–17 | HSBI_EvaluateOwnership:8; HSBI_TicketMatchesObservation:9; HSBI_IsActualBigCoreResidual:13 | Docs/07_TRANSACTION_EXECUTION_CONTRACT_RU.md; Docs/HSB.2C_Execution_Intent_Spec.md | F036/F046/F057/F062/F063 | ERR-010/024/030/049; IMP-005/008/016 | Request, expected/actual ownership, finite/grid/enum/partial boundaries; INDIVIDUAL_GUARD_MAPPING_PARTIAL |
| `Include/Execution/HSBI_TransactionTypes.mqh` | `1b244dc72cd345f0f032dde14eb89227db20a7333cbc2c72afa2046c4720d8c9` / `bf82abf9b8aa212ce3c96f6c859e70000968b52d` | 1–24 | HSBI_IsCompletedOutcome:6; HSBI_IsRetryOfSameAction:7; HSBI_IsFreshEvent:8; HSBI_TransactionBarrierPassed:9; HSBI_RetryAllowed:20 | Docs/07_TRANSACTION_EXECUTION_CONTRACT_RU.md; Docs/HSB.2C_Execution_Intent_Spec.md | F036/F046/F057/F062/F063 | ERR-010/024/030/049; IMP-005/008/016 | Request, expected/actual ownership, finite/grid/enum/partial boundaries; INDIVIDUAL_GUARD_MAPPING_PARTIAL |
| `Include/Money/HSBI_AllocationLedgerTypes.mqh` | `b539c3c52089e22c2e5cba5a95b81bdc5267b59402bf0f3662f48e80dc1b155c` / `87f86ec7498bd115f5a21da34d596c0ce0c2170a` | 1–11 | HSBI_AllocatedTotal:6; HSBI_ValidateAllocationConservation:7; HSBI_ClassifyAllocationDuplicate:8; HSBI_CanConsumeBucket:9; HSBI_CanConsumeAmount:10 | Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md; Docs/24_BROKER_MONEY_MODEL_RU.md; Docs/31_MONEY_PROOF_IDENTITY_RU.md; Docs/32_RESERVE_ALLOCATION_CONSUMPTION_RU.md | F007–023/F034–036/F040–043/F049/F053–057/F060/F064/F065 | ERR-001–008/011/022/033/034/043/044/047/048; IMP-001–005/009/010/014/020 | Signed/projected/actual domain, source identity, allocation, owner/bucket; backend отсутствует; INDIVIDUAL_GUARD_MAPPING_PARTIAL |
| `Include/Money/HSBI_AllocationPolicyTypes.mqh` | `f92a56ef4016231d435840b360ad8310eaa227657fddaf59dec1a3fb7001f3c0` / `720942a0049cacc76691e600efdef7018e91d482` | 1–32 | HSBI_ValidateAllocationPolicy:16; HSBI_AllocationPolicyDigest:25 | Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md; Docs/24_BROKER_MONEY_MODEL_RU.md; Docs/31_MONEY_PROOF_IDENTITY_RU.md; Docs/32_RESERVE_ALLOCATION_CONSUMPTION_RU.md | F007–023/F034–036/F040–043/F049/F053–057/F060/F064/F065 | ERR-001–008/011/022/033/034/043/044/047/048; IMP-001–005/009/010/014/020 | Signed/projected/actual domain, source identity, allocation, owner/bucket; backend отсутствует; INDIVIDUAL_GUARD_MAPPING_PARTIAL |
| `Include/Money/HSBI_BasketMoneyEvaluator.mqh` | `f2038e34a8cc22d2e98cf870e479e6a3cbfe3d6edee64855ffb8784d1e5007fb` / `4bea204e91a4719b4b24086304cb51051909a7de` | 1–29 | HSBI_BasketLegInput:7; HSBI_EvaluateBasketMoney:11; HSBI_BasketMoneyProofDigest:20 | Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md; Docs/24_BROKER_MONEY_MODEL_RU.md; Docs/31_MONEY_PROOF_IDENTITY_RU.md; Docs/32_RESERVE_ALLOCATION_CONSUMPTION_RU.md | F007–023/F034–036/F040–043/F049/F053–057/F060/F064/F065 | ERR-001–008/011/022/033/034/043/044/047/048; IMP-001–005/009/010/014/020 | Signed/projected/actual domain, source identity, allocation, owner/bucket; backend отсутствует; INDIVIDUAL_GUARD_MAPPING_PARTIAL |
| `Include/Money/HSBI_BrokerMarginModel.mqh` | `6d9734df01ff3717a537e59dfea8a345443ee558585d2e08313428e652a8e345` / `a8c0f43465785d7d6c82517124c3e3b028862337` | 1–18 | HSBI_CalculateProjectedMargin:5 | Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md; Docs/24_BROKER_MONEY_MODEL_RU.md; Docs/31_MONEY_PROOF_IDENTITY_RU.md; Docs/32_RESERVE_ALLOCATION_CONSUMPTION_RU.md | F007–023/F034–036/F040–043/F049/F053–057/F060/F064/F065 | ERR-001–008/011/022/033/034/043/044/047/048; IMP-001–005/009/010/014/020 | Signed/projected/actual domain, source identity, allocation, owner/bucket; backend отсутствует; INDIVIDUAL_GUARD_MAPPING_PARTIAL |
| `Include/Money/HSBI_BrokerMoneyModel.mqh` | `66b0389135f3438acb712d8cf694db4de24f6b7e80a4b6dad1ac249e879ab068` / `4dbee633bceb914365e536acc00208955c01588f` | 1–22 | HSBI_MoneyResult:5; HSBI_CalculateProjectedProfit:6 | Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md; Docs/24_BROKER_MONEY_MODEL_RU.md; Docs/31_MONEY_PROOF_IDENTITY_RU.md; Docs/32_RESERVE_ALLOCATION_CONSUMPTION_RU.md | F007–023/F034–036/F040–043/F049/F053–057/F060/F064/F065 | ERR-001–008/011/022/033/034/043/044/047/048; IMP-001–005/009/010/014/020 | Signed/projected/actual domain, source identity, allocation, owner/bucket; backend отсутствует; INDIVIDUAL_GUARD_MAPPING_PARTIAL |
| `Include/Money/HSBI_BrokerMoneyTypes.mqh` | `276e9ff6308b575be208f4cc23663d7a0489d9bcce8ec67a1a9472f437a092a4` / `ebcd16b2a9ea770d9c8525f5ed3285f3a5129870` | 1–20 | HSBI_IsFiniteNumber:10; HSBI_ValidateBrokerProperties:11 | Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md; Docs/24_BROKER_MONEY_MODEL_RU.md; Docs/31_MONEY_PROOF_IDENTITY_RU.md; Docs/32_RESERVE_ALLOCATION_CONSUMPTION_RU.md | F007–023/F034–036/F040–043/F049/F053–057/F060/F064/F065 | ERR-001–008/011/022/033/034/043/044/047/048; IMP-001–005/009/010/014/020 | Signed/projected/actual domain, source identity, allocation, owner/bucket; backend отсутствует; INDIVIDUAL_GUARD_MAPPING_PARTIAL |
| `Include/Money/HSBI_CandidateMoneyEvaluator.mqh` | `1a50a1d0c4078049c6723d4db1c7ba1409dff6fca244d10a8e7f955eee21f945` / `5402799247ff948b2616306060764004b468abf2` | 1–28 | HSBI_EvaluateCandidateMoney:10 | Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md; Docs/24_BROKER_MONEY_MODEL_RU.md; Docs/31_MONEY_PROOF_IDENTITY_RU.md; Docs/32_RESERVE_ALLOCATION_CONSUMPTION_RU.md | F007–023/F034–036/F040–043/F049/F053–057/F060/F064/F065 | ERR-001–008/011/022/033/034/043/044/047/048; IMP-001–005/009/010/014/020 | Signed/projected/actual domain, source identity, allocation, owner/bucket; backend отсутствует; INDIVIDUAL_GUARD_MAPPING_PARTIAL |
| `Include/Money/HSBI_CatchUpModel.mqh` | `daab1f3d7fa18de44dea6ac293b09cd33bcc3263e691b6f3f7a5fc1dcc10b83c` / `33a87589e8663ddf97b8c7495978b7462149d733` | 1–17 | HSBI_EvaluateCatchUp:4 | Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md; Docs/24_BROKER_MONEY_MODEL_RU.md; Docs/31_MONEY_PROOF_IDENTITY_RU.md; Docs/32_RESERVE_ALLOCATION_CONSUMPTION_RU.md | F007–023/F034–036/F040–043/F049/F053–057/F060/F064/F065 | ERR-001–008/011/022/033/034/043/044/047/048; IMP-001–005/009/010/014/020 | Signed/projected/actual domain, source identity, allocation, owner/bucket; backend отсутствует; INDIVIDUAL_GUARD_MAPPING_PARTIAL |
| `Include/Money/HSBI_CatchUpTypes.mqh` | `2d54a0ac9b149a89d3f35c2b72abad97820f7ef73d2b86118389db59bd4a142a` / `431dd7f52b9ee82f127d04d5db6a95e25545095c` | 1–6 | DTO/enums/config declarations; no matched function | Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md; Docs/24_BROKER_MONEY_MODEL_RU.md; Docs/31_MONEY_PROOF_IDENTITY_RU.md; Docs/32_RESERVE_ALLOCATION_CONSUMPTION_RU.md | F007–023/F034–036/F040–043/F049/F053–057/F060/F064/F065 | ERR-001–008/011/022/033/034/043/044/047/048; IMP-001–005/009/010/014/020 | Signed/projected/actual domain, source identity, allocation, owner/bucket; backend отсутствует; INDIVIDUAL_GUARD_MAPPING_PARTIAL |
| `Include/Money/HSBI_CostModel.mqh` | `4f19ebab853118d7946f99a5fed2b9d84cbfd16c83390df9f5721c53c207f590` / `293a22c0ff14bc6d635e0cc50c79c8e3d4a7d5cd` | 1–20 | HSBI_ValidateCostSnapshot:5; HSBI_TryActualDealNet:11; HSBI_TryProjectedNetMoney:15 | Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md; Docs/24_BROKER_MONEY_MODEL_RU.md; Docs/31_MONEY_PROOF_IDENTITY_RU.md; Docs/32_RESERVE_ALLOCATION_CONSUMPTION_RU.md | F007–023/F034–036/F040–043/F049/F053–057/F060/F064/F065 | ERR-001–008/011/022/033/034/043/044/047/048; IMP-001–005/009/010/014/020 | Signed/projected/actual domain, source identity, allocation, owner/bucket; backend отсутствует; INDIVIDUAL_GUARD_MAPPING_PARTIAL |
| `Include/Money/HSBI_EconomicLedgerTypes.mqh` | `d9bcbef0fa7b6c5da61e7bafa6a6314458601252a2e580aac21396daadf95ed4` / `e589337d228323dba278b242d01e61fc0ee733fe` | 1–13 | HSBI_BuildSourceDealKey:7; HSBI_ValidateEconomicRecord:8; HSBI_SameEconomicRecord:9; HSBI_ClassifyEconomicDuplicate:10; HSBI_SerializeEconomicRecord:11; HSBI_IsHarvestSourceEntry:12 | Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md; Docs/24_BROKER_MONEY_MODEL_RU.md; Docs/31_MONEY_PROOF_IDENTITY_RU.md; Docs/32_RESERVE_ALLOCATION_CONSUMPTION_RU.md | F007–023/F034–036/F040–043/F049/F053–057/F060/F064/F065 | ERR-001–008/011/022/033/034/043/044/047/048; IMP-001–005/009/010/014/020 | Signed/projected/actual domain, source identity, allocation, owner/bucket; backend отсутствует; INDIVIDUAL_GUARD_MAPPING_PARTIAL |
| `Include/Money/HSBI_LevelMarginEvaluator.mqh` | `11e0a67346fb7ca7334d59507c44daee2c0517acee9786a251d03752f8dc774f` / `2227a0ef16caa44f4e4ffefcf860499773dbf471` | 1–13 | HSBI_EvaluateProjectedLegMargin:5 | Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md; Docs/24_BROKER_MONEY_MODEL_RU.md; Docs/31_MONEY_PROOF_IDENTITY_RU.md; Docs/32_RESERVE_ALLOCATION_CONSUMPTION_RU.md | F007–023/F034–036/F040–043/F049/F053–057/F060/F064/F065 | ERR-001–008/011/022/033/034/043/044/047/048; IMP-001–005/009/010/014/020 | Signed/projected/actual domain, source identity, allocation, owner/bucket; backend отсутствует; INDIVIDUAL_GUARD_MAPPING_PARTIAL |
| `Include/Money/HSBI_LevelMoneyEvaluator.mqh` | `cbe8d9c662250eaad105987f1540c00e56932cf9546c1bff29ca000e604a19b6` / `3c89ae2355945ec7c75fac2694967ae5f1785967` | 1–16 | HSBI_EvaluateProjectedLegMoney:7 | Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md; Docs/24_BROKER_MONEY_MODEL_RU.md; Docs/31_MONEY_PROOF_IDENTITY_RU.md; Docs/32_RESERVE_ALLOCATION_CONSUMPTION_RU.md | F007–023/F034–036/F040–043/F049/F053–057/F060/F064/F065 | ERR-001–008/011/022/033/034/043/044/047/048; IMP-001–005/009/010/014/020 | Signed/projected/actual domain, source identity, allocation, owner/bucket; backend отсутствует; INDIVIDUAL_GUARD_MAPPING_PARTIAL |
| `Include/Money/HSBI_MoneyProofIdentity.mqh` | `f36029a3f62cf3d245962ea18d408555d507851e9a5e9e1e9d11c5868a28f17d` / `cb00b547b9f4d3d9eac7a473415b25627c3ac91d` | 1–30 | HSBI_ValidateMoneyProofIdentity:10; HSBI_IsSameMoneyProofIdentity:16; HSBI_MoneyProofIdentityDigest:23 | Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md; Docs/24_BROKER_MONEY_MODEL_RU.md; Docs/31_MONEY_PROOF_IDENTITY_RU.md; Docs/32_RESERVE_ALLOCATION_CONSUMPTION_RU.md | F007–023/F034–036/F040–043/F049/F053–057/F060/F064/F065 | ERR-001–008/011/022/033/034/043/044/047/048; IMP-001–005/009/010/014/020 | Signed/projected/actual domain, source identity, allocation, owner/bucket; backend отсутствует; INDIVIDUAL_GUARD_MAPPING_PARTIAL |
| `Include/Money/HSBI_MoneyState.mqh` | `0faeebfc6781198ead86e8cffac7e154947f1830e6b38d27d7900d069ac38396` / `d318c28cc23ddaf19d22a9c7a47e9202800d1786` | 1–6 | HSBI_ValidateMoneyState:5 | Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md; Docs/24_BROKER_MONEY_MODEL_RU.md; Docs/31_MONEY_PROOF_IDENTITY_RU.md; Docs/32_RESERVE_ALLOCATION_CONSUMPTION_RU.md | F007–023/F034–036/F040–043/F049/F053–057/F060/F064/F065 | ERR-001–008/011/022/033/034/043/044/047/048; IMP-001–005/009/010/014/020 | Signed/projected/actual domain, source identity, allocation, owner/bucket; backend отсутствует; INDIVIDUAL_GUARD_MAPPING_PARTIAL |
| `Include/Money/HSBI_MoneyTypes.mqh` | `d7d00aa5a139ec82730e84ab18748ba49f12a339d0716255517b3377a4f94d70` / `2a3226fe19fdeb8053b618d2d7ca72ed111e6bb5` | 1–10 | HSBI_BuildRecoveryPL:9 | Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md; Docs/24_BROKER_MONEY_MODEL_RU.md; Docs/31_MONEY_PROOF_IDENTITY_RU.md; Docs/32_RESERVE_ALLOCATION_CONSUMPTION_RU.md | F007–023/F034–036/F040–043/F049/F053–057/F060/F064/F065 | ERR-001–008/011/022/033/034/043/044/047/048; IMP-001–005/009/010/014/020 | Signed/projected/actual domain, source identity, allocation, owner/bucket; backend отсутствует; INDIVIDUAL_GUARD_MAPPING_PARTIAL |
| `Include/Money/HSBI_ReserveAllocationTypes.mqh` | `18a3318d954d2f2426ec715441fc159fca364cdb1b65011b449e94d0671dd00f` / `f1464320f1f853f12f8e3f3ddc3708bad2a0cd4d` | 1–35 | HSBI_ValidateReserveAllocationSource:15; HSBI_ValidateReserveConsumption:25; HSBI_IsDuplicateReserveConsumption:27; HSBI_ReserveConsumptionConflict:29; HSBI_ReserveAllocationSourceDigest:31; HSBI_ReserveConsumptionKeyDigest:33 | Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md; Docs/24_BROKER_MONEY_MODEL_RU.md; Docs/31_MONEY_PROOF_IDENTITY_RU.md; Docs/32_RESERVE_ALLOCATION_CONSUMPTION_RU.md | F007–023/F034–036/F040–043/F049/F053–057/F060/F064/F065 | ERR-001–008/011/022/033/034/043/044/047/048; IMP-001–005/009/010/014/020 | Signed/projected/actual domain, source identity, allocation, owner/bucket; backend отсутствует; INDIVIDUAL_GUARD_MAPPING_PARTIAL |
| `Include/Money/HSBI_ReserveCatchUpEvaluator.mqh` | `5d967cf22e7d0fdc3d37aae6077b15c4330526dcef4c5b8eda74340a64ff174d` / `87a8b7e97727ce6e47c2a2f0abc3e237f6203204` | 1–83 | HSBI_ValidateReserveSourceProof:24; HSBI_ValidateFarLossProof:30; HSBI_EvaluateReserveCatchUp:35; HSBI_ReserveCatchUpDigest:78 | Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md; Docs/24_BROKER_MONEY_MODEL_RU.md; Docs/31_MONEY_PROOF_IDENTITY_RU.md; Docs/32_RESERVE_ALLOCATION_CONSUMPTION_RU.md | F007–023/F034–036/F040–043/F049/F053–057/F060/F064/F065 | ERR-001–008/011/022/033/034/043/044/047/048; IMP-001–005/009/010/014/020 | Signed/projected/actual domain, source identity, allocation, owner/bucket; backend отсутствует; INDIVIDUAL_GUARD_MAPPING_PARTIAL |
| `Include/Persistence/HSBI_ExecutionJournal.mqh` | `aeba6d8813c0079ae4f8e5c7484895e891e6acb91ae7aeacec751977adf1f76f` / `e65d6d9b0f04a3e236952ec577ea144bf57ee2b2` | 1–45 | HSBI_ExecutionJournalEntryDigest:12; HSBI_ValidateJournalEntry:18; HSBI_IsDuplicateJournalEntry:21; HSBI_IsJournalEntryConflict:23; HSBI_ClassifyJournalAppend:25; HSBI_ValidateJournalChain:31 | Docs/16_PERSISTENCE_AND_RESTART_RU.md; Docs/17_RECONCILIATION_AND_TERMINAL_SAFE_RU.md; Docs/HSB_2E_PERSISTENCE_SCHEMA_RU.md | F057/F060/F065/F066 | ERR-017/025/030/050; IMP-009 | Snapshot/journal validation не durability; complete history отдельно; INDIVIDUAL_GUARD_MAPPING_PARTIAL |
| `Include/Persistence/HSBI_ExecutionStateSnapshot.mqh` | `e228f6b8e2e2d0bc2aeaa8cbab6c7656412465a9f887fa8fe6b152d463e3d971` / `4fc1e37af6430d206bb2c7b480681473cd9c2bf2` | 1–44 | HSBI_ExecutionStateSnapshotDigest:12; HSBI_ValidateNestedExecutionIntent:19; HSBI_IsActiveIntentStatus:25; HSBI_ValidateExecutionStateSnapshot:27; HSBI_RecoverExecutionState:42 | Docs/16_PERSISTENCE_AND_RESTART_RU.md; Docs/17_RECONCILIATION_AND_TERMINAL_SAFE_RU.md; Docs/HSB_2E_PERSISTENCE_SCHEMA_RU.md | F057/F060/F065/F066 | ERR-017/025/030/050; IMP-009 | Snapshot/journal validation не durability; complete history отдельно; INDIVIDUAL_GUARD_MAPPING_PARTIAL |
| `Include/Persistence/HSBI_JournalTypes.mqh` | `800b8610c306a6d197df37b99ad93da09278f09a68049543578577d2348d80c8` / `c2f007a44020dba1f5e0cb2c4f52342d1d0c9f8f` | 1–8 | HSBI_ValidateJournalRecord:6; HSBI_SerializeJournalIds:7 | Docs/16_PERSISTENCE_AND_RESTART_RU.md; Docs/17_RECONCILIATION_AND_TERMINAL_SAFE_RU.md; Docs/HSB_2E_PERSISTENCE_SCHEMA_RU.md | F057/F060/F065/F066 | ERR-017/025/030/050; IMP-009 | Snapshot/journal validation не durability; complete history отдельно; INDIVIDUAL_GUARD_MAPPING_PARTIAL |
| `Include/Persistence/HSBI_PersistenceInterface.mqh` | `e72b591500db88e2596c498fcdf7dbfdbe3641eef91ebbee80ce59e3aeddab06` / `36b7181f50fe4554d24f9ea6813906f9f4240d49` | 1–8 | HSBI_PersistSnapshotStub:7 | Docs/16_PERSISTENCE_AND_RESTART_RU.md; Docs/17_RECONCILIATION_AND_TERMINAL_SAFE_RU.md; Docs/HSB_2E_PERSISTENCE_SCHEMA_RU.md | F057/F060/F065/F066 | ERR-017/025/030/050; IMP-009 | Snapshot/journal validation не durability; complete history отдельно; INDIVIDUAL_GUARD_MAPPING_PARTIAL |
| `Include/Persistence/HSBI_ReconciliationTypes.mqh` | `dc7260cd56d8392664ebecfb9fd3790cfe768f1a1ab9d428ed6bf83c14679c0d` / `1e79faeeef3b32aa5318f815f8308b67950ae3b2` | 1–8 | HSBI_CompareReconciliation:7 | Docs/16_PERSISTENCE_AND_RESTART_RU.md; Docs/17_RECONCILIATION_AND_TERMINAL_SAFE_RU.md; Docs/HSB_2E_PERSISTENCE_SCHEMA_RU.md | F057/F060/F065/F066 | ERR-017/025/030/050; IMP-009 | Snapshot/journal validation не durability; complete history отдельно; INDIVIDUAL_GUARD_MAPPING_PARTIAL |
| `Include/Persistence/HSBI_SnapshotTypes.mqh` | `d40945509150276d1e8ca60de173cf64af3a6ddff91f5ac1361c8533d41a5b9e` / `f3c7789f323657aee83c34544b0143165b454279` | 1–11 | HSBI_ValidateSnapshotSchema:8; HSBI_TestDigest:9; HSBI_SerializeSnapshotIds:10 | Docs/16_PERSISTENCE_AND_RESTART_RU.md; Docs/17_RECONCILIATION_AND_TERMINAL_SAFE_RU.md; Docs/HSB_2E_PERSISTENCE_SCHEMA_RU.md | F057/F060/F065/F066 | ERR-017/025/030/050; IMP-009 | Snapshot/journal validation не durability; complete history отдельно; INDIVIDUAL_GUARD_MAPPING_PARTIAL |
| `Include/Planning/HSBI_BrokerGrid.mqh` | `4cb955469a6c502456d9db146cb5fd80568807cc23abcdcdd9bcf5e4f4dd110c` / `82a06297b2c98113f18d92ebf3cd7bdc615749a0` | 1–38 | HSBI_GridTolerance:7; HSBI_IsPriceOnTickGrid:8; HSBI_NormalizePriceToTick:13; HSBI_ValidatePriceGrid:19; HSBI_PriceDistanceInTicks:20; HSBI_IsVolumeOnGrid:21; HSBI_FloorVolumeToStep:26; HSBI_CeilVolumeToStep:27; HSBI_NormalizeVolume:28; HSBI_ValidateVolume:33 | Docs/05_GEOMETRY_MODEL_RU.md; Docs/25_BROKER_GRID_AND_ROUNDING_RU.md; Docs/27_FUTURE_SMALL_SOLVER_RU.md; Docs/28_NEW_FAR_SOLVER_RU.md; Docs/29_CANDIDATE_OBJECTIVE_AND_TIEBREAK_RU.md; Docs/30_FUTURE_SMALL_AGGREGATE_PROOF_RU.md | F001–006/F023/F027–030/F037–039/F044–048/F051/F052/F058/F061 | ERR-013–015/018–021/031/032/037/039–041/045/046; IMP-007/010–013/016/021/022 | Actual residual versus planned N, Gross versus Net, mirrored coordinate, grid и finite-prefix scope; INDIVIDUAL_GUARD_MAPPING_PARTIAL |
| `Include/Planning/HSBI_CandidatePlan.mqh` | `3643a4a741e24e293656674b3681a74a5ef448610428f28a07dbf355533ac856` / `f056148d2bccd020b01d6c8a7433fbba9e83f158` | 1–9 | HSBI_ValidateCandidatePlan:6; HSBI_CandidatePlanFingerprint:7; HSBI_SameCandidatePlan:8 | Docs/05_GEOMETRY_MODEL_RU.md; Docs/25_BROKER_GRID_AND_ROUNDING_RU.md; Docs/27_FUTURE_SMALL_SOLVER_RU.md; Docs/28_NEW_FAR_SOLVER_RU.md; Docs/29_CANDIDATE_OBJECTIVE_AND_TIEBREAK_RU.md; Docs/30_FUTURE_SMALL_AGGREGATE_PROOF_RU.md | F001–006/F023/F027–030/F037–039/F044–048/F051/F052/F058/F061 | ERR-013–015/018–021/031/032/037/039–041/045/046; IMP-007/010–013/016/021/022 | Actual residual versus planned N, Gross versus Net, mirrored coordinate, grid и finite-prefix scope; INDIVIDUAL_GUARD_MAPPING_PARTIAL |
| `Include/Planning/HSBI_ControlPrices.mqh` | `5bd35f0cc4b7ee1aac1a772b2932f13ba385922e26d5f2649bbda76837256a4b` / `2540db9d53533319319b698d999187f785f0815c` | 1–25 | HSBI_IsSnapshotFresh:11; HSBI_NormalizePriceToTick:12; HSBI_ResolveCloseSide:13; HSBI_ValidateMarketSnapshot:14; HSBI_ValidateControlPriceSet:15; HSBI_ValidateTypedControlPrice:16 | Docs/05_GEOMETRY_MODEL_RU.md; Docs/25_BROKER_GRID_AND_ROUNDING_RU.md; Docs/27_FUTURE_SMALL_SOLVER_RU.md; Docs/28_NEW_FAR_SOLVER_RU.md; Docs/29_CANDIDATE_OBJECTIVE_AND_TIEBREAK_RU.md; Docs/30_FUTURE_SMALL_AGGREGATE_PROOF_RU.md | F001–006/F023/F027–030/F037–039/F044–048/F051/F052/F058/F061 | ERR-013–015/018–021/031/032/037/039–041/045/046; IMP-007/010–013/016/021/022 | Actual residual versus planned N, Gross versus Net, mirrored coordinate, grid и finite-prefix scope; INDIVIDUAL_GUARD_MAPPING_PARTIAL |
| `Include/Planning/HSBI_DecisionResult.mqh` | `cb5f7cd0c719ca81ad35547d49af8ba827d94d3bb41dbb88c0451eebf306849d` / `2847c1b1c61502ffa7cba9813e0a843afcf1a50b` | 1–5 | DTO/enums/config declarations; no matched function | Docs/05_GEOMETRY_MODEL_RU.md; Docs/25_BROKER_GRID_AND_ROUNDING_RU.md; Docs/27_FUTURE_SMALL_SOLVER_RU.md; Docs/28_NEW_FAR_SOLVER_RU.md; Docs/29_CANDIDATE_OBJECTIVE_AND_TIEBREAK_RU.md; Docs/30_FUTURE_SMALL_AGGREGATE_PROOF_RU.md | F001–006/F023/F027–030/F037–039/F044–048/F051/F052/F058/F061 | ERR-013–015/018–021/031/032/037/039–041/045/046; IMP-007/010–013/016/021/022 | Actual residual versus planned N, Gross versus Net, mirrored coordinate, grid и finite-prefix scope; INDIVIDUAL_GUARD_MAPPING_PARTIAL |
| `Include/Planning/HSBI_FutureSmallProofAggregator.mqh` | `7bea2c75eec23825d5cbcca82fa72022b73f8c1626f5ffbce30ac79d722b03a0` / `4678ae152960e98b9f398b4497786061d7e8a524` | 1–60 | HSBI_AggregateDigest:16; HSBI_AggregateFutureSmallProof:23 | Docs/05_GEOMETRY_MODEL_RU.md; Docs/25_BROKER_GRID_AND_ROUNDING_RU.md; Docs/27_FUTURE_SMALL_SOLVER_RU.md; Docs/28_NEW_FAR_SOLVER_RU.md; Docs/29_CANDIDATE_OBJECTIVE_AND_TIEBREAK_RU.md; Docs/30_FUTURE_SMALL_AGGREGATE_PROOF_RU.md | F001–006/F023/F027–030/F037–039/F044–048/F051/F052/F058/F061 | ERR-013–015/018–021/031/032/037/039–041/045/046; IMP-007/010–013/016/021/022 | Actual residual versus planned N, Gross versus Net, mirrored coordinate, grid и finite-prefix scope; INDIVIDUAL_GUARD_MAPPING_PARTIAL |
| `Include/Planning/HSBI_FutureSmallSolver.mqh` | `c403bbad6089076500823219dac296e69100bed0e2cb950eb1f248749b868cf6` / `be55c93f051f57ddffd189b9d2e8eee4c3ddaf9d` | 1–151 | HSBI_CalculateFutureSmallDepth:5; HSBI_ValidateConservativeBound:12; HSBI_ValidateLevelMarket:18; HSBI_ValidateLevelCosts:27; HSBI_ValidateFarProjection:32; HSBI_LevelControlPrice:39; HSBI_ValidateFutureSmallInput:45; HSBI_EvaluateFutureSmallLevel:57; HSBI_FutureSmallLevelDigest:93; HSBI_FutureSmallProofDigest:106; HSBI_SolveFutureSmall:113 | Docs/05_GEOMETRY_MODEL_RU.md; Docs/25_BROKER_GRID_AND_ROUNDING_RU.md; Docs/27_FUTURE_SMALL_SOLVER_RU.md; Docs/28_NEW_FAR_SOLVER_RU.md; Docs/29_CANDIDATE_OBJECTIVE_AND_TIEBREAK_RU.md; Docs/30_FUTURE_SMALL_AGGREGATE_PROOF_RU.md | F001–006/F023/F027–030/F037–039/F044–048/F051/F052/F058/F061 | ERR-013–015/018–021/031/032/037/039–041/045/046; IMP-007/010–013/016/021/022 | Actual residual versus planned N, Gross versus Net, mirrored coordinate, grid и finite-prefix scope; INDIVIDUAL_GUARD_MAPPING_PARTIAL |
| `Include/Planning/HSBI_FutureSmallTypes.mqh` | `16fcecb00c05f2e03b90f81823bdf1c2aac4a7b6263713b29ad9feb18b218325` / `ee962ed40a99b0d0a1fdd22f2ee071cc3fb6cbcc` | 1–82 | DTO/enums/config declarations; no matched function | Docs/05_GEOMETRY_MODEL_RU.md; Docs/25_BROKER_GRID_AND_ROUNDING_RU.md; Docs/27_FUTURE_SMALL_SOLVER_RU.md; Docs/28_NEW_FAR_SOLVER_RU.md; Docs/29_CANDIDATE_OBJECTIVE_AND_TIEBREAK_RU.md; Docs/30_FUTURE_SMALL_AGGREGATE_PROOF_RU.md | F001–006/F023/F027–030/F037–039/F044–048/F051/F052/F058/F061 | ERR-013–015/018–021/031/032/037/039–041/045/046; IMP-007/010–013/016/021/022 | Actual residual versus planned N, Gross versus Net, mirrored coordinate, grid и finite-prefix scope; INDIVIDUAL_GUARD_MAPPING_PARTIAL |
| `Include/Planning/HSBI_GeometrySolver.mqh` | `62b3b4a8d7a374e15b96b46a380e3c2f8f0e74aa57ae8749c0261ebab27a11f9` / `707cc1678ca4d98888b3acc2599838094fe13a78` | 1–38 | HSBI_ValidateRecoverySlope:6; HSBI_EvaluateRecoveryMoneyDirection:12; HSBI_SolveBigGeometry:21 | Docs/05_GEOMETRY_MODEL_RU.md; Docs/25_BROKER_GRID_AND_ROUNDING_RU.md; Docs/27_FUTURE_SMALL_SOLVER_RU.md; Docs/28_NEW_FAR_SOLVER_RU.md; Docs/29_CANDIDATE_OBJECTIVE_AND_TIEBREAK_RU.md; Docs/30_FUTURE_SMALL_AGGREGATE_PROOF_RU.md | F001–006/F023/F027–030/F037–039/F044–048/F051/F052/F058/F061 | ERR-013–015/018–021/031/032/037/039–041/045/046; IMP-007/010–013/016/021/022 | Actual residual versus planned N, Gross versus Net, mirrored coordinate, grid и finite-prefix scope; INDIVIDUAL_GUARD_MAPPING_PARTIAL |
| `Include/Planning/HSBI_GeometryTypes.mqh` | `3126ecc200269b885bf2b5b46b8e72356f61e176b829ab0f40ee307e5b4e8b49` / `3471f80349bdb20f8a13a99d11fd9b9244e93498` | 1–7 | DTO/enums/config declarations; no matched function | Docs/05_GEOMETRY_MODEL_RU.md; Docs/25_BROKER_GRID_AND_ROUNDING_RU.md; Docs/27_FUTURE_SMALL_SOLVER_RU.md; Docs/28_NEW_FAR_SOLVER_RU.md; Docs/29_CANDIDATE_OBJECTIVE_AND_TIEBREAK_RU.md; Docs/30_FUTURE_SMALL_AGGREGATE_PROOF_RU.md | F001–006/F023/F027–030/F037–039/F044–048/F051/F052/F058/F061 | ERR-013–015/018–021/031/032/037/039–041/045/046; IMP-007/010–013/016/021/022 | Actual residual versus planned N, Gross versus Net, mirrored coordinate, grid и finite-prefix scope; INDIVIDUAL_GUARD_MAPPING_PARTIAL |
| `Include/Planning/HSBI_NewFarCandidate.mqh` | `9e09da3a5d22579807375be836931a11ecf666e79108dde2c9724f60f1cd2bf1` / `758f1c89cf75701d3616dabec2fcb06413ee2d4a` | 1–42 | HSBI_ValidateNewFarCandidateStructure:19; HSBI_IsCandidateSourceValid:24; HSBI_IsCompleteCandidateProof:26; HSBI_CompareCandidateTieBreak:33 | Docs/05_GEOMETRY_MODEL_RU.md; Docs/25_BROKER_GRID_AND_ROUNDING_RU.md; Docs/27_FUTURE_SMALL_SOLVER_RU.md; Docs/28_NEW_FAR_SOLVER_RU.md; Docs/29_CANDIDATE_OBJECTIVE_AND_TIEBREAK_RU.md; Docs/30_FUTURE_SMALL_AGGREGATE_PROOF_RU.md | F001–006/F023/F027–030/F037–039/F044–048/F051/F052/F058/F061 | ERR-013–015/018–021/031/032/037/039–041/045/046; IMP-007/010–013/016/021/022 | Actual residual versus planned N, Gross versus Net, mirrored coordinate, grid и finite-prefix scope; INDIVIDUAL_GUARD_MAPPING_PARTIAL |
| `Include/Planning/HSBI_NewFarSolver.mqh` | `9dcf60b6edc245a8a5ee3a05f35d4d8d26c12479f570a66aa5e4f0e703497cd2` / `3d19eccd6cd318b9b4591e2bc0ccaa95f661930d` | 1–154 | HSBI_FutureSmallTemplateDigest:35; HSBI_NewFarInputDigest:47; HSBI_FinalizeNewFarPlanDigest:59; HSBI_ValidateNewFarSource:60; HSBI_AllowedTransitionLoss:74; HSBI_BuildCandidateFutureSmallInput:75; HSBI_NewFarProofIdentity:80; HSBI_CandidateProofDigest:84; HSBI_SolveNewFar:94 | Docs/05_GEOMETRY_MODEL_RU.md; Docs/25_BROKER_GRID_AND_ROUNDING_RU.md; Docs/27_FUTURE_SMALL_SOLVER_RU.md; Docs/28_NEW_FAR_SOLVER_RU.md; Docs/29_CANDIDATE_OBJECTIVE_AND_TIEBREAK_RU.md; Docs/30_FUTURE_SMALL_AGGREGATE_PROOF_RU.md | F001–006/F023/F027–030/F037–039/F044–048/F051/F052/F058/F061 | ERR-013–015/018–021/031/032/037/039–041/045/046; IMP-007/010–013/016/021/022 | Actual residual versus planned N, Gross versus Net, mirrored coordinate, grid и finite-prefix scope; INDIVIDUAL_GUARD_MAPPING_PARTIAL |
| `Include/Risk/HSBI_CalculationGateTypes.mqh` | `64791ac97362dfd8a5bcf5e5b294b1b71f8d984acc10a41853d27e20328e0900` / `06b75ded19b5c5d51e401066592dfc3ff1981e71` | 1–14 | HSBI_FailClosed:6; HSBI_CalculationResultFlagsValid:10 | Docs/15_RISK_AND_MARGIN_CONTRACT_RU.md | F024–026/F031–033/F036/F052/F059 | ERR-009/034/035/038/041; IMP-005/015/019/021/022 | Finite/domain guards и independent adverse/margin model; cap не fill guarantee; INDIVIDUAL_GUARD_MAPPING_PARTIAL |
| `Include/Risk/HSBI_FutureSmallRiskEvaluator.mqh` | `8ffa044f6819186aac145df165c80a32c0d7225142b28d3ef413326518277f7b` / `870d84b3f49a85e7db5c6d5ead777efea1c9faa3` | 1–52 | HSBI_EvaluateFutureSmallRisk:29 | Docs/15_RISK_AND_MARGIN_CONTRACT_RU.md | F024–026/F031–033/F036/F052/F059 | ERR-009/034/035/038/041; IMP-005/015/019/021/022 | Finite/domain guards и independent adverse/margin model; cap не fill guarantee; INDIVIDUAL_GUARD_MAPPING_PARTIAL |
| `Include/Risk/HSBI_NewFarGateTypes.mqh` | `d82738006b15bb85990171b96cf65662a2699b6b890501fdd6cf31e73c1e9272` / `7d50669bda8ff2d000566ad7a38281140a77ae83` | 1–18 | HSBI_EvaluateNewFarGates:6 | Docs/15_RISK_AND_MARGIN_CONTRACT_RU.md | F024–026/F031–033/F036/F052/F059 | ERR-009/034/035/038/041; IMP-005/015/019/021/022 | Finite/domain guards и independent adverse/margin model; cap не fill guarantee; INDIVIDUAL_GUARD_MAPPING_PARTIAL |
| `Include/Risk/HSBI_RiskGateResult.mqh` | `d0d7072973dac81be9284562046b7227ecfafbe14962c9ad05a3f8e2c73585c8` / `f172bd2ab9cfc461ab403a8ce490a4b71ce3c8c4` | 1–7 | HSBI_ValidateRiskInput:6 | Docs/15_RISK_AND_MARGIN_CONTRACT_RU.md | F024–026/F031–033/F036/F052/F059 | ERR-009/034/035/038/041; IMP-005/015/019/021/022 | Finite/domain guards и independent adverse/margin model; cap не fill guarantee; INDIVIDUAL_GUARD_MAPPING_PARTIAL |
| `Include/Risk/HSBI_RiskTypes.mqh` | `327b2b000c136c19340ebcdca287341b7866da9bd209aac713ae393700c6bf4d` / `6f40356c18949a0465c1595b0229a67bbcd46dc7` | 1–5 | DTO/enums/config declarations; no matched function | Docs/15_RISK_AND_MARGIN_CONTRACT_RU.md | F024–026/F031–033/F036/F052/F059 | ERR-009/034/035/038/041; IMP-005/015/019/021/022 | Finite/domain guards и independent adverse/margin model; cap не fill guarantee; INDIVIDUAL_GUARD_MAPPING_PARTIAL |
| `Include/Runtime/HSBI_RuntimeDecisionTypes.mqh` | `cacba88273d9d85bd34f09d978178fc89fdceb672b3651cba683aea1679110f4` / `0cc2619ed6ce7a93ea28c3c655a8d147e18a9231` | 1–18 | HSBI_RuntimeDecisionContextDigest:17 | Docs/07_TRANSACTION_EXECUTION_CONTRACT_RU.md; Docs/16_PERSISTENCE_AND_RESTART_RU.md; Docs/17_RECONCILIATION_AND_TERMINAL_SAFE_RU.md | F036/F057/F060/F065 | ERR-013/016/017/030/033; IMP-001/008/009 | Локальные barriers не подключены к полному main lifecycle; INDIVIDUAL_GUARD_MAPPING_PARTIAL |
| `Include/Runtime/HSBI_RuntimeDecisionValidator.mqh` | `0332a192d4b9a5389f377d252111fb0317f074bc9ff7b51658a9e8de2d5fbd9b` / `aecbf35e7ced9fd756d80803c63626b9b52c0846` | 1–30 | HSBI_RuntimeReject:4; HSBI_RuntimePositionMatches:5; HSBI_ValidateRuntimeDecisionContext:6 | Docs/07_TRANSACTION_EXECUTION_CONTRACT_RU.md; Docs/16_PERSISTENCE_AND_RESTART_RU.md; Docs/17_RECONCILIATION_AND_TERMINAL_SAFE_RU.md | F036/F057/F060/F065 | ERR-013/016/017/030/033; IMP-001/008/009 | Локальные barriers не подключены к полному main lifecycle; INDIVIDUAL_GUARD_MAPPING_PARTIAL |
| `Include/Runtime/HSBI_RuntimeRestartValidator.mqh` | `ec27d83911b89a77c31a6d7347a700e31e8bf631268aaaddfe4eedf976b5cbe7` / `81001f9eadb42a2c8255f38392d1739064dc6749` | 1–18 | HSBI_ValidateRestartedRuntimeState:5 | Docs/07_TRANSACTION_EXECUTION_CONTRACT_RU.md; Docs/16_PERSISTENCE_AND_RESTART_RU.md; Docs/17_RECONCILIATION_AND_TERMINAL_SAFE_RU.md | F036/F057/F060/F065 | ERR-013/016/017/030/033; IMP-001/008/009 | Локальные barriers не подключены к полному main lifecycle; INDIVIDUAL_GUARD_MAPPING_PARTIAL |
| `Include/Runtime/HSBI_RuntimeTransactionBarrier.mqh` | `0e04217f0bd873a784ab65cc87514c7deb65c149b8b23fa7218d885b5cf30f1a` / `2a5df55b4b5814eed26f684b8d86583cf2b53eb6` | 1–19 | HSBI_CanAdvanceRuntimeDecision:5 | Docs/07_TRANSACTION_EXECUTION_CONTRACT_RU.md; Docs/16_PERSISTENCE_AND_RESTART_RU.md; Docs/17_RECONCILIATION_AND_TERMINAL_SAFE_RU.md | F036/F057/F060/F065 | ERR-013/016/017/030/033; IMP-001/008/009 | Локальные barriers не подключены к полному main lifecycle; INDIVIDUAL_GUARD_MAPPING_PARTIAL |
| `Include/Scenarios/HSBI_BigHarvestTypes.mqh` | `0516b1ec1b5720265df3072d28035719d3ed369f29c8bb28177b94a98873f483` / `5be5c560ae6093281ad0f3f30cd7613514f675b1` | 1–5 | DTO/enums/config declarations; no matched function | Docs/09_INITIAL_LOCK_SPECIFICATION_RU.md; Docs/10_BIG_HARVEST_SPECIFICATION_RU.md; Docs/11_PARTIAL_FAR_SPECIFICATION_RU.md; Docs/12_FINAL_CLOSE_SPECIFICATION_RU.md; Docs/13_SMALL_TRANSITION_SPECIFICATION_RU.md | F007/F010–015/F024–026/F035/F040/F050/F052–057 | ERR-016/022/032/036/041/044/045; IMP-008/013/014/019–022 | DTO не handler; full actual settlement / cycle PnL не выполнены; INDIVIDUAL_GUARD_MAPPING_PARTIAL |
| `Include/Scenarios/HSBI_FinalCloseTypes.mqh` | `3adfe776abae340a17b8ae8977c848f15c3b89cc2216085e71a9bf59ae6c53cd` / `319af55c5054e082582da0598c79ed0d319a1599` | 1–5 | DTO/enums/config declarations; no matched function | Docs/09_INITIAL_LOCK_SPECIFICATION_RU.md; Docs/10_BIG_HARVEST_SPECIFICATION_RU.md; Docs/11_PARTIAL_FAR_SPECIFICATION_RU.md; Docs/12_FINAL_CLOSE_SPECIFICATION_RU.md; Docs/13_SMALL_TRANSITION_SPECIFICATION_RU.md | F007/F010–015/F024–026/F035/F040/F050/F052–057 | ERR-016/022/032/036/041/044/045; IMP-008/013/014/019–022 | DTO не handler; full actual settlement / cycle PnL не выполнены; INDIVIDUAL_GUARD_MAPPING_PARTIAL |
| `Include/Scenarios/HSBI_InitialLockTypes.mqh` | `f67baeae393cc58d4d584eb9b22819991ba281f7986f7273d1672a1def634262` / `79b6f2df50ea5c9b38bae46849bddb9f99de108b` | 1–5 | DTO/enums/config declarations; no matched function | Docs/09_INITIAL_LOCK_SPECIFICATION_RU.md; Docs/10_BIG_HARVEST_SPECIFICATION_RU.md; Docs/11_PARTIAL_FAR_SPECIFICATION_RU.md; Docs/12_FINAL_CLOSE_SPECIFICATION_RU.md; Docs/13_SMALL_TRANSITION_SPECIFICATION_RU.md | F007/F010–015/F024–026/F035/F040/F050/F052–057 | ERR-016/022/032/036/041/044/045; IMP-008/013/014/019–022 | DTO не handler; full actual settlement / cycle PnL не выполнены; INDIVIDUAL_GUARD_MAPPING_PARTIAL |
| `Include/Scenarios/HSBI_PartialFarTypes.mqh` | `ea862ce2f05239cc7aef8a94a256f4eaa50534c37f55d3d6c59d5ea6cf545fc5` / `19b41ac1061bee2cd5bd7412b94df2efcb0499c9` | 1–5 | DTO/enums/config declarations; no matched function | Docs/09_INITIAL_LOCK_SPECIFICATION_RU.md; Docs/10_BIG_HARVEST_SPECIFICATION_RU.md; Docs/11_PARTIAL_FAR_SPECIFICATION_RU.md; Docs/12_FINAL_CLOSE_SPECIFICATION_RU.md; Docs/13_SMALL_TRANSITION_SPECIFICATION_RU.md | F007/F010–015/F024–026/F035/F040/F050/F052–057 | ERR-016/022/032/036/041/044/045; IMP-008/013/014/019–022 | DTO не handler; full actual settlement / cycle PnL не выполнены; INDIVIDUAL_GUARD_MAPPING_PARTIAL |
| `Include/Scenarios/HSBI_ScenarioTypes.mqh` | `7cc05c0455d372ef7219b3ac4b86e9b8f2753131bcd8a5ea2819bd8a90dff1f3` / `cd6598113b76dd2754c1ab7c5091c7e59b8d9a9c` | 1–6 | DTO/enums/config declarations; no matched function | Docs/09_INITIAL_LOCK_SPECIFICATION_RU.md; Docs/10_BIG_HARVEST_SPECIFICATION_RU.md; Docs/11_PARTIAL_FAR_SPECIFICATION_RU.md; Docs/12_FINAL_CLOSE_SPECIFICATION_RU.md; Docs/13_SMALL_TRANSITION_SPECIFICATION_RU.md | F007/F010–015/F024–026/F035/F040/F050/F052–057 | ERR-016/022/032/036/041/044/045; IMP-008/013/014/019–022 | DTO не handler; full actual settlement / cycle PnL не выполнены; INDIVIDUAL_GUARD_MAPPING_PARTIAL |
| `Include/Scenarios/HSBI_SmallTransitionTypes.mqh` | `abf62239594b699449646178cfffaf4e15b6317eec9728088fcd98a76531cef1` / `edbe990f0b0a6df2d4cba4368ad126764abad021` | 1–5 | DTO/enums/config declarations; no matched function | Docs/09_INITIAL_LOCK_SPECIFICATION_RU.md; Docs/10_BIG_HARVEST_SPECIFICATION_RU.md; Docs/11_PARTIAL_FAR_SPECIFICATION_RU.md; Docs/12_FINAL_CLOSE_SPECIFICATION_RU.md; Docs/13_SMALL_TRANSITION_SPECIFICATION_RU.md | F007/F010–015/F024–026/F035/F040/F050/F052–057 | ERR-016/022/032/036/041/044/045; IMP-008/013/014/019–022 | DTO не handler; full actual settlement / cycle PnL не выполнены; INDIVIDUAL_GUARD_MAPPING_PARTIAL |
| `Hybrid_Split_Big_Independent_EA.mq5` | `71e511c620df5de7f1f9e0d865664efeaf4cf6edbcbb07f20efaf25c40e9bd62` / `3b306df062b5aabac16ee5874f9cf233c21d3e36` | 1–44 | OnInit:19; OnDeinit:29; OnTick:35; OnTimer:41 | Docs/00_PROJECT_CHARTER_RU.md; Docs/18_MQL5_ARCHITECTURE_SPECIFICATION_RU.md | F057/F060 | ERR-016/028; IMP-008/017 | OnInit disabled; OnTick no-trade stub; OnTimer diagnostics; OnDeinit timer stop; INDIVIDUAL_GUARD_MAPPING_PARTIAL |

Sources=74; lexical function declarations=199. Function count не число проверенных guards.


## FINAL-CLOSURE — индивидуальные карточки первой группы27 функций

База b4d8f1ea5caf492f3abd030e5502d40582c52dc8. Сигнатуры/полные тела и callsites статически сопоставлены; код не исполнялся. Это27 отдельных semantic reviews, не общий review всех199 functions. Оставшиеся172 требуют индивидуального продолжения. Callsite list — статические project references; отсутствие native execution честно сохраняется.

### FUNCTION HSBI_BuildRuntimePolicy

| Field | Individual analysis |
|---|---|
| 1 FullName | HSBI_BuildRuntimePolicy |
| 2 File | Include/Core/HSBI_RuntimePolicy.mqh |
| 3 DeclarationLine | 12 |
| 4 BodyRange | 13–22 |
| 5 Purpose | Mode→canonical capabilities |
| 6 InputParameters | const HSBI_RuntimeMode mode |
| 7 Outputs | HSBI_RuntimePolicy |
| 8 Dimensions | Mode enum/bools dimensionless |
| 9 AdmittedValues | MQL declared types. Дополнительные domain requirements и отсутствующие guards указаны в полях10/18; не утверждённый broker domain. |
| 10 Preconditions | Canonical declared mode/callback context; неизвестные режимы invalid/false согласно body. Нет permission на финансовые side effects. |
| 11 Postconditions | dispatch flag остаётся false;known modes дают явно перечисленные capabilities |
| 12 AllLocalGuardGroups | ZeroMemory;explicit recognized modes;unknown invalid; A03-G-011 |
| 13 OutgoingCalls | ZeroMemory:14 [native/language] |
| 14 ProductionCallsites | HSBI_ValidateContext (Include/Core/HSBI_Context.mqh:55); HSBI_IsInjectedProofAllowed (Include/Core/HSBI_RuntimePolicy.mqh:23); HSBI_IsProductionPreflightAllowed (Include/Core/HSBI_RuntimePolicy.mqh:24); HSBI_IsStaticCalculationAllowed (Include/Core/HSBI_RuntimePolicy.mqh:26); HSBI_IsCompletionSourceAllowed (Include/Core/HSBI_RuntimePolicy.mqh:29); OnInit (Hybrid_Split_Big_Independent_EA.mq5:21) |
| 15 NormativeClauses | Docs/00_PROJECT_CHARTER_RU.md:17–18 |
| 16 FormulaIDs | F036/F060 |
| 17 ErrorHandling | dispatch flag остаётся false;known modes дают явно перечисленные capabilities; ERR-016/028; IMP-008/017 |
| 18 MissingChecksOrLimits | Capabilities не являются economic authority/funding permission |
| 19 ActualIntegration | STATIC_CALLS_PRESENT; no financial dispatch path in main |
| 20 Verdict | MATCH_LOCAL_DISABLED_POLICY; native/broker verification NOT_RUN |

R2-дополнение к сохранённой карточке (исходные20 полей и body не пересозданы):

| R2 field | Value |
|---|---|
| Function ID | Include/Core/HSBI_RuntimePolicy.mqh:12:HSBI_BuildRuntimePolicy |
| Signature | HSBI_RuntimePolicy HSBI_BuildRuntimePolicy(const HSBI_RuntimeMode mode) |
| Actual authority | Canonical compile/runtime configuration; NOT_APPLICABLE financial/broker proof |
| Proof boundary | Local configuration/no-trade capability check; не экономический grant/commit |

Фактическое тело для сверки всех clauses (цитата source, не новый исполняемый код):

~~~text
{
   HSBI_RuntimePolicy p;ZeroMemory(p);p.mode=mode;
   if(mode==HSBI_RUNTIME_UNSPECIFIED)return p;
   if(mode==HSBI_RUNTIME_DISABLED){p.diagnosticsAllowed=true;p.valid=true;return p;}
   if(mode==HSBI_RUNTIME_UNIT_TEST){p.diagnosticsAllowed=true;p.staticCalculationAllowed=true;p.injectedFixtureAllowed=true;p.valid=true;return p;}
   if(mode==HSBI_RUNTIME_STRATEGY_TESTER_DRY_RUN||mode==HSBI_RUNTIME_DEMO_DRY_RUN){p.diagnosticsAllowed=true;p.staticCalculationAllowed=true;p.persistenceAllowed=true;p.valid=true;return p;}
   if(mode==HSBI_RUNTIME_SHADOW){p.diagnosticsAllowed=true;p.staticCalculationAllowed=true;p.productionPreflightAllowed=true;p.persistenceAllowed=true;p.valid=true;return p;}
   if(mode==HSBI_RUNTIME_PRODUCTION||mode==HSBI_RUNTIME_ADMIN_VERIFICATION){p.diagnosticsAllowed=true;p.staticCalculationAllowed=true;p.productionPreflightAllowed=true;p.persistenceAllowed=true;p.terminalCompletionAllowed=true;p.valid=true;return p;}
   return p; // legacy real modes are fail-closed at this stage
}
~~~

### FUNCTION HSBI_IsInjectedProofAllowed

| Field | Individual analysis |
|---|---|
| 1 FullName | HSBI_IsInjectedProofAllowed |
| 2 File | Include/Core/HSBI_RuntimePolicy.mqh |
| 3 DeclarationLine | 23 |
| 4 BodyRange | 23–23 |
| 5 Purpose | Injected fixture capability |
| 6 InputParameters | const HSBI_RuntimeMode mode |
| 7 Outputs | bool |
| 8 Dimensions | Mode/bool dimensionless |
| 9 AdmittedValues | MQL declared types. Дополнительные domain requirements и отсутствующие guards указаны в полях10/18; не утверждённый broker domain. |
| 10 Preconditions | Canonical declared mode/callback context; неизвестные режимы invalid/false согласно body. Нет permission на финансовые side effects. |
| 11 Postconditions | Возвращает injectedFixtureAllowed; unknown false |
| 12 AllLocalGuardGroups | Canonical builder table; A03-G-011 |
| 13 OutgoingCalls | HSBI_BuildRuntimePolicy:23 [project] |
| 14 ProductionCallsites | HSBI_ValidateFutureSmallInput (Include/Planning/HSBI_FutureSmallSolver.mqh:47); HSBI_EvaluateFutureSmallLevel (Include/Planning/HSBI_FutureSmallSolver.mqh:61) |
| 15 NormativeClauses | Docs/HSB.2C_R1_P2_Runtime_Policy_Canonical_RU.md:1–11 |
| 16 FormulaIDs | F060 |
| 17 ErrorHandling | Возвращает injectedFixtureAllowed; unknown false; ERR-013/028; IMP-001/017 |
| 18 MissingChecksOrLimits | Не validation конкретного proof/fixture |
| 19 ActualIntegration | STATIC_CALLS_PRESENT; no financial dispatch path in main |
| 20 Verdict | MATCH_LOCAL_CAPABILITY_ONLY; native/broker verification NOT_RUN |

R2-дополнение к сохранённой карточке (исходные20 полей и body не пересозданы):

| R2 field | Value |
|---|---|
| Function ID | Include/Core/HSBI_RuntimePolicy.mqh:23:HSBI_IsInjectedProofAllowed |
| Signature | bool HSBI_IsInjectedProofAllowed(const HSBI_RuntimeMode mode) |
| Actual authority | Canonical compile/runtime configuration; NOT_APPLICABLE financial/broker proof |
| Proof boundary | Local configuration/no-trade capability check; не экономический grant/commit |

Фактическое тело для сверки всех clauses (цитата source, не новый исполняемый код):

~~~text
{return HSBI_BuildRuntimePolicy(mode).injectedFixtureAllowed;}
~~~

### FUNCTION HSBI_IsProductionPreflightAllowed

| Field | Individual analysis |
|---|---|
| 1 FullName | HSBI_IsProductionPreflightAllowed |
| 2 File | Include/Core/HSBI_RuntimePolicy.mqh |
| 3 DeclarationLine | 24 |
| 4 BodyRange | 24–24 |
| 5 Purpose | Preflight capability |
| 6 InputParameters | const HSBI_RuntimeMode mode |
| 7 Outputs | bool |
| 8 Dimensions | Mode/bool dimensionless |
| 9 AdmittedValues | MQL declared types. Дополнительные domain requirements и отсутствующие guards указаны в полях10/18; не утверждённый broker domain. |
| 10 Preconditions | Canonical declared mode/callback context; неизвестные режимы invalid/false согласно body. Нет permission на финансовые side effects. |
| 11 Postconditions | Возвращает productionPreflightAllowed;unknown false |
| 12 AllLocalGuardGroups | Canonical builder table; A03-G-011 |
| 13 OutgoingCalls | HSBI_BuildRuntimePolicy:24 [project] |
| 14 ProductionCallsites | HSBI_ValidateExecutionPreflight (Include/Execution/HSBI_ExecutionPreflight.mqh:20); HSBI_ValidateRuntimeDecisionContext (Include/Runtime/HSBI_RuntimeDecisionValidator.mqh:8) |
| 15 NormativeClauses | Docs/HSB.2C_R1_P2_Runtime_Policy_Canonical_RU.md:1–11 |
| 16 FormulaIDs | F060 |
| 17 ErrorHandling | Возвращает productionPreflightAllowed;unknown false; ERR-016/028; IMP-008/017 |
| 18 MissingChecksOrLimits | Не сам preflight,не dispatch authorization |
| 19 ActualIntegration | STATIC_CALLS_PRESENT; no financial dispatch path in main |
| 20 Verdict | MATCH_LOCAL_CAPABILITY_ONLY; native/broker verification NOT_RUN |

R2-дополнение к сохранённой карточке (исходные20 полей и body не пересозданы):

| R2 field | Value |
|---|---|
| Function ID | Include/Core/HSBI_RuntimePolicy.mqh:24:HSBI_IsProductionPreflightAllowed |
| Signature | bool HSBI_IsProductionPreflightAllowed(const HSBI_RuntimeMode mode) |
| Actual authority | Canonical compile/runtime configuration; NOT_APPLICABLE financial/broker proof |
| Proof boundary | Local configuration/no-trade capability check; не экономический grant/commit |

Фактическое тело для сверки всех clauses (цитата source, не новый исполняемый код):

~~~text
{return HSBI_BuildRuntimePolicy(mode).productionPreflightAllowed;}
~~~

### FUNCTION HSBI_IsBrokerDispatchAllowed

| Field | Individual analysis |
|---|---|
| 1 FullName | HSBI_IsBrokerDispatchAllowed |
| 2 File | Include/Core/HSBI_RuntimePolicy.mqh |
| 3 DeclarationLine | 25 |
| 4 BodyRange | 25–25 |
| 5 Purpose | Безусловный broker block |
| 6 InputParameters | const HSBI_RuntimeMode mode |
| 7 Outputs | bool=false |
| 8 Dimensions | Mode enum input ignored |
| 9 AdmittedValues | MQL declared types. Дополнительные domain requirements и отсутствующие guards указаны в полях10/18; не утверждённый broker domain. |
| 10 Preconditions | Canonical declared mode/callback context; неизвестные режимы invalid/false согласно body. Нет permission на финансовые side effects. |
| 11 Postconditions | False для всех входов, no side effects |
| 12 AllLocalGuardGroups | Безусловный false; A03-G-012 |
| 13 OutgoingCalls | Нет вызовов |
| 14 ProductionCallsites | OnInit (Hybrid_Split_Big_Independent_EA.mq5:22) |
| 15 NormativeClauses | Docs/00_PROJECT_CHARTER_RU.md:17–18 |
| 16 FormulaIDs | F060 |
| 17 ErrorHandling | False для всех входов, no side effects; ERR-016; IMP-008 |
| 18 MissingChecksOrLimits | Trading отсутствие намеренно, не финансовая ошибка |
| 19 ActualIntegration | STATIC_CALLS_PRESENT; no financial dispatch path in main |
| 20 Verdict | MATCH_NO_DISPATCH; native/broker verification NOT_RUN |

R2-дополнение к сохранённой карточке (исходные20 полей и body не пересозданы):

| R2 field | Value |
|---|---|
| Function ID | Include/Core/HSBI_RuntimePolicy.mqh:25:HSBI_IsBrokerDispatchAllowed |
| Signature | bool HSBI_IsBrokerDispatchAllowed(const HSBI_RuntimeMode mode) |
| Actual authority | Canonical compile/runtime configuration; NOT_APPLICABLE financial/broker proof |
| Proof boundary | Local configuration/no-trade capability check; не экономический grant/commit |

Фактическое тело для сверки всех clauses (цитата source, не новый исполняемый код):

~~~text
{return false;}
~~~

### FUNCTION HSBI_IsStaticCalculationAllowed

| Field | Individual analysis |
|---|---|
| 1 FullName | HSBI_IsStaticCalculationAllowed |
| 2 File | Include/Core/HSBI_RuntimePolicy.mqh |
| 3 DeclarationLine | 26 |
| 4 BodyRange | 26–26 |
| 5 Purpose | Static calculation capability |
| 6 InputParameters | const HSBI_RuntimeMode mode |
| 7 Outputs | bool |
| 8 Dimensions | Mode/bool dimensionless |
| 9 AdmittedValues | MQL declared types. Дополнительные domain requirements и отсутствующие guards указаны в полях10/18; не утверждённый broker domain. |
| 10 Preconditions | Canonical declared mode/callback context; неизвестные режимы invalid/false согласно body. Нет permission на финансовые side effects. |
| 11 Postconditions | Возвращает staticCalculationAllowed;unknown false |
| 12 AllLocalGuardGroups | Canonical builder table; A03-G-011 |
| 13 OutgoingCalls | HSBI_BuildRuntimePolicy:26 [project] |
| 14 ProductionCallsites | HSBI_EvaluateReserveCatchUp (Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:55); HSBI_ValidateFutureSmallInput (Include/Planning/HSBI_FutureSmallSolver.mqh:47); HSBI_EvaluateFutureSmallLevel (Include/Planning/HSBI_FutureSmallSolver.mqh:61); HSBI_SolveNewFar (Include/Planning/HSBI_NewFarSolver.mqh:99) |
| 15 NormativeClauses | Docs/HSB.2C_R1_P2_Runtime_Policy_Canonical_RU.md:1–11 |
| 16 FormulaIDs | F060 |
| 17 ErrorHandling | Возвращает staticCalculationAllowed;unknown false; ERR-028/033; IMP-017 |
| 18 MissingChecksOrLimits | Не actual/available/funding/dispatch |
| 19 ActualIntegration | STATIC_CALLS_PRESENT; no financial dispatch path in main |
| 20 Verdict | MATCH_LOCAL_CAPABILITY_ONLY; native/broker verification NOT_RUN |

R2-дополнение к сохранённой карточке (исходные20 полей и body не пересозданы):

| R2 field | Value |
|---|---|
| Function ID | Include/Core/HSBI_RuntimePolicy.mqh:26:HSBI_IsStaticCalculationAllowed |
| Signature | bool HSBI_IsStaticCalculationAllowed(const HSBI_RuntimeMode mode) |
| Actual authority | Canonical compile/runtime configuration; NOT_APPLICABLE financial/broker proof |
| Proof boundary | Local configuration/no-trade capability check; не экономический grant/commit |

Фактическое тело для сверки всех clauses (цитата source, не новый исполняемый код):

~~~text
{return HSBI_BuildRuntimePolicy(mode).staticCalculationAllowed;}
~~~

### FUNCTION HSBI_IsCompletionSourceAllowed

| Field | Individual analysis |
|---|---|
| 1 FullName | HSBI_IsCompletionSourceAllowed |
| 2 File | Include/Core/HSBI_RuntimePolicy.mqh |
| 3 DeclarationLine | 28 |
| 4 BodyRange | 29–29 |
| 5 Purpose | Completion mode/source label |
| 6 InputParameters | const HSBI_RuntimeMode mode,const int source |
| 7 Outputs | bool |
| 8 Dimensions | Mode enum/source integer label |
| 9 AdmittedValues | MQL declared types. Дополнительные domain requirements и отсутствующие guards указаны в полях10/18; не утверждённый broker domain. |
| 10 Preconditions | Canonical declared mode/callback context; неизвестные режимы invalid/false согласно body. Нет permission на финансовые side effects. |
| 11 Postconditions | bool без state delta |
| 12 AllLocalGuardGroups | Capability AND source==0; A03-G-013 |
| 13 OutgoingCalls | HSBI_BuildRuntimePolicy:29 [project] |
| 14 ProductionCallsites | HSBI_ReconcileExecutionOutcome (Include/Execution/HSBI_ExternalOutcome.mqh:25) |
| 15 NormativeClauses | Docs/07_TRANSACTION_EXECUTION_CONTRACT_RU.md:19–25 |
| 16 FormulaIDs | F060 |
| 17 ErrorHandling | bool без state delta; ERR-010/013/033; IMP-001/005/008 |
| 18 MissingChecksOrLimits | source0 label не independently authenticated terminal evidence |
| 19 ActualIntegration | STATIC_CALLS_PRESENT; no financial dispatch path in main |
| 20 Verdict | LOCAL_LABEL_NOT_AUTHENTICITY; native/broker verification NOT_RUN |

R2-дополнение к сохранённой карточке (исходные20 полей и body не пересозданы):

| R2 field | Value |
|---|---|
| Function ID | Include/Core/HSBI_RuntimePolicy.mqh:28:HSBI_IsCompletionSourceAllowed |
| Signature | bool HSBI_IsCompletionSourceAllowed(const HSBI_RuntimeMode mode,const int source) |
| Actual authority | Canonical compile/runtime configuration; NOT_APPLICABLE financial/broker proof |
| Proof boundary | Local configuration/no-trade capability check; не экономический grant/commit |

Фактическое тело для сверки всех clauses (цитата source, не новый исполняемый код):

~~~text
{return HSBI_BuildRuntimePolicy(mode).terminalCompletionAllowed&&source==0;}
~~~

### FUNCTION HSBI_SubmitActionStub

| Field | Individual analysis |
|---|---|
| 1 FullName | HSBI_SubmitActionStub |
| 2 File | Include/Execution/HSBI_NoTradeExecution.mqh |
| 3 DeclarationLine | 5 |
| 4 BodyRange | 5–5 |
| 5 Purpose | Неторговый отказ |
| 6 InputParameters | Нет explicit inputs |
| 7 Outputs | HSBI_NoTradeResult |
| 8 Dimensions | Bool/reason dimensionless |
| 9 AdmittedValues | NOT_APPLICABLE: no explicit inputs; callback/global state scope indicated separately. |
| 10 Preconditions | Canonical declared mode/callback context; неизвестные режимы invalid/false согласно body. Нет permission на финансовые side effects. |
| 11 Postconditions | TRADING_NOT_IMPLEMENTED,без orders/ledger writes |
| 12 AllLocalGuardGroups | Безусловный success=false; A03-G-015 |
| 13 OutgoingCalls | Нет вызовов |
| 14 ProductionCallsites | HSBI_OpenPositionStub (Include/Execution/HSBI_NoTradeExecution.mqh:6); HSBI_ClosePositionStub (Include/Execution/HSBI_NoTradeExecution.mqh:7); HSBI_PartialCloseStub (Include/Execution/HSBI_NoTradeExecution.mqh:8); OnTick (Hybrid_Split_Big_Independent_EA.mq5:37) |
| 15 NormativeClauses | Docs/00_PROJECT_CHARTER_RU.md:17–18 |
| 16 FormulaIDs | F060 |
| 17 ErrorHandling | TRADING_NOT_IMPLEMENTED,без orders/ledger writes; ERR-016; IMP-008 |
| 18 MissingChecksOrLimits | Не реализованный execution handler |
| 19 ActualIntegration | STATIC_CALLS_PRESENT; no financial dispatch path in main |
| 20 Verdict | MATCH_NO_TRADE_STUB; native/broker verification NOT_RUN |

R2-дополнение к сохранённой карточке (исходные20 полей и body не пересозданы):

| R2 field | Value |
|---|---|
| Function ID | Include/Execution/HSBI_NoTradeExecution.mqh:5:HSBI_SubmitActionStub |
| Signature | HSBI_NoTradeResult HSBI_SubmitActionStub() |
| Actual authority | Canonical compile/runtime configuration; NOT_APPLICABLE financial/broker proof |
| Proof boundary | Local configuration/no-trade capability check; не экономический grant/commit |

Фактическое тело для сверки всех clauses (цитата source, не новый исполняемый код):

~~~text
{HSBI_NoTradeResult r;r.success=false;r.reason=HSBI_REASON_TRADING_NOT_IMPLEMENTED;return r;}
~~~

### FUNCTION HSBI_OpenPositionStub

| Field | Individual analysis |
|---|---|
| 1 FullName | HSBI_OpenPositionStub |
| 2 File | Include/Execution/HSBI_NoTradeExecution.mqh |
| 3 DeclarationLine | 6 |
| 4 BodyRange | 6–6 |
| 5 Purpose | Неторговый open facade |
| 6 InputParameters | Нет explicit inputs |
| 7 Outputs | HSBI_NoTradeResult |
| 8 Dimensions | Bool/reason dimensionless |
| 9 AdmittedValues | NOT_APPLICABLE: no explicit inputs; callback/global state scope indicated separately. |
| 10 Preconditions | Canonical declared mode/callback context; неизвестные режимы invalid/false согласно body. Нет permission на финансовые side effects. |
| 11 Postconditions | success=false |
| 12 AllLocalGuardGroups | Unconditional SubmitActionStub delegation; A03-G-015 |
| 13 OutgoingCalls | HSBI_SubmitActionStub:6 [project] |
| 14 ProductionCallsites | NOT_FOUND по всем74 sources |
| 15 NormativeClauses | Docs/00_PROJECT_CHARTER_RU.md:17–18 |
| 16 FormulaIDs | F060 |
| 17 ErrorHandling | success=false; ERR-016; IMP-008 |
| 18 MissingChecksOrLimits | Не actual open handler |
| 19 ActualIntegration | NO_PRODUCTION_CALLER_FOUND |
| 20 Verdict | MATCH_NO_TRADE_STUB; native/broker verification NOT_RUN |

R2-дополнение к сохранённой карточке (исходные20 полей и body не пересозданы):

| R2 field | Value |
|---|---|
| Function ID | Include/Execution/HSBI_NoTradeExecution.mqh:6:HSBI_OpenPositionStub |
| Signature | HSBI_NoTradeResult HSBI_OpenPositionStub() |
| Actual authority | Canonical compile/runtime configuration; NOT_APPLICABLE financial/broker proof |
| Proof boundary | Local configuration/no-trade capability check; не экономический grant/commit |

Фактическое тело для сверки всех clauses (цитата source, не новый исполняемый код):

~~~text
{return HSBI_SubmitActionStub();}
~~~

### FUNCTION HSBI_ClosePositionStub

| Field | Individual analysis |
|---|---|
| 1 FullName | HSBI_ClosePositionStub |
| 2 File | Include/Execution/HSBI_NoTradeExecution.mqh |
| 3 DeclarationLine | 7 |
| 4 BodyRange | 7–7 |
| 5 Purpose | Неторговый close facade |
| 6 InputParameters | Нет explicit inputs |
| 7 Outputs | HSBI_NoTradeResult |
| 8 Dimensions | Bool/reason dimensionless |
| 9 AdmittedValues | NOT_APPLICABLE: no explicit inputs; callback/global state scope indicated separately. |
| 10 Preconditions | Canonical declared mode/callback context; неизвестные режимы invalid/false согласно body. Нет permission на финансовые side effects. |
| 11 Postconditions | success=false |
| 12 AllLocalGuardGroups | Unconditional SubmitActionStub delegation; A03-G-015 |
| 13 OutgoingCalls | HSBI_SubmitActionStub:7 [project] |
| 14 ProductionCallsites | NOT_FOUND по всем74 sources |
| 15 NormativeClauses | Docs/00_PROJECT_CHARTER_RU.md:17–18 |
| 16 FormulaIDs | F060 |
| 17 ErrorHandling | success=false; ERR-016; IMP-008 |
| 18 MissingChecksOrLimits | Не actual close handler |
| 19 ActualIntegration | NO_PRODUCTION_CALLER_FOUND |
| 20 Verdict | MATCH_NO_TRADE_STUB; native/broker verification NOT_RUN |

R2-дополнение к сохранённой карточке (исходные20 полей и body не пересозданы):

| R2 field | Value |
|---|---|
| Function ID | Include/Execution/HSBI_NoTradeExecution.mqh:7:HSBI_ClosePositionStub |
| Signature | HSBI_NoTradeResult HSBI_ClosePositionStub() |
| Actual authority | Canonical compile/runtime configuration; NOT_APPLICABLE financial/broker proof |
| Proof boundary | Local configuration/no-trade capability check; не экономический grant/commit |

Фактическое тело для сверки всех clauses (цитата source, не новый исполняемый код):

~~~text
{return HSBI_SubmitActionStub();}
~~~

### FUNCTION HSBI_PartialCloseStub

| Field | Individual analysis |
|---|---|
| 1 FullName | HSBI_PartialCloseStub |
| 2 File | Include/Execution/HSBI_NoTradeExecution.mqh |
| 3 DeclarationLine | 8 |
| 4 BodyRange | 8–8 |
| 5 Purpose | Неторговый partial facade |
| 6 InputParameters | Нет explicit inputs |
| 7 Outputs | HSBI_NoTradeResult |
| 8 Dimensions | Bool/reason dimensionless |
| 9 AdmittedValues | NOT_APPLICABLE: no explicit inputs; callback/global state scope indicated separately. |
| 10 Preconditions | Canonical declared mode/callback context; неизвестные режимы invalid/false согласно body. Нет permission на финансовые side effects. |
| 11 Postconditions | success=false |
| 12 AllLocalGuardGroups | Unconditional SubmitActionStub delegation; A03-G-015 |
| 13 OutgoingCalls | HSBI_SubmitActionStub:8 [project] |
| 14 ProductionCallsites | NOT_FOUND по всем74 sources |
| 15 NormativeClauses | Docs/00_PROJECT_CHARTER_RU.md:17–18 |
| 16 FormulaIDs | F060/F062 |
| 17 ErrorHandling | success=false; ERR-016; IMP-008 |
| 18 MissingChecksOrLimits | Не partial fill accounting |
| 19 ActualIntegration | NO_PRODUCTION_CALLER_FOUND |
| 20 Verdict | MATCH_NO_TRADE_STUB; native/broker verification NOT_RUN |

R2-дополнение к сохранённой карточке (исходные20 полей и body не пересозданы):

| R2 field | Value |
|---|---|
| Function ID | Include/Execution/HSBI_NoTradeExecution.mqh:8:HSBI_PartialCloseStub |
| Signature | HSBI_NoTradeResult HSBI_PartialCloseStub() |
| Actual authority | Canonical compile/runtime configuration; NOT_APPLICABLE financial/broker proof |
| Proof boundary | Local configuration/no-trade capability check; не экономический grant/commit |

Фактическое тело для сверки всех clauses (цитата source, не новый исполняемый код):

~~~text
{return HSBI_SubmitActionStub();}
~~~

### FUNCTION HSBI_AllocatedTotal

| Field | Individual analysis |
|---|---|
| 1 FullName | HSBI_AllocatedTotal |
| 2 File | Include/Money/HSBI_AllocationLedgerTypes.mqh |
| 3 DeclarationLine | 6 |
| 4 BodyRange | 6–6 |
| 5 Purpose | Сумма пяти buckets |
| 6 InputParameters | const HSBI_AllocationLedgerRecord &r |
| 7 Outputs | double |
| 8 Dimensions | Одна currency/precision для всех слагаемых |
| 9 AdmittedValues | MQL declared types. Дополнительные domain requirements и отсутствующие guards указаны в полях10/18; не утверждённый broker domain. |
| 10 Preconditions | Typed object/arguments. Known finite values/units/authority нужны для финансового использования; соблюдение не следует из декларации типа. Конкретные ограничения: Не гарантирует finite/nonnegative/overflow/partition; helper only |
| 11 Postconditions | Сумма пяти денежных полей |
| 12 AllLocalGuardGroups | Нет guards; NOT_APPLICABLE |
| 13 OutgoingCalls | Нет вызовов |
| 14 ProductionCallsites | HSBI_ValidateAllocationConservation (Include/Money/HSBI_AllocationLedgerTypes.mqh:7); HSBI_ValidateAllocationConservation (Include/Money/HSBI_AllocationLedgerTypes.mqh:7); HSBI_ClassifyAllocationDuplicate (Include/Money/HSBI_AllocationLedgerTypes.mqh:8); HSBI_ClassifyAllocationDuplicate (Include/Money/HSBI_AllocationLedgerTypes.mqh:8) |
| 15 NormativeClauses | Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md:10–12 |
| 16 FormulaIDs | F012/F016/F064 |
| 17 ErrorHandling | Сумма пяти денежных полей; ERR-005/006; IMP-003/005 |
| 18 MissingChecksOrLimits | Не гарантирует finite/nonnegative/overflow/partition; helper only |
| 19 ActualIntegration | STATIC_CALLS_PRESENT; no financial dispatch path in main |
| 20 Verdict | ARITHMETIC_HELPER_ONLY; native/broker verification NOT_RUN |

R2-дополнение к сохранённой карточке (исходные20 полей и body не пересозданы):

| R2 field | Value |
|---|---|
| Function ID | Include/Money/HSBI_AllocationLedgerTypes.mqh:6:HSBI_AllocatedTotal |
| Signature | double HSBI_AllocatedTotal(const HSBI_AllocationLedgerRecord &r) |
| Actual authority | Supplied DTO/expected scalar arguments; independent actual provider внутри функции отсутствует |
| Proof boundary | Local accepted body/path; конкретные callers перечислены в исходной карточке; global financial mandatory caller не доказан |

Фактическое тело для сверки всех clauses (цитата source, не новый исполняемый код):

~~~text
{return r.finalReserveAllocated+r.partialFarAllocated+r.transitionAllocated+r.carryAllocated+r.residual;}
~~~

### FUNCTION HSBI_ValidateAllocationConservation

| Field | Individual analysis |
|---|---|
| 1 FullName | HSBI_ValidateAllocationConservation |
| 2 File | Include/Money/HSBI_AllocationLedgerTypes.mqh |
| 3 DeclarationLine | 7 |
| 4 BodyRange | 7–7 |
| 5 Purpose | Legacy allocation cap check |
| 6 InputParameters | const HSBI_AllocationLedgerRecord &r |
| 7 Outputs | bool |
| 8 Dimensions | Все amounts account money;epsilon money |
| 9 AdmittedValues | MQL declared types. Дополнительные domain requirements и отсутствующие guards указаны в полях10/18; не утверждённый broker domain. |
| 10 Preconditions | Typed object/arguments. Known finite values/units/authority нужны для финансового использования; соблюдение не следует из декларации типа. Конкретные ограничения: Нет nonnegative vector/exact partition/independent source/owner/once; negative-source branch иной |
| 11 Postconditions | Negative source→total<=epsilon; positive source→total<=source+eps AND consumed<=available+eps |
| 12 AllLocalGuardGroups | valid/key,sign source,total cap,consumed bound; A03-G-005 |
| 13 OutgoingCalls | HSBI_AllocatedTotal:7 [project]; HSBI_AllocatedTotal:7 [project] |
| 14 ProductionCallsites | NOT_FOUND по всем74 sources |
| 15 NormativeClauses | Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md:10–24 |
| 16 FormulaIDs | F012–015/F064 |
| 17 ErrorHandling | Negative source→total<=epsilon; positive source→total<=source+eps AND consumed<=available+eps; ERR-005/006; IMP-003/005 |
| 18 MissingChecksOrLimits | Нет nonnegative vector/exact partition/independent source/owner/once; negative-source branch иной |
| 19 ActualIntegration | NO_PRODUCTION_CALLER_FOUND |
| 20 Verdict | IMPLEMENTED_MISMATCH; native/broker verification NOT_RUN |

R2-дополнение к сохранённой карточке (исходные20 полей и body не пересозданы):

| R2 field | Value |
|---|---|
| Function ID | Include/Money/HSBI_AllocationLedgerTypes.mqh:7:HSBI_ValidateAllocationConservation |
| Signature | bool HSBI_ValidateAllocationConservation(const HSBI_AllocationLedgerRecord &r) |
| Actual authority | Supplied DTO/expected scalar arguments; independent actual provider внутри функции отсутствует |
| Proof boundary | Local accepted body/path; конкретные callers перечислены в исходной карточке; global financial mandatory caller не доказан |

Фактическое тело для сверки всех clauses (цитата source, не новый исполняемый код):

~~~text
{if(!r.valid||r.sourceDealKey=="")return false;if(r.sourceDealNet<0.0)return HSBI_AllocatedTotal(r)<=0.0000001;return HSBI_AllocatedTotal(r)<=r.sourceDealNet+0.0000001&&r.consumed<=r.available+0.0000001;}
~~~

### FUNCTION HSBI_ClassifyAllocationDuplicate

| Field | Individual analysis |
|---|---|
| 1 FullName | HSBI_ClassifyAllocationDuplicate |
| 2 File | Include/Money/HSBI_AllocationLedgerTypes.mqh |
| 3 DeclarationLine | 8 |
| 4 BodyRange | 8–8 |
| 5 Purpose | Legacy allocation duplicate |
| 6 InputParameters | const HSBI_AllocationLedgerRecord &a,const HSBI_AllocationLedgerRecord &b |
| 7 Outputs | int0/1/2 |
| 8 Dimensions | Total account money; keys/events dimensionless |
| 9 AdmittedValues | MQL declared types. Дополнительные domain requirements и отсутствующие guards указаны в полях10/18; не утверждённый broker domain. |
| 10 Preconditions | Typed object/arguments. Known finite values/units/authority нужны для финансового использования; соблюдение не следует из декларации типа. Конкретные ограничения: Same total≠same vector/policy/full payload |
| 11 Postconditions | 0 other source/event;1 equal totals;2 otherwise |
| 12 AllLocalGuardGroups | source/event mismatch; total equality within epsilon; A03-G-006 |
| 13 OutgoingCalls | MathAbs:8 [native/language]; HSBI_AllocatedTotal:8 [project]; HSBI_AllocatedTotal:8 [project] |
| 14 ProductionCallsites | NOT_FOUND по всем74 sources |
| 15 NormativeClauses | Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md:10–16 |
| 16 FormulaIDs | F016/F057 |
| 17 ErrorHandling | 0 other source/event;1 equal totals;2 otherwise; ERR-004; IMP-003 |
| 18 MissingChecksOrLimits | Same total≠same vector/policy/full payload |
| 19 ActualIntegration | NO_PRODUCTION_CALLER_FOUND |
| 20 Verdict | IMPLEMENTED_MISMATCH; native/broker verification NOT_RUN |

R2-дополнение к сохранённой карточке (исходные20 полей и body не пересозданы):

| R2 field | Value |
|---|---|
| Function ID | Include/Money/HSBI_AllocationLedgerTypes.mqh:8:HSBI_ClassifyAllocationDuplicate |
| Signature | int HSBI_ClassifyAllocationDuplicate(const HSBI_AllocationLedgerRecord &a,const HSBI_AllocationLedgerRecord &b) |
| Actual authority | Supplied DTO/expected scalar arguments; independent actual provider внутри функции отсутствует |
| Proof boundary | Local accepted body/path; конкретные callers перечислены в исходной карточке; global financial mandatory caller не доказан |

Фактическое тело для сверки всех clauses (цитата source, не новый исполняемый код):

~~~text
{if(a.sourceDealKey!=b.sourceDealKey||a.allocationEventId!=b.allocationEventId)return 0;bool same=MathAbs(HSBI_AllocatedTotal(a)-HSBI_AllocatedTotal(b))<0.0000001;return same?1:2;}
~~~

### FUNCTION HSBI_CanConsumeBucket

| Field | Individual analysis |
|---|---|
| 1 FullName | HSBI_CanConsumeBucket |
| 2 File | Include/Money/HSBI_AllocationLedgerTypes.mqh |
| 3 DeclarationLine | 9 |
| 4 BodyRange | 9–9 |
| 5 Purpose | FinalReserve isolation filter |
| 6 InputParameters | const HSBI_MoneyBucket bucket,const bool partialFarConsumer |
| 7 Outputs | bool |
| 8 Dimensions | Bucket enum,consumer bool dimensionless |
| 9 AdmittedValues | MQL declared types. Дополнительные domain requirements и отсутствующие guards указаны в полях10/18; не утверждённый broker domain. |
| 10 Preconditions | Typed object/arguments. Known finite values/units/authority нужны для финансового использования; соблюдение не следует из декларации типа. Конкретные ограничения: Unknown enum,owner,purpose/source authority не проверены; не полное consume разрешение |
| 11 Postconditions | Запрещено только одно сочетание |
| 12 AllLocalGuardGroups | partialFarConsumer AND FinalReserve→false; else true; A03-G-007 |
| 13 OutgoingCalls | Нет вызовов |
| 14 ProductionCallsites | NOT_FOUND по всем74 sources |
| 15 NormativeClauses | Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md:18–20 |
| 16 FormulaIDs | F019 |
| 17 ErrorHandling | Запрещено только одно сочетание; ERR-007/049; IMP-004/005 |
| 18 MissingChecksOrLimits | Unknown enum,owner,purpose/source authority не проверены; не полное consume разрешение |
| 19 ActualIntegration | NO_PRODUCTION_CALLER_FOUND |
| 20 Verdict | PARTIAL_PURPOSE_FILTER; native/broker verification NOT_RUN |

R2-дополнение к сохранённой карточке (исходные20 полей и body не пересозданы):

| R2 field | Value |
|---|---|
| Function ID | Include/Money/HSBI_AllocationLedgerTypes.mqh:9:HSBI_CanConsumeBucket |
| Signature | bool HSBI_CanConsumeBucket(const HSBI_MoneyBucket bucket,const bool partialFarConsumer) |
| Actual authority | Supplied DTO/expected scalar arguments; independent actual provider внутри функции отсутствует |
| Proof boundary | Local accepted body/path; конкретные callers перечислены в исходной карточке; global financial mandatory caller не доказан |

Фактическое тело для сверки всех clauses (цитата source, не новый исполняемый код):

~~~text
{if(partialFarConsumer&&bucket==HSBI_BUCKET_FINAL_RESERVE)return false;return true;}
~~~

### FUNCTION HSBI_CanConsumeAmount

| Field | Individual analysis |
|---|---|
| 1 FullName | HSBI_CanConsumeAmount |
| 2 File | Include/Money/HSBI_AllocationLedgerTypes.mqh |
| 3 DeclarationLine | 10 |
| 4 BodyRange | 10–10 |
| 5 Purpose | Scalar affordability filter |
| 6 InputParameters | const HSBI_AllocationLedgerRecord &r,const double amount |
| 7 Outputs | bool |
| 8 Dimensions | amount/available account money |
| 9 AdmittedValues | MQL declared types. Дополнительные domain requirements и отсутствующие guards указаны в полях10/18; не утверждённый broker domain. |
| 10 Preconditions | Typed object/arguments. Known finite values/units/authority нужны для финансового использования; соблюдение не следует из декларации типа. Конкретные ограничения: valid/authority/owner/reservations/finite не проверены;zero допустим для helper, не самостоятельный defect |
| 11 Postconditions | bool, no actual debit |
| 12 AllLocalGuardGroups | amount>=0 AND amount<=available+eps; A03-G-008 |
| 13 OutgoingCalls | Нет вызовов |
| 14 ProductionCallsites | NOT_FOUND по всем74 sources |
| 15 NormativeClauses | Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md:14–24 |
| 16 FormulaIDs | F015/F019 |
| 17 ErrorHandling | bool, no actual debit; ERR-005/007/033; IMP-003/004/005 |
| 18 MissingChecksOrLimits | valid/authority/owner/reservations/finite не проверены;zero допустим для helper, не самостоятельный defect |
| 19 ActualIntegration | NO_PRODUCTION_CALLER_FOUND |
| 20 Verdict | LOCAL_FILTER_NOT_AUTHORIZATION; native/broker verification NOT_RUN |

R2-дополнение к сохранённой карточке (исходные20 полей и body не пересозданы):

| R2 field | Value |
|---|---|
| Function ID | Include/Money/HSBI_AllocationLedgerTypes.mqh:10:HSBI_CanConsumeAmount |
| Signature | bool HSBI_CanConsumeAmount(const HSBI_AllocationLedgerRecord &r,const double amount) |
| Actual authority | Supplied DTO/expected scalar arguments; independent actual provider внутри функции отсутствует |
| Proof boundary | Local accepted body/path; конкретные callers перечислены в исходной карточке; global financial mandatory caller не доказан |

Фактическое тело для сверки всех clauses (цитата source, не новый исполняемый код):

~~~text
{return amount>=0.0&&amount<=r.available+0.0000001;}
~~~

### FUNCTION HSBI_BuildSourceDealKey

| Field | Individual analysis |
|---|---|
| 1 FullName | HSBI_BuildSourceDealKey |
| 2 File | Include/Money/HSBI_EconomicLedgerTypes.mqh |
| 3 DeclarationLine | 7 |
| 4 BodyRange | 7–7 |
| 5 Purpose | Legacy source key |
| 6 InputParameters | const HSBI_EconomicLedgerRecord &r |
| 7 Outputs | string |
| 8 Dimensions | IDs dimensionless, symbol opaque text |
| 9 AdmittedValues | MQL declared types. Дополнительные domain requirements и отсутствующие guards указаны в полях10/18; не утверждённый broker domain. |
| 10 Preconditions | Typed object/arguments. Known finite values/units/authority нужны для финансового использования; соблюдение не следует из декларации типа. Конкретные ограничения: Broker/Server/Account отсутствуют; key не independent source proof |
| 11 Postconditions | Всегда symbol&#124;magic&#124;cycle&#124;deal |
| 12 AllLocalGuardGroups | Нет schema/authority guards; NOT_APPLICABLE |
| 13 OutgoingCalls | LongToString:7 [native/language]; HSBI_UlongToString:7 [project]; HSBI_UlongToString:7 [project] |
| 14 ProductionCallsites | NOT_FOUND по всем74 sources |
| 15 NormativeClauses | Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md:8–16 |
| 16 FormulaIDs | F017/F060 |
| 17 ErrorHandling | Всегда symbol&#124;magic&#124;cycle&#124;deal; ERR-002; IMP-001 |
| 18 MissingChecksOrLimits | Broker/Server/Account отсутствуют; key не independent source proof |
| 19 ActualIntegration | NO_PRODUCTION_CALLER_FOUND |
| 20 Verdict | LEGACY_NAMESPACE_MISMATCH; native/broker verification NOT_RUN |

R2-дополнение к сохранённой карточке (исходные20 полей и body не пересозданы):

| R2 field | Value |
|---|---|
| Function ID | Include/Money/HSBI_EconomicLedgerTypes.mqh:7:HSBI_BuildSourceDealKey |
| Signature | string HSBI_BuildSourceDealKey(const HSBI_EconomicLedgerRecord &r) |
| Actual authority | Supplied DTO/expected scalar arguments; independent actual provider внутри функции отсутствует |
| Proof boundary | Local accepted body/path; конкретные callers перечислены в исходной карточке; global financial mandatory caller не доказан |

Фактическое тело для сверки всех clauses (цитата source, не новый исполняемый код):

~~~text
{return r.symbol+"|"+LongToString(r.magic)+"|"+HSBI_UlongToString(r.cycleId)+"|"+HSBI_UlongToString(r.dealTicket);}
~~~

### FUNCTION HSBI_ValidateEconomicRecord

| Field | Individual analysis |
|---|---|
| 1 FullName | HSBI_ValidateEconomicRecord |
| 2 File | Include/Money/HSBI_EconomicLedgerTypes.mqh |
| 3 DeclarationLine | 8 |
| 4 BodyRange | 8–8 |
| 5 Purpose | Локальный record shape |
| 6 InputParameters | const HSBI_EconomicLedgerRecord &r |
| 7 Outputs | bool |
| 8 Dimensions | volume lot; остальные проверяемые поля IDs/text |
| 9 AdmittedValues | MQL declared types. Дополнительные domain requirements и отсутствующие guards указаны в полях10/18; не утверждённый broker domain. |
| 10 Preconditions | Typed object/arguments. Known finite values/units/authority нужны для финансового использования; соблюдение не следует из декларации типа. Конкретные ограничения: Не finite/компоненты/net consistency/key recomputation/known role/entry/currency |
| 11 Postconditions | true iff перечисленная конъюнкция |
| 12 AllLocalGuardGroups | IDs>0, volume>0, nonempty symbol/key, valid; A03-G-001 |
| 13 OutgoingCalls | Нет вызовов |
| 14 ProductionCallsites | NOT_FOUND по всем74 sources |
| 15 NormativeClauses | Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md:6–16 |
| 16 FormulaIDs | F007/F017/F036/F060 |
| 17 ErrorHandling | true iff перечисленная конъюнкция; ERR-001/002/033; IMP-001/004/005 |
| 18 MissingChecksOrLimits | Не finite/компоненты/net consistency/key recomputation/known role/entry/currency |
| 19 ActualIntegration | NO_PRODUCTION_CALLER_FOUND |
| 20 Verdict | PARTIAL_SHAPE_NO_AUTHORITY; native/broker verification NOT_RUN |

R2-дополнение к сохранённой карточке (исходные20 полей и body не пересозданы):

| R2 field | Value |
|---|---|
| Function ID | Include/Money/HSBI_EconomicLedgerTypes.mqh:8:HSBI_ValidateEconomicRecord |
| Signature | bool HSBI_ValidateEconomicRecord(const HSBI_EconomicLedgerRecord &r) |
| Actual authority | Supplied DTO/expected scalar arguments; independent actual provider внутри функции отсутствует |
| Proof boundary | Local accepted body/path; конкретные callers перечислены в исходной карточке; global financial mandatory caller не доказан |

Фактическое тело для сверки всех clauses (цитата source, не новый исполняемый код):

~~~text
{return r.dealTicket>0&&r.orderTicket>0&&r.positionIdentifier>0&&r.symbol!=""&&r.cycleId>0&&r.actionId>0&&r.eventId>0&&r.volume>0&&r.sourceDealKey!=""&&r.valid;}
~~~

### FUNCTION HSBI_SameEconomicRecord

| Field | Individual analysis |
|---|---|
| 1 FullName | HSBI_SameEconomicRecord |
| 2 File | Include/Money/HSBI_EconomicLedgerTypes.mqh |
| 3 DeclarationLine | 9 |
| 4 BodyRange | 9–9 |
| 5 Purpose | Legacy economic equality |
| 6 InputParameters | const HSBI_EconomicLedgerRecord &a,const HSBI_EconomicLedgerRecord &b |
| 7 Outputs | bool |
| 8 Dimensions | Net money,volume lot,price price |
| 9 AdmittedValues | MQL declared types. Дополнительные domain requirements и отсутствующие guards указаны в полях10/18; не утверждённый broker domain. |
| 10 Preconditions | Typed object/arguments. Known finite values/units/authority нужны для финансового использования; соблюдение не следует из декларации типа. Конкретные ограничения: Profit/Swap/Commission/Fee не сравниваются; raw immutable equality не epsilon |
| 11 Postconditions | true только по четырём comparisons, state unchanged |
| 12 AllLocalGuardGroups | key equal;abs net delta<1e-7;volume/price equal; A03-G-002 |
| 13 OutgoingCalls | MathAbs:9 [native/language] |
| 14 ProductionCallsites | HSBI_ClassifyEconomicDuplicate (Include/Money/HSBI_EconomicLedgerTypes.mqh:10) |
| 15 NormativeClauses | Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md:14–16 |
| 16 FormulaIDs | F017/F057 |
| 17 ErrorHandling | true только по четырём comparisons, state unchanged; ERR-001; IMP-001 |
| 18 MissingChecksOrLimits | Profit/Swap/Commission/Fee не сравниваются; raw immutable equality не epsilon |
| 19 ActualIntegration | STATIC_CALLS_PRESENT; no financial dispatch path in main |
| 20 Verdict | IMPLEMENTED_MISMATCH; native/broker verification NOT_RUN |

R2-дополнение к сохранённой карточке (исходные20 полей и body не пересозданы):

| R2 field | Value |
|---|---|
| Function ID | Include/Money/HSBI_EconomicLedgerTypes.mqh:9:HSBI_SameEconomicRecord |
| Signature | bool HSBI_SameEconomicRecord(const HSBI_EconomicLedgerRecord &a,const HSBI_EconomicLedgerRecord &b) |
| Actual authority | Supplied DTO/expected scalar arguments; independent actual provider внутри функции отсутствует |
| Proof boundary | Local accepted body/path; конкретные callers перечислены в исходной карточке; global financial mandatory caller не доказан |

Фактическое тело для сверки всех clauses (цитата source, не новый исполняемый код):

~~~text
{return a.sourceDealKey==b.sourceDealKey&&MathAbs(a.dealNet-b.dealNet)<0.0000001&&a.volume==b.volume&&a.price==b.price;}
~~~

### FUNCTION HSBI_ClassifyEconomicDuplicate

| Field | Individual analysis |
|---|---|
| 1 FullName | HSBI_ClassifyEconomicDuplicate |
| 2 File | Include/Money/HSBI_EconomicLedgerTypes.mqh |
| 3 DeclarationLine | 10 |
| 4 BodyRange | 10–10 |
| 5 Purpose | Legacy duplicate classifier |
| 6 InputParameters | const HSBI_EconomicLedgerRecord &existing,const HSBI_EconomicLedgerRecord &incoming |
| 7 Outputs | int0/1/2 |
| 8 Dimensions | Identity keys dimensionless; delegated values retain units |
| 9 AdmittedValues | MQL declared types. Дополнительные domain requirements и отсутствующие guards указаны в полях10/18; не утверждённый broker domain. |
| 10 Preconditions | Typed object/arguments. Known finite values/units/authority нужны для финансового использования; соблюдение не следует из декларации типа. Конкретные ограничения: Нет unavailable/reject/history completeness;0 не funding eligibility |
| 11 Postconditions | 0 different key;1 same;2 conflict; no state delta |
| 12 AllLocalGuardGroups | Different key branch, otherwise SameEconomicRecord; A03-G-003 |
| 13 OutgoingCalls | HSBI_SameEconomicRecord:10 [project] |
| 14 ProductionCallsites | NOT_FOUND по всем74 sources |
| 15 NormativeClauses | Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md:14–16 |
| 16 FormulaIDs | F017/F057/F060 |
| 17 ErrorHandling | 0 different key;1 same;2 conflict; no state delta; ERR-001/002/033; IMP-001/004 |
| 18 MissingChecksOrLimits | Нет unavailable/reject/history completeness;0 не funding eligibility |
| 19 ActualIntegration | NO_PRODUCTION_CALLER_FOUND |
| 20 Verdict | INCOMPLETE_STATUS_AUTHORITY; native/broker verification NOT_RUN |

R2-дополнение к сохранённой карточке (исходные20 полей и body не пересозданы):

| R2 field | Value |
|---|---|
| Function ID | Include/Money/HSBI_EconomicLedgerTypes.mqh:10:HSBI_ClassifyEconomicDuplicate |
| Signature | int HSBI_ClassifyEconomicDuplicate(const HSBI_EconomicLedgerRecord &existing,const HSBI_EconomicLedgerRecord &incoming) |
| Actual authority | Supplied DTO/expected scalar arguments; independent actual provider внутри функции отсутствует |
| Proof boundary | Local accepted body/path; конкретные callers перечислены в исходной карточке; global financial mandatory caller не доказан |

Фактическое тело для сверки всех clauses (цитата source, не новый исполняемый код):

~~~text
{if(existing.sourceDealKey!=incoming.sourceDealKey)return 0;return HSBI_SameEconomicRecord(existing,incoming)?1:2;}
~~~

### FUNCTION HSBI_SerializeEconomicRecord

| Field | Individual analysis |
|---|---|
| 1 FullName | HSBI_SerializeEconomicRecord |
| 2 File | Include/Money/HSBI_EconomicLedgerTypes.mqh |
| 3 DeclarationLine | 11 |
| 4 BodyRange | 11–11 |
| 5 Purpose | Диагностический serializer |
| 6 InputParameters | const HSBI_EconomicLedgerRecord &r |
| 7 Outputs | string |
| 8 Dimensions | volume lot/price price/net money rendered8digits |
| 9 AdmittedValues | MQL declared types. Дополнительные domain requirements и отсутствующие guards указаны в полях10/18; не утверждённый broker domain. |
| 10 Preconditions | Typed object/arguments. Known finite values/units/authority нужны для финансового использования; соблюдение не следует из декларации типа. Конкретные ограничения: Не полный immutable body и не доказанный authoritative codec; precision loss |
| 11 Postconditions | Четыре rounded fields, no state delta |
| 12 AllLocalGuardGroups | Нет guards; NOT_APPLICABLE |
| 13 OutgoingCalls | DoubleToString:11 [native/language]; DoubleToString:11 [native/language]; DoubleToString:11 [native/language] |
| 14 ProductionCallsites | NOT_FOUND по всем74 sources |
| 15 NormativeClauses | Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md:8–16 |
| 16 FormulaIDs | F017/F042/F049 |
| 17 ErrorHandling | Четыре rounded fields, no state delta; ERR-003; IMP-002 |
| 18 MissingChecksOrLimits | Не полный immutable body и не доказанный authoritative codec; precision loss |
| 19 ActualIntegration | NO_PRODUCTION_CALLER_FOUND |
| 20 Verdict | LIMITED_DIAGNOSTIC_SCOPE; native/broker verification NOT_RUN |

R2-дополнение к сохранённой карточке (исходные20 полей и body не пересозданы):

| R2 field | Value |
|---|---|
| Function ID | Include/Money/HSBI_EconomicLedgerTypes.mqh:11:HSBI_SerializeEconomicRecord |
| Signature | string HSBI_SerializeEconomicRecord(const HSBI_EconomicLedgerRecord &r) |
| Actual authority | Supplied DTO/expected scalar arguments; independent actual provider внутри функции отсутствует |
| Proof boundary | Local accepted body/path; конкретные callers перечислены в исходной карточке; global financial mandatory caller не доказан |

Фактическое тело для сверки всех clauses (цитата source, не новый исполняемый код):

~~~text
{return r.sourceDealKey+"|"+DoubleToString(r.volume,8)+"|"+DoubleToString(r.price,8)+"|"+DoubleToString(r.dealNet,8);}
~~~

### FUNCTION HSBI_IsHarvestSourceEntry

| Field | Individual analysis |
|---|---|
| 1 FullName | HSBI_IsHarvestSourceEntry |
| 2 File | Include/Money/HSBI_EconomicLedgerTypes.mqh |
| 3 DeclarationLine | 12 |
| 4 BodyRange | 12–12 |
| 5 Purpose | Положительный non-opening filter |
| 6 InputParameters | const HSBI_EconomicLedgerRecord &r |
| 7 Outputs | bool |
| 8 Dimensions | net account money, entry enum |
| 9 AdmittedValues | MQL declared types. Дополнительные domain requirements и отсутствующие guards указаны в полях10/18; не утверждённый broker domain. |
| 10 Preconditions | Typed object/arguments. Known finite values/units/authority нужны для финансового использования; соблюдение не следует из декларации типа. Конкретные ограничения: Не known enum/valid/role/history/finite/once; не полный funding gate |
| 11 Postconditions | Результат scalar фильтра, no grant/debit |
| 12 AllLocalGuardGroups | entryType!=0 AND net>0; A03-G-004 |
| 13 OutgoingCalls | Нет вызовов |
| 14 ProductionCallsites | NOT_FOUND по всем74 sources |
| 15 NormativeClauses | Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md:6–12 |
| 16 FormulaIDs | F007/F018/F060 |
| 17 ErrorHandling | Результат scalar фильтра, no grant/debit; ERR-022/033/047/049; IMP-001/004/014 |
| 18 MissingChecksOrLimits | Не known enum/valid/role/history/finite/once; не полный funding gate |
| 19 ActualIntegration | NO_PRODUCTION_CALLER_FOUND |
| 20 Verdict | LOCAL_FILTER_NOT_FUNDING; native/broker verification NOT_RUN |

R2-дополнение к сохранённой карточке (исходные20 полей и body не пересозданы):

| R2 field | Value |
|---|---|
| Function ID | Include/Money/HSBI_EconomicLedgerTypes.mqh:12:HSBI_IsHarvestSourceEntry |
| Signature | bool HSBI_IsHarvestSourceEntry(const HSBI_EconomicLedgerRecord &r) |
| Actual authority | Supplied DTO/expected scalar arguments; independent actual provider внутри функции отсутствует |
| Proof boundary | Local accepted body/path; конкретные callers перечислены в исходной карточке; global financial mandatory caller не доказан |

Фактическое тело для сверки всех clauses (цитата source, не новый исполняемый код):

~~~text
{return r.entryType!=0&&r.dealNet>0.0;}
~~~

### FUNCTION HSBI_ValidateMoneyState

| Field | Individual analysis |
|---|---|
| 1 FullName | HSBI_ValidateMoneyState |
| 2 File | Include/Money/HSBI_MoneyState.mqh |
| 3 DeclarationLine | 5 |
| 4 BodyRange | 5–5 |
| 5 Purpose | Неотрицательные бюджеты |
| 6 InputParameters | const HSBI_MoneyState &s |
| 7 Outputs | bool |
| 8 Dimensions | Account money;revision ID |
| 9 AdmittedValues | MQL declared types. Дополнительные domain requirements и отсутствующие guards указаны в полях10/18; не утверждённый broker domain. |
| 10 Preconditions | Typed object/arguments. Known finite values/units/authority нужны для финансового использования; соблюдение не следует из декларации типа. Конкретные ограничения: valid/revision/finite ignored; NaN budget отвергается >=, Infinity проходит |
| 11 Postconditions | bool без изменения state |
| 12 AllLocalGuardGroups | five budgets>=0; A03-G-009 |
| 13 OutgoingCalls | Нет вызовов |
| 14 ProductionCallsites | NOT_FOUND по всем74 sources |
| 15 NormativeClauses | Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md:10–24 |
| 16 FormulaIDs | F013/F036 |
| 17 ErrorHandling | bool без изменения state; ERR-011; IMP-005 |
| 18 MissingChecksOrLimits | valid/revision/finite ignored; NaN budget отвергается >=, Infinity проходит |
| 19 ActualIntegration | NO_PRODUCTION_CALLER_FOUND |
| 20 Verdict | IMPLEMENTED_MISMATCH; native/broker verification NOT_RUN |

R2-дополнение к сохранённой карточке (исходные20 полей и body не пересозданы):

| R2 field | Value |
|---|---|
| Function ID | Include/Money/HSBI_MoneyState.mqh:5:HSBI_ValidateMoneyState |
| Signature | bool HSBI_ValidateMoneyState(const HSBI_MoneyState &s) |
| Actual authority | Supplied DTO/expected scalar arguments; independent actual provider внутри функции отсутствует |
| Proof boundary | Local accepted body/path; конкретные callers перечислены в исходной карточке; global financial mandatory caller не доказан |

Фактическое тело для сверки всех clauses (цитата source, не новый исполняемый код):

~~~text
{return s.finalReserve>=0&&s.partialFarBudget>=0&&s.transitionBudget>=0&&s.carry>=0&&s.residual>=0;}
~~~

### FUNCTION HSBI_ValidateRiskInput

| Field | Individual analysis |
|---|---|
| 1 FullName | HSBI_ValidateRiskInput |
| 2 File | Include/Risk/HSBI_RiskGateResult.mqh |
| 3 DeclarationLine | 6 |
| 4 BodyRange | 6–6 |
| 5 Purpose | Сравнить переданные risk values/limits |
| 6 InputParameters | const HSBI_RiskInput &x,const HSBI_RiskLimits &l |
| 7 Outputs | HSBI_RiskGateResult |
| 8 Dimensions | marginLevel/DD percent;freeMargin/loss money;projectedMargin/gross/spread exact unit binding DTO UNDEFINED |
| 9 AdmittedValues | MQL declared types. Дополнительные domain requirements и отсутствующие guards указаны в полях10/18; не утверждённый broker domain. |
| 10 Preconditions | Typed object/arguments. Known finite values/units/authority нужны для финансового использования; соблюдение не следует из декларации типа. Конкретные ограничения: Нет finite/domain/limits constructor;projectedMargin percent-vs-money/spread units caller not established; provider отсутствует |
| 11 Postconditions | stale/caps reject; otherwise passed=true,mask63; no state changes |
| 12 AllLocalGuardGroups | fresh;6 cap groups; A03-G-010 |
| 13 OutgoingCalls | Нет вызовов |
| 14 ProductionCallsites | NOT_FOUND по всем74 sources |
| 15 NormativeClauses | Docs/15_RISK_AND_MARGIN_CONTRACT_RU.md:5–15 |
| 16 FormulaIDs | F026/F031–033/F036 |
| 17 ErrorHandling | stale/caps reject; otherwise passed=true,mask63; no state changes; ERR-009/034/038; IMP-005/015/021 |
| 18 MissingChecksOrLimits | Нет finite/domain/limits constructor;projectedMargin percent-vs-money/spread units caller not established; provider отсутствует |
| 19 ActualIntegration | NO_PRODUCTION_CALLER_FOUND |
| 20 Verdict | IMPLEMENTED_MISMATCH; native/broker verification NOT_RUN |

R2-дополнение к сохранённой карточке (исходные20 полей и body не пересозданы):

| R2 field | Value |
|---|---|
| Function ID | Include/Risk/HSBI_RiskGateResult.mqh:6:HSBI_ValidateRiskInput |
| Signature | HSBI_RiskGateResult HSBI_ValidateRiskInput(const HSBI_RiskInput &x,const HSBI_RiskLimits &l) |
| Actual authority | Supplied DTO/expected scalar arguments; independent actual provider внутри функции отсутствует |
| Proof boundary | Local accepted body/path; конкретные callers перечислены в исходной карточке; global financial mandatory caller не доказан |

Фактическое тело для сверки всех clauses (цитата source, не новый исполняемый код):

~~~text
{HSBI_RiskGateResult r;r.passed=false;r.gateMask=0;r.failedGate=0;r.reason=HSBI_REASON_INTERNAL_INVARIANT_FAILED;r.failClosed=true;if(!x.snapshotFresh){r.reason=HSBI_REASON_STALE_SNAPSHOT;return r;}if(x.projectedMargin>l.maxProjectedMargin){r.failedGate=1;return r;}if(x.projectedMarginLevel<l.minMarginLevel){r.failedGate=2;return r;}if(x.freeMarginAfter<l.minFreeMargin){r.failedGate=3;return r;}if(x.cycleDrawdown>l.maxCycleDrawdown||x.accountDrawdown>l.maxAccountDrawdown){r.failedGate=4;return r;}if(x.grossExposure>l.maxGrossExposure||x.managedPositions>l.maxManagedPositions){r.failedGate=5;return r;}if(x.worstCaseLoss>l.maxWorstCaseLoss||x.transitionLoss>l.maxTransitionLoss||x.spread>l.maxSpread){r.failedGate=6;return r;}r.passed=true;r.gateMask=63;r.failedGate=-1;r.reason=HSBI_REASON_OK;return r;}
~~~

### FUNCTION OnInit

| Field | Individual analysis |
|---|---|
| 1 FullName | OnInit |
| 2 File | Hybrid_Split_Big_Independent_EA.mq5 |
| 3 DeclarationLine | 19 |
| 4 BodyRange | 20–27 |
| 5 Purpose | Инициализировать disabled skeleton |
| 6 InputParameters | Нет explicit inputs |
| 7 Outputs | INIT_FAILED/SUCCEEDED |
| 8 Dimensions | Mode/reason dimensionless,timer seconds |
| 9 AdmittedValues | NOT_APPLICABLE: no explicit inputs; callback/global state scope indicated separately. |
| 10 Preconditions | Canonical declared mode/callback context; неизвестные режимы invalid/false согласно body. Нет permission на финансовые side effects. |
| 11 Postconditions | DISABLED policy/context/log/timer requested; no trade |
| 12 AllLocalGuardGroups | !policy.valid OR dispatchAllowed→INIT_FAILED; A03-G-014 |
| 13 OutgoingCalls | HSBI_BuildRuntimePolicy:21 [project]; HSBI_IsBrokerDispatchAllowed:22 [project]; HSBI_InitializeContext:23 [project]; HSBI_Log:24 [project]; EventSetTimer:25 [native/language] |
| 14 ProductionCallsites | MQL platform callback [static API contract], runtime NOT_RUN |
| 15 NormativeClauses | Docs/00_PROJECT_CHARTER_RU.md:17–18; Docs/18_MQL5_ARCHITECTURE_SPECIFICATION_RU.md:6–30 |
| 16 FormulaIDs | F060 |
| 17 ErrorHandling | DISABLED policy/context/log/timer requested; no trade; ERR-016/028; IMP-008/017 |
| 18 MissingChecksOrLimits | EventSetTimer result не обрабатывается;no financial readiness claimed |
| 19 ActualIntegration | MQL_CALLBACK_STATIC; actual execution NOT_RUN |
| 20 Verdict | STATIC_DISABLED_ENTRY; native/broker verification NOT_RUN |

R2-дополнение к сохранённой карточке (исходные20 полей и body не пересозданы):

| R2 field | Value |
|---|---|
| Function ID | Hybrid_Split_Big_Independent_EA.mq5:19:OnInit |
| Signature | int OnInit() |
| Actual authority | MQL callback + локальный g_hsbi_context; broker/history authority не используется |
| Proof boundary | OnInit policy gate обязательный до initialization; OnTick stub alwaysfalse; OnTimer logging only; OnDeinit cleanup only — по конкретному callback body |

Фактическое тело для сверки всех clauses (цитата source, не новый исполняемый код):

~~~text
{
   HSBI_RuntimePolicy policy=HSBI_BuildRuntimePolicy(HSBI_RUNTIME_DISABLED);
   if(!policy.valid||HSBI_IsBrokerDispatchAllowed(policy.mode))return(INIT_FAILED);
   HSBI_InitializeContext(g_hsbi_context,policy.mode);
   HSBI_Log("HSBI-GEN-033",HSBI_REASON_OK,"NON_TRADING_SKELETON initialized");
   EventSetTimer(1);
   return(INIT_SUCCEEDED);
}
~~~

### FUNCTION OnDeinit

| Field | Individual analysis |
|---|---|
| 1 FullName | OnDeinit |
| 2 File | Hybrid_Split_Big_Independent_EA.mq5 |
| 3 DeclarationLine | 29 |
| 4 BodyRange | 30–33 |
| 5 Purpose | Остановить diagnostic timer |
| 6 InputParameters | const int reason |
| 7 Outputs | void |
| 8 Dimensions | reason integer dimensionless |
| 9 AdmittedValues | MQL declared types. Дополнительные domain requirements и отсутствующие guards указаны в полях10/18; не утверждённый broker domain. |
| 10 Preconditions | Canonical declared mode/callback context; неизвестные режимы invalid/false согласно body. Нет permission на финансовые side effects. |
| 11 Postconditions | EventKillTimer и log |
| 12 AllLocalGuardGroups | Нет финансовых guards; NOT_APPLICABLE |
| 13 OutgoingCalls | EventKillTimer:31 [native/language]; HSBI_Log:32 [project] |
| 14 ProductionCallsites | MQL platform callback [static API contract], runtime NOT_RUN |
| 15 NormativeClauses | Docs/18_MQL5_ARCHITECTURE_SPECIFICATION_RU.md:6–30 |
| 16 FormulaIDs | F060 |
| 17 ErrorHandling | EventKillTimer и log; ERR-016; IMP-008 |
| 18 MissingChecksOrLimits | Не shutdown settlement lifecycle |
| 19 ActualIntegration | MQL_CALLBACK_STATIC; actual execution NOT_RUN |
| 20 Verdict | STATIC_DIAGNOSTIC_ENTRY; native/broker verification NOT_RUN |

R2-дополнение к сохранённой карточке (исходные20 полей и body не пересозданы):

| R2 field | Value |
|---|---|
| Function ID | Hybrid_Split_Big_Independent_EA.mq5:29:OnDeinit |
| Signature | void OnDeinit(const int reason) |
| Actual authority | MQL callback + локальный g_hsbi_context; broker/history authority не используется |
| Proof boundary | OnInit policy gate обязательный до initialization; OnTick stub alwaysfalse; OnTimer logging only; OnDeinit cleanup only — по конкретному callback body |

Фактическое тело для сверки всех clauses (цитата source, не новый исполняемый код):

~~~text
{
   EventKillTimer();
   HSBI_Log("HSBI-GEN-033",HSBI_REASON_OK,"NON_TRADING_SKELETON deinitialized");
}
~~~

### FUNCTION OnTick

| Field | Individual analysis |
|---|---|
| 1 FullName | OnTick |
| 2 File | Hybrid_Split_Big_Independent_EA.mq5 |
| 3 DeclarationLine | 35 |
| 4 BodyRange | 36–39 |
| 5 Purpose | Вызвать no-trade stub |
| 6 InputParameters | Нет explicit inputs |
| 7 Outputs | void |
| 8 Dimensions | reason enum dimensionless |
| 9 AdmittedValues | NOT_APPLICABLE: no explicit inputs; callback/global state scope indicated separately. |
| 10 Preconditions | Canonical declared mode/callback context; неизвестные режимы invalid/false согласно body. Нет permission на финансовые side effects. |
| 11 Postconditions | Изменяется только g_hsbi_context.lastReason |
| 12 AllLocalGuardGroups | Unconditional stub success=false; A03-G-015 |
| 13 OutgoingCalls | HSBI_SubmitActionStub:37 [project] |
| 14 ProductionCallsites | MQL platform callback [static API contract], runtime NOT_RUN |
| 15 NormativeClauses | Docs/00_PROJECT_CHARTER_RU.md:17–18 |
| 16 FormulaIDs | F057/F060 |
| 17 ErrorHandling | Изменяется только g_hsbi_context.lastReason; ERR-016; IMP-008 |
| 18 MissingChecksOrLimits | Нет финансовых handlers/funding/dispatch |
| 19 ActualIntegration | MQL_CALLBACK_STATIC; actual execution NOT_RUN |
| 20 Verdict | STATIC_NO_TRADE_ENTRY; native/broker verification NOT_RUN |

R2-дополнение к сохранённой карточке (исходные20 полей и body не пересозданы):

| R2 field | Value |
|---|---|
| Function ID | Hybrid_Split_Big_Independent_EA.mq5:35:OnTick |
| Signature | void OnTick() |
| Actual authority | MQL callback + локальный g_hsbi_context; broker/history authority не используется |
| Proof boundary | OnInit policy gate обязательный до initialization; OnTick stub alwaysfalse; OnTimer logging only; OnDeinit cleanup only — по конкретному callback body |

Фактическое тело для сверки всех clauses (цитата source, не новый исполняемый код):

~~~text
{
   HSBI_NoTradeResult blocked=HSBI_SubmitActionStub();
   g_hsbi_context.lastReason=blocked.reason;
}
~~~

### FUNCTION OnTimer

| Field | Individual analysis |
|---|---|
| 1 FullName | OnTimer |
| 2 File | Hybrid_Split_Big_Independent_EA.mq5 |
| 3 DeclarationLine | 41 |
| 4 BodyRange | 42–44 |
| 5 Purpose | Обновить context diagnostics |
| 6 InputParameters | Нет explicit inputs |
| 7 Outputs | void |
| 8 Dimensions | Context retains units; no money calculation in entry |
| 9 AdmittedValues | NOT_APPLICABLE: no explicit inputs; callback/global state scope indicated separately. |
| 10 Preconditions | Canonical declared mode/callback context; неизвестные режимы invalid/false согласно body. Нет permission на финансовые side effects. |
| 11 Postconditions | HSBI_UpdateDiagnosticSnapshot(g_hsbi_context) |
| 12 AllLocalGuardGroups | Diagnostic validator delegated; NOT_APPLICABLE |
| 13 OutgoingCalls | HSBI_UpdateDiagnosticSnapshot:43 [project] |
| 14 ProductionCallsites | MQL platform callback [static API contract], runtime NOT_RUN |
| 15 NormativeClauses | Docs/18_MQL5_ARCHITECTURE_SPECIFICATION_RU.md:6–30 |
| 16 FormulaIDs | F060 |
| 17 ErrorHandling | HSBI_UpdateDiagnosticSnapshot(g_hsbi_context); ERR-016/028; IMP-008/017 |
| 18 MissingChecksOrLimits | Diagnostics flags не financial authority |
| 19 ActualIntegration | MQL_CALLBACK_STATIC; actual execution NOT_RUN |
| 20 Verdict | STATIC_DIAGNOSTIC_ENTRY; native/broker verification NOT_RUN |

R2-дополнение к сохранённой карточке (исходные20 полей и body не пересозданы):

| R2 field | Value |
|---|---|
| Function ID | Hybrid_Split_Big_Independent_EA.mq5:41:OnTimer |
| Signature | void OnTimer() |
| Actual authority | MQL callback + локальный g_hsbi_context; broker/history authority не используется |
| Proof boundary | OnInit policy gate обязательный до initialization; OnTick stub alwaysfalse; OnTimer logging only; OnDeinit cleanup only — по конкретному callback body |

Фактическое тело для сверки всех clauses (цитата source, не новый исполняемый код):

~~~text
{
   HSBI_UpdateDiagnosticSnapshot(g_hsbi_context);
}
~~~

## FINAL-CLOSURE —11 индивидуальных FSM/transaction функций

Проверяется scope helper, не существование торгового lifecycle. Все статические callsites ниже получены из тел74 production-файлов; внешние/динамические вызовы не доказаны.

### FUNCTION HSBI_IsTransitionAllowed

| Field | Individual analysis |
|---|---|
| 1 FullName | HSBI_IsTransitionAllowed |
| 2 File | Include/Core/HSBI_StateMachine.mqh |
| 3 DeclarationLine | 5 |
| 4 BodyRange | 5–5 |
| 5 Purpose | Проверить только topology пары состояний |
| 6 InputParameters | const HSBI_State from,const HSBI_State to |
| 7 Outputs | bool |
| 8 Dimensions | from/to: enum, без money units |
| 9 AdmittedValues | Один из33 объявленных HSBI_State; casts вне domain не проверяются |
| 10 Preconditions | Caller обязан валидировать enum и все financial prerequisites; самого обязательного financial caller нет |
| 11 Postconditions | true ровно для source topology; false остальных enum-пар |
| 12 AllLocalGuards | self equality;9normal pairs; reconciliation targets;3global targets |
| 13 OutgoingCalls | NONE (project functions) |
| 14 ProductionCallsites | HSBI_ProposeStateTransition @ Include/Core/HSBI_StateMachine.mqh:6 |
| 15 NormativeClauses | Docs/06_STATE_MACHINE_SPECIFICATION_RU.md:6–22; Docs/07_TRANSACTION_EXECUTION_CONTRACT_RU.md:6–25; Docs/16_PERSISTENCE_AND_RESTART_RU.md:11–19; Docs/17_RECONCILIATION_AND_TERMINAL_SAFE_RU.md:10–22 |
| 16 FormulaIDs | F024/F025/F026/F065 |
| 17 ErrorHandling | false/constant target/allowed flag согласно индивидуальным clauses; exceptions/status persistence не реализованы |
| 18 MissingChecksOrLimits | нет event/outcome/finite/money/authority/persist checks; accepted cast self не означает авторизованный FSM |
| 19 ActualIntegration | Main financial entry integration NOT_IMPLEMENTED; static callers перечислены отдельно; native NOT_RUN |
| 20 Verdict | TOPOLOGY_ONLY; не financial authorization |

R2-дополнение к сохранённой карточке (исходные20 полей и body не пересозданы):

| R2 field | Value |
|---|---|
| Function ID | Include/Core/HSBI_StateMachine.mqh:5:HSBI_IsTransitionAllowed |
| Signature | bool HSBI_IsTransitionAllowed(const HSBI_State from,const HSBI_State to) |
| Actual authority | Supplied DTO/expected scalar arguments; independent actual provider внутри функции отсутствует |
| Proof boundary | Local accepted body/path; конкретные callers перечислены в исходной карточке; global financial mandatory caller не доказан |

Полное фактическое тело (цитата, не новый исполняемый код):

~~~text
{if(from==to)return true;if(from==HSBI_STATE_DISABLED&&to==HSBI_STATE_IDLE)return true;if(from==HSBI_STATE_IDLE&&to==HSBI_STATE_INITIAL_PLAN_READY)return true;if(from==HSBI_STATE_INITIAL_PLAN_READY&&to==HSBI_STATE_INITIAL_OPENING_BUY)return true;if(from==HSBI_STATE_INITIAL_OPENING_BUY&&to==HSBI_STATE_INITIAL_OPENING_SELL)return true;if(from==HSBI_STATE_INITIAL_OPENING_SELL&&to==HSBI_STATE_INITIAL_LOCK_ACTIVE)return true;if(from==HSBI_STATE_INITIAL_LOCK_ACTIVE&&to==HSBI_STATE_INITIAL_PLUS_CLOSING)return true;if(from==HSBI_STATE_INITIAL_PLUS_CLOSING&&to==HSBI_STATE_FAR_ACTIVE)return true;if(from==HSBI_STATE_FAR_ACTIVE&&to==HSBI_STATE_CANDIDATE_PLANNED)return true;if(from==HSBI_STATE_CANDIDATE_PLANNED&&to==HSBI_STATE_BASKET_OPENING_CORE)return true;if(from==HSBI_STATE_RECONCILING&&(to==HSBI_STATE_TERMINAL_SAFE||to==HSBI_STATE_FAR_ACTIVE||to==HSBI_STATE_IDLE))return true;if(to==HSBI_STATE_RECONCILING||to==HSBI_STATE_TERMINAL_SAFE||to==HSBI_STATE_EMERGENCY)return true;return false;}
~~~

### FUNCTION HSBI_ProposeStateTransition

| Field | Individual analysis |
|---|---|
| 1 FullName | HSBI_ProposeStateTransition |
| 2 File | Include/Core/HSBI_StateMachine.mqh |
| 3 DeclarationLine | 6 |
| 4 BodyRange | 6–6 |
| 5 Purpose | Сформировать результат предложения без изменения context |
| 6 InputParameters | const HSBI_RecoveryContext &c,const HSBI_State to |
| 7 Outputs | HSBI_StateTransitionResult |
| 8 Dimensions | State enum; StateRevision ulong; reason enum |
| 9 AdmittedValues | валидный context/currentState/to, revision<ULONG_MAX если increment |
| 10 Preconditions | Topology guard и overflow bound должны быть установлены; overflow не проверяется |
| 11 Postconditions | allowed + from/to + revision+(allowed?1:0); исходный context неизменён |
| 12 AllLocalGuards | HSBI_IsTransitionAllowed(c.currentState,to) |
| 13 OutgoingCalls | HSBI_IsTransitionAllowed:6 |
| 14 ProductionCallsites | HSBI_ApplyPureStateTransition @ Include/Core/HSBI_StateMachine.mqh:7 |
| 15 NormativeClauses | Docs/06_STATE_MACHINE_SPECIFICATION_RU.md:6–22; Docs/07_TRANSACTION_EXECUTION_CONTRACT_RU.md:6–25; Docs/16_PERSISTENCE_AND_RESTART_RU.md:11–19; Docs/17_RECONCILIATION_AND_TERMINAL_SAFE_RU.md:10–22 |
| 16 FormulaIDs | F024/F065 |
| 17 ErrorHandling | false/constant target/allowed flag согласно индивидуальным clauses; exceptions/status persistence не реализованы |
| 18 MissingChecksOrLimits | нет revision overflow guard, actual/persisted-result proof |
| 19 ActualIntegration | Main financial entry integration NOT_IMPLEMENTED; static callers перечислены отдельно; native NOT_RUN |
| 20 Verdict | PURE_PROPOSAL_PARTIAL; not execution admission |

R2-дополнение к сохранённой карточке (исходные20 полей и body не пересозданы):

| R2 field | Value |
|---|---|
| Function ID | Include/Core/HSBI_StateMachine.mqh:6:HSBI_ProposeStateTransition |
| Signature | HSBI_StateTransitionResult HSBI_ProposeStateTransition(const HSBI_RecoveryContext &c,const HSBI_State to) |
| Actual authority | Supplied DTO/expected scalar arguments; independent actual provider внутри функции отсутствует |
| Proof boundary | Local accepted body/path; конкретные callers перечислены в исходной карточке; global financial mandatory caller не доказан |

Полное фактическое тело (цитата, не новый исполняемый код):

~~~text
{HSBI_StateTransitionResult r;r.fromState=c.currentState;r.toState=to;r.allowed=HSBI_IsTransitionAllowed(c.currentState,to);r.proposedRevision=c.stateRevision+(r.allowed?1:0);r.reason=r.allowed?HSBI_REASON_OK:HSBI_REASON_INVALID_STATE_TRANSITION;return r;}
~~~

### FUNCTION HSBI_ApplyPureStateTransition

| Field | Individual analysis |
|---|---|
| 1 FullName | HSBI_ApplyPureStateTransition |
| 2 File | Include/Core/HSBI_StateMachine.mqh |
| 3 DeclarationLine | 7 |
| 4 BodyRange | 7–7 |
| 5 Purpose | Применить локальное изменение current/previous/revision |
| 6 InputParameters | HSBI_RecoveryContext &c,const HSBI_State to |
| 7 Outputs | bool |
| 8 Dimensions | State enum; revision ulong |
| 9 AdmittedValues | валидный context/to; revision без overflow |
| 10 Preconditions | Все financial prereqs обязан обеспечить внешний mandatory caller; такой orchestrator отсутствует |
| 11 Postconditions | при !allowed false/zero delta; при allowed previous=current,current=to,revision=proposed |
| 12 AllLocalGuards | HSBI_ProposeStateTransition; if(!r.allowed)return false |
| 13 OutgoingCalls | HSBI_ProposeStateTransition:7 |
| 14 ProductionCallsites | NO_PRODUCTION_CALLSITE_FOUND in74 source bodies |
| 15 NormativeClauses | Docs/06_STATE_MACHINE_SPECIFICATION_RU.md:6–22; Docs/07_TRANSACTION_EXECUTION_CONTRACT_RU.md:6–25; Docs/16_PERSISTENCE_AND_RESTART_RU.md:11–19; Docs/17_RECONCILIATION_AND_TERMINAL_SAFE_RU.md:10–22 |
| 16 FormulaIDs | F024/F065 |
| 17 ErrorHandling | false/constant target/allowed flag согласно индивидуальным clauses; exceptions/status persistence не реализованы |
| 18 MissingChecksOrLimits | нет event replay identity, outcome proof, persisted ledger guard; self-loop это не event-replay API |
| 19 ActualIntegration | Main financial entry integration NOT_IMPLEMENTED; static callers перечислены отдельно; native NOT_RUN |
| 20 Verdict | LOCAL_STATE_MUTATION_ONLY; полный runtime NOT_IMPLEMENTED |

R2-дополнение к сохранённой карточке (исходные20 полей и body не пересозданы):

| R2 field | Value |
|---|---|
| Function ID | Include/Core/HSBI_StateMachine.mqh:7:HSBI_ApplyPureStateTransition |
| Signature | bool HSBI_ApplyPureStateTransition(HSBI_RecoveryContext &c,const HSBI_State to) |
| Actual authority | Supplied DTO/expected scalar arguments; independent actual provider внутри функции отсутствует |
| Proof boundary | Local accepted body/path; конкретные callers перечислены в исходной карточке; global financial mandatory caller не доказан |

Полное фактическое тело (цитата, не новый исполняемый код):

~~~text
{HSBI_StateTransitionResult r=HSBI_ProposeStateTransition(c,to);if(!r.allowed)return false;c.previousState=c.currentState;c.currentState=to;c.stateRevision=r.proposedRevision;return true;}
~~~

### FUNCTION HSBI_ConflictTargetState

| Field | Individual analysis |
|---|---|
| 1 FullName | HSBI_ConflictTargetState |
| 2 File | Include/Core/HSBI_StateMachine.mqh |
| 3 DeclarationLine | 8 |
| 4 BodyRange | 8–8 |
| 5 Purpose | Вернуть declarative target обычного конфликта |
| 6 InputParameters | NONE |
| 7 Outputs | HSBI_State |
| 8 Dimensions | enum HSBI_State |
| 9 AdmittedValues | NOT_APPLICABLE: inputs отсутствуют |
| 10 Preconditions | Caller классифицирует конфликт до выбора helper |
| 11 Postconditions | HSBI_STATE_RECONCILING, без изменения context |
| 12 AllLocalGuards | NOT_APPLICABLE: constant return |
| 13 OutgoingCalls | NONE (project functions) |
| 14 ProductionCallsites | NO_PRODUCTION_CALLSITE_FOUND in74 source bodies |
| 15 NormativeClauses | Docs/06_STATE_MACHINE_SPECIFICATION_RU.md:6–22; Docs/07_TRANSACTION_EXECUTION_CONTRACT_RU.md:6–25; Docs/16_PERSISTENCE_AND_RESTART_RU.md:11–19; Docs/17_RECONCILIATION_AND_TERMINAL_SAFE_RU.md:10–22 |
| 16 FormulaIDs | F024 |
| 17 ErrorHandling | false/constant target/allowed flag согласно индивидуальным clauses; exceptions/status persistence не реализованы |
| 18 MissingChecksOrLimits | не различает severity/transaction conflicts; mandatory priority отсутствует в общем helper |
| 19 ActualIntegration | Main financial entry integration NOT_IMPLEMENTED; static callers перечислены отдельно; native NOT_RUN |
| 20 Verdict | CONSTANT_TARGET_NOT_HANDLER |

R2-дополнение к сохранённой карточке (исходные20 полей и body не пересозданы):

| R2 field | Value |
|---|---|
| Function ID | Include/Core/HSBI_StateMachine.mqh:8:HSBI_ConflictTargetState |
| Signature | HSBI_State HSBI_ConflictTargetState() |
| Actual authority | Supplied DTO/expected scalar arguments; independent actual provider внутри функции отсутствует |
| Proof boundary | Local accepted body/path; конкретные callers перечислены в исходной карточке; global financial mandatory caller не доказан |

Полное фактическое тело (цитата, не новый исполняемый код):

~~~text
{return HSBI_STATE_RECONCILING;}
~~~

### FUNCTION HSBI_CriticalErrorTargetState

| Field | Individual analysis |
|---|---|
| 1 FullName | HSBI_CriticalErrorTargetState |
| 2 File | Include/Core/HSBI_StateMachine.mqh |
| 3 DeclarationLine | 9 |
| 4 BodyRange | 9–9 |
| 5 Purpose | Вернуть target по unresolved flag |
| 6 InputParameters | const bool unresolved |
| 7 Outputs | HSBI_State |
| 8 Dimensions | bool → enum |
| 9 AdmittedValues | unresolved является корректно вычисленным bool, не external proof |
| 10 Preconditions | Caller независимо устанавливает critical/unresolved |
| 11 Postconditions | true→TERMINAL_SAFE,false→EMERGENCY; zero state delta |
| 12 AllLocalGuards | ternary unresolved flag |
| 13 OutgoingCalls | NONE (project functions) |
| 14 ProductionCallsites | NO_PRODUCTION_CALLSITE_FOUND in74 source bodies |
| 15 NormativeClauses | Docs/06_STATE_MACHINE_SPECIFICATION_RU.md:6–22; Docs/07_TRANSACTION_EXECUTION_CONTRACT_RU.md:6–25; Docs/16_PERSISTENCE_AND_RESTART_RU.md:11–19; Docs/17_RECONCILIATION_AND_TERMINAL_SAFE_RU.md:10–22 |
| 16 FormulaIDs | F024 |
| 17 ErrorHandling | false/constant target/allowed flag согласно индивидуальным clauses; exceptions/status persistence не реализованы |
| 18 MissingChecksOrLimits | источник unresolved и no-auto-resume не проверяются внутри; target не execution |
| 19 ActualIntegration | Main financial entry integration NOT_IMPLEMENTED; static callers перечислены отдельно; native NOT_RUN |
| 20 Verdict | CONSTANT_TARGET_NOT_HANDLER |

R2-дополнение к сохранённой карточке (исходные20 полей и body не пересозданы):

| R2 field | Value |
|---|---|
| Function ID | Include/Core/HSBI_StateMachine.mqh:9:HSBI_CriticalErrorTargetState |
| Signature | HSBI_State HSBI_CriticalErrorTargetState(const bool unresolved) |
| Actual authority | Supplied DTO/expected scalar arguments; independent actual provider внутри функции отсутствует |
| Proof boundary | Local accepted body/path; конкретные callers перечислены в исходной карточке; global financial mandatory caller не доказан |

Полное фактическое тело (цитата, не новый исполняемый код):

~~~text
{return unresolved?HSBI_STATE_TERMINAL_SAFE:HSBI_STATE_EMERGENCY;}
~~~

### FUNCTION HSBI_TransactionConflictTargetState

| Field | Individual analysis |
|---|---|
| 1 FullName | HSBI_TransactionConflictTargetState |
| 2 File | Include/Core/HSBI_StateMachine.mqh |
| 3 DeclarationLine | 10 |
| 4 BodyRange | 10–10 |
| 5 Purpose | Вернуть declarative target transaction conflict |
| 6 InputParameters | NONE |
| 7 Outputs | HSBI_State |
| 8 Dimensions | enum HSBI_State |
| 9 AdmittedValues | NOT_APPLICABLE: inputs отсутствуют |
| 10 Preconditions | Caller доказал transaction conflict |
| 11 Postconditions | HSBI_STATE_TERMINAL_SAFE; zero delta |
| 12 AllLocalGuards | NOT_APPLICABLE: constant return |
| 13 OutgoingCalls | NONE (project functions) |
| 14 ProductionCallsites | NO_PRODUCTION_CALLSITE_FOUND in74 source bodies |
| 15 NormativeClauses | Docs/06_STATE_MACHINE_SPECIFICATION_RU.md:6–22; Docs/07_TRANSACTION_EXECUTION_CONTRACT_RU.md:6–25; Docs/16_PERSISTENCE_AND_RESTART_RU.md:11–19; Docs/17_RECONCILIATION_AND_TERMINAL_SAFE_RU.md:10–22 |
| 16 FormulaIDs | F024/F053 |
| 17 ErrorHandling | false/constant target/allowed flag согласно индивидуальным clauses; exceptions/status persistence не реализованы |
| 18 MissingChecksOrLimits | не хранит EventKey/body и не проверяет conflict; не полный reconciliation |
| 19 ActualIntegration | Main financial entry integration NOT_IMPLEMENTED; static callers перечислены отдельно; native NOT_RUN |
| 20 Verdict | CONSTANT_TARGET_NOT_HANDLER |

R2-дополнение к сохранённой карточке (исходные20 полей и body не пересозданы):

| R2 field | Value |
|---|---|
| Function ID | Include/Core/HSBI_StateMachine.mqh:10:HSBI_TransactionConflictTargetState |
| Signature | HSBI_State HSBI_TransactionConflictTargetState() |
| Actual authority | Supplied DTO/expected scalar arguments; independent actual provider внутри функции отсутствует |
| Proof boundary | Local accepted body/path; конкретные callers перечислены в исходной карточке; global financial mandatory caller не доказан |

Полное фактическое тело (цитата, не новый исполняемый код):

~~~text
{return HSBI_STATE_TERMINAL_SAFE;}
~~~

### FUNCTION HSBI_IsCompletedOutcome

| Field | Individual analysis |
|---|---|
| 1 FullName | HSBI_IsCompletedOutcome |
| 2 File | Include/Execution/HSBI_TransactionTypes.mqh |
| 3 DeclarationLine | 6 |
| 4 BodyRange | 6–6 |
| 5 Purpose | Сравнить outcome с единственным COMPLETED enum |
| 6 InputParameters | const HSBI_TransactionOutcome o |
| 7 Outputs | bool |
| 8 Dimensions | transaction outcome enum → bool |
| 9 AdmittedValues | один из7 объявленных HSBI_TransactionOutcome |
| 10 Preconditions | Подтверждение actual deal/volume вне helper |
| 11 Postconditions | true iff HSBI_TX_COMPLETED; zero delta |
| 12 AllLocalGuards | exact equality COMPLETED |
| 13 OutgoingCalls | NONE (project functions) |
| 14 ProductionCallsites | NO_PRODUCTION_CALLSITE_FOUND in74 source bodies |
| 15 NormativeClauses | Docs/06_STATE_MACHINE_SPECIFICATION_RU.md:6–22; Docs/07_TRANSACTION_EXECUTION_CONTRACT_RU.md:6–25; Docs/16_PERSISTENCE_AND_RESTART_RU.md:11–19; Docs/17_RECONCILIATION_AND_TERMINAL_SAFE_RU.md:10–22 |
| 16 FormulaIDs | F024/F063 |
| 17 ErrorHandling | false/constant target/allowed flag согласно индивидуальным clauses; exceptions/status persistence не реализованы |
| 18 MissingChecksOrLimits | не валидирует полноту/ownership/currency; enum membership не explicit |
| 19 ActualIntegration | Main financial entry integration NOT_IMPLEMENTED; static callers перечислены отдельно; native NOT_RUN |
| 20 Verdict | LOCAL_ENUM_PREDICATE |

R2-дополнение к сохранённой карточке (исходные20 полей и body не пересозданы):

| R2 field | Value |
|---|---|
| Function ID | Include/Execution/HSBI_TransactionTypes.mqh:6:HSBI_IsCompletedOutcome |
| Signature | bool HSBI_IsCompletedOutcome(const HSBI_TransactionOutcome o) |
| Actual authority | Supplied DTO/expected scalar arguments; independent actual provider внутри функции отсутствует |
| Proof boundary | Local accepted body/path; конкретные callers перечислены в исходной карточке; global financial mandatory caller не доказан |

Полное фактическое тело (цитата, не новый исполняемый код):

~~~text
{return o==HSBI_TX_COMPLETED;}
~~~

### FUNCTION HSBI_IsRetryOfSameAction

| Field | Individual analysis |
|---|---|
| 1 FullName | HSBI_IsRetryOfSameAction |
| 2 File | Include/Execution/HSBI_TransactionTypes.mqh |
| 3 DeclarationLine | 7 |
| 4 BodyRange | 7–7 |
| 5 Purpose | Проверить ненулевой одинаковый ActionID |
| 6 InputParameters | const ulong originalActionId,const ulong retryActionId |
| 7 Outputs | bool |
| 8 Dimensions | ulong IDs, не деньги |
| 9 AdmittedValues | original/retry ulong; original>0 |
| 10 Preconditions | История pending/completed устанавливается caller |
| 11 Postconditions | true iff original>0 && original==retry; zero delta |
| 12 AllLocalGuards | originalActionId>0; equality retry |
| 13 OutgoingCalls | NONE (project functions) |
| 14 ProductionCallsites | HSBI_RetryAllowed @ Include/Execution/HSBI_TransactionTypes.mqh:22 |
| 15 NormativeClauses | Docs/06_STATE_MACHINE_SPECIFICATION_RU.md:6–22; Docs/07_TRANSACTION_EXECUTION_CONTRACT_RU.md:6–25; Docs/16_PERSISTENCE_AND_RESTART_RU.md:11–19; Docs/17_RECONCILIATION_AND_TERMINAL_SAFE_RU.md:10–22 |
| 16 FormulaIDs | F024/F053 |
| 17 ErrorHandling | false/constant target/allowed flag согласно индивидуальным clauses; exceptions/status persistence не реализованы |
| 18 MissingChecksOrLimits | нет actual history/PENDING/attempt uniqueness; один helper не safe retry |
| 19 ActualIntegration | Main financial entry integration NOT_IMPLEMENTED; static callers перечислены отдельно; native NOT_RUN |
| 20 Verdict | LOCAL_ID_PREDICATE |

R2-дополнение к сохранённой карточке (исходные20 полей и body не пересозданы):

| R2 field | Value |
|---|---|
| Function ID | Include/Execution/HSBI_TransactionTypes.mqh:7:HSBI_IsRetryOfSameAction |
| Signature | bool HSBI_IsRetryOfSameAction(const ulong originalActionId,const ulong retryActionId) |
| Actual authority | Supplied DTO/expected scalar arguments; independent actual provider внутри функции отсутствует |
| Proof boundary | Local accepted body/path; конкретные callers перечислены в исходной карточке; global financial mandatory caller не доказан |

Полное фактическое тело (цитата, не новый исполняемый код):

~~~text
{return originalActionId>0&&originalActionId==retryActionId;}
~~~

### FUNCTION HSBI_IsFreshEvent

| Field | Individual analysis |
|---|---|
| 1 FullName | HSBI_IsFreshEvent |
| 2 File | Include/Execution/HSBI_TransactionTypes.mqh |
| 3 DeclarationLine | 8 |
| 4 BodyRange | 8–8 |
| 5 Purpose | Проверить строгий порядок eventId |
| 6 InputParameters | const ulong lastEventId,const ulong eventId |
| 7 Outputs | bool |
| 8 Dimensions | ulong EventID, не wall-clock time |
| 9 AdmittedValues | last/event ulong; EventID ordering contract должен быть утверждён |
| 10 Preconditions | Caller имеет authoritative lastAppliedEventId, не presented echo |
| 11 Postconditions | true iff eventId>lastEventId; zero delta |
| 12 AllLocalGuards | строгое > |
| 13 OutgoingCalls | NONE (project functions) |
| 14 ProductionCallsites | HSBI_TransactionBarrierPassed @ Include/Execution/HSBI_TransactionTypes.mqh:13 |
| 15 NormativeClauses | Docs/06_STATE_MACHINE_SPECIFICATION_RU.md:6–22; Docs/07_TRANSACTION_EXECUTION_CONTRACT_RU.md:6–25; Docs/16_PERSISTENCE_AND_RESTART_RU.md:11–19; Docs/17_RECONCILIATION_AND_TERMINAL_SAFE_RU.md:10–22 |
| 16 FormulaIDs | F053/F065 |
| 17 ErrorHandling | false/constant target/allowed flag согласно индивидуальным clauses; exceptions/status persistence не реализованы |
| 18 MissingChecksOrLimits | не source identity/immutable body proof; out-of-order legitimate events требуют reconciliation, не silent skip |
| 19 ActualIntegration | Main financial entry integration NOT_IMPLEMENTED; static callers перечислены отдельно; native NOT_RUN |
| 20 Verdict | LOCAL_ORDER_PREDICATE |

R2-дополнение к сохранённой карточке (исходные20 полей и body не пересозданы):

| R2 field | Value |
|---|---|
| Function ID | Include/Execution/HSBI_TransactionTypes.mqh:8:HSBI_IsFreshEvent |
| Signature | bool HSBI_IsFreshEvent(const ulong lastEventId,const ulong eventId) |
| Actual authority | Supplied DTO/expected scalar arguments; independent actual provider внутри функции отсутствует |
| Proof boundary | Local accepted body/path; конкретные callers перечислены в исходной карточке; global financial mandatory caller не доказан |

Полное фактическое тело (цитата, не новый исполняемый код):

~~~text
{return eventId>lastEventId;}
~~~

### FUNCTION HSBI_TransactionBarrierPassed

| Field | Individual analysis |
|---|---|
| 1 FullName | HSBI_TransactionBarrierPassed |
| 2 File | Include/Execution/HSBI_TransactionTypes.mqh |
| 3 DeclarationLine | 9 |
| 4 BodyRange | 10–19 |
| 5 Purpose | Проверить локальный DTO transaction barrier |
| 6 InputParameters | const HSBI_TransactionBarrierInput &x |
| 7 Outputs | bool |
| 8 Dimensions | volume lots; Event/Action/Revision IDs ulong; bool evidence flags |
| 9 AdmittedValues | конечные nonnegative actual/expected volume; finite checks отсутствуют |
| 10 Preconditions | actualPositionRead/actualDealRead/ownershipConfirmed должны происходить от independent mandatory provider |
| 11 Postconditions | true только после перечисленных clauses; context не меняется |
| 12 AllLocalGuards | COMPLETED;expectedAction>0/equal;fresh event;3actual/ownership flags;expectedVolume>0;abs(volume difference)<=1e-7;revision equality;!reconciliationConflict |
| 13 OutgoingCalls | HSBI_IsFreshEvent:13 |
| 14 ProductionCallsites | NO_PRODUCTION_CALLSITE_FOUND in74 source bodies |
| 15 NormativeClauses | Docs/06_STATE_MACHINE_SPECIFICATION_RU.md:6–22; Docs/07_TRANSACTION_EXECUTION_CONTRACT_RU.md:6–25; Docs/16_PERSISTENCE_AND_RESTART_RU.md:11–19; Docs/17_RECONCILIATION_AND_TERMINAL_SAFE_RU.md:10–22 |
| 16 FormulaIDs | F024/F025/F036/F063 |
| 17 ErrorHandling | false/constant target/allowed flag согласно индивидуальным clauses; exceptions/status persistence не реализованы |
| 18 MissingChecksOrLimits | nonfinite domain; transaction.ledgerApplied не читается; persisted-result proof отсутствует; flags не authentic evidence |
| 19 ActualIntegration | Main financial entry integration NOT_IMPLEMENTED; static callers перечислены отдельно; native NOT_RUN |
| 20 Verdict | INCOMPLETE_BARRIER; source guard defect scope ERR010, not live-trade exploit |

R2-дополнение к сохранённой карточке (исходные20 полей и body не пересозданы):

| R2 field | Value |
|---|---|
| Function ID | Include/Execution/HSBI_TransactionTypes.mqh:9:HSBI_TransactionBarrierPassed |
| Signature | bool HSBI_TransactionBarrierPassed(const HSBI_TransactionBarrierInput &x) |
| Actual authority | Supplied DTO/expected scalar arguments; independent actual provider внутри функции отсутствует |
| Proof boundary | Local accepted body/path; конкретные callers перечислены в исходной карточке; global financial mandatory caller не доказан |

Полное фактическое тело (цитата, не новый исполняемый код):

~~~text
{
   if(x.transaction.outcome!=HSBI_TX_COMPLETED)return false;
   if(x.expectedActionId==0||x.transaction.actionId!=x.expectedActionId)return false;
   if(!HSBI_IsFreshEvent(x.lastAppliedEventId,x.transaction.eventId))return false;
   if(!x.transaction.actualPositionRead||!x.actualDealRead||!x.ownershipConfirmed)return false;
   if(x.transaction.expectedVolume<=0.0||MathAbs(x.transaction.accumulatedVolume-x.transaction.expectedVolume)>0.0000001)return false;
   if(x.actualStateRevision!=x.expectedStateRevision)return false;
   if(x.reconciliationConflict)return false;
   return true;
}
~~~

### FUNCTION HSBI_RetryAllowed

| Field | Individual analysis |
|---|---|
| 1 FullName | HSBI_RetryAllowed |
| 2 File | Include/Execution/HSBI_TransactionTypes.mqh |
| 3 DeclarationLine | 20 |
| 4 BodyRange | 21–23 |
| 5 Purpose | Локально разрешить retry по pending flag и ActionID |
| 6 InputParameters | const ulong originalActionId,const ulong retryActionId,const HSBI_TransactionOutcome priorOutcome,const bool pendingOrReconciling |
| 7 Outputs | bool |
| 8 Dimensions | IDs ulong; outcome enum; bool |
| 9 AdmittedValues | объявленный outcome и корректно authoritative pendingOrReconciling |
| 10 Preconditions | Caller перечитал history, исключил completed deal/duplicate request, проверил state/ownership/snapshot |
| 11 Postconditions | pending && same nonzero action && priorOutcome!=COMPLETED; zero delta |
| 12 AllLocalGuards | pendingOrReconciling;HSBI_IsRetryOfSameAction;priorOutcome!=COMPLETED |
| 13 OutgoingCalls | HSBI_IsRetryOfSameAction:22 |
| 14 ProductionCallsites | NO_PRODUCTION_CALLSITE_FOUND in74 source bodies |
| 15 NormativeClauses | Docs/06_STATE_MACHINE_SPECIFICATION_RU.md:6–22; Docs/07_TRANSACTION_EXECUTION_CONTRACT_RU.md:6–25; Docs/16_PERSISTENCE_AND_RESTART_RU.md:11–19; Docs/17_RECONCILIATION_AND_TERMINAL_SAFE_RU.md:10–22 |
| 16 FormulaIDs | F024/F053 |
| 17 ErrorHandling | false/constant target/allowed flag согласно индивидуальным clauses; exceptions/status persistence не реализованы |
| 18 MissingChecksOrLimits | не проверяет все Docs07 retry prerequisites; unknown outcome допускается если caller утверждает pending |
| 19 ActualIntegration | Main financial entry integration NOT_IMPLEMENTED; static callers перечислены отдельно; native NOT_RUN |
| 20 Verdict | RETRY_HELPER_ONLY; full mandatory caller not established |

R2-дополнение к сохранённой карточке (исходные20 полей и body не пересозданы):

| R2 field | Value |
|---|---|
| Function ID | Include/Execution/HSBI_TransactionTypes.mqh:20:HSBI_RetryAllowed |
| Signature | bool HSBI_RetryAllowed(const ulong originalActionId,const ulong retryActionId,const HSBI_TransactionOutcome priorOutcome,const bool pendingOrReconciling) |
| Actual authority | Supplied DTO/expected scalar arguments; independent actual provider внутри функции отсутствует |
| Proof boundary | Local accepted body/path; конкретные callers перечислены в исходной карточке; global financial mandatory caller не доказан |

Полное фактическое тело (цитата, не новый исполняемый код):

~~~text
{
   return pendingOrReconciling&&HSBI_IsRetryOfSameAction(originalActionId,retryActionId)&&priorOutcome!=HSBI_TX_COMPLETED;
}
~~~


## FINAL-CLOSURE — индивидуальные Runtime decision/restart/barrier функции

### FUNCTION HSBI_RuntimeReject

| Field | Individual analysis |
|---|---|
| 1 FullName | HSBI_RuntimeReject |
| 2 File | Include/Runtime/HSBI_RuntimeDecisionValidator.mqh |
| 3 DeclarationLine | 4 |
| 4 BodyRange | 4–4 |
| 5 Purpose | Построить zero-initialized diagnostic decision result |
| 6 InputParameters | const HSBI_RuntimeDecisionContext &x,const HSBI_RuntimeDecisionStatus status,const HSBI_RuntimeDecisionReason reason,const string req |
| 7 Outputs | HSBI_RuntimeDecisionResult |
| 8 Dimensions | IDs ulong; status/reason enums; digest/string |
| 9 AdmittedValues | status/reason/req заданы caller; исходный context константный |
| 10 Preconditions | Caller различает diagnostic status и financial permission |
| 11 Postconditions | valid=false после ZeroMemory; копирует plan/cycle/revision/inputDigest/requirementId; исходный context unchanged |
| 12 AllLocalGuards | нет local validation: это result constructor |
| 13 OutgoingCalls | NONE project functions |
| 14 ProductionCallsites | HSBI_ValidateRuntimeDecisionContext @ Include/Runtime/HSBI_RuntimeDecisionValidator.mqh:8; HSBI_ValidateRuntimeDecisionContext @ Include/Runtime/HSBI_RuntimeDecisionValidator.mqh:9; HSBI_ValidateRuntimeDecisionContext @ Include/Runtime/HSBI_RuntimeDecisionValidator.mqh:10; HSBI_ValidateRuntimeDecisionContext @ Include/Runtime/HSBI_RuntimeDecisionValidator.mqh:11; HSBI_ValidateRuntimeDecisionContext @ Include/Runtime/HSBI_RuntimeDecisionValidator.mqh:12; HSBI_ValidateRuntimeDecisionContext @ Include/Runtime/HSBI_RuntimeDecisionValidator.mqh:13; HSBI_ValidateRuntimeDecisionContext @ Include/Runtime/HSBI_RuntimeDecisionValidator.mqh:14; HSBI_ValidateRuntimeDecisionContext @ Include/Runtime/HSBI_RuntimeDecisionValidator.mqh:15; HSBI_ValidateRuntimeDecisionContext @ Include/Runtime/HSBI_RuntimeDecisionValidator.mqh:16; HSBI_ValidateRuntimeDecisionContext @ Include/Runtime/HSBI_RuntimeDecisionValidator.mqh:17; HSBI_ValidateRuntimeDecisionContext @ Include/Runtime/HSBI_RuntimeDecisionValidator.mqh:18; HSBI_ValidateRuntimeDecisionContext @ Include/Runtime/HSBI_RuntimeDecisionValidator.mqh:19; HSBI_ValidateRuntimeDecisionContext @ Include/Runtime/HSBI_RuntimeDecisionValidator.mqh:20; HSBI_ValidateRuntimeDecisionContext @ Include/Runtime/HSBI_RuntimeDecisionValidator.mqh:21; HSBI_ValidateRuntimeDecisionContext @ Include/Runtime/HSBI_RuntimeDecisionValidator.mqh:22; HSBI_ValidateRuntimeDecisionContext @ Include/Runtime/HSBI_RuntimeDecisionValidator.mqh:23; HSBI_ValidateRuntimeDecisionContext @ Include/Runtime/HSBI_RuntimeDecisionValidator.mqh:24; HSBI_ValidateRuntimeDecisionContext @ Include/Runtime/HSBI_RuntimeDecisionValidator.mqh:25; HSBI_ValidateRuntimeDecisionContext @ Include/Runtime/HSBI_RuntimeDecisionValidator.mqh:26; HSBI_ValidateRuntimeDecisionContext @ Include/Runtime/HSBI_RuntimeDecisionValidator.mqh:27; HSBI_ValidateRuntimeDecisionContext @ Include/Runtime/HSBI_RuntimeDecisionValidator.mqh:28; HSBI_ValidateRestartedRuntimeState @ Include/Runtime/HSBI_RuntimeRestartValidator.mqh:7; HSBI_ValidateRestartedRuntimeState @ Include/Runtime/HSBI_RuntimeRestartValidator.mqh:8; HSBI_ValidateRestartedRuntimeState @ Include/Runtime/HSBI_RuntimeRestartValidator.mqh:9; HSBI_ValidateRestartedRuntimeState @ Include/Runtime/HSBI_RuntimeRestartValidator.mqh:10; HSBI_ValidateRestartedRuntimeState @ Include/Runtime/HSBI_RuntimeRestartValidator.mqh:11; HSBI_ValidateRestartedRuntimeState @ Include/Runtime/HSBI_RuntimeRestartValidator.mqh:12; HSBI_ValidateRestartedRuntimeState @ Include/Runtime/HSBI_RuntimeRestartValidator.mqh:13; HSBI_ValidateRestartedRuntimeState @ Include/Runtime/HSBI_RuntimeRestartValidator.mqh:14; HSBI_ValidateRestartedRuntimeState @ Include/Runtime/HSBI_RuntimeRestartValidator.mqh:15; HSBI_CanAdvanceRuntimeDecision @ Include/Runtime/HSBI_RuntimeTransactionBarrier.mqh:8; HSBI_CanAdvanceRuntimeDecision @ Include/Runtime/HSBI_RuntimeTransactionBarrier.mqh:8; HSBI_CanAdvanceRuntimeDecision @ Include/Runtime/HSBI_RuntimeTransactionBarrier.mqh:9; HSBI_CanAdvanceRuntimeDecision @ Include/Runtime/HSBI_RuntimeTransactionBarrier.mqh:10; HSBI_CanAdvanceRuntimeDecision @ Include/Runtime/HSBI_RuntimeTransactionBarrier.mqh:11; HSBI_CanAdvanceRuntimeDecision @ Include/Runtime/HSBI_RuntimeTransactionBarrier.mqh:12; HSBI_CanAdvanceRuntimeDecision @ Include/Runtime/HSBI_RuntimeTransactionBarrier.mqh:13; HSBI_CanAdvanceRuntimeDecision @ Include/Runtime/HSBI_RuntimeTransactionBarrier.mqh:14; HSBI_CanAdvanceRuntimeDecision @ Include/Runtime/HSBI_RuntimeTransactionBarrier.mqh:14; HSBI_CanAdvanceRuntimeDecision @ Include/Runtime/HSBI_RuntimeTransactionBarrier.mqh:15; HSBI_CanAdvanceRuntimeDecision @ Include/Runtime/HSBI_RuntimeTransactionBarrier.mqh:16 |
| 15 NormativeClauses | Docs/06:8–22; Docs/07:6–25; Docs/16:8–19; Docs/17:3–22; exact paths in FSM_COMPLETE_MATRIX |
| 16 FormulaIDs | F036/F060 |
| 17 ErrorHandling | Первый typed return по body; FAIL/NO_OP не меняют вход; implementation exceptions не скрываются аудитом |
| 18 MissingChecksOrLimits | Не валидирует enum/digest/authority; constructor сам не обещает проверку |
| 19 ActualIntegration | Pure DTO validator; no financial main entry integration; native NOT_RUN |
| 20 Verdict | RESULT_CONSTRUCTOR; не финансовый guard |

R2-дополнение к сохранённой карточке (исходные20 полей и body не пересозданы):

| R2 field | Value |
|---|---|
| Function ID | Include/Runtime/HSBI_RuntimeDecisionValidator.mqh:4:HSBI_RuntimeReject |
| Signature | HSBI_RuntimeDecisionResult HSBI_RuntimeReject(const HSBI_RuntimeDecisionContext &x,const HSBI_RuntimeDecisionStatus status,const HSBI_RuntimeDecisionReason reason,const string req) |
| Actual authority | Supplied DTO/expected scalar arguments; independent actual provider внутри функции отсутствует |
| Proof boundary | Local accepted body/path; конкретные callers перечислены в исходной карточке; global financial mandatory caller не доказан |

Полное фактическое тело (цитата, не новый исполняемый код):

~~~text
{HSBI_RuntimeDecisionResult r;ZeroMemory(r);r.status=status;r.reason=reason;r.planId=x.planId;r.cycleId=x.cycleId;r.stateRevision=x.stateRevision;r.inputDigest=x.inputDigest;r.requirementId=req;return r;}
~~~

### FUNCTION HSBI_RuntimePositionMatches

| Field | Individual analysis |
|---|---|
| 1 FullName | HSBI_RuntimePositionMatches |
| 2 File | Include/Runtime/HSBI_RuntimeDecisionValidator.mqh |
| 3 DeclarationLine | 5 |
| 4 BodyRange | 5–5 |
| 5 Purpose | Сравнить local descriptor с ожидаемым role/context |
| 6 InputParameters | const HSBI_PositionDescriptor &p,const HSBI_RuntimeDecisionContext &x,const HSBI_Role role |
| 7 Outputs | bool |
| 8 Dimensions | volume lots; namespace IDs; direction/role enums |
| 9 AdmittedValues | actualVolume finite>0, role известна, context independently authoritative |
| 10 Preconditions | Caller предоставляет actual descriptor и independent expected context |
| 11 Postconditions | true iff identifier/ticket>0,actualVolume>0,role exact,direction!=NONE и account/symbol/magic/cycle equal |
| 12 AllLocalGuards | identifier>0;ticket>0;actualVolume>0;role equality;direction!=NONE;4 namespace equalities |
| 13 OutgoingCalls | NONE project functions |
| 14 ProductionCallsites | HSBI_ValidateRuntimeDecisionContext @ Include/Runtime/HSBI_RuntimeDecisionValidator.mqh:18 |
| 15 NormativeClauses | Docs/06:8–22; Docs/07:6–25; Docs/16:8–19; Docs/17:3–22; exact paths in FSM_COMPLETE_MATRIX |
| 16 FormulaIDs | F036/F053/F062 |
| 17 ErrorHandling | Первый typed return по body; FAIL/NO_OP не меняют вход; implementation exceptions не скрываются аудитом |
| 18 MissingChecksOrLimits | не finite-positive volume для Infinity, direction!=NONE допускает unknown enum; сверка с x не доказывает независимое происхождение |
| 19 ActualIntegration | Pure DTO validator; no financial main entry integration; native NOT_RUN |
| 20 Verdict | LOCAL_MATCH_PARTIAL; source domain/provenance limits |

R2-дополнение к сохранённой карточке (исходные20 полей и body не пересозданы):

| R2 field | Value |
|---|---|
| Function ID | Include/Runtime/HSBI_RuntimeDecisionValidator.mqh:5:HSBI_RuntimePositionMatches |
| Signature | bool HSBI_RuntimePositionMatches(const HSBI_PositionDescriptor &p,const HSBI_RuntimeDecisionContext &x,const HSBI_Role role) |
| Actual authority | Supplied DTO/expected scalar arguments; independent actual provider внутри функции отсутствует |
| Proof boundary | Local accepted body/path; конкретные callers перечислены в исходной карточке; global financial mandatory caller не доказан |

Полное фактическое тело (цитата, не новый исполняемый код):

~~~text
{return p.identifier>0&&p.ticket>0&&p.actualVolume>0.0&&p.role==role&&p.direction!=HSBI_DIRECTION_NONE&&p.identity.accountLogin==x.accountLogin&&p.identity.symbol==x.symbol&&p.identity.magic==x.magic&&p.identity.cycleId==x.cycleId;}
~~~

### FUNCTION HSBI_ValidateRuntimeDecisionContext

| Field | Individual analysis |
|---|---|
| 1 FullName | HSBI_ValidateRuntimeDecisionContext |
| 2 File | Include/Runtime/HSBI_RuntimeDecisionValidator.mqh |
| 3 DeclarationLine | 6 |
| 4 BodyRange | 7–29 |
| 5 Purpose | Локально проверить композицию decision DTO |
| 6 InputParameters | const HSBI_RuntimeDecisionContext &x,const long account,const string symbol,const long magic,const ulong cycle,const ulong plan,const ulong revision |
| 7 Outputs | HSBI_RuntimeDecisionResult |
| 8 Dimensions | money currency; volume lots; IDs/revision; schema ints; bool evidence flags |
| 9 AdmittedValues | полные корректные DTO, finite численные поля и независимые expected account/symbol/magic/cycle/plan/revision |
| 10 Preconditions | Authoritative provider должен связывать money/risk/allocation/actual evidence; self-expected не authority |
| 11 Postconditions | typed status на первом отказе; VALID даёт selected candidate/aggregate/catchup/allocation, requiredNextState=RECONCILING; не меняет context и ledgers |
| 12 AllLocalGuards | immutable+productionPreflight;namespace;revision;schema/moneyVersion;3fresh flags;reconciliation conflict/confirmed;nonzeroevent/action;position flags;residual match;aggregate completeness;candidate match;catchup flags;money/risk identity validators;allocation validators;consumption;persist flag;context digest |
| 13 OutgoingCalls | HSBI_IsProductionPreflightAllowed:8; HSBI_RuntimeReject:8; HSBI_RuntimeReject:9; HSBI_RuntimeReject:10; HSBI_RuntimeReject:11; HSBI_RuntimeReject:12; HSBI_RuntimeReject:13; HSBI_RuntimeReject:14; HSBI_RuntimeReject:15; HSBI_RuntimeReject:16; HSBI_RuntimeReject:17; HSBI_RuntimePositionMatches:18; HSBI_RuntimeReject:18; HSBI_RuntimeReject:19; HSBI_IsCompleteCandidateProof:20; HSBI_RuntimeReject:20; HSBI_RuntimeReject:21; HSBI_ValidateMoneyProofIdentity:22; HSBI_RuntimeReject:22; HSBI_ValidateMoneyProofIdentity:23; HSBI_RuntimeReject:23; HSBI_ValidateAllocationPolicy:24; HSBI_ValidateReserveAllocationSource:24; HSBI_RuntimeReject:24; HSBI_ValidateReserveConsumption:25; HSBI_RuntimeReject:25; HSBI_RuntimeReject:26; HSBI_RuntimeDecisionContextDigest:27; HSBI_RuntimeReject:27; HSBI_RuntimeReject:28 |
| 14 ProductionCallsites | HSBI_ValidateRestartedRuntimeState @ Include/Runtime/HSBI_RuntimeRestartValidator.mqh:16; HSBI_CanAdvanceRuntimeDecision @ Include/Runtime/HSBI_RuntimeTransactionBarrier.mqh:7 |
| 15 NormativeClauses | Docs/06:8–22; Docs/07:6–25; Docs/16:8–19; Docs/17:3–22; exact paths in FSM_COMPLETE_MATRIX |
| 16 FormulaIDs | F013/F019/F024/F036/F053/F057/F062 |
| 17 ErrorHandling | Первый typed return по body; FAIL/NO_OP не меняют вход; implementation exceptions не скрываются аудитом |
| 18 MissingChecksOrLimits | expected arguments могут быть скопированы из x callers; структурная validate identity не независимый broker proof; consumption amount-binding ERR048; enum ERR049; нет durable mutation |
| 19 ActualIntegration | Pure DTO validator; no financial main entry integration; native NOT_RUN |
| 20 Verdict | LOCAL_COMPOSITION_PARTIAL; not global or production spending |

R2-дополнение к сохранённой карточке (исходные20 полей и body не пересозданы):

| R2 field | Value |
|---|---|
| Function ID | Include/Runtime/HSBI_RuntimeDecisionValidator.mqh:6:HSBI_ValidateRuntimeDecisionContext |
| Signature | HSBI_RuntimeDecisionResult HSBI_ValidateRuntimeDecisionContext(const HSBI_RuntimeDecisionContext &x,const long account,const string symbol,const long magic,const ulong cycle,const ulong plan,const ulong revision) |
| Actual authority | Supplied DTO/expected scalar arguments; independent actual provider внутри функции отсутствует |
| Proof boundary | Local accepted body/path; конкретные callers перечислены в исходной карточке; global financial mandatory caller не доказан |

Полное фактическое тело (цитата, не новый исполняемый код):

~~~text
{
 if(!x.immutable||!HSBI_IsProductionPreflightAllowed(x.runtimeMode))return HSBI_RuntimeReject(x,HSBI_DECISION_REJECTED,HSBI_RD_CONTEXT_INVALID,"HSBI-2D-CTX");
 if(x.accountLogin!=account||x.symbol!=symbol||x.magic!=magic||x.cycleId!=cycle||x.planId!=plan)return HSBI_RuntimeReject(x,HSBI_DECISION_REJECTED,HSBI_RD_IDENTITY_MISMATCH,"HSBI-2D-ID");
 if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,"HSBI-2D-REV");
 if(x.schemaVersion!=HSBI_SCHEMA_VERSION)return HSBI_RuntimeReject(x,HSBI_DECISION_REJECTED,HSBI_RD_SCHEMA_VERSION_MISMATCH,"HSBI-2D-SCHEMA");
 if(x.moneyStateVersion!=HSBI_MONEY_STATE_VERSION)return HSBI_RuntimeReject(x,HSBI_DECISION_REJECTED,HSBI_RD_MONEY_STATE_VERSION_MISMATCH,"HSBI-2D-MONEY-VERSION");
 if(!x.marketFresh||!x.costFresh||!x.allocationPolicy.fresh)return HSBI_RuntimeReject(x,HSBI_DECISION_STALE,HSBI_RD_STALE_SNAPSHOT,"HSBI-2D-FRESH");
 if(x.reconciliationConflict)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_RECONCILIATION_CONFLICT,"HSBI-2D-RECON");
 if(!x.reconciliationConfirmed)return HSBI_RuntimeReject(x,HSBI_DECISION_RECONCILIATION_REQUIRED,HSBI_RD_RECONCILIATION_REQUIRED,"HSBI-2D-RECON");
 if(x.eventId==0||x.actionId==0)return HSBI_RuntimeReject(x,HSBI_DECISION_REJECTED,x.eventId==0?HSBI_RD_EVENT_NOT_FRESH:HSBI_RD_ACTION_ID_MISMATCH,"HSBI-2D-EVENT");
 if(!x.positionActuallyRead||!x.ownershipConfirmed)return HSBI_RuntimeReject(x,HSBI_DECISION_REJECTED,HSBI_RD_POSITION_NOT_CONFIRMED,"HSBI-2D-POS");
 if(!x.residualActual||!HSBI_RuntimePositionMatches(x.actualResidual,x,HSBI_ROLE_BIG_CORE))return HSBI_RuntimeReject(x,HSBI_DECISION_REJECTED,HSBI_RD_ACTUAL_RESIDUAL_REQUIRED,"HSBI-2D-RESIDUAL");
 if(!x.aggregate.valid||x.aggregate.levelCount<2||x.aggregate.evaluatedLevelCount!=x.aggregate.levelCount||!x.aggregate.runtimeConfirmed||!x.aggregate.allMoneyProofsValid||!x.aggregate.allMarginProofsValid||!x.aggregate.allRiskProofsValid)return HSBI_RuntimeReject(x,HSBI_DECISION_UNAVAILABLE,HSBI_RD_FUTURE_SMALL_INCOMPLETE,"HSBI-2D-FS");
 if(!HSBI_IsCompleteCandidateProof(x.candidate)||x.candidate.sourceBigCoreIdentifier!=x.actualResidual.identifier||x.candidate.sourceBigCoreTicket!=x.actualResidual.ticket)return HSBI_RuntimeReject(x,HSBI_DECISION_REJECTED,HSBI_RD_NEW_FAR_INVALID,"HSBI-2D-NF");
 if(!x.catchUp.valid||!x.catchUp.runtimeConfirmed||!x.catchUp.reserveSourceIdentityValid||!x.catchUp.farLossSourceIdentityValid)return HSBI_RuntimeReject(x,HSBI_DECISION_UNAVAILABLE,HSBI_RD_CATCH_UP_INVALID,"HSBI-2D-CATCHUP");
 if(!x.moneyRuntimeConfirmed||!HSBI_ValidateMoneyProofIdentity(x.moneyIdentity)||!x.marginRuntimeConfirmed)return HSBI_RuntimeReject(x,HSBI_DECISION_UNAVAILABLE,HSBI_RD_MONEY_UNAVAILABLE,"HSBI-2D-MONEY");
 if(!x.riskRuntimeConfirmed||!HSBI_ValidateMoneyProofIdentity(x.riskIdentity))return HSBI_RuntimeReject(x,HSBI_DECISION_UNAVAILABLE,HSBI_RD_RISK_UNAVAILABLE,"HSBI-2D-RISK");
 if(!HSBI_ValidateAllocationPolicy(x.allocationPolicy)||!HSBI_ValidateReserveAllocationSource(x.allocationSource))return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_ALLOCATION_CONFLICT,"HSBI-2D-ALLOC");
 if(x.consumptionConflict||!HSBI_ValidateReserveConsumption(x.consumptionKey,x.planId,x.stateRevision))return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_CONSUMPTION_CONFLICT,"HSBI-2D-CONSUME");
 if(!x.persistencePrepared)return HSBI_RuntimeReject(x,HSBI_DECISION_PERSISTENCE_REQUIRED,HSBI_RD_PERSISTENCE_REQUIRED,"HSBI-2D-PERSIST");
 if(x.inputDigest==""||x.inputDigest!=HSBI_RuntimeDecisionContextDigest(x))return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_DIGEST_MISMATCH,"HSBI-2D-DIGEST");
 HSBI_RuntimeDecisionResult r=HSBI_RuntimeReject(x,HSBI_DECISION_VALID,HSBI_RD_OK,"HSBI-2D-VALID");r.valid=true;r.selectedCandidate=x.candidate;r.selectedAggregate=x.aggregate;r.catchUp=x.catchUp;r.allocation=x.allocationSource;r.requiredNextState=HSBI_STATE_RECONCILING;r.pendingActionId=x.actionId;r.outputDigest=x.inputDigest+"|VALID";return r;
}
~~~

### FUNCTION HSBI_ValidateRestartedRuntimeState

| Field | Individual analysis |
|---|---|
| 1 FullName | HSBI_ValidateRestartedRuntimeState |
| 2 File | Include/Runtime/HSBI_RuntimeRestartValidator.mqh |
| 3 DeclarationLine | 5 |
| 4 BodyRange | 6–17 |
| 5 Purpose | Сопоставить сохранённое и текущее состояние для локальной restart eligibility |
| 6 InputParameters | const HSBI_RestartedRuntimeState &s |
| 7 Outputs | HSBI_RuntimeDecisionResult |
| 8 Dimensions | snapshots/IDs/revision; volume lots; allocation money |
| 9 AdmittedValues | persisted snapshot + journal/actual history подтверждены независимо, версии поддержаны |
| 10 Preconditions | provider обязан заполнить history/source/duplicate flags; checksum alone не authenticity |
| 11 Postconditions | first-failure typed status; duplicateConsumption→NO_OP при prechecks; иначе delegates decision validator; zero input delta |
| 12 AllLocalGuards | snapshot present/digest nonempty;snapshot validator;plan/rev/event/action binding;historyUnchanged&&!sourceReused&&!payloadConflict;duplicate branch;unresolvedPending;broker/recon flags;5residual equalities;allocation+consumption digest equality;decision validator |
| 13 OutgoingCalls | HSBI_RuntimeReject:7; HSBI_ValidateExecutionStateSnapshot:8; HSBI_RuntimeReject:8; HSBI_RuntimeReject:9; HSBI_RuntimeReject:10; HSBI_RuntimeReject:11; HSBI_RuntimeReject:12; HSBI_RuntimeReject:13; HSBI_RuntimeReject:14; HSBI_ReserveAllocationSourceDigest:15; HSBI_ReserveAllocationSourceDigest:15; HSBI_ReserveConsumptionKeyDigest:15; HSBI_ReserveConsumptionKeyDigest:15; HSBI_RuntimeReject:15; HSBI_ValidateRuntimeDecisionContext:16 |
| 14 ProductionCallsites | NO_PRODUCTION_CALLSITE_FOUND in74 source bodies |
| 15 NormativeClauses | Docs/06:8–22; Docs/07:6–25; Docs/16:8–19; Docs/17:3–22; exact paths in FSM_COMPLETE_MATRIX |
| 16 FormulaIDs | F024/F053/F057/F062/F066 |
| 17 ErrorHandling | Первый typed return по body; FAIL/NO_OP не меняют вход; implementation exceptions не скрываются аудитом |
| 18 MissingChecksOrLimits | duplicate early NO_OP не новый spending authorization; future accepted path не доказывается одним history bool; final expected namespace берётся из current, не independent provider |
| 19 ActualIntegration | Pure DTO validator; no financial main entry integration; native NOT_RUN |
| 20 Verdict | RECONSTRUCTION_COMPARISON_PARTIAL; native/durable UNPROVEN |

R2-дополнение к сохранённой карточке (исходные20 полей и body не пересозданы):

| R2 field | Value |
|---|---|
| Function ID | Include/Runtime/HSBI_RuntimeRestartValidator.mqh:5:HSBI_ValidateRestartedRuntimeState |
| Signature | HSBI_RuntimeDecisionResult HSBI_ValidateRestartedRuntimeState(const HSBI_RestartedRuntimeState &s) |
| Actual authority | Supplied DTO/expected scalar arguments; independent actual provider внутри функции отсутствует |
| Proof boundary | Local accepted body/path; конкретные callers перечислены в исходной карточке; global financial mandatory caller не доказан |

Полное фактическое тело (цитата, не новый исполняемый код):

~~~text
{
 if(!s.snapshotPresent||s.persistedDigest=="")return HSBI_RuntimeReject(s.current,HSBI_DECISION_PERSISTENCE_REQUIRED,HSBI_RD_PERSISTENCE_REQUIRED,"HSBI-2D-RESTART");
 if(!HSBI_ValidateExecutionStateSnapshot(s.persisted,s.current.schemaVersion,s.persisted.snapshotVersion,s.current.accountLogin,s.current.symbol,s.current.magic,s.current.cycleId,s.expectedStateRevision))return HSBI_RuntimeReject(s.current,HSBI_DECISION_CONFLICT,HSBI_RD_DIGEST_MISMATCH,"HSBI-2D-RESTART-SNAPSHOT");
 if(s.current.planId!=s.expectedPlanId||s.current.stateRevision!=s.expectedStateRevision||s.current.eventId!=s.expectedEventId||s.current.actionId!=s.expectedActionId)return HSBI_RuntimeReject(s.current,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,"HSBI-2D-RESTART-ID");
 if(!s.historyUnchanged||s.sourceReused||s.payloadConflict)return HSBI_RuntimeReject(s.current,HSBI_DECISION_CONFLICT,HSBI_RD_DOUBLE_COUNT_BLOCKED,"HSBI-2D-RESTART-HISTORY");
 if(s.duplicateConsumption)return HSBI_RuntimeReject(s.current,HSBI_DECISION_NO_OP,HSBI_RD_OK,"HSBI-2D-RESTART-NOOP");
 if(s.unresolvedPending)return HSBI_RuntimeReject(s.current,HSBI_DECISION_PERSISTENCE_REQUIRED,HSBI_RD_PENDING_ACTION_CONFLICT,"HSBI-2D-RESTART-PENDING");
 if(!s.brokerMoneyConfirmed||!s.reconciliationConfirmed)return HSBI_RuntimeReject(s.current,HSBI_DECISION_RECONCILIATION_REQUIRED,HSBI_RD_RECONCILIATION_REQUIRED,"HSBI-2D-RESTART-PROOF");
 if(s.persistedResidual.identifier!=s.current.actualResidual.identifier||s.persistedResidual.ticket!=s.current.actualResidual.ticket||s.persistedResidual.actualVolume!=s.current.actualResidual.actualVolume||s.persistedResidual.role!=s.current.actualResidual.role||s.persistedResidual.direction!=s.current.actualResidual.direction)return HSBI_RuntimeReject(s.current,HSBI_DECISION_CONFLICT,HSBI_RD_POSITION_NOT_CONFIRMED,"HSBI-2D-RESTART-POS");
 if(HSBI_ReserveAllocationSourceDigest(s.persistedAllocation)!=HSBI_ReserveAllocationSourceDigest(s.current.allocationSource)||HSBI_ReserveConsumptionKeyDigest(s.persistedConsumption)!=HSBI_ReserveConsumptionKeyDigest(s.current.consumptionKey))return HSBI_RuntimeReject(s.current,HSBI_DECISION_CONFLICT,HSBI_RD_ALLOCATION_CONFLICT,"HSBI-2D-RESTART-ALLOC");
 return HSBI_ValidateRuntimeDecisionContext(s.current,s.current.accountLogin,s.current.symbol,s.current.magic,s.current.cycleId,s.current.planId,s.current.stateRevision);
}
~~~

### FUNCTION HSBI_CanAdvanceRuntimeDecision

| Field | Individual analysis |
|---|---|
| 1 FullName | HSBI_CanAdvanceRuntimeDecision |
| 2 File | Include/Runtime/HSBI_RuntimeTransactionBarrier.mqh |
| 3 DeclarationLine | 5 |
| 4 BodyRange | 6–18 |
| 5 Purpose | Проверить локальный barrier admission без исполнения |
| 6 InputParameters | const HSBI_RuntimeBarrierInput &b |
| 7 Outputs | HSBI_RuntimeDecisionResult |
| 8 Dimensions | IDs/revision; context money/volume; bool proof flags; digests |
| 9 AdmittedValues | валидный decision context и independently expected IDs/digest; actual flags подтверждены |
| 10 Preconditions | External mandatory provider должен доказать provenance и actual completion отдельно; helper generic TransactionBarrierPassed не вызывается |
| 11 Postconditions | delegates decision validation; first typed failure/NO_OP/CONFLICT; final valid result digest OR ADVANCE, не пишет state и не отправляет request |
| 12 AllLocalGuards | decision caller mandatory;completed/lastAction duplicate branch;fresh/recon;event/action binding;5position flags;money/margin/risk;persist prepared;expectedDigest nonempty/equality |
| 13 OutgoingCalls | HSBI_ValidateRuntimeDecisionContext:7; HSBI_RuntimeReject:8; HSBI_RuntimeReject:8; HSBI_RuntimeReject:9; HSBI_RuntimeReject:10; HSBI_RuntimeReject:11; HSBI_RuntimeReject:12; HSBI_RuntimeReject:13; HSBI_RuntimeReject:14; HSBI_RuntimeReject:14; HSBI_RuntimeReject:15; HSBI_RuntimeReject:16 |
| 14 ProductionCallsites | NO_PRODUCTION_CALLSITE_FOUND in74 source bodies |
| 15 NormativeClauses | Docs/06:8–22; Docs/07:6–25; Docs/16:8–19; Docs/17:3–22; exact paths in FSM_COMPLETE_MATRIX |
| 16 FormulaIDs | F024/F025/F036/F053/F057/F062/F063 |
| 17 ErrorHandling | Первый typed return по body; FAIL/NO_OP не меняют вход; implementation exceptions не скрываются аудитом |
| 18 MissingChecksOrLimits | completedOutcome здесь ранняя replay/conflict ветвь, не generic TX_COMPLETED; независимый account/symbol/magic не переданы (self context); snapshots/result persistence только flags; retryRequested unused |
| 19 ActualIntegration | Pure DTO validator; no financial main entry integration; native NOT_RUN |
| 20 Verdict | LOCAL_BARRIER_PARTIAL; not authoritative transaction commit |

R2-дополнение к сохранённой карточке (исходные20 полей и body не пересозданы):

| R2 field | Value |
|---|---|
| Function ID | Include/Runtime/HSBI_RuntimeTransactionBarrier.mqh:5:HSBI_CanAdvanceRuntimeDecision |
| Signature | HSBI_RuntimeDecisionResult HSBI_CanAdvanceRuntimeDecision(const HSBI_RuntimeBarrierInput &b) |
| Actual authority | Supplied DTO/expected scalar arguments; independent actual provider внутри функции отсутствует |
| Proof boundary | Local accepted body/path; конкретные callers перечислены в исходной карточке; global financial mandatory caller не доказан |

Полное фактическое тело (цитата, не новый исполняемый код):

~~~text
{
 HSBI_RuntimeDecisionResult admission=HSBI_ValidateRuntimeDecisionContext(b.context,b.context.accountLogin,b.context.symbol,b.context.magic,b.expectedCycleId,b.expectedPlanId,b.expectedStateRevision);if(!admission.valid)return admission;
 if(b.completedOutcome||b.lastCompletedActionId==b.expectedActionId){if(b.lastCompletedActionId==b.expectedActionId&&b.lastCompletedPayloadDigest==b.payloadDigest)return HSBI_RuntimeReject(b.context,HSBI_DECISION_NO_OP,HSBI_RD_OK,"HSBI-2D-BARRIER-NOOP");return HSBI_RuntimeReject(b.context,HSBI_DECISION_CONFLICT,HSBI_RD_PENDING_ACTION_CONFLICT,"HSBI-2D-BARRIER-COMPLETED");}
 if(!b.snapshotsFresh)return HSBI_RuntimeReject(b.context,HSBI_DECISION_STALE,HSBI_RD_STALE_SNAPSHOT,"HSBI-2D-BARRIER-FRESH");
 if(!b.reconciliationAllowed)return HSBI_RuntimeReject(b.context,HSBI_DECISION_RECONCILIATION_REQUIRED,HSBI_RD_RECONCILIATION_REQUIRED,"HSBI-2D-BARRIER-RECON");
 if(b.context.eventId<=b.expectedEventId)return HSBI_RuntimeReject(b.context,HSBI_DECISION_REJECTED,HSBI_RD_EVENT_NOT_FRESH,"HSBI-2D-BARRIER-EVENT");
 if(b.context.actionId!=b.expectedActionId)return HSBI_RuntimeReject(b.context,HSBI_DECISION_CONFLICT,HSBI_RD_ACTION_ID_MISMATCH,"HSBI-2D-BARRIER-ACTION");
 if(!b.positionRead||!b.ticketConfirmed||!b.volumeConfirmed||!b.directionConfirmed||!b.ownershipConfirmed)return HSBI_RuntimeReject(b.context,HSBI_DECISION_REJECTED,HSBI_RD_POSITION_NOT_CONFIRMED,"HSBI-2D-BARRIER-POS");
 if(!b.moneyConfirmed||!b.marginConfirmed)return HSBI_RuntimeReject(b.context,HSBI_DECISION_UNAVAILABLE,HSBI_RD_MONEY_UNAVAILABLE,"HSBI-2D-BARRIER-MONEY");if(!b.riskConfirmed)return HSBI_RuntimeReject(b.context,HSBI_DECISION_UNAVAILABLE,HSBI_RD_RISK_UNAVAILABLE,"HSBI-2D-BARRIER-RISK");
 if(!b.persistencePrepared)return HSBI_RuntimeReject(b.context,HSBI_DECISION_PERSISTENCE_REQUIRED,HSBI_RD_PERSISTENCE_REQUIRED,"HSBI-2D-BARRIER-PERSIST");
 if(b.expectedDigest==""||b.expectedDigest!=b.context.inputDigest)return HSBI_RuntimeReject(b.context,HSBI_DECISION_CONFLICT,HSBI_RD_DIGEST_MISMATCH,"HSBI-2D-BARRIER-DIGEST");
 admission.outputDigest=b.context.inputDigest+"|ADVANCE";admission.requirementId="HSBI-2D-BARRIER";return admission;
}
~~~

## R2 — индивидуальные Core функции, продолжение без замены43 карт

### FUNCTION HSBI_InitializeContext

| Field | Individual analysis |
|---|---|
| Function ID | Include/Core/HSBI_Context.mqh:8:HSBI_InitializeContext |
| Source | Include/Core/HSBI_Context.mqh:8–8 |
| Signature | void HSBI_InitializeContext(HSBI_RecoveryContext &c,const HSBI_RuntimeMode mode) |
| Inputs | HSBI_RecoveryContext &c,const HSBI_RuntimeMode mode |
| Outputs / Postconditions | ZeroMemory всего context, mode задан, current/previous DISABLED, schema versions/constants, lastReason OK |
| Domain | mode: объявленный runtime enum; context mutable |
| Preconditions | Startup/reset до reconciliation; это не восстановление финансового состояния |
| Guards | Нет входной enum validation, все поля обнуляются явно |
| Callers | HSBI_ResetContext @ Include/Core/HSBI_Context.mqh:9; OnInit @ Hybrid_Split_Big_Independent_EA.mq5:23 |
| Dependencies | NONE project functions |
| Normative contract | Docs/18:6; Docs/06:6–22 |
| Formula IDs | F024/F065 |
| Error IDs | ERR016/017 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | INITIALIZER_NOT_RECOVERY |
| Limitations / side effects | Сбрасывает память context; не использовать как миграцию/financial reset действующего ledger |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{ZeroMemory(c);c.runtimeMode=mode;c.currentState=HSBI_STATE_DISABLED;c.previousState=HSBI_STATE_DISABLED;c.schemaVersion=HSBI_SCHEMA_VERSION;c.moneyStateVersion=HSBI_MONEY_STATE_VERSION;c.lastReason=HSBI_REASON_OK;}
~~~

### FUNCTION HSBI_ResetContext

| Field | Individual analysis |
|---|---|
| Function ID | Include/Core/HSBI_Context.mqh:9:HSBI_ResetContext |
| Source | Include/Core/HSBI_Context.mqh:9–9 |
| Signature | void HSBI_ResetContext(HSBI_RecoveryContext &c) |
| Inputs | HSBI_RecoveryContext &c |
| Outputs / Postconditions | InitializeContext(c,DISABLED) |
| Domain | mutable context; no independent money authority |
| Preconditions | Только явно разрешённый reset local каркаса |
| Guards | Безусловная делегация InitializeContext |
| Callers | NO_CALLER_FOUND: all74 production source bodies, no dynamic/native proof |
| Dependencies | HSBI_InitializeContext @ Include/Core/HSBI_Context.mqh:9 |
| Normative contract | Docs/18:6; Docs/16:14–19 |
| Formula IDs | F024/F065 |
| Error IDs | ERR016/017 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | RESET_NOT_DURABLE_ROLLBACK |
| Limitations / side effects | Не reconciliation и не durable rollback; стирает локальные поля |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{HSBI_InitializeContext(c,HSBI_RUNTIME_DISABLED);}
~~~

### FUNCTION HSBI_ContextPositionValid

| Field | Individual analysis |
|---|---|
| Function ID | Include/Core/HSBI_Context.mqh:10:HSBI_ContextPositionValid |
| Source | Include/Core/HSBI_Context.mqh:10–18 |
| Signature | bool HSBI_ContextPositionValid(const HSBI_PositionDescriptor &p) |
| Inputs | const HSBI_PositionDescriptor &p |
| Outputs / Postconditions | Для NONE все ticket/identifier/volumes нулевые; active ветвь проверяет local consistency |
| Domain | p.role enum; volumes lots>=0; IDs ulong |
| Preconditions | Descriptor supplied caller; finite values/identity provenance отдельно |
| Guards | NONE branch4equalities;knownRole;2negativevolumechecks;ticket→identifier;identityRole;identityIdentifier |
| Callers | HSBI_ValidateContext @ Include/Core/HSBI_Context.mqh:45; HSBI_ValidateContext @ Include/Core/HSBI_Context.mqh:45; HSBI_ValidateContext @ Include/Core/HSBI_Context.mqh:45; HSBI_ValidateContext @ Include/Core/HSBI_Context.mqh:45; HSBI_ValidateContext @ Include/Core/HSBI_Context.mqh:45; HSBI_ValidateContext @ Include/Core/HSBI_Context.mqh:45; HSBI_ValidateContext @ Include/Core/HSBI_Context.mqh:45 |
| Dependencies | HSBI_IsKnownRole @ Include/Core/HSBI_Context.mqh:13 |
| Normative contract | Docs/02:19–34 |
| Formula IDs | F036/F053/F062 |
| Error IDs | ERR012/049 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | LOCAL_SHAPE_INCOMPLETE |
| Limitations / side effects | NaN/Infinity не исключены отрицательными сравнениями; direction/actual evidence здесь не проверяются |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{
   if(p.role==HSBI_ROLE_NONE)return p.ticket==0&&p.identifier==0&&p.actualVolume==0.0&&p.requestedVolume==0.0;
   if(!HSBI_IsKnownRole(p.role)||p.actualVolume<0.0||p.requestedVolume<0.0)return false;
   if(p.ticket>0&&p.identifier==0)return false;
   if(p.identity.role!=HSBI_ROLE_NONE&&p.identity.role!=p.role)return false;
   if(p.identity.positionIdentifier>0&&p.identity.positionIdentifier!=p.identifier)return false;
   return true;
}
~~~

### FUNCTION HSBI_ContextRolesConflict

| Field | Individual analysis |
|---|---|
| Function ID | Include/Core/HSBI_Context.mqh:19:HSBI_ContextRolesConflict |
| Source | Include/Core/HSBI_Context.mqh:19–26 |
| Signature | bool HSBI_ContextRolesConflict(const HSBI_RecoveryContext &c) |
| Inputs | const HSBI_RecoveryContext &c |
| Outputs / Postconditions | true при чужой non-NONE роли в4 проверяемых slots |
| Domain | far/core/trend/small roles enums |
| Preconditions | Caller отдельно проверяет initialBuy/initialSell/newFarCandidate |
| Guards | 4 пары role!=NONE && role!=expected |
| Callers | HSBI_ValidateContext @ Include/Core/HSBI_Context.mqh:47 |
| Dependencies | NONE project functions |
| Normative contract | Docs/02:7–16,23–30 |
| Formula IDs | F053/F062 |
| Error IDs | ERR012 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | FOUR_SLOT_FILTER_ONLY |
| Limitations / side effects | Initial/candidate slots не покрыты; false не proof глобальной role uniqueness |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{
   if(c.far.role!=HSBI_ROLE_NONE&&c.far.role!=HSBI_ROLE_FAR)return true;
   if(c.bigCore.role!=HSBI_ROLE_NONE&&c.bigCore.role!=HSBI_ROLE_BIG_CORE)return true;
   if(c.bigTrend.role!=HSBI_ROLE_NONE&&c.bigTrend.role!=HSBI_ROLE_BIG_TREND)return true;
   if(c.smallBase.role!=HSBI_ROLE_NONE&&c.smallBase.role!=HSBI_ROLE_SMALL_BASE)return true;
   return false;
}
~~~

### FUNCTION HSBI_ContextPositionInScope

| Field | Individual analysis |
|---|---|
| Function ID | Include/Core/HSBI_Context.mqh:27:HSBI_ContextPositionInScope |
| Source | Include/Core/HSBI_Context.mqh:27–32 |
| Signature | bool HSBI_ContextPositionInScope(const HSBI_RecoveryContext &c,const HSBI_PositionDescriptor &p) |
| Inputs | const HSBI_RecoveryContext &c,const HSBI_PositionDescriptor &p |
| Outputs / Postconditions | NONE→true; иначе valid identity +4 namespace equalities |
| Domain | Account long>0,Symbol string,Magic signed nonzero,Cycle ulong>0 |
| Preconditions | Context сам authoritative только при внешнем независимом origin |
| Guards | NONE shortcut;IsValidIdentity;account/symbol/magic/cycle equality |
| Callers | HSBI_ValidateContext @ Include/Core/HSBI_Context.mqh:46; HSBI_ValidateContext @ Include/Core/HSBI_Context.mqh:46; HSBI_ValidateContext @ Include/Core/HSBI_Context.mqh:46; HSBI_ValidateContext @ Include/Core/HSBI_Context.mqh:46; HSBI_ValidateContext @ Include/Core/HSBI_Context.mqh:46; HSBI_ValidateContext @ Include/Core/HSBI_Context.mqh:46; HSBI_ValidateContext @ Include/Core/HSBI_Context.mqh:46 |
| Dependencies | HSBI_IsValidIdentity @ Include/Core/HSBI_Context.mqh:30 |
| Normative contract | Docs/02:19–34 |
| Formula IDs | F053/F062 |
| Error IDs | ERR012/013/033/049 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | LOCAL_NAMESPACE_MATCH |
| Limitations / side effects | NONE не доказывает отсутствие real position; не подтверждает broker ownership и ticket |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{
   if(p.role==HSBI_ROLE_NONE)return true;
   if(!HSBI_IsValidIdentity(p.identity))return false;
   return p.identity.accountLogin==c.accountLogin&&p.identity.symbol==c.symbol&&p.identity.magic==c.magic&&p.identity.cycleId==c.cycleId;
}
~~~

### FUNCTION HSBI_ValidateContext

| Field | Individual analysis |
|---|---|
| Function ID | Include/Core/HSBI_Context.mqh:33:HSBI_ValidateContext |
| Source | Include/Core/HSBI_Context.mqh:33–59 |
| Signature | bool HSBI_ValidateContext(const HSBI_RecoveryContext &c) |
| Inputs | const HSBI_RecoveryContext &c |
| Outputs / Postconditions | false на первом перечисленном отказе; true не authorizes dispatch |
| Domain | enum modes/states,versions,IDs,7positions; money fields не валидируются |
| Preconditions | Actual/provider и financial invariants отдельно; context и enum корректно представлены |
| Guards | mode bounds+stage allowed;2statebounds;2versions;namespace;2revision0rules;recon0..5;7positionvalid;7scope;rolesconflict;4slotFarcount;closedpending;policy dispatch;compile flags |
| Callers | NO_CALLER_FOUND: all74 production source bodies, no dynamic/native proof |
| Dependencies | HSBI_IsRuntimeModeAllowedAtStage1 @ Include/Core/HSBI_Context.mqh:36; HSBI_ContextPositionValid @ Include/Core/HSBI_Context.mqh:45; HSBI_ContextPositionValid @ Include/Core/HSBI_Context.mqh:45; HSBI_ContextPositionValid @ Include/Core/HSBI_Context.mqh:45; HSBI_ContextPositionValid @ Include/Core/HSBI_Context.mqh:45; HSBI_ContextPositionValid @ Include/Core/HSBI_Context.mqh:45; HSBI_ContextPositionValid @ Include/Core/HSBI_Context.mqh:45; HSBI_ContextPositionValid @ Include/Core/HSBI_Context.mqh:45; HSBI_ContextPositionInScope @ Include/Core/HSBI_Context.mqh:46; HSBI_ContextPositionInScope @ Include/Core/HSBI_Context.mqh:46; HSBI_ContextPositionInScope @ Include/Core/HSBI_Context.mqh:46; HSBI_ContextPositionInScope @ Include/Core/HSBI_Context.mqh:46; HSBI_ContextPositionInScope @ Include/Core/HSBI_Context.mqh:46; HSBI_ContextPositionInScope @ Include/Core/HSBI_Context.mqh:46; HSBI_ContextPositionInScope @ Include/Core/HSBI_Context.mqh:46; HSBI_ContextRolesConflict @ Include/Core/HSBI_Context.mqh:47; HSBI_BuildRuntimePolicy @ Include/Core/HSBI_Context.mqh:55 |
| Normative contract | Docs/02:23–36; Docs/06:6–22; Docs/18:28–30 |
| Formula IDs | F024/F036/F053/F065 |
| Error IDs | ERR011/012/016/017/049 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | COMPOSITE_CONTEXT_PARTIAL |
| Limitations / side effects | Far count/slot roles не полные7slots; money/revisions/global source registry/finite/durable proofs отсутствуют |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{
   if(c.runtimeMode<HSBI_RUNTIME_DISABLED||c.runtimeMode>HSBI_RUNTIME_REAL_LIMITED)return false;
   if(!HSBI_IsRuntimeModeAllowedAtStage1(c.runtimeMode))return false;
   if(c.currentState<HSBI_STATE_DISABLED||c.currentState>HSBI_STATE_CYCLE_CLOSED)return false;
   if(c.previousState<HSBI_STATE_DISABLED||c.previousState>HSBI_STATE_CYCLE_CLOSED)return false;
   if(c.schemaVersion!=HSBI_SCHEMA_VERSION)return false;
   if(c.moneyStateVersion!=HSBI_MONEY_STATE_VERSION)return false;
   if(c.accountLogin<=0||c.symbol==""||c.magic==0||c.cycleId==0)return false;
   if(c.stateRevision==0&&c.previousState!=c.currentState)return false;
   if(c.stateRevision==0&&c.currentState!=HSBI_STATE_DISABLED&&c.currentState!=HSBI_STATE_IDLE)return false;
   if(c.reconciliationStatus<0||c.reconciliationStatus>5)return false;
   if(!HSBI_ContextPositionValid(c.far)||!HSBI_ContextPositionValid(c.bigCore)||!HSBI_ContextPositionValid(c.bigTrend)||!HSBI_ContextPositionValid(c.smallBase)||!HSBI_ContextPositionValid(c.initialBuy)||!HSBI_ContextPositionValid(c.initialSell)||!HSBI_ContextPositionValid(c.newFarCandidate))return false;
   if(!HSBI_ContextPositionInScope(c,c.far)||!HSBI_ContextPositionInScope(c,c.bigCore)||!HSBI_ContextPositionInScope(c,c.bigTrend)||!HSBI_ContextPositionInScope(c,c.smallBase)||!HSBI_ContextPositionInScope(c,c.initialBuy)||!HSBI_ContextPositionInScope(c,c.initialSell)||!HSBI_ContextPositionInScope(c,c.newFarCandidate))return false;
   if(HSBI_ContextRolesConflict(c))return false;
   int farCount=0;
   if(c.far.role==HSBI_ROLE_FAR)farCount++;
   if(c.bigCore.role==HSBI_ROLE_FAR)farCount++;
   if(c.bigTrend.role==HSBI_ROLE_FAR)farCount++;
   if(c.smallBase.role==HSBI_ROLE_FAR)farCount++;
   if(farCount>1)return false;
   if(c.currentState==HSBI_STATE_CYCLE_CLOSED&&c.pendingActionId!=0)return false;
   HSBI_RuntimePolicy policy=HSBI_BuildRuntimePolicy(c.runtimeMode);
   if(policy.brokerDispatchAllowed)return false;
   if(HSBI_TRADING_IMPLEMENTED||HSBI_REAL_TRADING_ALLOWED)return false;
   return true;
}
~~~

### FUNCTION HSBI_IsValidIdentity

| Field | Individual analysis |
|---|---|
| Function ID | Include/Core/HSBI_Identifiers.mqh:6:HSBI_IsValidIdentity |
| Source | Include/Core/HSBI_Identifiers.mqh:6–6 |
| Signature | bool HSBI_IsValidIdentity(const HSBI_Identity &x) |
| Inputs | const HSBI_Identity &x |
| Outputs / Postconditions | bool конъюнкции5 условий |
| Domain | account>0,symbol nonempty,magic!=0,cycle>0,role!=NONE |
| Preconditions | Caller подтверждает known role и broker/EA-origin ownership |
| Guards | 5 named scalar predicates |
| Callers | HSBI_ContextPositionInScope @ Include/Core/HSBI_Context.mqh:30; HSBI_CompareReconciliation @ Include/Persistence/HSBI_ReconciliationTypes.mqh:7; HSBI_ValidateCandidatePlan @ Include/Planning/HSBI_CandidatePlan.mqh:6 |
| Dependencies | NONE project functions |
| Normative contract | Docs/02:19–34 |
| Formula IDs | F053/F062 |
| Error IDs | ERR012/013/049 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | SHAPE_ONLY_NOT_PROVENANCE |
| Limitations / side effects | role!=NONE принимает unknown enum;positionIdentifier не требуется этой shape функцией |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{return x.accountLogin>0 && x.symbol!="" && x.magic!=0 && x.cycleId>0 && x.role!=HSBI_ROLE_NONE;}
~~~

### FUNCTION HSBI_SameCycle

| Field | Individual analysis |
|---|---|
| Function ID | Include/Core/HSBI_Identifiers.mqh:7:HSBI_SameCycle |
| Source | Include/Core/HSBI_Identifiers.mqh:7–7 |
| Signature | bool HSBI_SameCycle(const HSBI_Identity &a,const HSBI_Identity &b) |
| Inputs | const HSBI_Identity &a,const HSBI_Identity &b |
| Outputs / Postconditions | true iff account/symbol/magic/cycle равны |
| Domain | 4 namespace fields, без money units |
| Preconditions | Два объекта валидированы caller и expected независим |
| Guards | 4 exact equalities |
| Callers | HSBI_SamePositionOwner @ Include/Core/HSBI_Identifiers.mqh:8 |
| Dependencies | NONE project functions |
| Normative contract | Docs/02:19–34 |
| Formula IDs | F053/F062 |
| Error IDs | ERR013/033 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | LOCAL_EQUALITY_ONLY |
| Limitations / side effects | Два malformed/copy objects тоже могут равняться; это не validator/source proof |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{return a.accountLogin==b.accountLogin && a.symbol==b.symbol && a.magic==b.magic && a.cycleId==b.cycleId;}
~~~

### FUNCTION HSBI_SamePositionOwner

| Field | Individual analysis |
|---|---|
| Function ID | Include/Core/HSBI_Identifiers.mqh:8:HSBI_SamePositionOwner |
| Source | Include/Core/HSBI_Identifiers.mqh:8–8 |
| Signature | bool HSBI_SamePositionOwner(const HSBI_Identity &a,const HSBI_Identity &b) |
| Inputs | const HSBI_Identity &a,const HSBI_Identity &b |
| Outputs / Postconditions | SameCycle && positionIdentifier equal && role equal |
| Domain | namespace +positionIdentifier ulong+role enum |
| Preconditions | Validity/independent expected identity до equality |
| Guards | SameCycle;2equalities |
| Callers | HSBI_EvaluateOwnership @ Include/Execution/HSBI_OwnershipGuardTypes.mqh:8; HSBI_TicketMatchesObservation @ Include/Execution/HSBI_OwnershipGuardTypes.mqh:11; HSBI_ValidateNewFarSource @ Include/Planning/HSBI_NewFarSolver.mqh:64 |
| Dependencies | HSBI_SameCycle @ Include/Core/HSBI_Identifiers.mqh:8 |
| Normative contract | Docs/02:19–30 |
| Formula IDs | F053/F062 |
| Error IDs | ERR012/013 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | LOCAL_POSITION_IDENTITY_EQUALITY |
| Limitations / side effects | Нулевые identifiers могут совпасть; ticket/direction/volume не в scope equality |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{return HSBI_SameCycle(a,b)&&a.positionIdentifier==b.positionIdentifier&&a.role==b.role;}
~~~

### FUNCTION HSBI_SameSymbolScope

| Field | Individual analysis |
|---|---|
| Function ID | Include/Core/HSBI_Identifiers.mqh:9:HSBI_SameSymbolScope |
| Source | Include/Core/HSBI_Identifiers.mqh:9–9 |
| Signature | bool HSBI_SameSymbolScope(const HSBI_Identity &a,const HSBI_Identity &b) |
| Inputs | const HSBI_Identity &a,const HSBI_Identity &b |
| Outputs / Postconditions | true iff3equalities |
| Domain | namespace3 fields; не cycle/source uniqueness |
| Preconditions | Caller явно просит symbol scope, а не cycle ownership |
| Guards | account/symbol/magic equality |
| Callers | NO_CALLER_FOUND: all74 production source bodies, no dynamic/native proof |
| Dependencies | NONE project functions |
| Normative contract | Docs/02:19–26 |
| Formula IDs | F053/F062 |
| Error IDs | ERR013/033 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | SYMBOL_SCOPE_ONLY |
| Limitations / side effects | Cycle/position/role intentionally absent: нельзя использовать как полный ownership |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{return a.accountLogin==b.accountLogin&&a.symbol==b.symbol&&a.magic==b.magic;}
~~~

### FUNCTION HSBI_UlongToString

| Field | Individual analysis |
|---|---|
| Function ID | Include/Core/HSBI_Identifiers.mqh:10:HSBI_UlongToString |
| Source | Include/Core/HSBI_Identifiers.mqh:10–22 |
| Signature | string HSBI_UlongToString(const ulong value) |
| Inputs | const ulong value |
| Outputs / Postconditions | 0→строка0; иначе repeated quotient/remainder builds digits без double |
| Domain | ulong0..ULONG_MAX; digit int0..9 |
| Preconditions | NOT_APPLICABLE external authority: pure numeric formatter |
| Guards | zero case;while remaining>0;remainder%10;division10 |
| Callers | HSBI_SerializeIdentity @ Include/Core/HSBI_Identifiers.mqh:23; HSBI_SerializeIdentity @ Include/Core/HSBI_Identifiers.mqh:23; HSBI_BuildPanelModel @ Include/Diagnostics/HSBI_PanelModel.mqh:5; HSBI_SerializeActionIds @ Include/Execution/HSBI_ActionTypes.mqh:7; HSBI_SerializeActionIds @ Include/Execution/HSBI_ActionTypes.mqh:7; HSBI_SerializeActionIds @ Include/Execution/HSBI_ActionTypes.mqh:7; HSBI_SerializeActionIds @ Include/Execution/HSBI_ActionTypes.mqh:7; HSBI_SerializeActionIds @ Include/Execution/HSBI_ActionTypes.mqh:7; HSBI_SerializeActionIds @ Include/Execution/HSBI_ActionTypes.mqh:7; HSBI_SerializeActionIds @ Include/Execution/HSBI_ActionTypes.mqh:7; HSBI_SerializeEventIds @ Include/Execution/HSBI_EventTypes.mqh:7; HSBI_SerializeEventIds @ Include/Execution/HSBI_EventTypes.mqh:7; HSBI_SerializeEventIds @ Include/Execution/HSBI_EventTypes.mqh:7; HSBI_SerializeEventIds @ Include/Execution/HSBI_EventTypes.mqh:7; HSBI_SerializeEventIds @ Include/Execution/HSBI_EventTypes.mqh:7; HSBI_ExecutionIntentDigest @ Include/Execution/HSBI_ExecutionIntent.mqh:17; HSBI_ExecutionIntentDigest @ Include/Execution/HSBI_ExecutionIntent.mqh:17; HSBI_ExecutionIntentDigest @ Include/Execution/HSBI_ExecutionIntent.mqh:18; HSBI_ExecutionIntentDigest @ Include/Execution/HSBI_ExecutionIntent.mqh:18; HSBI_ExecutionIntentDigest @ Include/Execution/HSBI_ExecutionIntent.mqh:20; HSBI_ExecutionIntentDigest @ Include/Execution/HSBI_ExecutionIntent.mqh:21; HSBI_ExecutionIntentDigest @ Include/Execution/HSBI_ExecutionIntent.mqh:21; HSBI_ExecutionIntentDigest @ Include/Execution/HSBI_ExecutionIntent.mqh:21; HSBI_ExecutionIntentDigest @ Include/Execution/HSBI_ExecutionIntent.mqh:22; HSBI_ExecutionIntentDigest @ Include/Execution/HSBI_ExecutionIntent.mqh:22; HSBI_ExecutionIntentDigest @ Include/Execution/HSBI_ExecutionIntent.mqh:22; HSBI_ExecutionIntentDigest @ Include/Execution/HSBI_ExecutionIntent.mqh:23; HSBI_ExecutionIntentDigest @ Include/Execution/HSBI_ExecutionIntent.mqh:23; HSBI_IntentIdempotencyKey @ Include/Execution/HSBI_ExecutionIntent.mqh:42; HSBI_IntentIdempotencyKey @ Include/Execution/HSBI_ExecutionIntent.mqh:42; HSBI_IntentIdempotencyKey @ Include/Execution/HSBI_ExecutionIntent.mqh:42; HSBI_ExternalOutcomeDigest @ Include/Execution/HSBI_ExternalOutcome.mqh:14; HSBI_ExternalOutcomeDigest @ Include/Execution/HSBI_ExternalOutcome.mqh:14; HSBI_ExternalOutcomeDigest @ Include/Execution/HSBI_ExternalOutcome.mqh:14; HSBI_ExternalOutcomeDigest @ Include/Execution/HSBI_ExternalOutcome.mqh:15; HSBI_ExternalOutcomeDigest @ Include/Execution/HSBI_ExternalOutcome.mqh:15; HSBI_ExternalOutcomeDigest @ Include/Execution/HSBI_ExternalOutcome.mqh:17; HSBI_ExternalOutcomeDigest @ Include/Execution/HSBI_ExternalOutcome.mqh:17; HSBI_ExternalOutcomeDigest @ Include/Execution/HSBI_ExternalOutcome.mqh:17; HSBI_AllocationPolicyDigest @ Include/Money/HSBI_AllocationPolicyTypes.mqh:29; HSBI_AllocationPolicyDigest @ Include/Money/HSBI_AllocationPolicyTypes.mqh:29; HSBI_BuildSourceDealKey @ Include/Money/HSBI_EconomicLedgerTypes.mqh:7; HSBI_BuildSourceDealKey @ Include/Money/HSBI_EconomicLedgerTypes.mqh:7; HSBI_MoneyProofIdentityDigest @ Include/Money/HSBI_MoneyProofIdentity.mqh:25; HSBI_MoneyProofIdentityDigest @ Include/Money/HSBI_MoneyProofIdentity.mqh:26; HSBI_MoneyProofIdentityDigest @ Include/Money/HSBI_MoneyProofIdentity.mqh:27; HSBI_MoneyProofIdentityDigest @ Include/Money/HSBI_MoneyProofIdentity.mqh:27; HSBI_MoneyProofIdentityDigest @ Include/Money/HSBI_MoneyProofIdentity.mqh:27; HSBI_MoneyProofIdentityDigest @ Include/Money/HSBI_MoneyProofIdentity.mqh:28; HSBI_MoneyProofIdentityDigest @ Include/Money/HSBI_MoneyProofIdentity.mqh:28; HSBI_ReserveAllocationSourceDigest @ Include/Money/HSBI_ReserveAllocationTypes.mqh:32; HSBI_ReserveAllocationSourceDigest @ Include/Money/HSBI_ReserveAllocationTypes.mqh:32; HSBI_ReserveAllocationSourceDigest @ Include/Money/HSBI_ReserveAllocationTypes.mqh:32; HSBI_ReserveConsumptionKeyDigest @ Include/Money/HSBI_ReserveAllocationTypes.mqh:34; HSBI_ReserveConsumptionKeyDigest @ Include/Money/HSBI_ReserveAllocationTypes.mqh:34; HSBI_ReserveConsumptionKeyDigest @ Include/Money/HSBI_ReserveAllocationTypes.mqh:34; HSBI_ExecutionJournalEntryDigest @ Include/Persistence/HSBI_ExecutionJournal.mqh:13; HSBI_ExecutionJournalEntryDigest @ Include/Persistence/HSBI_ExecutionJournal.mqh:13; HSBI_ExecutionJournalEntryDigest @ Include/Persistence/HSBI_ExecutionJournal.mqh:13; HSBI_ExecutionJournalEntryDigest @ Include/Persistence/HSBI_ExecutionJournal.mqh:14; HSBI_ExecutionJournalEntryDigest @ Include/Persistence/HSBI_ExecutionJournal.mqh:14; HSBI_ExecutionJournalEntryDigest @ Include/Persistence/HSBI_ExecutionJournal.mqh:14; HSBI_ExecutionJournalEntryDigest @ Include/Persistence/HSBI_ExecutionJournal.mqh:15; HSBI_ExecutionStateSnapshotDigest @ Include/Persistence/HSBI_ExecutionStateSnapshot.mqh:14; HSBI_ExecutionStateSnapshotDigest @ Include/Persistence/HSBI_ExecutionStateSnapshot.mqh:14; HSBI_ExecutionStateSnapshotDigest @ Include/Persistence/HSBI_ExecutionStateSnapshot.mqh:15; HSBI_ExecutionStateSnapshotDigest @ Include/Persistence/HSBI_ExecutionStateSnapshot.mqh:15; HSBI_SerializeJournalIds @ Include/Persistence/HSBI_JournalTypes.mqh:7; HSBI_SerializeJournalIds @ Include/Persistence/HSBI_JournalTypes.mqh:7; HSBI_SerializeJournalIds @ Include/Persistence/HSBI_JournalTypes.mqh:7; HSBI_TestDigest @ Include/Persistence/HSBI_SnapshotTypes.mqh:9; HSBI_TestDigest @ Include/Persistence/HSBI_SnapshotTypes.mqh:9; HSBI_SerializeSnapshotIds @ Include/Persistence/HSBI_SnapshotTypes.mqh:10; HSBI_SerializeSnapshotIds @ Include/Persistence/HSBI_SnapshotTypes.mqh:10; HSBI_CandidatePlanFingerprint @ Include/Planning/HSBI_CandidatePlan.mqh:7; HSBI_CandidatePlanFingerprint @ Include/Planning/HSBI_CandidatePlan.mqh:7; HSBI_CandidatePlanFingerprint @ Include/Planning/HSBI_CandidatePlan.mqh:7; HSBI_CandidatePlanFingerprint @ Include/Planning/HSBI_CandidatePlan.mqh:7; HSBI_FutureSmallLevelDigest @ Include/Planning/HSBI_FutureSmallSolver.mqh:101; HSBI_FutureSmallLevelDigest @ Include/Planning/HSBI_FutureSmallSolver.mqh:101; HSBI_FutureSmallLevelDigest @ Include/Planning/HSBI_FutureSmallSolver.mqh:101; HSBI_FutureSmallLevelDigest @ Include/Planning/HSBI_FutureSmallSolver.mqh:102; HSBI_FutureSmallLevelDigest @ Include/Planning/HSBI_FutureSmallSolver.mqh:102; HSBI_FutureSmallProofDigest @ Include/Planning/HSBI_FutureSmallSolver.mqh:108; HSBI_FutureSmallProofDigest @ Include/Planning/HSBI_FutureSmallSolver.mqh:108; HSBI_FutureSmallTemplateDigest @ Include/Planning/HSBI_NewFarSolver.mqh:39; HSBI_FutureSmallTemplateDigest @ Include/Planning/HSBI_NewFarSolver.mqh:41; HSBI_FutureSmallTemplateDigest @ Include/Planning/HSBI_NewFarSolver.mqh:41; HSBI_FutureSmallTemplateDigest @ Include/Planning/HSBI_NewFarSolver.mqh:42; HSBI_FutureSmallTemplateDigest @ Include/Planning/HSBI_NewFarSolver.mqh:42; HSBI_FutureSmallTemplateDigest @ Include/Planning/HSBI_NewFarSolver.mqh:43; HSBI_FutureSmallTemplateDigest @ Include/Planning/HSBI_NewFarSolver.mqh:44; HSBI_NewFarInputDigest @ Include/Planning/HSBI_NewFarSolver.mqh:50; HSBI_NewFarInputDigest @ Include/Planning/HSBI_NewFarSolver.mqh:50; HSBI_NewFarInputDigest @ Include/Planning/HSBI_NewFarSolver.mqh:50; HSBI_NewFarInputDigest @ Include/Planning/HSBI_NewFarSolver.mqh:51; HSBI_NewFarInputDigest @ Include/Planning/HSBI_NewFarSolver.mqh:52; HSBI_NewFarInputDigest @ Include/Planning/HSBI_NewFarSolver.mqh:55; HSBI_NewFarInputDigest @ Include/Planning/HSBI_NewFarSolver.mqh:57; HSBI_NewFarInputDigest @ Include/Planning/HSBI_NewFarSolver.mqh:57; HSBI_RuntimeDecisionContextDigest @ Include/Runtime/HSBI_RuntimeDecisionTypes.mqh:17; HSBI_RuntimeDecisionContextDigest @ Include/Runtime/HSBI_RuntimeDecisionTypes.mqh:17; HSBI_RuntimeDecisionContextDigest @ Include/Runtime/HSBI_RuntimeDecisionTypes.mqh:17; HSBI_RuntimeDecisionContextDigest @ Include/Runtime/HSBI_RuntimeDecisionTypes.mqh:17; HSBI_RuntimeDecisionContextDigest @ Include/Runtime/HSBI_RuntimeDecisionTypes.mqh:17; HSBI_RuntimeDecisionContextDigest @ Include/Runtime/HSBI_RuntimeDecisionTypes.mqh:17; HSBI_RuntimeDecisionContextDigest @ Include/Runtime/HSBI_RuntimeDecisionTypes.mqh:17 |
| Dependencies | NONE project functions |
| Normative contract | CONTRACT_NOT_FOUND для exact formatter; архитектурный owner Docs/18:6 |
| Formula IDs | F041/F042/F060 |
| Error IDs | ERR003/029/040 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | STATIC_FORMATTER_NATIVE_NOT_RUN |
| Limitations / side effects | Алгоритм сохраняет unsigned input; native/compiler behaviour не выполнялось; не versioned full codec |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{
   if(value==0)return "0";
   ulong remaining=value;
   string result="";
   while(remaining>0)
   {
      const int digit=(int)(remaining%10);
      result=StringSubstr("0123456789",digit,1)+result;
      remaining/=10;
   }
   return result;
}
~~~

### FUNCTION HSBI_SerializeIdentity

| Field | Individual analysis |
|---|---|
| Function ID | Include/Core/HSBI_Identifiers.mqh:23:HSBI_SerializeIdentity |
| Source | Include/Core/HSBI_Identifiers.mqh:23–23 |
| Signature | string HSBI_SerializeIdentity(const HSBI_Identity &x) |
| Inputs | const HSBI_Identity &x |
| Outputs / Postconditions | 6 fields в fixed textual order; const inputs unchanged |
| Domain | long/ulong IDs; symbol text; role integer |
| Preconditions | Validity и escaping/domain обеспечиваются caller |
| Guards | Нет shape guards; delegates unsigned formatter |
| Callers | NO_CALLER_FOUND: all74 production source bodies, no dynamic/native proof |
| Dependencies | HSBI_UlongToString @ Include/Core/HSBI_Identifiers.mqh:23; HSBI_UlongToString @ Include/Core/HSBI_Identifiers.mqh:23 |
| Normative contract | Docs/02:19–21; NUM-CODEC PROPOSED |
| Formula IDs | F042/F053/F060 |
| Error IDs | ERR003/033/040 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | TEXT_REPRESENTATION_NOT_CANONICAL_CODEC |
| Limitations / side effects | Delimiter escape/UTF8/codec version/full broker source namespace отсутствуют; не authoritative codec |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{return LongToString(x.accountLogin)+"|"+x.symbol+"|"+LongToString(x.magic)+"|"+HSBI_UlongToString(x.cycleId)+"|"+HSBI_UlongToString(x.positionIdentifier)+"|"+IntegerToString((int)x.role);}
~~~

### FUNCTION HSBI_ExactlyOneFarOrZero

| Field | Individual analysis |
|---|---|
| Function ID | Include/Core/HSBI_Invariants.mqh:5:HSBI_ExactlyOneFarOrZero |
| Source | Include/Core/HSBI_Invariants.mqh:5–5 |
| Signature | HSBI_ValidationResult HSBI_ExactlyOneFarOrZero(const HSBI_RecoveryContext &c) |
| Inputs | const HSBI_RecoveryContext &c |
| Outputs / Postconditions | passed=(n<=1), details count, duplicateFar reason при>1 |
| Domain | role count integer0..4 |
| Preconditions | Caller предоставляет полный relevant registry; сейчас scope только4slots |
| Guards | CountFarRoles; n<=1 |
| Callers | HSBI_NoDualTail @ Include/Core/HSBI_Invariants.mqh:6 |
| Dependencies | HSBI_CountFarRoles @ Include/Core/HSBI_Invariants.mqh:5; HSBI_Result @ Include/Core/HSBI_Invariants.mqh:5 |
| Normative contract | Docs/02:25,30 |
| Formula IDs | F053/F062 |
| Error IDs | ERR012 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | INCOMPLETE_GLOBAL_ROLE_GUARD |
| Limitations / side effects | Не учитывает initial/candidate slots и NEW_FAR candidate; не count actual unique positions |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{int n=HSBI_CountFarRoles(c.far,c.bigCore,c.bigTrend,c.smallBase);return HSBI_Result(n<=1,n<=1?HSBI_REASON_OK:HSBI_REASON_DUPLICATE_FAR,"HSBI-ID-010",IntegerToString(n));}
~~~

### FUNCTION HSBI_NoDualTail

| Field | Individual analysis |
|---|---|
| Function ID | Include/Core/HSBI_Invariants.mqh:6:HSBI_NoDualTail |
| Source | Include/Core/HSBI_Invariants.mqh:6–6 |
| Signature | HSBI_ValidationResult HSBI_NoDualTail(const HSBI_RecoveryContext &c) |
| Inputs | const HSBI_RecoveryContext &c |
| Outputs / Postconditions | Возвращает delegated validation result |
| Domain | context roles |
| Preconditions | Тот же scope что ExactlyOneFarOrZero |
| Guards | Безусловный ExactlyOneFarOrZero |
| Callers | NO_CALLER_FOUND: all74 production source bodies, no dynamic/native proof |
| Dependencies | HSBI_ExactlyOneFarOrZero @ Include/Core/HSBI_Invariants.mqh:6 |
| Normative contract | Docs/02:25,30 |
| Formula IDs | F053/F062 |
| Error IDs | ERR012 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | ALIAS_SAME_INCOMPLETE_SCOPE |
| Limitations / side effects | Никакой дополнительной защиты относительно delegated helper |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{return HSBI_ExactlyOneFarOrZero(c);}
~~~

### FUNCTION HSBI_NoUnknownRole

| Field | Individual analysis |
|---|---|
| Function ID | Include/Core/HSBI_Invariants.mqh:7:HSBI_NoUnknownRole |
| Source | Include/Core/HSBI_Invariants.mqh:7–7 |
| Signature | HSBI_ValidationResult HSBI_NoUnknownRole(const HSBI_PositionDescriptor &p) |
| Inputs | const HSBI_PositionDescriptor &p |
| Outputs / Postconditions | passed knownRole OR  OR NONE |
| Domain | HSBI_Role enum |
| Preconditions | NONE допустим для пустого DTO slot |
| Guards | KnownRole range OR NONE; typed reason |
| Callers | NO_CALLER_FOUND: all74 production source bodies, no dynamic/native proof |
| Dependencies | HSBI_Result @ Include/Core/HSBI_Invariants.mqh:7; HSBI_IsKnownRole @ Include/Core/HSBI_Invariants.mqh:7; HSBI_IsKnownRole @ Include/Core/HSBI_Invariants.mqh:7 |
| Normative contract | Docs/02:7–16,30 |
| Formula IDs | F053/F062 |
| Error IDs | ERR012/049 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | LOCAL_CLOSED_ROLE_DOMAIN |
| Limitations / side effects | Не подтверждает slot-role ownership или descriptor validity |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{return HSBI_Result(HSBI_IsKnownRole(p.role)||p.role==HSBI_ROLE_NONE,HSBI_IsKnownRole(p.role)||p.role==HSBI_ROLE_NONE?HSBI_REASON_OK:HSBI_REASON_UNKNOWN_ROLE,"HSBI-ID-010","");}
~~~

### FUNCTION HSBI_ContextIdentityComplete

| Field | Individual analysis |
|---|---|
| Function ID | Include/Core/HSBI_Invariants.mqh:8:HSBI_ContextIdentityComplete |
| Source | Include/Core/HSBI_Invariants.mqh:8–8 |
| Signature | HSBI_ValidationResult HSBI_ContextIdentityComplete(const HSBI_RecoveryContext &c) |
| Inputs | const HSBI_RecoveryContext &c |
| Outputs / Postconditions | passed3conditions |
| Domain | account>0,symbol nonempty,magic!=0 |
| Preconditions | Caller не должен считать этот helper полной cycle identity |
| Guards | 3scalar guards |
| Callers | NO_CALLER_FOUND: all74 production source bodies, no dynamic/native proof |
| Dependencies | HSBI_Result @ Include/Core/HSBI_Invariants.mqh:8 |
| Normative contract | Docs/02:19–30 |
| Formula IDs | F053/F062 |
| Error IDs | ERR012/013 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | PARTIAL_IDENTITY_SHAPE |
| Limitations / side effects | CycleID/position/role отсутствуют; scope имени complete ограничен тремя полями |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{bool ok=c.accountLogin>0&&c.symbol!=""&&c.magic!=0;return HSBI_Result(ok,ok?HSBI_REASON_OK:HSBI_REASON_INVALID_IDENTITY,"HSBI-ID-010","");}
~~~

### FUNCTION HSBI_StateRevisionMonotonic

| Field | Individual analysis |
|---|---|
| Function ID | Include/Core/HSBI_Invariants.mqh:9:HSBI_StateRevisionMonotonic |
| Source | Include/Core/HSBI_Invariants.mqh:9–9 |
| Signature | HSBI_ValidationResult HSBI_StateRevisionMonotonic(const ulong before,const ulong after) |
| Inputs | const ulong before,const ulong after |
| Outputs / Postconditions | passed after>=before |
| Domain | ulong before/after |
| Preconditions | Не строгий increment, не atomic CAS |
| Guards | unsigned >= comparison |
| Callers | NO_CALLER_FOUND: all74 production source bodies, no dynamic/native proof |
| Dependencies | HSBI_Result @ Include/Core/HSBI_Invariants.mqh:9 |
| Normative contract | Docs/06:21; Docs/07:9 |
| Formula IDs | F065 |
| Error IDs | ERR025 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | NONDECREASING_ONLY |
| Limitations / side effects | Equal revisions допустимы по nondecreasing definition; не предотвращает wrap при source increment |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{bool ok=after>=before;return HSBI_Result(ok,ok?HSBI_REASON_OK:HSBI_REASON_INTERNAL_INVARIANT_FAILED,"HSBI-FSM-002","");}
~~~

### FUNCTION HSBI_NoPendingActionConflict

| Field | Individual analysis |
|---|---|
| Function ID | Include/Core/HSBI_Invariants.mqh:10:HSBI_NoPendingActionConflict |
| Source | Include/Core/HSBI_Invariants.mqh:10–10 |
| Signature | HSBI_ValidationResult HSBI_NoPendingActionConflict(const HSBI_RecoveryContext &c) |
| Inputs | const HSBI_RecoveryContext &c |
| Outputs / Postconditions | false iff pendingAction>0 && CYCLE_CLOSED |
| Domain | pendingActionId ulong; current state enum |
| Preconditions | Другие state/action correlations не scope этого helper |
| Guards | single forbidden conjunction |
| Callers | NO_CALLER_FOUND: all74 production source bodies, no dynamic/native proof |
| Dependencies | HSBI_Result @ Include/Core/HSBI_Invariants.mqh:10 |
| Normative contract | Docs/06:6–22; Docs/07:24 |
| Formula IDs | F024/F065 |
| Error IDs | ERR016/049 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | ONE_LOCAL_STATE_INVARIANT |
| Limitations / side effects | Нет проверки всех lifecycle states/unknown enum/action authority |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{bool ok=!(c.pendingActionId>0&&c.currentState==HSBI_STATE_CYCLE_CLOSED);return HSBI_Result(ok,ok?HSBI_REASON_OK:HSBI_REASON_PENDING_ACTION,"HSBI-TX-006","");}
~~~

### FUNCTION HSBI_NoFinalReserveForPartialFar

| Field | Individual analysis |
|---|---|
| Function ID | Include/Core/HSBI_Invariants.mqh:11:HSBI_NoFinalReserveForPartialFar |
| Source | Include/Core/HSBI_Invariants.mqh:11–11 |
| Signature | HSBI_ValidationResult HSBI_NoFinalReserveForPartialFar(const HSBI_MoneyBucket source) |
| Inputs | const HSBI_MoneyBucket source |
| Outputs / Postconditions | passed iff source!=FINAL_RESERVE |
| Domain | MoneyBucket enum |
| Preconditions | Caller уже проверил bucket domain и consumer purpose |
| Guards | single != comparison |
| Callers | NO_CALLER_FOUND: all74 production source bodies, no dynamic/native proof |
| Dependencies | HSBI_Result @ Include/Core/HSBI_Invariants.mqh:11 |
| Normative contract | Docs/11_PARTIAL_FAR_SPECIFICATION_RU.md:5–7; Docs/06:22 |
| Formula IDs | F019 |
| Error IDs | ERR007/049 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | PURPOSE_FILTER_NOT_SOURCE_AUTHORIZATION |
| Limitations / side effects | Unknown enum также !=FinalReserve; purpose/amount/owner authority отсутствуют |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{bool ok=source!=HSBI_BUCKET_FINAL_RESERVE;return HSBI_Result(ok,ok?HSBI_REASON_OK:HSBI_REASON_FINAL_RESERVE_FOR_PARTIAL_FAR,"HSBI-PF-001","");}
~~~

### FUNCTION HSBI_AllocationConservation

| Field | Individual analysis |
|---|---|
| Function ID | Include/Core/HSBI_Invariants.mqh:12:HSBI_AllocationConservation |
| Source | Include/Core/HSBI_Invariants.mqh:12–12 |
| Signature | HSBI_ValidationResult HSBI_AllocationConservation(const double allocated,const double available) |
| Inputs | const double allocated,const double available |
| Outputs / Postconditions | passed iff allocated<=available+1e-7 |
| Domain | allocated/available samecurrency finite money |
| Preconditions | Nonnegative partition/complete source authority вне helper |
| Guards | single upper bound |
| Callers | NO_CALLER_FOUND: all74 production source bodies, no dynamic/native proof |
| Dependencies | HSBI_Result @ Include/Core/HSBI_Invariants.mqh:12 |
| Normative contract | Docs/08:12–24 |
| Formula IDs | F012/F013/F064 |
| Error IDs | ERR005/006 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | SCALAR_BOUND_NOT_CONSERVATION_PROOF |
| Limitations / side effects | Отрицательные allocated/available, Infinity и полный bucket vector не проверяются |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{bool ok=allocated<=available+0.0000001;return HSBI_Result(ok,ok?HSBI_REASON_OK:HSBI_REASON_LEDGER_CONSERVATION_FAILED,"HSBI-MONEY-014","");}
~~~

### FUNCTION HSBI_RealTradingForbiddenAtHSB1

| Field | Individual analysis |
|---|---|
| Function ID | Include/Core/HSBI_Invariants.mqh:13:HSBI_RealTradingForbiddenAtHSB1 |
| Source | Include/Core/HSBI_Invariants.mqh:13–13 |
| Signature | HSBI_ValidationResult HSBI_RealTradingForbiddenAtHSB1() |
| Inputs | NONE |
| Outputs / Postconditions | passed iff !REAL_TRADING_ALLOWED&&!TRADING_IMPLEMENTED |
| Domain | bool compile constants |
| Preconditions | NOT_APPLICABLE financial authority |
| Guards | 2flags false |
| Callers | NO_CALLER_FOUND: all74 production source bodies, no dynamic/native proof |
| Dependencies | HSBI_Result @ Include/Core/HSBI_Invariants.mqh:13 |
| Normative contract | Docs/18:28–30; Docs/00_PROJECT_CHARTER_RU.md |
| Formula IDs | F060 |
| Error IDs | ERR016 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | STATIC_NO_TRADE_POLICY |
| Limitations / side effects | reasonOK даже theoretical passedfalse: diagnostic contract надо различать; flags не financial proof |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{return HSBI_Result(!HSBI_REAL_TRADING_ALLOWED&&!HSBI_TRADING_IMPLEMENTED,HSBI_REASON_OK,"HSBI-GEN-030","");}
~~~

### FUNCTION HSBI_ReasonToString

| Field | Individual analysis |
|---|---|
| Function ID | Include/Core/HSBI_ReasonCodes.mqh:4:HSBI_ReasonToString |
| Source | Include/Core/HSBI_ReasonCodes.mqh:4–4 |
| Signature | string HSBI_ReasonToString(const HSBI_ReasonCode reason) |
| Inputs | const HSBI_ReasonCode reason |
| Outputs / Postconditions | 9 explicit cases strings; остальные HSBI_REASON |
| Domain | reason enum |
| Preconditions | Используется только diagnostics |
| Guards | switch9cases+default |
| Callers | HSBI_Log @ Include/Diagnostics/HSBI_Logger.mqh:6; HSBI_BuildPanelModel @ Include/Diagnostics/HSBI_PanelModel.mqh:5 |
| Dependencies | NONE project functions |
| Normative contract | CONTRACT_NOT_FOUND для exact string mapping; diagnostics owner Docs/18:6,28 |
| Formula IDs | F060 |
| Error IDs | ERR027/028 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | DIAGNOSTIC_ONLY |
| Limitations / side effects | Generic fallback теряет детали, не принимает решение/торговлю; unknown не approval |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{switch(reason){case HSBI_REASON_OK:return "OK";case HSBI_REASON_TRADING_NOT_IMPLEMENTED:return "TRADING_NOT_IMPLEMENTED";case HSBI_REASON_REAL_TRADING_FORBIDDEN:return "REAL_TRADING_FORBIDDEN";case HSBI_REASON_INVALID_IDENTITY:return "INVALID_IDENTITY";case HSBI_REASON_INVALID_STATE_TRANSITION:return "INVALID_STATE_TRANSITION";case HSBI_REASON_DUPLICATE_FAR:return "DUPLICATE_FAR";case HSBI_REASON_STALE_SNAPSHOT:return "STALE_SNAPSHOT";case HSBI_REASON_INVALID_VOLUME:return "INVALID_VOLUME";case HSBI_REASON_RECONCILIATION_REQUIRED:return "RECONCILIATION_REQUIRED";default:return "HSBI_REASON";}}
~~~

### FUNCTION HSBI_IsKnownRole

| Field | Individual analysis |
|---|---|
| Function ID | Include/Core/HSBI_Roles.mqh:6:HSBI_IsKnownRole |
| Source | Include/Core/HSBI_Roles.mqh:6–6 |
| Signature | bool HSBI_IsKnownRole(const HSBI_Role role) |
| Inputs | const HSBI_Role role |
| Outputs / Postconditions | true iff lower<=role<=upper |
| Domain | INITIAL_BUY..NEW_FAR включительно |
| Preconditions | Текущая enum ordering contiguous; NONE отдельно caller |
| Guards | 2rangebounds |
| Callers | HSBI_ContextPositionValid @ Include/Core/HSBI_Context.mqh:13; HSBI_NoUnknownRole @ Include/Core/HSBI_Invariants.mqh:7; HSBI_NoUnknownRole @ Include/Core/HSBI_Invariants.mqh:7; HSBI_ValidatePositionDescriptor @ Include/Core/HSBI_Roles.mqh:7 |
| Dependencies | NONE project functions |
| Normative contract | Docs/02:7–16 |
| Formula IDs | F053/F062 |
| Error IDs | ERR012/049 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | LOCAL_ROLE_DOMAIN_MATCH |
| Limitations / side effects | При изменении enum version range должен пересматриваться; ownership не проверяется |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{return role>=HSBI_ROLE_INITIAL_BUY&&role<=HSBI_ROLE_NEW_FAR;}
~~~

### FUNCTION HSBI_ValidatePositionDescriptor

| Field | Individual analysis |
|---|---|
| Function ID | Include/Core/HSBI_Roles.mqh:7:HSBI_ValidatePositionDescriptor |
| Source | Include/Core/HSBI_Roles.mqh:7–7 |
| Signature | HSBI_ValidationResult HSBI_ValidatePositionDescriptor(const HSBI_PositionDescriptor &p) |
| Inputs | const HSBI_PositionDescriptor &p |
| Outputs / Postconditions | reject unknown role/negativevolume/ticket-without-id; иначе passed |
| Domain | known role; requested/actual lots>=0; ticket/identifier ulong |
| Preconditions | Не empty NONE DTO validator; broker facts вне helper |
| Guards | KnownRole;2negativevolume;ticket implication |
| Callers | NO_CALLER_FOUND: all74 production source bodies, no dynamic/native proof |
| Dependencies | HSBI_IsKnownRole @ Include/Core/HSBI_Roles.mqh:7; HSBI_Result @ Include/Core/HSBI_Roles.mqh:7; HSBI_Result @ Include/Core/HSBI_Roles.mqh:7; HSBI_Result @ Include/Core/HSBI_Roles.mqh:7; HSBI_Result @ Include/Core/HSBI_Roles.mqh:7 |
| Normative contract | Docs/02:19–34 |
| Formula IDs | F036/F053/F062 |
| Error IDs | ERR012/013/049 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | ACTIVE_DESCRIPTOR_PARTIAL |
| Limitations / side effects | NaN/Infinity/direction/identity/provenance/grid отсутствуют |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{if(!HSBI_IsKnownRole(p.role))return HSBI_Result(false,HSBI_REASON_UNKNOWN_ROLE,"HSBI-ID-010","unknown role");if(p.actualVolume<0.0||p.requestedVolume<0.0)return HSBI_Result(false,HSBI_REASON_INVALID_VOLUME,"HSBI-ID-010","negative volume");if(p.ticket>0&&p.identifier==0)return HSBI_Result(false,HSBI_REASON_INVALID_IDENTITY,"HSBI-ID-010","ticket without identifier");return HSBI_Result(true,HSBI_REASON_OK,"HSBI-ID-010","");}
~~~

### FUNCTION HSBI_CanPromoteToFar

| Field | Individual analysis |
|---|---|
| Function ID | Include/Core/HSBI_Roles.mqh:8:HSBI_CanPromoteToFar |
| Source | Include/Core/HSBI_Roles.mqh:8–8 |
| Signature | bool HSBI_CanPromoteToFar(const HSBI_PositionDescriptor &p,const ulong originalBigCoreIdentifier) |
| Inputs | const HSBI_PositionDescriptor &p,const ulong originalBigCoreIdentifier |
| Outputs / Postconditions | true iff BIG_CORE && id==original && actualVolume>0 |
| Domain | role enum;identifier ulong;actualVolume lots |
| Preconditions | Independent originalBigCoreIdentifier и actual residual подтверждены caller |
| Guards | role exact;id equal;volume>0 |
| Callers | NO_CALLER_FOUND: all74 production source bodies, no dynamic/native proof |
| Dependencies | NONE project functions |
| Normative contract | Docs/02:13,27; Docs/14_NEW_FAR_SOLVER_SPECIFICATION_RU.md |
| Formula IDs | F027/F028/F053 |
| Error IDs | ERR013/041/045 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | LOCAL_PROMOTION_FILTER_ONLY |
| Limitations / side effects | OriginalId0 иdescriptor0 равны при volume>0; Infinity не excluded; no independent source/time binding |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{return p.role==HSBI_ROLE_BIG_CORE&&p.identifier==originalBigCoreIdentifier&&p.actualVolume>0.0;}
~~~

### FUNCTION HSBI_ValidateRoleTransition

| Field | Individual analysis |
|---|---|
| Function ID | Include/Core/HSBI_Roles.mqh:9:HSBI_ValidateRoleTransition |
| Source | Include/Core/HSBI_Roles.mqh:9–9 |
| Signature | bool HSBI_ValidateRoleTransition(const HSBI_Role from,const HSBI_Role to) |
| Inputs | const HSBI_Role from,const HSBI_Role to |
| Outputs / Postconditions | toFAR fromBIG_CORE/NEW_FAR else from==to |
| Domain | from/to role enum |
| Preconditions | State/action/actual completion отдельный mandatory boundary |
| Guards | targetFAR conditional;2source alternatives;self equality |
| Callers | NO_CALLER_FOUND: all74 production source bodies, no dynamic/native proof |
| Dependencies | NONE project functions |
| Normative contract | Docs/02:9–16,27; Docs/09_INITIAL_LOCK_SPECIFICATION_RU.md |
| Formula IDs | F024/F053 |
| Error IDs | ERR012/016/049 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | ROLE_TOPOLOGY_ONLY |
| Limitations / side effects | Unknown cast self accepted; initial-role→FAR первоначальной классификации не выражено этим helper; не делать silent alias |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{if(to==HSBI_ROLE_FAR)return from==HSBI_ROLE_BIG_CORE||from==HSBI_ROLE_NEW_FAR;return from==to;}
~~~

### FUNCTION HSBI_CountFarRoles

| Field | Individual analysis |
|---|---|
| Function ID | Include/Core/HSBI_Roles.mqh:10:HSBI_CountFarRoles |
| Source | Include/Core/HSBI_Roles.mqh:10–10 |
| Signature | int HSBI_CountFarRoles(const HSBI_PositionDescriptor &a,const HSBI_PositionDescriptor &b,const HSBI_PositionDescriptor &c,const HSBI_PositionDescriptor &d) |
| Inputs | const HSBI_PositionDescriptor &a,const HSBI_PositionDescriptor &b,const HSBI_PositionDescriptor &c,const HSBI_PositionDescriptor &d |
| Outputs / Postconditions | n = sum(role==FAR) по4args |
| Domain | 4role labels→int0..4 |
| Preconditions | Registry полнота/uniqueactualpositions не доказываются |
| Guards | 4exactlabel comparisons |
| Callers | HSBI_ExactlyOneFarOrZero @ Include/Core/HSBI_Invariants.mqh:5; HSBI_BuildDiagnosticSnapshot @ Include/Diagnostics/HSBI_Diagnostics.mqh:5 |
| Dependencies | NONE project functions |
| Normative contract | Docs/02:25,30 |
| Formula IDs | F053/F062 |
| Error IDs | ERR012 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | FOUR_ARGUMENT_LABEL_COUNT |
| Limitations / side effects | Aliases считаются неоднократно; roles вне4args игнорируются; NEW_FAR label не FAR |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{int n=0;if(a.role==HSBI_ROLE_FAR)n++;if(b.role==HSBI_ROLE_FAR)n++;if(c.role==HSBI_ROLE_FAR)n++;if(d.role==HSBI_ROLE_FAR)n++;return n;}
~~~

### FUNCTION HSBI_IsRuntimeModeAllowedAtStage1

| Field | Individual analysis |
|---|---|
| Function ID | Include/Core/HSBI_RuntimeMode.mqh:5:HSBI_IsRuntimeModeAllowedAtStage1 |
| Source | Include/Core/HSBI_RuntimeMode.mqh:5–6 |
| Signature | bool HSBI_IsRuntimeModeAllowedAtStage1(const HSBI_RuntimeMode mode) |
| Inputs | const HSBI_RuntimeMode mode |
| Outputs / Postconditions | true только DISABLED/UNIT_TEST/STRATEGY_TESTER_DRY_RUN |
| Domain | runtime enum |
| Preconditions | Canonical RuntimePolicy остаётся отдельно |
| Guards | 3exact mode equalities |
| Callers | HSBI_ValidateContext @ Include/Core/HSBI_Context.mqh:36 |
| Dependencies | NONE project functions |
| Normative contract | Docs/18:28–30; Docs/HSB.2C_R1_Runtime_Mode_Policy_RU.md |
| Formula IDs | F060 |
| Error IDs | ERR016/028 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | STAGE1_WHITELIST |
| Limitations / side effects | Совместимость с productionPreflight capabilities не означает разрешение production runtime |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{return mode==HSBI_RUNTIME_DISABLED||mode==HSBI_RUNTIME_UNIT_TEST||mode==HSBI_RUNTIME_STRATEGY_TESTER_DRY_RUN;}
~~~

### FUNCTION HSBI_ValidateStateTopology

| Field | Individual analysis |
|---|---|
| Function ID | Include/Core/HSBI_StateValidator.mqh:4:HSBI_ValidateStateTopology |
| Source | Include/Core/HSBI_StateValidator.mqh:4–4 |
| Signature | HSBI_ValidationResult HSBI_ValidateStateTopology(const HSBI_RecoveryContext &c) |
| Inputs | const HSBI_RecoveryContext &c |
| Outputs / Postconditions | reject closed+pending;reject FAR_ACTIVE without far.roleFAR;иначе passed |
| Domain | state enum,Far role,pendingActionID |
| Preconditions | Context и actual positions валидированы отдельно |
| Guards | 2forbiddenconditions |
| Callers | NO_CALLER_FOUND: all74 production source bodies, no dynamic/native proof |
| Dependencies | HSBI_Result @ Include/Core/HSBI_StateValidator.mqh:4; HSBI_Result @ Include/Core/HSBI_StateValidator.mqh:4; HSBI_Result @ Include/Core/HSBI_StateValidator.mqh:4 |
| Normative contract | Docs/06:6–22; Docs/02:25–30 |
| Formula IDs | F024/F053/F065 |
| Error IDs | ERR012/016/049 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | TWO_STATE_FILTER_ONLY |
| Limitations / side effects | Не полная FSM/roles/actual presence: FAR label не actual position proof |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{if(c.currentState==HSBI_STATE_CYCLE_CLOSED&&c.pendingActionId!=0)return HSBI_Result(false,HSBI_REASON_PENDING_ACTION,"HSBI-FSM-002","closed state has pending action");if(c.currentState==HSBI_STATE_FAR_ACTIVE&&c.far.role!=HSBI_ROLE_FAR)return HSBI_Result(false,HSBI_REASON_INVALID_STATE_TRANSITION,"HSBI-FSM-002","FAR_ACTIVE without FAR");return HSBI_Result(true,HSBI_REASON_OK,"HSBI-FSM-002","");}
~~~

### FUNCTION HSBI_OutcomeCompletesAction

| Field | Individual analysis |
|---|---|
| Function ID | Include/Core/HSBI_StateValidator.mqh:5:HSBI_OutcomeCompletesAction |
| Source | Include/Core/HSBI_StateValidator.mqh:5–5 |
| Signature | bool HSBI_OutcomeCompletesAction(const HSBI_EventType e) |
| Inputs | const HSBI_EventType e |
| Outputs / Postconditions | true iff COMPLETED_FILL |
| Domain | EventType enum |
| Preconditions | Completion proof actual deals/ledger не из enum |
| Guards | single equality |
| Callers | NO_CALLER_FOUND: all74 production source bodies, no dynamic/native proof |
| Dependencies | NONE project functions |
| Normative contract | Docs/06:9,22; Docs/07:14–24 |
| Formula IDs | F024/F063 |
| Error IDs | ERR010/016 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | EVENT_LABEL_ONLY |
| Limitations / side effects | Не проверяет actual membership/volume/persistence; arbitrary presented event не proof |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{return e==HSBI_EVENT_COMPLETED_FILL;}
~~~

### FUNCTION HSBI_Result

| Field | Individual analysis |
|---|---|
| Function ID | Include/Core/HSBI_Types.mqh:7:HSBI_Result |
| Source | Include/Core/HSBI_Types.mqh:7–7 |
| Signature | HSBI_ValidationResult HSBI_Result(const bool passed,const int reason,const string req,const string details) |
| Inputs | const bool passed,const int reason,const string req,const string details |
| Outputs / Postconditions | Копирует4поля, не меняет входы |
| Domain | passed bool,reason int,req/details strings |
| Preconditions | Caller вычислил результат и reason; factory не validator |
| Guards | Нет guard: result constructor |
| Callers | HSBI_ExactlyOneFarOrZero @ Include/Core/HSBI_Invariants.mqh:5; HSBI_NoUnknownRole @ Include/Core/HSBI_Invariants.mqh:7; HSBI_ContextIdentityComplete @ Include/Core/HSBI_Invariants.mqh:8; HSBI_StateRevisionMonotonic @ Include/Core/HSBI_Invariants.mqh:9; HSBI_NoPendingActionConflict @ Include/Core/HSBI_Invariants.mqh:10; HSBI_NoFinalReserveForPartialFar @ Include/Core/HSBI_Invariants.mqh:11; HSBI_AllocationConservation @ Include/Core/HSBI_Invariants.mqh:12; HSBI_RealTradingForbiddenAtHSB1 @ Include/Core/HSBI_Invariants.mqh:13; HSBI_ValidatePositionDescriptor @ Include/Core/HSBI_Roles.mqh:7; HSBI_ValidatePositionDescriptor @ Include/Core/HSBI_Roles.mqh:7; HSBI_ValidatePositionDescriptor @ Include/Core/HSBI_Roles.mqh:7; HSBI_ValidatePositionDescriptor @ Include/Core/HSBI_Roles.mqh:7; HSBI_ValidateStateTopology @ Include/Core/HSBI_StateValidator.mqh:4; HSBI_ValidateStateTopology @ Include/Core/HSBI_StateValidator.mqh:4; HSBI_ValidateStateTopology @ Include/Core/HSBI_StateValidator.mqh:4; HSBI_ValidateMarketSnapshot @ Include/Planning/HSBI_ControlPrices.mqh:14; HSBI_ValidateControlPriceSet @ Include/Planning/HSBI_ControlPrices.mqh:15; HSBI_ValidateNewFarCandidateStructure @ Include/Planning/HSBI_NewFarCandidate.mqh:22 |
| Dependencies | NONE project functions |
| Normative contract | CONTRACT_NOT_FOUND для standalone factory; types layer Docs/18:6 |
| Formula IDs | F036/F060 |
| Error IDs | ERR027 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | DTO_CONSTRUCTOR_NO_FINANCIAL_SIDE_EFFECT |
| Limitations / side effects | Конструктор может принять inconsistent passed/reason, использовать как результат только после обязательного caller proof |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{HSBI_ValidationResult r;r.passed=passed;r.reason=reason;r.requirementId=req;r.details=details;return r;}
~~~


## R2 — индивидуальные intent/reserve/snapshot/ownership функции, продолжение без замены43 карт

### FUNCTION HSBI_ExecutionIntentDigest

| Field | Individual analysis |
|---|---|
| Function ID | Include/Execution/HSBI_ExecutionIntent.mqh:15:HSBI_ExecutionIntentDigest |
| Source | Include/Execution/HSBI_ExecutionIntent.mqh:15–25 |
| Signature | string HSBI_ExecutionIntentDigest(const HSBI_ExecutionIntent &x) |
| Inputs | const HSBI_ExecutionIntent &x |
| Outputs / Postconditions | Возвращает concatenation всех перечисленных полей, включая status |
| Domain | IDs64,volumes lots8dec,price12dec,timestamps signed,text |
| Preconditions | Shape валидируется отдельно; строка не independent authority |
| Guards | Нет guards; deterministic formatting calls |
| Callers | HSBI_ValidateExecutionIntentDigest @ Include/Execution/HSBI_ExecutionIntent.mqh:26 |
| Dependencies | HSBI_UlongToString @ Include/Execution/HSBI_ExecutionIntent.mqh:17; HSBI_UlongToString @ Include/Execution/HSBI_ExecutionIntent.mqh:17; HSBI_UlongToString @ Include/Execution/HSBI_ExecutionIntent.mqh:18; HSBI_UlongToString @ Include/Execution/HSBI_ExecutionIntent.mqh:18; HSBI_UlongToString @ Include/Execution/HSBI_ExecutionIntent.mqh:20; HSBI_UlongToString @ Include/Execution/HSBI_ExecutionIntent.mqh:21; HSBI_UlongToString @ Include/Execution/HSBI_ExecutionIntent.mqh:21; HSBI_UlongToString @ Include/Execution/HSBI_ExecutionIntent.mqh:21; HSBI_UlongToString @ Include/Execution/HSBI_ExecutionIntent.mqh:22; HSBI_UlongToString @ Include/Execution/HSBI_ExecutionIntent.mqh:22; HSBI_UlongToString @ Include/Execution/HSBI_ExecutionIntent.mqh:22; HSBI_UlongToString @ Include/Execution/HSBI_ExecutionIntent.mqh:23; HSBI_UlongToString @ Include/Execution/HSBI_ExecutionIntent.mqh:23 |
| Normative contract | Docs/07:6–24; Docs/HSB.2C_Execution_Intent_Spec.md |
| Formula IDs | F042/F053/F060 |
| Error IDs | ERR003/013/026/040 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | FINGERPRINT_NOT_BROKER_PROOF |
| Limitations / side effects | Fixed decimals не injective raw64 codec; delimiter encoding не length-prefix; hash от собственного DTO не подтверждает plan |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{
   return HSBI_UlongToString(x.intentId)+"|"+HSBI_UlongToString(x.planId)+"|"+x.planDigest+"|"+x.candidateDigest+"|"+x.aggregateProofDigest+"|"+
      HSBI_UlongToString(x.cycleId)+"|"+HSBI_UlongToString(x.stateRevision)+"|"+LongToString(x.accountLogin)+"|"+x.symbol+"|"+LongToString(x.magic)+"|"+
      IntegerToString((int)x.direction)+"|"+IntegerToString((int)x.role)+"|"+DoubleToString(x.requestedVolume,8)+"|"+DoubleToString(x.normalizedVolume,8)+"|"+
      DoubleToString(x.controlPrice,12)+"|"+IntegerToString((int)x.controlPriceSide)+"|"+HSBI_UlongToString(x.marketSnapshotId)+"|"+
      HSBI_UlongToString(x.costSnapshotId)+"|"+HSBI_UlongToString(x.riskSnapshotId)+"|"+HSBI_UlongToString(x.marginSnapshotId)+"|"+
      HSBI_UlongToString(x.sourcePositionIdentifier)+"|"+HSBI_UlongToString(x.sourceTicket)+"|"+HSBI_UlongToString(x.sourceDealId)+"|"+
      HSBI_UlongToString(x.sourceEventId)+"|"+HSBI_UlongToString(x.expectedActionId)+"|"+x.expectedTransition+"|"+
      LongToString((long)x.creationTimestamp)+"|"+LongToString((long)x.expiryTimestamp)+"|"+IntegerToString((int)x.status);
}
~~~

### FUNCTION HSBI_ValidateExecutionIntentDigest

| Field | Individual analysis |
|---|---|
| Function ID | Include/Execution/HSBI_ExecutionIntent.mqh:26:HSBI_ValidateExecutionIntentDigest |
| Source | Include/Execution/HSBI_ExecutionIntent.mqh:26–26 |
| Signature | bool HSBI_ValidateExecutionIntentDigest(const HSBI_ExecutionIntent &x) |
| Inputs | const HSBI_ExecutionIntent &x |
| Outputs / Postconditions | true iff nonempty digest==recomputed |
| Domain | string digest / intent fields |
| Preconditions | Доверенность expected plan/provider отдельно |
| Guards | nonempty; exact digest equality |
| Callers | HSBI_ValidateExecutionIntentStructure @ Include/Execution/HSBI_ExecutionIntent.mqh:40; HSBI_ValidateExecutionPreflight @ Include/Execution/HSBI_ExecutionPreflight.mqh:21; HSBI_ReconcileExecutionOutcome @ Include/Execution/HSBI_ExternalOutcome.mqh:25 |
| Dependencies | HSBI_ExecutionIntentDigest @ Include/Execution/HSBI_ExecutionIntent.mqh:26 |
| Normative contract | Docs/07:9–12; Docs/16:8 |
| Formula IDs | F053/F057/F060 |
| Error IDs | ERR013/026 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | SELF_CONTENT_BINDING_ONLY |
| Limitations / side effects | Recomputing altered input даёт новый consistent digest; нет independent journal binding |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{return x.digest!=""&&x.digest==HSBI_ExecutionIntentDigest(x);}
~~~

### FUNCTION HSBI_IsValidIntentStatus

| Field | Individual analysis |
|---|---|
| Function ID | Include/Execution/HSBI_ExecutionIntent.mqh:27:HSBI_IsValidIntentStatus |
| Source | Include/Execution/HSBI_ExecutionIntent.mqh:27–27 |
| Signature | bool HSBI_IsValidIntentStatus(const HSBI_IntentStatus s) |
| Inputs | const HSBI_IntentStatus s |
| Outputs / Postconditions | true iff inclusive bounds |
| Domain | CREATED..SUPERSEDED contiguous enum |
| Preconditions | Текущая версия enum |
| Guards | lower/upper numeric bounds |
| Callers | HSBI_ValidateExecutionIntentStructure @ Include/Execution/HSBI_ExecutionIntent.mqh:39 |
| Dependencies | NONE project functions |
| Normative contract | Docs/07:14–24; Docs/HSB.2C_Preflight_and_Lifecycle.md |
| Formula IDs | F024/F036 |
| Error IDs | ERR016/049 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | LOCAL_STATUS_DOMAIN |
| Limitations / side effects | Не разрешает lifecycle transition и не завершает actual action |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{return (int)s>=(int)HSBI_INTENT_CREATED&&(int)s<=(int)HSBI_INTENT_SUPERSEDED;}
~~~

### FUNCTION HSBI_ValidateExecutionIntentStructure

| Field | Individual analysis |
|---|---|
| Function ID | Include/Execution/HSBI_ExecutionIntent.mqh:28:HSBI_ValidateExecutionIntentStructure |
| Source | Include/Execution/HSBI_ExecutionIntent.mqh:28–41 |
| Signature | bool HSBI_ValidateExecutionIntentStructure(const HSBI_ExecutionIntent &x) |
| Inputs | const HSBI_ExecutionIntent &x |
| Outputs / Postconditions | false first violation; true only local shape/digest |
| Domain | IDs>0,namespace,finitepositive lots/price,BID/ASK,dates,status |
| Preconditions | Independent source/plan/snapshot evidence и actual authority обеспечиваются caller |
| Guards | 5nonzeroIDs;namespace;direction/role!=NONE;3finitepositive;side inBID/ASK;known-direction side;4snapIDs;4sourceIDs;4nonemptystrings;orderedtime;validstatus;digest |
| Callers | HSBI_ValidateExecutionPreflight @ Include/Execution/HSBI_ExecutionPreflight.mqh:20; HSBI_ValidateNestedExecutionIntent @ Include/Persistence/HSBI_ExecutionStateSnapshot.mqh:22 |
| Dependencies | HSBI_IsFiniteNumber @ Include/Execution/HSBI_ExecutionIntent.mqh:32; HSBI_IsFiniteNumber @ Include/Execution/HSBI_ExecutionIntent.mqh:32; HSBI_IsFiniteNumber @ Include/Execution/HSBI_ExecutionIntent.mqh:32; HSBI_IsValidIntentStatus @ Include/Execution/HSBI_ExecutionIntent.mqh:39; HSBI_ValidateExecutionIntentDigest @ Include/Execution/HSBI_ExecutionIntent.mqh:40 |
| Normative contract | Docs/07:9–24; Docs/02:23–28 |
| Formula IDs | F024/F036/F053/F060 |
| Error IDs | ERR013/026/049 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | SHAPE_PARTIAL_CLOSED_ENUM_GAP |
| Limitations / side effects | Unknown direction/role≠NONE проходят; recomputed digest не authority; close-side rule не обобщать на opening без action contract |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{
   if(x.intentId==0||x.planId==0||x.cycleId==0||x.stateRevision==0||x.expectedActionId==0)return false;
   if(x.accountLogin<=0||x.symbol==""||x.magic==0||x.direction==HSBI_DIRECTION_NONE||x.role==HSBI_ROLE_NONE)return false;
   if(!HSBI_IsFiniteNumber(x.requestedVolume)||!HSBI_IsFiniteNumber(x.normalizedVolume)||!HSBI_IsFiniteNumber(x.controlPrice)||
      x.requestedVolume<=0.0||x.normalizedVolume<=0.0||x.controlPrice<=0.0)return false;
   if(x.controlPriceSide!=HSBI_PRICE_SIDE_BID&&x.controlPriceSide!=HSBI_PRICE_SIDE_ASK)return false;
   if((x.direction==HSBI_DIRECTION_BUY&&x.controlPriceSide!=HSBI_PRICE_SIDE_BID)||(x.direction==HSBI_DIRECTION_SELL&&x.controlPriceSide!=HSBI_PRICE_SIDE_ASK))return false;
   if(x.marketSnapshotId==0||x.costSnapshotId==0||x.riskSnapshotId==0||x.marginSnapshotId==0)return false;
   if(x.sourcePositionIdentifier==0||x.sourceTicket==0||x.sourceDealId==0||x.sourceEventId==0)return false;
   if(x.planDigest==""||x.candidateDigest==""||x.aggregateProofDigest==""||x.expectedTransition=="")return false;
   if(x.creationTimestamp<=0||x.expiryTimestamp<=x.creationTimestamp||!HSBI_IsValidIntentStatus(x.status))return false;
   return HSBI_ValidateExecutionIntentDigest(x);
}
~~~

### FUNCTION HSBI_IntentIdempotencyKey

| Field | Individual analysis |
|---|---|
| Function ID | Include/Execution/HSBI_ExecutionIntent.mqh:42:HSBI_IntentIdempotencyKey |
| Source | Include/Execution/HSBI_ExecutionIntent.mqh:42–42 |
| Signature | string HSBI_IntentIdempotencyKey(const HSBI_ExecutionIntent &x) |
| Inputs | const HSBI_ExecutionIntent &x |
| Outputs / Postconditions | concat intentId/expectedActionId/planDigest/stateRevision |
| Domain | intent/action/revision ulong,planDigest string |
| Preconditions | Не SourceDealKey и не funding event |
| Guards | Нет validation guards |
| Callers | HSBI_IsSameIntentRetry @ Include/Execution/HSBI_ExecutionIntent.mqh:43; HSBI_IsSameIntentRetry @ Include/Execution/HSBI_ExecutionIntent.mqh:43; HSBI_IsIntentConflict @ Include/Execution/HSBI_ExecutionIntent.mqh:44; HSBI_IsIntentConflict @ Include/Execution/HSBI_ExecutionIntent.mqh:44 |
| Dependencies | HSBI_UlongToString @ Include/Execution/HSBI_ExecutionIntent.mqh:42; HSBI_UlongToString @ Include/Execution/HSBI_ExecutionIntent.mqh:42; HSBI_UlongToString @ Include/Execution/HSBI_ExecutionIntent.mqh:42 |
| Normative contract | Docs/07:9,18–21 |
| Formula IDs | F053/F057 |
| Error IDs | ERR013/033 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | LOCAL_INTENT_KEY |
| Limitations / side effects | Key excludes many payload fields, equality требует body binding; неизвестная history не NEW |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{return HSBI_UlongToString(x.intentId)+"|"+HSBI_UlongToString(x.expectedActionId)+"|"+x.planDigest+"|"+HSBI_UlongToString(x.stateRevision);}
~~~

### FUNCTION HSBI_IsSameIntentRetry

| Field | Individual analysis |
|---|---|
| Function ID | Include/Execution/HSBI_ExecutionIntent.mqh:43:HSBI_IsSameIntentRetry |
| Source | Include/Execution/HSBI_ExecutionIntent.mqh:43–43 |
| Signature | bool HSBI_IsSameIntentRetry(const HSBI_ExecutionIntent &a,const HSBI_ExecutionIntent &b) |
| Inputs | const HSBI_ExecutionIntent &a,const HSBI_ExecutionIntent &b |
| Outputs / Postconditions | true iff key equal && digest equal |
| Domain | 2const intents |
| Preconditions | Оба structures/digests валидированы caller |
| Guards | 2exactequalities |
| Callers | NO_CALLER_FOUND: all74 production source bodies, no dynamic/native proof |
| Dependencies | HSBI_IntentIdempotencyKey @ Include/Execution/HSBI_ExecutionIntent.mqh:43; HSBI_IntentIdempotencyKey @ Include/Execution/HSBI_ExecutionIntent.mqh:43 |
| Normative contract | Docs/07:18,21 |
| Formula IDs | F053/F057 |
| Error IDs | ERR013/017/030 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | LOCAL_RETRY_EQUALITY |
| Limitations / side effects | Два одинаковых forged digest без shape validation могут совпасть; no history/attempt proof |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{return HSBI_IntentIdempotencyKey(a)==HSBI_IntentIdempotencyKey(b)&&a.digest==b.digest;}
~~~

### FUNCTION HSBI_IsIntentConflict

| Field | Individual analysis |
|---|---|
| Function ID | Include/Execution/HSBI_ExecutionIntent.mqh:44:HSBI_IsIntentConflict |
| Source | Include/Execution/HSBI_ExecutionIntent.mqh:44–44 |
| Signature | bool HSBI_IsIntentConflict(const HSBI_ExecutionIntent &a,const HSBI_ExecutionIntent &b) |
| Inputs | const HSBI_ExecutionIntent &a,const HSBI_ExecutionIntent &b |
| Outputs / Postconditions | same key && different digest |
| Domain | 2const intents |
| Preconditions | Valid independent prior journal от caller |
| Guards | 2equalities/inequality |
| Callers | NO_CALLER_FOUND: all74 production source bodies, no dynamic/native proof |
| Dependencies | HSBI_IntentIdempotencyKey @ Include/Execution/HSBI_ExecutionIntent.mqh:44; HSBI_IntentIdempotencyKey @ Include/Execution/HSBI_ExecutionIntent.mqh:44 |
| Normative contract | Docs/07:21; Docs/17:11–13 |
| Formula IDs | F053/F057/F060 |
| Error IDs | ERR003/013/030 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | LOCAL_CONFLICT_CLASSIFIER |
| Limitations / side effects | Не независимая history; same recomputed rounded fingerprint может скрывать изменения rawpayload |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{return HSBI_IntentIdempotencyKey(a)==HSBI_IntentIdempotencyKey(b)&&a.digest!=b.digest;}
~~~

### FUNCTION HSBI_ValidateReserveSourceProof

| Field | Individual analysis |
|---|---|
| Function ID | Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:24:HSBI_ValidateReserveSourceProof |
| Source | Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:24–29 |
| Signature | bool HSBI_ValidateReserveSourceProof(const HSBI_BrokerMoneyEvaluationResult &p,const HSBI_MoneyProofIdentity &expected) |
| Inputs | const HSBI_BrokerMoneyEvaluationResult &p,const HSBI_MoneyProofIdentity &expected |
| Outputs / Postconditions | true iff10 групп result flags/type/net/identity/role |
| Domain | finite netMoney>0,BigCore/BigTrend,identity DTO |
| Preconditions | Expected identity независимая; функция явно projected, не settled grant |
| Guards | valid,PASS,projected,!actual,runtimeConfirmed,positivefinite net,validate identity,same identity,BigCore/Trend |
| Callers | HSBI_EvaluateReserveCatchUp @ Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:42 |
| Dependencies | HSBI_IsFiniteNumber @ Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:27; HSBI_ValidateMoneyProofIdentity @ Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:27; HSBI_IsSameMoneyProofIdentity @ Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:27 |
| Normative contract | Docs/08:6–24; Docs/31_MONEY_PROOF_IDENTITY_RU.md |
| Formula IDs | F007/F017/F019/F022 |
| Error IDs | ERR007/008/013/033/048 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | PROJECTED_SOURCE_LOCAL_SCOPE |
| Limitations / side effects | runtimeConfirmed bool не actual settlement; не сравнивает с reserveEligibleMoney/authoritative allocation amount |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{
   return p.valid&&p.status==HSBI_CALC_PASS&&p.projected&&!p.actual&&p.runtimeConfirmed&&p.netMoney>0.0&&
      HSBI_IsFiniteNumber(p.netMoney)&&HSBI_ValidateMoneyProofIdentity(p.identity)&&HSBI_IsSameMoneyProofIdentity(p.identity,expected)&&
      (p.identity.role==HSBI_ROLE_BIG_CORE||p.identity.role==HSBI_ROLE_BIG_TREND);
}
~~~

### FUNCTION HSBI_ValidateFarLossProof

| Field | Individual analysis |
|---|---|
| Function ID | Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:30:HSBI_ValidateFarLossProof |
| Source | Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:30–34 |
| Signature | bool HSBI_ValidateFarLossProof(const HSBI_BrokerMoneyEvaluationResult &p,const HSBI_MoneyProofIdentity &expected) |
| Inputs | const HSBI_BrokerMoneyEvaluationResult &p,const HSBI_MoneyProofIdentity &expected |
| Outputs / Postconditions | valid/PASS/projected/!actual/runtimeConfirmed/finite/identityequal/FAR |
| Domain | finite signed netMoney,role FAR |
| Preconditions | ExpectedFar independent; actual loss отдельно |
| Guards | 8групп exact checks |
| Callers | HSBI_EvaluateReserveCatchUp @ Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:43 |
| Dependencies | HSBI_IsFiniteNumber @ Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:32; HSBI_ValidateMoneyProofIdentity @ Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:33; HSBI_IsSameMoneyProofIdentity @ Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:33 |
| Normative contract | Docs/08:6–24; D04 proposed |
| Formula IDs | F020/F021/F022 |
| Error IDs | ERR013/043/048 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | PROJECTED_FAR_PROOF_ONLY |
| Limitations / side effects | Не bind переданный farLossIncreaseMoney к max(0,-proof.netMoney); amount gap ERR048 |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{
   return p.valid&&p.status==HSBI_CALC_PASS&&p.projected&&!p.actual&&p.runtimeConfirmed&&HSBI_IsFiniteNumber(p.netMoney)&&
      HSBI_ValidateMoneyProofIdentity(p.identity)&&HSBI_IsSameMoneyProofIdentity(p.identity,expected)&&p.identity.role==HSBI_ROLE_FAR;
}
~~~

### FUNCTION HSBI_EvaluateReserveCatchUp

| Field | Individual analysis |
|---|---|
| Function ID | Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:35:HSBI_EvaluateReserveCatchUp |
| Source | Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:35–77 |
| Signature | HSBI_ReserveCatchUpResult HSBI_EvaluateReserveCatchUp(const HSBI_ReserveCatchUpInput &x) |
| Inputs | const HSBI_ReserveCatchUpInput &x |
| Outputs / Postconditions | UNAVAILABLE/REJECT/ERROR либо PASS с margin>0; входы/ledgers неизменны |
| Domain | money samecurrency; lots positive; share[0,1]; IDs/flags |
| Preconditions | Independent allocation/source/far amounts/journal обязательны вне supplied DTO |
| Guards | source/far validators;allocation validator+policy/deal;consumption shape;duplicate/conflict;mode/policy/fresh/IDs;5finite;allocated/newbranch;nonnegativecosts;positivevol;share*netBig>far;positive margin |
| Callers | HSBI_SolveNewFar @ Include/Planning/HSBI_NewFarSolver.mqh:127 |
| Dependencies | HSBI_ValidateReserveSourceProof @ Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:42; HSBI_ValidateFarLossProof @ Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:43; HSBI_ValidateReserveAllocationSource @ Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:44; HSBI_ValidateReserveConsumption @ Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:47; HSBI_IsDuplicateReserveConsumption @ Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:48; HSBI_ReserveConsumptionConflict @ Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:49; HSBI_MoneyProofIdentityDigest @ Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:51; HSBI_MoneyProofIdentityDigest @ Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:52; HSBI_ReserveAllocationSourceDigest @ Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:53; HSBI_ReserveConsumptionKeyDigest @ Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:54; HSBI_IsStaticCalculationAllowed @ Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:55; HSBI_ValidateAllocationPolicy @ Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:55; HSBI_IsFiniteNumber @ Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:61; HSBI_IsFiniteNumber @ Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:61; HSBI_IsFiniteNumber @ Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:61; HSBI_IsFiniteNumber @ Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:62; HSBI_IsFiniteNumber @ Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:62 |
| Normative contract | Docs/08:6–24; Docs/24_BROKER_MONEY_MODEL_RU.md; D01/D02/D04 pending |
| Formula IDs | F006/F013/F015/F019/F020/F022 |
| Error IDs | ERR007/008/013/033/043/048 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | LOCAL_PURE_EVALUATOR_NOT_LEDGER_COMMIT |
| Limitations / side effects | Нет полного amount-binding, sourceAllocationKey binding/global exhaustion journal; projected proof не settled funds; final margin arithmetic finite output отдельно не validated |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{
   HSBI_ReserveCatchUpResult r;ZeroMemory(r);r.status=HSBI_CALC_UNAVAILABLE;r.reason=HSBI_REASON_NOT_INITIALIZED;
   r.details="RESERVE_SOURCE_UNAVAILABLE";r.projected=x.projected;r.reserveShare=x.allocationPolicy.reserveShare;
   r.reserveEligibleMoney=x.reserveEligibleMoney;r.farLossIncreaseMoney=x.farLossIncreaseMoney;r.executionSafetyBuffer=x.executionSafetyBuffer;
   r.sourceDealId=x.sourceDealId;r.sourceEventId=x.sourceEventId;r.planId=x.planId;r.stateRevision=x.stateRevision;
   r.reserveIdentity=x.reserveSourceProof.identity;r.farLossIdentity=x.farLossProof.identity;
   r.reserveSourceIdentityValid=HSBI_ValidateReserveSourceProof(x.reserveSourceProof,x.expectedReserveIdentity);
   r.farLossSourceIdentityValid=HSBI_ValidateFarLossProof(x.farLossProof,x.expectedFarIdentity);
   r.allocationSourceValid=HSBI_ValidateReserveAllocationSource(x.reserveAllocationSource)&&
      x.reserveAllocationSource.allocationPolicyVersion==x.allocationPolicy.policyVersion&&
      x.reserveAllocationSource.sourceDealId==x.reserveSourceProof.identity.sourceDealId;
   r.consumptionAllowed=HSBI_ValidateReserveConsumption(x.consumptionKey,x.planId,x.stateRevision);
   bool duplicate=x.hasPriorConsumption&&HSBI_IsDuplicateReserveConsumption(x.consumptionKey,x.priorConsumptionKey);
   bool conflict=x.hasPriorConsumption&&HSBI_ReserveConsumptionConflict(x.consumptionKey,x.priorConsumptionKey);
   r.doubleCountFree=!duplicate&&!conflict;r.runtimeConfirmed=x.reserveSourceProof.runtimeConfirmed&&x.farLossProof.runtimeConfirmed;
   r.reserveSourceDigest=HSBI_MoneyProofIdentityDigest(x.reserveSourceProof.identity);
   r.farLossSourceDigest=HSBI_MoneyProofIdentityDigest(x.farLossProof.identity);
   r.allocationSourceDigest=HSBI_ReserveAllocationSourceDigest(x.reserveAllocationSource);
   r.consumptionKeyDigest=HSBI_ReserveConsumptionKeyDigest(x.consumptionKey);
   if(!HSBI_IsStaticCalculationAllowed(x.runtimeMode)||x.testOnlySource||!HSBI_ValidateAllocationPolicy(x.allocationPolicy)||!x.moneyAvailable||!x.fresh||x.snapshotId==0||x.planId==0||x.stateRevision==0)return r;
   if(duplicate){r.status=HSBI_CALC_REJECT;r.details="DUPLICATE_CONSUMPTION_NOOP";return r;}
   if(conflict){r.status=HSBI_CALC_REJECT;r.details="CONSUMPTION_CONFLICT";return r;}
   if(!r.reserveSourceIdentityValid){r.status=HSBI_CALC_REJECT;r.details="RESERVE_SOURCE_IDENTITY_MISMATCH";return r;}
   if(!r.farLossSourceIdentityValid){r.status=HSBI_CALC_REJECT;r.details="FAR_LOSS_SOURCE_IDENTITY_MISMATCH";return r;}
   if(!r.allocationSourceValid||!r.consumptionAllowed||!r.doubleCountFree||!r.runtimeConfirmed){r.status=HSBI_CALC_REJECT;r.details="ALLOCATION_OR_CONSUMPTION_INVALID";return r;}
   if(!HSBI_IsFiniteNumber(x.reserveEligibleMoney)||!HSBI_IsFiniteNumber(x.farLossIncreaseMoney)||!HSBI_IsFiniteNumber(x.executionSafetyBuffer)||
      !HSBI_IsFiniteNumber(x.netBigVolume)||!HSBI_IsFiniteNumber(x.farVolume)){r.status=HSBI_CALC_ERROR;r.details="NONFINITE_CATCH_UP";return r;}
   if(x.reserveEligibleMoneyAlreadyAllocated){
      if(x.reserveAllocationSource.reserveAllocated<=0.0||x.reserveAllocationSource.reserveAllocated>x.reserveAllocationSource.allocatableNet||
         x.reserveAllocationSource.alreadyConsumed>0.0){r.status=HSBI_CALC_REJECT;r.details="ALLOCATED_SOURCE_NOT_AVAILABLE";return r;}
      r.reserveGainMoney=x.reserveAllocationSource.reserveAllocated;
   } else {
      if(x.reserveEligibleMoney<=0.0||x.sourceDealId!=x.reserveSourceProof.identity.sourceDealId||x.sourceEventId!=x.reserveSourceProof.identity.sourceEventId){
         r.status=HSBI_CALC_REJECT;r.details="ELIGIBLE_SOURCE_NOT_BOUND";return r;}
      r.reserveGainMoney=x.reserveEligibleMoney*x.allocationPolicy.reserveShare;
   }
   if(x.farLossIncreaseMoney<0.0||x.executionSafetyBuffer<0.0||x.netBigVolume<=0.0||x.farVolume<=0.0){r.status=HSBI_CALC_REJECT;r.details="INVALID_CATCH_UP_INPUT";return r;}
   if(x.allocationPolicy.reserveShare*x.netBigVolume<=x.farVolume){r.status=HSBI_CALC_REJECT;r.details="LOT_CONDITION_FAILED";return r;}
   r.catchUpMargin=r.reserveGainMoney-x.farLossIncreaseMoney-x.executionSafetyBuffer;
   if(r.catchUpMargin<=0.0){r.status=HSBI_CALC_REJECT;r.details="MONEY_CONDITION_FAILED";return r;}
   r.status=HSBI_CALC_PASS;r.valid=true;r.reason=HSBI_REASON_OK;r.details="PASS";return r;
}
~~~

### FUNCTION HSBI_ReserveCatchUpDigest

| Field | Individual analysis |
|---|---|
| Function ID | Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:78:HSBI_ReserveCatchUpDigest |
| Source | Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:78–82 |
| Signature | string HSBI_ReserveCatchUpDigest(const HSBI_ReserveCatchUpResult &r) |
| Inputs | const HSBI_ReserveCatchUpResult &r |
| Outputs / Postconditions | concat selected outputs/runtime/doubleCount flags |
| Domain | status/bools,share12dec,money8dec,digests |
| Preconditions | Result validated separately; not full immutable identity |
| Guards | Нет guards |
| Callers | HSBI_SolveNewFar @ Include/Planning/HSBI_NewFarSolver.mqh:143; HSBI_RuntimeDecisionContextDigest @ Include/Runtime/HSBI_RuntimeDecisionTypes.mqh:17 |
| Dependencies | NONE project functions |
| Normative contract | Docs/16:8; NUM-CODEC proposed |
| Formula IDs | F042/F057/F060 |
| Error IDs | ERR003/026/040 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | DIAGNOSTIC_FINGERPRINT |
| Limitations / side effects | Не canonical money codec/independent allocation proof; частьmetadata не included |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{return IntegerToString((int)r.status)+"|"+IntegerToString((int)r.valid)+"|"+DoubleToString(r.reserveShare,12)+"|"+
   DoubleToString(r.reserveEligibleMoney,8)+"|"+DoubleToString(r.reserveGainMoney,8)+"|"+DoubleToString(r.farLossIncreaseMoney,8)+"|"+
   DoubleToString(r.executionSafetyBuffer,8)+"|"+DoubleToString(r.catchUpMargin,8)+"|"+r.reserveSourceDigest+"|"+r.farLossSourceDigest+"|"+
   r.allocationSourceDigest+"|"+r.consumptionKeyDigest+"|"+IntegerToString((int)r.runtimeConfirmed)+"|"+IntegerToString((int)r.doubleCountFree);}
~~~

### FUNCTION HSBI_ExecutionStateSnapshotDigest

| Field | Individual analysis |
|---|---|
| Function ID | Include/Persistence/HSBI_ExecutionStateSnapshot.mqh:12:HSBI_ExecutionStateSnapshotDigest |
| Source | Include/Persistence/HSBI_ExecutionStateSnapshot.mqh:12–18 |
| Signature | string HSBI_ExecutionStateSnapshotDigest(const HSBI_ExecutionStateSnapshot &x) |
| Inputs | const HSBI_ExecutionStateSnapshot &x |
| Outputs / Postconditions | concat metadata/nested digests; вход неизменён |
| Domain | versions/IDs,counters,bools,timestamps,nested digest strings |
| Preconditions | Nested digest/body проверяются separately |
| Guards | Нет shape guards |
| Callers | HSBI_ValidateExecutionStateSnapshot @ Include/Persistence/HSBI_ExecutionStateSnapshot.mqh:31 |
| Dependencies | HSBI_UlongToString @ Include/Persistence/HSBI_ExecutionStateSnapshot.mqh:14; HSBI_UlongToString @ Include/Persistence/HSBI_ExecutionStateSnapshot.mqh:14; HSBI_UlongToString @ Include/Persistence/HSBI_ExecutionStateSnapshot.mqh:15; HSBI_UlongToString @ Include/Persistence/HSBI_ExecutionStateSnapshot.mqh:15 |
| Normative contract | Docs/16:8–19; Docs/HSB.2C_Journal_Persistence_Reconciliation.md |
| Formula IDs | F057/F060/F066 |
| Error IDs | ERR013/017/050 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | LOCAL_CONTENT_FINGERPRINT |
| Limitations / side effects | Digest noncryptographic serialized string, no independent journal/authenticity; nested body binding mandatory |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{return IntegerToString(x.schemaVersion)+"|"+IntegerToString(x.snapshotVersion)+"|"+LongToString(x.accountLogin)+"|"+x.symbol+"|"+
   LongToString(x.magic)+"|"+HSBI_UlongToString(x.cycleId)+"|"+HSBI_UlongToString(x.stateRevision)+"|"+
   HSBI_UlongToString(x.lastConfirmedActionId)+"|"+HSBI_UlongToString(x.lastConfirmedEventId)+"|"+x.lastJournalDigest+"|"+
   x.pendingIntent.digest+"|"+x.completedIntent.digest+"|"+x.invalidatedIntent.digest+"|"+IntegerToString(x.activeIntentCount)+"|"+
   IntegerToString(x.completedActionCount)+"|"+IntegerToString((int)x.reconciliationConflict)+"|"+IntegerToString((int)x.failClosed)+"|"+
   IntegerToString((int)x.journalChainValid)+"|"+IntegerToString((int)x.fresh)+"|"+LongToString((long)x.creationTimestamp)+"|"+LongToString((long)x.updateTimestamp);}
~~~

### FUNCTION HSBI_ValidateNestedExecutionIntent

| Field | Individual analysis |
|---|---|
| Function ID | Include/Persistence/HSBI_ExecutionStateSnapshot.mqh:19:HSBI_ValidateNestedExecutionIntent |
| Source | Include/Persistence/HSBI_ExecutionStateSnapshot.mqh:19–24 |
| Signature | bool HSBI_ValidateNestedExecutionIntent(const HSBI_ExecutionIntent &i,const HSBI_ExecutionStateSnapshot &x) |
| Inputs | const HSBI_ExecutionIntent &i,const HSBI_ExecutionStateSnapshot &x |
| Outputs / Postconditions | id0→true; present→structure plus5context equalities andplan/action>0 |
| Domain | intentId0 absent либо shape+namespace+revision |
| Preconditions | Absent representation/authority caller responsibility |
| Guards | absence shortcut;structure;account/symbol/magic/cycle/revision;plan/action |
| Callers | HSBI_ValidateExecutionStateSnapshot @ Include/Persistence/HSBI_ExecutionStateSnapshot.mqh:32; HSBI_ValidateExecutionStateSnapshot @ Include/Persistence/HSBI_ExecutionStateSnapshot.mqh:32; HSBI_ValidateExecutionStateSnapshot @ Include/Persistence/HSBI_ExecutionStateSnapshot.mqh:32 |
| Dependencies | HSBI_ValidateExecutionIntentStructure @ Include/Persistence/HSBI_ExecutionStateSnapshot.mqh:22 |
| Normative contract | Docs/16:8–19; Docs/07:9 |
| Formula IDs | F053/F057/F066 |
| Error IDs | ERR013/017/049/050 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | LOCAL_NESTED_BINDING |
| Limitations / side effects | Absent id0 может иметь ignored other fields; scope presence contract; не actual history proof |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{
   if(i.intentId==0)return true;
   return HSBI_ValidateExecutionIntentStructure(i)&&i.accountLogin==x.accountLogin&&i.symbol==x.symbol&&i.magic==x.magic&&
      i.cycleId==x.cycleId&&i.stateRevision==x.stateRevision&&i.planId>0&&i.expectedActionId>0;
}
~~~

### FUNCTION HSBI_IsActiveIntentStatus

| Field | Individual analysis |
|---|---|
| Function ID | Include/Persistence/HSBI_ExecutionStateSnapshot.mqh:25:HSBI_IsActiveIntentStatus |
| Source | Include/Persistence/HSBI_ExecutionStateSnapshot.mqh:25–26 |
| Signature | bool HSBI_IsActiveIntentStatus(const HSBI_IntentStatus s) |
| Inputs | const HSBI_IntentStatus s |
| Outputs / Postconditions | true CREATED/PREFLIGHT/PERSISTED/BLOCKED/PENDING/RECEIVED/RECONCILING |
| Domain | 7exact status labels |
| Preconditions | NOT_APPLICABLE financial authority; enum only |
| Guards | 7exactequalities |
| Callers | HSBI_ValidateExecutionStateSnapshot @ Include/Persistence/HSBI_ExecutionStateSnapshot.mqh:34 |
| Dependencies | NONE project functions |
| Normative contract | Docs/HSB.2C_Preflight_and_Lifecycle.md; Docs/07:14–24 |
| Formula IDs | F024/F066 |
| Error IDs | ERR016/050 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | LOCAL_PHASE_DOMAIN |
| Limitations / side effects | COMPLETED не active; неизвестное false; не volume/actual completion validation |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{return s==HSBI_INTENT_CREATED||s==HSBI_INTENT_PREFLIGHT_PASSED||s==HSBI_INTENT_PERSISTED||s==HSBI_INTENT_DISPATCH_BLOCKED||s==HSBI_INTENT_OUTCOME_PENDING||s==HSBI_INTENT_OUTCOME_RECEIVED||s==HSBI_INTENT_RECONCILING;}
~~~

### FUNCTION HSBI_ValidateExecutionStateSnapshot

| Field | Individual analysis |
|---|---|
| Function ID | Include/Persistence/HSBI_ExecutionStateSnapshot.mqh:27:HSBI_ValidateExecutionStateSnapshot |
| Source | Include/Persistence/HSBI_ExecutionStateSnapshot.mqh:27–41 |
| Signature | bool HSBI_ValidateExecutionStateSnapshot(const HSBI_ExecutionStateSnapshot &x,const int schema,const int version,const long account,const string symbol,const long magic,const ulong cycle,const ulong minimumRevision) |
| Inputs | const HSBI_ExecutionStateSnapshot &x,const int schema,const int version,const long account,const string symbol,const long magic,const ulong cycle,const ulong minimumRevision |
| Outputs / Postconditions | false first violation;true не новый spending authorization |
| Domain | versions/namespace/revision,counters0..1,timestamps,nested intents |
| Preconditions | Expected schema/namespace/minrev независимы; journalChainValid/fresh не внешнее доказательство |
| Guards | 8expectedbindings/rev;fresh/journal/conflict/failClosed/time;digest;2counterbounds;3nested validators;activeCount iff pending;status checks;completed+pending forbidden;invalidated/current action conflict |
| Callers | HSBI_RecoverExecutionState @ Include/Persistence/HSBI_ExecutionStateSnapshot.mqh:43; HSBI_ValidateRestartedRuntimeState @ Include/Runtime/HSBI_RuntimeRestartValidator.mqh:8 |
| Dependencies | HSBI_ExecutionStateSnapshotDigest @ Include/Persistence/HSBI_ExecutionStateSnapshot.mqh:31; HSBI_ValidateNestedExecutionIntent @ Include/Persistence/HSBI_ExecutionStateSnapshot.mqh:32; HSBI_ValidateNestedExecutionIntent @ Include/Persistence/HSBI_ExecutionStateSnapshot.mqh:32; HSBI_ValidateNestedExecutionIntent @ Include/Persistence/HSBI_ExecutionStateSnapshot.mqh:32; HSBI_IsActiveIntentStatus @ Include/Persistence/HSBI_ExecutionStateSnapshot.mqh:34 |
| Normative contract | Docs/16:8–19; Docs/HSB.2C_Journal_Persistence_Reconciliation.md:5 |
| Formula IDs | F024/F057/F060/F066 |
| Error IDs | ERR017/049/050 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | LOCAL_SNAPSHOT_VALIDATION_LIMITED |
| Limitations / side effects | completedActionCount не iff completedExists: semantic meaning unresolved ERR050; duplicate completed+pending check redundant; no actual history/durable authenticity |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{
   if(x.schemaVersion!=schema||x.snapshotVersion!=version||x.accountLogin!=account||x.symbol!=symbol||x.magic!=magic||x.cycleId!=cycle||
      x.stateRevision<minimumRevision||!x.fresh||!x.journalChainValid||x.reconciliationConflict||x.failClosed||x.creationTimestamp<=0||x.updateTimestamp<x.creationTimestamp||
      x.snapshotDigest!=HSBI_ExecutionStateSnapshotDigest(x)||x.activeIntentCount<0||x.activeIntentCount>1||x.completedActionCount<0||x.completedActionCount>1)return false;
   if(!HSBI_ValidateNestedExecutionIntent(x.pendingIntent,x)||!HSBI_ValidateNestedExecutionIntent(x.completedIntent,x)||!HSBI_ValidateNestedExecutionIntent(x.invalidatedIntent,x))return false;
   bool pendingExists=x.pendingIntent.intentId>0,completedExists=x.completedIntent.intentId>0,invalidatedExists=x.invalidatedIntent.intentId>0;
   if((x.activeIntentCount==1)!=pendingExists||pendingExists&&!HSBI_IsActiveIntentStatus(x.pendingIntent.status))return false;
   if(completedExists&&x.completedIntent.status!=HSBI_INTENT_COMPLETED)return false;
   if(invalidatedExists&&x.invalidatedIntent.status!=HSBI_INTENT_INVALIDATED&&x.invalidatedIntent.status!=HSBI_INTENT_CONFLICT&&x.invalidatedIntent.status!=HSBI_INTENT_SUPERSEDED)return false;
   if(completedExists&&pendingExists)return false;
   if(completedExists&&pendingExists&&x.completedIntent.expectedActionId==x.pendingIntent.expectedActionId)return false;
   if(invalidatedExists&&x.activeIntentCount>0&&x.invalidatedIntent.expectedActionId==x.pendingIntent.expectedActionId)return false;
   return true;
}
~~~

### FUNCTION HSBI_RecoverExecutionState

| Field | Individual analysis |
|---|---|
| Function ID | Include/Persistence/HSBI_ExecutionStateSnapshot.mqh:42:HSBI_RecoverExecutionState |
| Source | Include/Persistence/HSBI_ExecutionStateSnapshot.mqh:42–43 |
| Signature | HSBI_ExecutionRecoveryStatus HSBI_RecoverExecutionState(const HSBI_ExecutionStateSnapshot &x,const int schema,const int version,const long account,const string symbol,const long magic,const ulong cycle,const ulong revision) |
| Inputs | const HSBI_ExecutionStateSnapshot &x,const int schema,const int version,const long account,const string symbol,const long magic,const ulong cycle,const ulong revision |
| Outputs / Postconditions | valid→ACCEPTED;invalid+emptydigest→UNAVAILABLE;иначеREJECTED |
| Domain | snapshot const,expected params |
| Preconditions | No backend IO; actual reconciliation отдельно |
| Guards | ValidateExecutionStateSnapshot;digest empty discriminator |
| Callers | NO_CALLER_FOUND: all74 production source bodies, no dynamic/native proof |
| Dependencies | HSBI_ValidateExecutionStateSnapshot @ Include/Persistence/HSBI_ExecutionStateSnapshot.mqh:43 |
| Normative contract | Docs/16:14–19; Docs/17:3–22 |
| Formula IDs | F057/F066 |
| Error IDs | ERR013/017/050 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | PURE_RECOVERY_NOT_DURABLE_COMMIT |
| Limitations / side effects | ACCEPTED значит reconstructed local consistency, не reauthorization/real account truth |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{return HSBI_ValidateExecutionStateSnapshot(x,schema,version,account,symbol,magic,cycle,revision)?HSBI_RECOVERY_ACCEPTED:(x.snapshotDigest==""?HSBI_RECOVERY_UNAVAILABLE:HSBI_RECOVERY_REJECTED);}
~~~

### FUNCTION HSBI_ValidateExecutionPreflight

| Field | Individual analysis |
|---|---|
| Function ID | Include/Execution/HSBI_ExecutionPreflight.mqh:17:HSBI_ValidateExecutionPreflight |
| Source | Include/Execution/HSBI_ExecutionPreflight.mqh:17–34 |
| Signature | HSBI_ExecutionPreflightResult HSBI_ValidateExecutionPreflight(const HSBI_ExecutionPreflightInput &x) |
| Inputs | const HSBI_ExecutionPreflightInput &x |
| Outputs / Postconditions | typed preflight first failure либо PASS; no request/state writes |
| Domain | intent+aggregate+catchup+broker/price+currentnamespace+time |
| Preconditions | Flags/provider data независимы от presented, actor action semantics определены |
| Guards | mode+structure;digest;plan/candidate nonempty+aggregateDigest;fresh/expiry;conflicts;proof flags;currentnamespace/rev;brokerprops;volumegrid;typedprice;price delta tolerance |
| Callers | NO_CALLER_FOUND: all74 production source bodies, no dynamic/native proof |
| Dependencies | HSBI_IsProductionPreflightAllowed @ Include/Execution/HSBI_ExecutionPreflight.mqh:20; HSBI_ValidateExecutionIntentStructure @ Include/Execution/HSBI_ExecutionPreflight.mqh:20; HSBI_ValidateExecutionIntentDigest @ Include/Execution/HSBI_ExecutionPreflight.mqh:21; HSBI_ValidateBrokerProperties @ Include/Execution/HSBI_ExecutionPreflight.mqh:30; HSBI_ValidateVolume @ Include/Execution/HSBI_ExecutionPreflight.mqh:30; HSBI_ValidateTypedControlPrice @ Include/Execution/HSBI_ExecutionPreflight.mqh:31; HSBI_GridTolerance @ Include/Execution/HSBI_ExecutionPreflight.mqh:31 |
| Normative contract | Docs/07:6–24; Docs/18:28–30 |
| Formula IDs | F024/F036/F053/F060/F062 |
| Error IDs | ERR013/016/026/049 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | PREFLIGHT_LOCAL_NOT_BROKER_AUTHORIZATION |
| Limitations / side effects | Нет закрытого direction/role guard сверхStructure; digest equality не independent proofs; broker.symbol не bound во всех местах; no dispatch |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{
   HSBI_ExecutionPreflightResult r;ZeroMemory(r);r.status=HSBI_PREFLIGHT_REJECT;r.reason=HSBI_REASON_INTERNAL_INVARIANT_FAILED;r.details="REJECT";
   if(!HSBI_IsProductionPreflightAllowed(x.runtimeMode)||!HSBI_ValidateExecutionIntentStructure(x.intent)){r.reason=HSBI_REASON_INVALID_INTENT_STRUCTURE;r.details="INVALID_INTENT_STRUCTURE";return r;}
   if(!HSBI_ValidateExecutionIntentDigest(x.intent)){r.status=HSBI_PREFLIGHT_DIGEST_MISMATCH;r.details="INTENT_DIGEST_MISMATCH";return r;}
   if(x.intent.planDigest==""||x.intent.candidateDigest==""||x.intent.aggregateProofDigest!=x.aggregate.aggregateDigest){r.status=HSBI_PREFLIGHT_DIGEST_MISMATCH;r.details="PLAN_CANDIDATE_AGGREGATE_DIGEST_MISMATCH";return r;}
   if(!x.marketFresh||x.now>x.intent.expiryTimestamp||!x.controlPrice.fresh){r.status=HSBI_PREFLIGHT_STALE;r.details="STALE_OR_EXPIRED";return r;}
   if(x.reconciliationConflict||x.activeIntentPresent||x.allocationConflict||(x.appliedActionId==x.intent.expectedActionId&&x.appliedActionPayloadDigest!=x.intent.digest)){r.status=HSBI_PREFLIGHT_CONFLICT;r.details="CONFLICT";return r;}
   if(!x.planningFullyProven||!x.aggregate.valid||x.aggregate.levelCount<2||!x.worstCasePresent||!x.aggregate.runtimeConfirmed||
      !x.catchUp.valid||!x.catchUp.runtimeConfirmed||!x.catchUp.reserveSourceIdentityValid||!x.catchUp.farLossSourceIdentityValid||
      !x.farLossProofPresent||x.proxyOrTestOnly){r.status=HSBI_PREFLIGHT_UNAVAILABLE;r.details="PROOF_UNAVAILABLE";return r;}
   if(x.currentAccount!=x.intent.accountLogin||x.currentSymbol!=x.intent.symbol||x.currentMagic!=x.intent.magic||x.currentCycleId!=x.intent.cycleId||
      x.currentStateRevision!=x.intent.stateRevision){r.details="IDENTITY_OR_REVISION_MISMATCH";return r;}
   if(HSBI_ValidateBrokerProperties(x.broker)!=HSBI_BROKER_PROPERTIES_VALID||!HSBI_ValidateVolume(x.intent.normalizedVolume,x.broker)||
      !HSBI_ValidateTypedControlPrice(x.controlPrice,x.intent.symbol)||MathAbs(x.intent.controlPrice-x.controlPrice.selectedPrice)>HSBI_GridTolerance(x.broker.tickSize)){
      r.details="GRID_OR_PRICE_REJECT";return r;}
   r.status=HSBI_PREFLIGHT_PASS;r.valid=true;r.reason=HSBI_REASON_OK;r.details="PASS";r.digest=x.intent.digest+"|PREFLIGHT_PASS";return r;
}
~~~

### FUNCTION HSBI_IsIntentLifecycleTransitionAllowed

| Field | Individual analysis |
|---|---|
| Function ID | Include/Execution/HSBI_ExecutionPreflight.mqh:35:HSBI_IsIntentLifecycleTransitionAllowed |
| Source | Include/Execution/HSBI_ExecutionPreflight.mqh:35–46 |
| Signature | bool HSBI_IsIntentLifecycleTransitionAllowed(const HSBI_IntentStatus from,const HSBI_IntentStatus to,const bool validOutcome) |
| Inputs | const HSBI_IntentStatus from,const HSBI_IntentStatus to,const bool validOutcome |
| Outputs / Postconditions | error targets from!=COMPLETED;7normalphasebranches;RECONCILING→COMPLETED onlyvalidOutcome |
| Domain | from/to intent enums,validOutcome bool |
| Preconditions | Inputs known; outcome proof независим от bool |
| Guards | 4error targets;from branch sequence;last completion flag |
| Callers | NO_CALLER_FOUND: all74 production source bodies, no dynamic/native proof |
| Dependencies | NONE project functions |
| Normative contract | Docs/HSB.2C_Preflight_and_Lifecycle.md; Docs/07:14–24 |
| Formula IDs | F024/F063 |
| Error IDs | ERR016/049 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | INTENT_TOPOLOGY_ONLY |
| Limitations / side effects | Unknown from can enter error target; no durable/actual postcondition; topology not execution |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{
   if(to==HSBI_INTENT_REJECTED||to==HSBI_INTENT_EXPIRED||to==HSBI_INTENT_INVALIDATED||to==HSBI_INTENT_CONFLICT)return from!=HSBI_INTENT_COMPLETED;
   if(from==HSBI_INTENT_CREATED)return to==HSBI_INTENT_PREFLIGHT_PASSED;
   if(from==HSBI_INTENT_PREFLIGHT_PASSED)return to==HSBI_INTENT_PERSISTED;
   if(from==HSBI_INTENT_PERSISTED)return to==HSBI_INTENT_DISPATCH_BLOCKED;
   if(from==HSBI_INTENT_DISPATCH_BLOCKED)return to==HSBI_INTENT_OUTCOME_PENDING||to==HSBI_INTENT_RECONCILING;
   if(from==HSBI_INTENT_OUTCOME_PENDING)return to==HSBI_INTENT_OUTCOME_RECEIVED||to==HSBI_INTENT_RECONCILING;
   if(from==HSBI_INTENT_OUTCOME_RECEIVED)return to==HSBI_INTENT_RECONCILING;
   if(from==HSBI_INTENT_RECONCILING)return to==HSBI_INTENT_COMPLETED&&validOutcome;
   return false;
}
~~~

### FUNCTION HSBI_IntentRetryAllowed

| Field | Individual analysis |
|---|---|
| Function ID | Include/Execution/HSBI_ExecutionPreflight.mqh:47:HSBI_IntentRetryAllowed |
| Source | Include/Execution/HSBI_ExecutionPreflight.mqh:47–48 |
| Signature | bool HSBI_IntentRetryAllowed(const HSBI_ExecutionIntent &x,const ulong retryActionId) |
| Inputs | const HSBI_ExecutionIntent &x,const ulong retryActionId |
| Outputs / Postconditions | same action && status oneofPENDING/RECONCILING/BLOCKED |
| Domain | retryAction ulong,statusenum |
| Preconditions | Intent shape validated,current broker history checked caller |
| Guards | Action equality;3status whitelist |
| Callers | NO_CALLER_FOUND: all74 production source bodies, no dynamic/native proof |
| Dependencies | NONE project functions |
| Normative contract | Docs/07:17–24 |
| Formula IDs | F024/F053 |
| Error IDs | ERR016/017 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | LOCAL_RETRY_NOT_FULL_GATE |
| Limitations / side effects | Не explicitAction>0 внутриhelper; не history completed/pending uniqueness/ownership refresh |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{return retryActionId==x.expectedActionId&&(x.status==HSBI_INTENT_OUTCOME_PENDING||x.status==HSBI_INTENT_RECONCILING||x.status==HSBI_INTENT_DISPATCH_BLOCKED);}
~~~

### FUNCTION HSBI_EvaluateOwnership

| Field | Individual analysis |
|---|---|
| Function ID | Include/Execution/HSBI_OwnershipGuardTypes.mqh:8:HSBI_EvaluateOwnership |
| Source | Include/Execution/HSBI_OwnershipGuardTypes.mqh:8–8 |
| Signature | HSBI_OwnershipGuardResult HSBI_EvaluateOwnership(const HSBI_OwnershipGuardInput &x) |
| Inputs | const HSBI_OwnershipGuardInput &x |
| Outputs / Postconditions | 7mismatch bits;any mismatch allowedfalse/reconciletrue, elseallowedtrue |
| Domain | namespace,role/direction,ticket/revision,volume lots |
| Preconditions | Expected независимая; descriptors finite/valid separate |
| Guards | SamePositionOwner;role;direction;absvol<=eps;revision;plan/action nonzero;ticketpositiveequal |
| Callers | NO_CALLER_FOUND: all74 production source bodies, no dynamic/native proof |
| Dependencies | HSBI_SamePositionOwner @ Include/Execution/HSBI_OwnershipGuardTypes.mqh:8 |
| Normative contract | Docs/02:23–34; Docs/07:11–12 |
| Formula IDs | F036/F053/F062 |
| Error IDs | ERR012/013/049 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | LOCAL_OWNERSHIP_MATCH_PARTIAL |
| Limitations / side effects | VolumeNaN не rejected abs>eps; equal unknown enums canmatch; DTO consistency not independent provider |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{HSBI_OwnershipGuardResult r;r.allowed=true;r.reason=HSBI_REASON_OK;r.mismatchMask=0;r.requiresReconciliation=false;if(!HSBI_SamePositionOwner(x.expectedIdentity,x.actualIdentity)){r.mismatchMask|=1;}if(x.expectedRole!=x.actualRole)r.mismatchMask|=2;if(x.expectedDirection!=x.actualDirection)r.mismatchMask|=4;if(MathAbs(x.expectedVolume-x.actualVolume)>0.0000001)r.mismatchMask|=8;if(x.expectedStateRevision!=x.actualStateRevision)r.mismatchMask|=16;if(x.planId==0||x.actionId==0)r.mismatchMask|=32;if(x.expectedTicket==0||x.actualTicket!=x.expectedTicket)r.mismatchMask|=64;if(r.mismatchMask!=0){r.allowed=false;r.reason=HSBI_REASON_INVALID_IDENTITY;r.requiresReconciliation=true;}return r;}
~~~

### FUNCTION HSBI_TicketMatchesObservation

| Field | Individual analysis |
|---|---|
| Function ID | Include/Execution/HSBI_OwnershipGuardTypes.mqh:9:HSBI_TicketMatchesObservation |
| Source | Include/Execution/HSBI_OwnershipGuardTypes.mqh:9–12 |
| Signature | bool HSBI_TicketMatchesObservation(const HSBI_PositionDescriptor &expected,const HSBI_PositionDescriptor &actual) |
| Inputs | const HSBI_PositionDescriptor &expected,const HSBI_PositionDescriptor &actual |
| Outputs / Postconditions | expectedTicket>0/equal+sameowner+identifier/role equal |
| Domain | ticketpositive,identity/identifier/role |
| Preconditions | Expected owner независим, descriptors validated |
| Guards | 5groups comparisons |
| Callers | NO_CALLER_FOUND: all74 production source bodies, no dynamic/native proof |
| Dependencies | HSBI_SamePositionOwner @ Include/Execution/HSBI_OwnershipGuardTypes.mqh:11 |
| Normative contract | Docs/02:19–34 |
| Formula IDs | F053/F062 |
| Error IDs | ERR012/013 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | LOCAL_OBSERVATION_MATCH |
| Limitations / side effects | Не direction/volume/time proof; no actual observation acquisition |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{
   return expected.ticket>0&&actual.ticket==expected.ticket&&HSBI_SamePositionOwner(expected.identity,actual.identity)&&expected.identifier==actual.identifier&&expected.role==actual.role;
}
~~~

### FUNCTION HSBI_IsActualBigCoreResidual

| Field | Individual analysis |
|---|---|
| Function ID | Include/Execution/HSBI_OwnershipGuardTypes.mqh:13:HSBI_IsActualBigCoreResidual |
| Source | Include/Execution/HSBI_OwnershipGuardTypes.mqh:13–16 |
| Signature | bool HSBI_IsActualBigCoreResidual(const HSBI_PositionDescriptor &position,const ulong originalIdentifier) |
| Inputs | const HSBI_PositionDescriptor &position,const ulong originalIdentifier |
| Outputs / Postconditions | roleBIG_CORE &&2ids==original &&actualVolume>0 |
| Domain | BigCore role,originalIdentifier ulong,actual lots |
| Preconditions | Actual source/history proves residual; IDnonzero caller |
| Guards | 4clauses |
| Callers | HSBI_ValidateNewFarSource @ Include/Planning/HSBI_NewFarSolver.mqh:72 |
| Dependencies | NONE project functions |
| Normative contract | Docs/02:13,27; Docs/14_NEW_FAR_SOLVER_SPECIFICATION_RU.md |
| Formula IDs | F027/F028/F053 |
| Error IDs | ERR013/041/045 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | LOCAL_RESIDUAL_FILTER_ONLY |
| Limitations / side effects | Original0 maymatch2zeros; Infinity positive; naming actual не broker evidence |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{
   return position.role==HSBI_ROLE_BIG_CORE&&position.identifier==originalIdentifier&&position.identity.positionIdentifier==originalIdentifier&&position.actualVolume>0.0;
}
~~~

### FUNCTION HSBI_ValidateReserveAllocationSource

| Field | Individual analysis |
|---|---|
| Function ID | Include/Money/HSBI_ReserveAllocationTypes.mqh:15:HSBI_ValidateReserveAllocationSource |
| Source | Include/Money/HSBI_ReserveAllocationTypes.mqh:15–24 |
| Signature | bool HSBI_ValidateReserveAllocationSource(const HSBI_ReserveAllocationSource &x) |
| Inputs | const HSBI_ReserveAllocationSource &x |
| Outputs / Postconditions | valid flags/keys/IDs/positive allocatable +finite/nonnegative +sum<=net |
| Domain | all7money finite/nonnegative,IDs>0,keysnonempty |
| Preconditions | Independent authoritative immutable allocation/journal от caller |
| Guards | 3flags;2keys;3ids;netpositive;7finite;6nonnegative;total<=net+epsilon |
| Callers | HSBI_EvaluateReserveCatchUp @ Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:44; HSBI_ValidateRuntimeDecisionContext @ Include/Runtime/HSBI_RuntimeDecisionValidator.mqh:24 |
| Dependencies | HSBI_IsFiniteNumber @ Include/Money/HSBI_ReserveAllocationTypes.mqh:19; HSBI_IsFiniteNumber @ Include/Money/HSBI_ReserveAllocationTypes.mqh:19; HSBI_IsFiniteNumber @ Include/Money/HSBI_ReserveAllocationTypes.mqh:19; HSBI_IsFiniteNumber @ Include/Money/HSBI_ReserveAllocationTypes.mqh:20; HSBI_IsFiniteNumber @ Include/Money/HSBI_ReserveAllocationTypes.mqh:20; HSBI_IsFiniteNumber @ Include/Money/HSBI_ReserveAllocationTypes.mqh:20; HSBI_IsFiniteNumber @ Include/Money/HSBI_ReserveAllocationTypes.mqh:21 |
| Normative contract | Docs/08:12–24; Docs/32_RESERVE_ALLOCATION_CONSUMPTION_RU.md |
| Formula IDs | F012/F013/F019/F064 |
| Error IDs | ERR005/006/007/033/048 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | LOCAL_ALLOCATION_BOUND |
| Limitations / side effects | supplied flags не authoritative ledger; no equality committed total; double summing consumed meaning requires D01 mapping |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{
   if(!x.valid||!x.allocationConfirmed||!x.sourceReconciled||x.sourceDealKey==""||x.sourceAllocationKey==""||
      x.sourceDealId==0||x.allocationEventId==0||x.allocationPolicyVersion==0||x.allocatableNet<=0.0)return false;
   if(!HSBI_IsFiniteNumber(x.allocatableNet)||!HSBI_IsFiniteNumber(x.reserveAllocated)||!HSBI_IsFiniteNumber(x.partialFarAllocated)||
      !HSBI_IsFiniteNumber(x.transitionAllocated)||!HSBI_IsFiniteNumber(x.carryAllocated)||!HSBI_IsFiniteNumber(x.residualAllocated)||
      !HSBI_IsFiniteNumber(x.alreadyConsumed)||x.reserveAllocated<0.0||x.partialFarAllocated<0.0||x.transitionAllocated<0.0||
      x.carryAllocated<0.0||x.residualAllocated<0.0||x.alreadyConsumed<0.0)return false;
   return x.reserveAllocated+x.partialFarAllocated+x.transitionAllocated+x.carryAllocated+x.residualAllocated+x.alreadyConsumed<=x.allocatableNet+1e-10;
}
~~~

### FUNCTION HSBI_ValidateReserveConsumption

| Field | Individual analysis |
|---|---|
| Function ID | Include/Money/HSBI_ReserveAllocationTypes.mqh:25:HSBI_ValidateReserveConsumption |
| Source | Include/Money/HSBI_ReserveAllocationTypes.mqh:25–26 |
| Signature | bool HSBI_ValidateReserveConsumption(const HSBI_ReserveConsumptionKey &x,const ulong planId,const ulong revision) |
| Inputs | const HSBI_ReserveConsumptionKey &x,const ulong planId,const ulong revision |
| Outputs / Postconditions | nonemptykeys/event/consumer and requestedplan/revision equality |
| Domain | 2keys,textconsumer,event>0,plan/revulong |
| Preconditions | Keys bound authoritative allocation отдельно |
| Guards | 6conjuncts |
| Callers | HSBI_EvaluateReserveCatchUp @ Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:47; HSBI_ValidateRuntimeDecisionContext @ Include/Runtime/HSBI_RuntimeDecisionValidator.mqh:25 |
| Dependencies | NONE project functions |
| Normative contract | Docs/08:15–24; Docs/07:9 |
| Formula IDs | F015/F019/F053 |
| Error IDs | ERR007/033/048 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | KEY_SHAPE_NOT_CONSUMPTION_PERMISSION |
| Limitations / side effects | Не cross-bind key.sourceAllocationKey/sourceDealKey с allocation DTO; no amount/ownerbalance or explicitplan>0 |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{return x.sourceDealKey!=""&&x.sourceAllocationKey!=""&&x.consumptionEventId>0&&x.consumer!=""&&x.planId==planId&&x.stateRevision==revision;}
~~~

### FUNCTION HSBI_IsDuplicateReserveConsumption

| Field | Individual analysis |
|---|---|
| Function ID | Include/Money/HSBI_ReserveAllocationTypes.mqh:27:HSBI_IsDuplicateReserveConsumption |
| Source | Include/Money/HSBI_ReserveAllocationTypes.mqh:27–28 |
| Signature | bool HSBI_IsDuplicateReserveConsumption(const HSBI_ReserveConsumptionKey &a,const HSBI_ReserveConsumptionKey &b) |
| Inputs | const HSBI_ReserveConsumptionKey &a,const HSBI_ReserveConsumptionKey &b |
| Outputs / Postconditions | true iff6fields equal; zero delta |
| Domain | 6keyfields |
| Preconditions | Independent immutable journal key fromcaller |
| Guards | sourceDeal/sourceAllocation/plan/revision/event/consumer equal |
| Callers | HSBI_ReserveConsumptionConflict @ Include/Money/HSBI_ReserveAllocationTypes.mqh:30; HSBI_EvaluateReserveCatchUp @ Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:48 |
| Dependencies | NONE project functions |
| Normative contract | Docs/08:15–24 |
| Formula IDs | F019/F053/F057 |
| Error IDs | ERR007/033/048 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | LOCAL_KEY_EQUALITY |
| Limitations / side effects | Amount отсутствует в DTO, no full payload money replay proof; no global history |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{return a.sourceDealKey==b.sourceDealKey&&a.sourceAllocationKey==b.sourceAllocationKey&&a.planId==b.planId&&a.stateRevision==b.stateRevision&&a.consumptionEventId==b.consumptionEventId&&a.consumer==b.consumer;}
~~~

### FUNCTION HSBI_ReserveConsumptionConflict

| Field | Individual analysis |
|---|---|
| Function ID | Include/Money/HSBI_ReserveAllocationTypes.mqh:29:HSBI_ReserveConsumptionConflict |
| Source | Include/Money/HSBI_ReserveAllocationTypes.mqh:29–30 |
| Signature | bool HSBI_ReserveConsumptionConflict(const HSBI_ReserveConsumptionKey &a,const HSBI_ReserveConsumptionKey &b) |
| Inputs | const HSBI_ReserveConsumptionKey &a,const HSBI_ReserveConsumptionKey &b |
| Outputs / Postconditions | samealloc OR sameevent AND notexactduplicate |
| Domain | 2consumption keys |
| Preconditions | Namespace/global event scope approved separately |
| Guards | shared key/event;!duplicate |
| Callers | HSBI_EvaluateReserveCatchUp @ Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:49 |
| Dependencies | HSBI_IsDuplicateReserveConsumption @ Include/Money/HSBI_ReserveAllocationTypes.mqh:30 |
| Normative contract | Docs/08:15–24; D08 proposed |
| Formula IDs | F019/F053/F057 |
| Error IDs | ERR007/013/033 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | LOCAL_CONFLICT_POLICY_LIMITED |
| Limitations / side effects | Слишком broad event namespace может collision без account scoping; prerequisite D08; не доказан runtime incident |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{return (a.sourceAllocationKey==b.sourceAllocationKey||a.consumptionEventId==b.consumptionEventId)&&!HSBI_IsDuplicateReserveConsumption(a,b);}
~~~

### FUNCTION HSBI_ReserveAllocationSourceDigest

| Field | Individual analysis |
|---|---|
| Function ID | Include/Money/HSBI_ReserveAllocationTypes.mqh:31:HSBI_ReserveAllocationSourceDigest |
| Source | Include/Money/HSBI_ReserveAllocationTypes.mqh:31–32 |
| Signature | string HSBI_ReserveAllocationSourceDigest(const HSBI_ReserveAllocationSource &x) |
| Inputs | const HSBI_ReserveAllocationSource &x |
| Outputs / Postconditions | fixed string identity+allbudgetscalarfields |
| Domain | 5bucketmoney+consumed/net8dec,keys/IDs |
| Preconditions | DTO shape validated and independently authoritative separately |
| Guards | Нет validationguards |
| Callers | HSBI_EvaluateReserveCatchUp @ Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:53; HSBI_NewFarInputDigest @ Include/Planning/HSBI_NewFarSolver.mqh:57; HSBI_RuntimeDecisionContextDigest @ Include/Runtime/HSBI_RuntimeDecisionTypes.mqh:17; HSBI_ValidateRestartedRuntimeState @ Include/Runtime/HSBI_RuntimeRestartValidator.mqh:15; HSBI_ValidateRestartedRuntimeState @ Include/Runtime/HSBI_RuntimeRestartValidator.mqh:15 |
| Dependencies | HSBI_UlongToString @ Include/Money/HSBI_ReserveAllocationTypes.mqh:32; HSBI_UlongToString @ Include/Money/HSBI_ReserveAllocationTypes.mqh:32; HSBI_UlongToString @ Include/Money/HSBI_ReserveAllocationTypes.mqh:32 |
| Normative contract | Docs/08:12–24; NUM-CODEC proposed |
| Formula IDs | F016/F042/F057/F060 |
| Error IDs | ERR003/007/040/048 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | ALLOCATION_FINGERPRINT_ONLY |
| Limitations / side effects | Не raw exact codec; flags notincluded; digest self-derived not ledger authority |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{return x.sourceDealKey+"|"+x.sourceAllocationKey+"|"+HSBI_UlongToString(x.sourceDealId)+"|"+HSBI_UlongToString(x.allocationEventId)+"|"+HSBI_UlongToString(x.allocationPolicyVersion)+"|"+DoubleToString(x.allocatableNet,8)+"|"+DoubleToString(x.reserveAllocated,8)+"|"+DoubleToString(x.partialFarAllocated,8)+"|"+DoubleToString(x.transitionAllocated,8)+"|"+DoubleToString(x.carryAllocated,8)+"|"+DoubleToString(x.residualAllocated,8)+"|"+DoubleToString(x.alreadyConsumed,8);}
~~~

### FUNCTION HSBI_ReserveConsumptionKeyDigest

| Field | Individual analysis |
|---|---|
| Function ID | Include/Money/HSBI_ReserveAllocationTypes.mqh:33:HSBI_ReserveConsumptionKeyDigest |
| Source | Include/Money/HSBI_ReserveAllocationTypes.mqh:33–34 |
| Signature | string HSBI_ReserveConsumptionKeyDigest(const HSBI_ReserveConsumptionKey &x) |
| Inputs | const HSBI_ReserveConsumptionKey &x |
| Outputs / Postconditions | concat allkeyfields |
| Domain | keys,plan/rev/eventIDs,consumer |
| Preconditions | Not amount receipt; valid shape separately |
| Guards | Нет guards |
| Callers | HSBI_EvaluateReserveCatchUp @ Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:54; HSBI_NewFarInputDigest @ Include/Planning/HSBI_NewFarSolver.mqh:57; HSBI_RuntimeDecisionContextDigest @ Include/Runtime/HSBI_RuntimeDecisionTypes.mqh:17; HSBI_ValidateRestartedRuntimeState @ Include/Runtime/HSBI_RuntimeRestartValidator.mqh:15; HSBI_ValidateRestartedRuntimeState @ Include/Runtime/HSBI_RuntimeRestartValidator.mqh:15 |
| Dependencies | HSBI_UlongToString @ Include/Money/HSBI_ReserveAllocationTypes.mqh:34; HSBI_UlongToString @ Include/Money/HSBI_ReserveAllocationTypes.mqh:34; HSBI_UlongToString @ Include/Money/HSBI_ReserveAllocationTypes.mqh:34 |
| Normative contract | Docs/08:15–24; NUM-CODEC proposed |
| Formula IDs | F019/F042/F053/F060 |
| Error IDs | ERR003/007/048 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | KEY_FINGERPRINT_ONLY |
| Limitations / side effects | No amount inkey; не доказательство authoritative balance/replay receipt |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{return x.sourceDealKey+"|"+x.sourceAllocationKey+"|"+HSBI_UlongToString(x.planId)+"|"+HSBI_UlongToString(x.stateRevision)+"|"+HSBI_UlongToString(x.consumptionEventId)+"|"+x.consumer;}
~~~

### FUNCTION HSBI_ValidateMoneyProofIdentity

| Field | Individual analysis |
|---|---|
| Function ID | Include/Money/HSBI_MoneyProofIdentity.mqh:10:HSBI_ValidateMoneyProofIdentity |
| Source | Include/Money/HSBI_MoneyProofIdentity.mqh:10–15 |
| Signature | bool HSBI_ValidateMoneyProofIdentity(const HSBI_MoneyProofIdentity &x) |
| Inputs | const HSBI_MoneyProofIdentity &x |
| Outputs / Postconditions | 12scalarconjuncts true/false |
| Domain | account>0,symbol,magic,cycle,pos,deal,event,snapshot,plan,rev;role/direction!=NONE |
| Preconditions | Independent provider expected separately |
| Guards | allnonzero/nonempty checks,role/direction!=NONE |
| Callers | HSBI_ValidateReserveSourceProof @ Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:27; HSBI_ValidateFarLossProof @ Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:33; HSBI_ValidateRuntimeDecisionContext @ Include/Runtime/HSBI_RuntimeDecisionValidator.mqh:22; HSBI_ValidateRuntimeDecisionContext @ Include/Runtime/HSBI_RuntimeDecisionValidator.mqh:23 |
| Dependencies | NONE project functions |
| Normative contract | Docs/02:19–34; Docs/08:6–24 |
| Formula IDs | F036/F053/F062 |
| Error IDs | ERR013/033/049 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | PROOF_ID_SHAPE_ONLY |
| Limitations / side effects | Не closed enumknownrole/knownDirection; no provenance/authenticity/contentbinding |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{
   return x.accountLogin>0&&x.symbol!=""&&x.magic!=0&&x.cycleId>0&&x.positionIdentifier>0&&
      x.role!=HSBI_ROLE_NONE&&x.direction!=HSBI_DIRECTION_NONE&&x.sourceDealId>0&&x.sourceEventId>0&&
      x.snapshotId>0&&x.planId>0&&x.stateRevision>0;
}
~~~

### FUNCTION HSBI_IsSameMoneyProofIdentity

| Field | Individual analysis |
|---|---|
| Function ID | Include/Money/HSBI_MoneyProofIdentity.mqh:16:HSBI_IsSameMoneyProofIdentity |
| Source | Include/Money/HSBI_MoneyProofIdentity.mqh:16–22 |
| Signature | bool HSBI_IsSameMoneyProofIdentity(const HSBI_MoneyProofIdentity &a,const HSBI_MoneyProofIdentity &b) |
| Inputs | const HSBI_MoneyProofIdentity &a,const HSBI_MoneyProofIdentity &b |
| Outputs / Postconditions | true iffall12equalities |
| Domain | namespace+role/direction+source/event/snapshot/plan/rev |
| Preconditions | Both validated;expected independently obtained |
| Guards | 12exactequalities |
| Callers | HSBI_ValidateReserveSourceProof @ Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:27; HSBI_ValidateFarLossProof @ Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:33 |
| Dependencies | NONE project functions |
| Normative contract | Docs/02:23–34; D08 proposed |
| Formula IDs | F053/F062 |
| Error IDs | ERR013/033/048 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | LOCAL_PROOF_ID_EQUALITY |
| Limitations / side effects | Presented copied intoexpected triviallymatches; no amount/currency/precision payload |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{
   return a.accountLogin==b.accountLogin&&a.symbol==b.symbol&&a.magic==b.magic&&a.cycleId==b.cycleId&&
      a.positionIdentifier==b.positionIdentifier&&a.role==b.role&&a.direction==b.direction&&
      a.sourceDealId==b.sourceDealId&&a.sourceEventId==b.sourceEventId&&a.snapshotId==b.snapshotId&&
      a.planId==b.planId&&a.stateRevision==b.stateRevision;
}
~~~

### FUNCTION HSBI_MoneyProofIdentityDigest

| Field | Individual analysis |
|---|---|
| Function ID | Include/Money/HSBI_MoneyProofIdentity.mqh:23:HSBI_MoneyProofIdentityDigest |
| Source | Include/Money/HSBI_MoneyProofIdentity.mqh:23–29 |
| Signature | string HSBI_MoneyProofIdentityDigest(const HSBI_MoneyProofIdentity &x) |
| Inputs | const HSBI_MoneyProofIdentity &x |
| Outputs / Postconditions | fixedorder12fields |
| Domain | IDslong/ulong,role/directionint,symboltext |
| Preconditions | Not complete money proof payload; no authorityinside |
| Guards | Нет guards |
| Callers | HSBI_EvaluateReserveCatchUp @ Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:51; HSBI_EvaluateReserveCatchUp @ Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:52 |
| Dependencies | HSBI_UlongToString @ Include/Money/HSBI_MoneyProofIdentity.mqh:25; HSBI_UlongToString @ Include/Money/HSBI_MoneyProofIdentity.mqh:26; HSBI_UlongToString @ Include/Money/HSBI_MoneyProofIdentity.mqh:27; HSBI_UlongToString @ Include/Money/HSBI_MoneyProofIdentity.mqh:27; HSBI_UlongToString @ Include/Money/HSBI_MoneyProofIdentity.mqh:27; HSBI_UlongToString @ Include/Money/HSBI_MoneyProofIdentity.mqh:28; HSBI_UlongToString @ Include/Money/HSBI_MoneyProofIdentity.mqh:28 |
| Normative contract | Docs/16:8; D08/NUM-CODEC proposed |
| Formula IDs | F042/F053/F060 |
| Error IDs | ERR003/013/033/048 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | IDENTITY_FINGERPRINT_ONLY |
| Limitations / side effects | Не includes amount/currency/precision/contentprovider; не canonical typedcodec |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{
   return LongToString(x.accountLogin)+"|"+x.symbol+"|"+LongToString(x.magic)+"|"+HSBI_UlongToString(x.cycleId)+"|"+
      HSBI_UlongToString(x.positionIdentifier)+"|"+IntegerToString((int)x.role)+"|"+IntegerToString((int)x.direction)+"|"+
      HSBI_UlongToString(x.sourceDealId)+"|"+HSBI_UlongToString(x.sourceEventId)+"|"+HSBI_UlongToString(x.snapshotId)+"|"+
      HSBI_UlongToString(x.planId)+"|"+HSBI_UlongToString(x.stateRevision);
}
~~~


## R2 — индивидуальные money/diagnostics/action функции, продолжение без замены43 карт

### FUNCTION HSBI_IsFiniteNumber

| Field | Individual analysis |
|---|---|
| Function ID | Include/Money/HSBI_BrokerMoneyTypes.mqh:10:HSBI_IsFiniteNumber |
| Source | Include/Money/HSBI_BrokerMoneyTypes.mqh:10–10 |
| Signature | bool HSBI_IsFiniteNumber(const double value) |
| Inputs | const double value |
| Outputs / Postconditions | Return MathIsValidNumber(value) |
| Domain | binary64 double |
| Preconditions | Native MathIsValidNumber semantics; not executed here |
| Guards | Delegates native finite check |
| Callers | HSBI_ValidateExecutionIntentStructure @ Include/Execution/HSBI_ExecutionIntent.mqh:32; HSBI_ValidateExecutionIntentStructure @ Include/Execution/HSBI_ExecutionIntent.mqh:32; HSBI_ValidateExecutionIntentStructure @ Include/Execution/HSBI_ExecutionIntent.mqh:32; HSBI_ValidateAllocationPolicy @ Include/Money/HSBI_AllocationPolicyTypes.mqh:19; HSBI_ValidateAllocationPolicy @ Include/Money/HSBI_AllocationPolicyTypes.mqh:19; HSBI_ValidateAllocationPolicy @ Include/Money/HSBI_AllocationPolicyTypes.mqh:20; HSBI_ValidateAllocationPolicy @ Include/Money/HSBI_AllocationPolicyTypes.mqh:20; HSBI_EvaluateBasketMoney @ Include/Money/HSBI_BasketMoneyEvaluator.mqh:18; HSBI_EvaluateBasketMoney @ Include/Money/HSBI_BasketMoneyEvaluator.mqh:18; HSBI_EvaluateBasketMoney @ Include/Money/HSBI_BasketMoneyEvaluator.mqh:18; HSBI_CalculateProjectedMargin @ Include/Money/HSBI_BrokerMarginModel.mqh:14; HSBI_CalculateProjectedProfit @ Include/Money/HSBI_BrokerMoneyModel.mqh:12; HSBI_CalculateProjectedProfit @ Include/Money/HSBI_BrokerMoneyModel.mqh:12; HSBI_CalculateProjectedProfit @ Include/Money/HSBI_BrokerMoneyModel.mqh:17; HSBI_ValidateBrokerProperties @ Include/Money/HSBI_BrokerMoneyTypes.mqh:16; HSBI_ValidateBrokerProperties @ Include/Money/HSBI_BrokerMoneyTypes.mqh:16; HSBI_ValidateBrokerProperties @ Include/Money/HSBI_BrokerMoneyTypes.mqh:16; HSBI_ValidateBrokerProperties @ Include/Money/HSBI_BrokerMoneyTypes.mqh:16; HSBI_ValidateBrokerProperties @ Include/Money/HSBI_BrokerMoneyTypes.mqh:16; HSBI_ValidateBrokerProperties @ Include/Money/HSBI_BrokerMoneyTypes.mqh:16; HSBI_ValidateBrokerProperties @ Include/Money/HSBI_BrokerMoneyTypes.mqh:16; HSBI_EvaluateCatchUp @ Include/Money/HSBI_CatchUpModel.mqh:10; HSBI_EvaluateCatchUp @ Include/Money/HSBI_CatchUpModel.mqh:10; HSBI_EvaluateCatchUp @ Include/Money/HSBI_CatchUpModel.mqh:10; HSBI_EvaluateCatchUp @ Include/Money/HSBI_CatchUpModel.mqh:10; HSBI_EvaluateCatchUp @ Include/Money/HSBI_CatchUpModel.mqh:10; HSBI_EvaluateCatchUp @ Include/Money/HSBI_CatchUpModel.mqh:10; HSBI_ValidateCostSnapshot @ Include/Money/HSBI_CostModel.mqh:8; HSBI_ValidateCostSnapshot @ Include/Money/HSBI_CostModel.mqh:8; HSBI_ValidateCostSnapshot @ Include/Money/HSBI_CostModel.mqh:8; HSBI_ValidateCostSnapshot @ Include/Money/HSBI_CostModel.mqh:8; HSBI_ValidateCostSnapshot @ Include/Money/HSBI_CostModel.mqh:8; HSBI_TryActualDealNet @ Include/Money/HSBI_CostModel.mqh:13; HSBI_TryActualDealNet @ Include/Money/HSBI_CostModel.mqh:13; HSBI_TryProjectedNetMoney @ Include/Money/HSBI_CostModel.mqh:17; HSBI_TryProjectedNetMoney @ Include/Money/HSBI_CostModel.mqh:17; HSBI_TryProjectedNetMoney @ Include/Money/HSBI_CostModel.mqh:18; HSBI_EvaluateProjectedLegMargin @ Include/Money/HSBI_LevelMarginEvaluator.mqh:10; HSBI_EvaluateProjectedLegMoney @ Include/Money/HSBI_LevelMoneyEvaluator.mqh:13; HSBI_ValidateReserveAllocationSource @ Include/Money/HSBI_ReserveAllocationTypes.mqh:19; HSBI_ValidateReserveAllocationSource @ Include/Money/HSBI_ReserveAllocationTypes.mqh:19; HSBI_ValidateReserveAllocationSource @ Include/Money/HSBI_ReserveAllocationTypes.mqh:19; HSBI_ValidateReserveAllocationSource @ Include/Money/HSBI_ReserveAllocationTypes.mqh:20; HSBI_ValidateReserveAllocationSource @ Include/Money/HSBI_ReserveAllocationTypes.mqh:20; HSBI_ValidateReserveAllocationSource @ Include/Money/HSBI_ReserveAllocationTypes.mqh:20; HSBI_ValidateReserveAllocationSource @ Include/Money/HSBI_ReserveAllocationTypes.mqh:21; HSBI_ValidateReserveSourceProof @ Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:27; HSBI_ValidateFarLossProof @ Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:32; HSBI_EvaluateReserveCatchUp @ Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:61; HSBI_EvaluateReserveCatchUp @ Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:61; HSBI_EvaluateReserveCatchUp @ Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:61; HSBI_EvaluateReserveCatchUp @ Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:62; HSBI_EvaluateReserveCatchUp @ Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:62; HSBI_IsPriceOnTickGrid @ Include/Planning/HSBI_BrokerGrid.mqh:10; HSBI_IsPriceOnTickGrid @ Include/Planning/HSBI_BrokerGrid.mqh:10; HSBI_NormalizePriceToTick @ Include/Planning/HSBI_BrokerGrid.mqh:15; HSBI_NormalizePriceToTick @ Include/Planning/HSBI_BrokerGrid.mqh:15; HSBI_PriceDistanceInTicks @ Include/Planning/HSBI_BrokerGrid.mqh:20; HSBI_PriceDistanceInTicks @ Include/Planning/HSBI_BrokerGrid.mqh:20; HSBI_IsVolumeOnGrid @ Include/Planning/HSBI_BrokerGrid.mqh:23; HSBI_IsVolumeOnGrid @ Include/Planning/HSBI_BrokerGrid.mqh:23; HSBI_FloorVolumeToStep @ Include/Planning/HSBI_BrokerGrid.mqh:26; HSBI_FloorVolumeToStep @ Include/Planning/HSBI_BrokerGrid.mqh:26; HSBI_CeilVolumeToStep @ Include/Planning/HSBI_BrokerGrid.mqh:27; HSBI_CeilVolumeToStep @ Include/Planning/HSBI_BrokerGrid.mqh:27; HSBI_ValidateVolume @ Include/Planning/HSBI_BrokerGrid.mqh:35; HSBI_ValidateTypedControlPrice @ Include/Planning/HSBI_ControlPrices.mqh:19; HSBI_ValidateTypedControlPrice @ Include/Planning/HSBI_ControlPrices.mqh:19; HSBI_ValidateTypedControlPrice @ Include/Planning/HSBI_ControlPrices.mqh:19; HSBI_CalculateFutureSmallDepth @ Include/Planning/HSBI_FutureSmallSolver.mqh:7; HSBI_CalculateFutureSmallDepth @ Include/Planning/HSBI_FutureSmallSolver.mqh:7; HSBI_CalculateFutureSmallDepth @ Include/Planning/HSBI_FutureSmallSolver.mqh:7; HSBI_CalculateFutureSmallDepth @ Include/Planning/HSBI_FutureSmallSolver.mqh:8; HSBI_CalculateFutureSmallDepth @ Include/Planning/HSBI_FutureSmallSolver.mqh:9; HSBI_ValidateLevelMarket @ Include/Planning/HSBI_FutureSmallSolver.mqh:21; HSBI_ValidateLevelMarket @ Include/Planning/HSBI_FutureSmallSolver.mqh:21; HSBI_ValidateLevelMarket @ Include/Planning/HSBI_FutureSmallSolver.mqh:21; HSBI_ValidateRecoverySlope @ Include/Planning/HSBI_GeometrySolver.mqh:8; HSBI_ValidateRecoverySlope @ Include/Planning/HSBI_GeometrySolver.mqh:8; HSBI_ValidateRecoverySlope @ Include/Planning/HSBI_GeometrySolver.mqh:8; HSBI_ValidateRecoverySlope @ Include/Planning/HSBI_GeometrySolver.mqh:8; HSBI_ValidateRecoverySlope @ Include/Planning/HSBI_GeometrySolver.mqh:10; HSBI_EvaluateRecoveryMoneyDirection @ Include/Planning/HSBI_GeometrySolver.mqh:17; HSBI_EvaluateRecoveryMoneyDirection @ Include/Planning/HSBI_GeometrySolver.mqh:17; HSBI_SolveBigGeometry @ Include/Planning/HSBI_GeometrySolver.mqh:26; HSBI_SolveBigGeometry @ Include/Planning/HSBI_GeometrySolver.mqh:26; HSBI_SolveBigGeometry @ Include/Planning/HSBI_GeometrySolver.mqh:26; HSBI_SolveBigGeometry @ Include/Planning/HSBI_GeometrySolver.mqh:29; HSBI_SolveBigGeometry @ Include/Planning/HSBI_GeometrySolver.mqh:29; HSBI_SolveBigGeometry @ Include/Planning/HSBI_GeometrySolver.mqh:29; HSBI_SolveNewFar @ Include/Planning/HSBI_NewFarSolver.mqh:107; HSBI_EvaluateFutureSmallRisk @ Include/Risk/HSBI_FutureSmallRiskEvaluator.mqh:42; HSBI_EvaluateFutureSmallRisk @ Include/Risk/HSBI_FutureSmallRiskEvaluator.mqh:42; HSBI_EvaluateFutureSmallRisk @ Include/Risk/HSBI_FutureSmallRiskEvaluator.mqh:43; HSBI_EvaluateNewFarGates @ Include/Risk/HSBI_NewFarGateTypes.mqh:11; HSBI_EvaluateNewFarGates @ Include/Risk/HSBI_NewFarGateTypes.mqh:11; HSBI_EvaluateNewFarGates @ Include/Risk/HSBI_NewFarGateTypes.mqh:11; HSBI_EvaluateNewFarGates @ Include/Risk/HSBI_NewFarGateTypes.mqh:11; HSBI_EvaluateNewFarGates @ Include/Risk/HSBI_NewFarGateTypes.mqh:13; HSBI_EvaluateNewFarGates @ Include/Risk/HSBI_NewFarGateTypes.mqh:14; HSBI_EvaluateNewFarGates @ Include/Risk/HSBI_NewFarGateTypes.mqh:14; HSBI_EvaluateNewFarGates @ Include/Risk/HSBI_NewFarGateTypes.mqh:15 |
| Dependencies | NONE project functions |
| Normative contract | Docs/24_BROKER_MONEY_MODEL_RU.md:11 |
| Formula IDs | F036/F041 |
| Error IDs | ERR009/010/011/040 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | NATIVE_FINITE_HELPER_STATIC |
| Limitations / side effects | Не range/currency/unit validation; native result NOT_RUN |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{return MathIsValidNumber(value);}
~~~

### FUNCTION HSBI_ValidateBrokerProperties

| Field | Individual analysis |
|---|---|
| Function ID | Include/Money/HSBI_BrokerMoneyTypes.mqh:11:HSBI_ValidateBrokerProperties |
| Source | Include/Money/HSBI_BrokerMoneyTypes.mqh:11–19 |
| Signature | HSBI_BrokerPropertyStatus HSBI_ValidateBrokerProperties(const HSBI_BrokerProperties &p) |
| Inputs | const HSBI_BrokerProperties &p |
| Outputs / Postconditions | UNAVAILABLE if!valid;STALE if!fresh;INVALID ifshape/domain;elseVALID |
| Domain | symbol/digits,7finite numbers,IDs,time |
| Preconditions | Fresh/valid flags independently acquired caller |
| Guards | flags;symbol,digits>=0,snapshot/time;7finite;positivepoint/tick/min/step,max>=min,nonnegative tickvalues |
| Callers | HSBI_ValidateExecutionPreflight @ Include/Execution/HSBI_ExecutionPreflight.mqh:30; HSBI_CalculateProjectedMargin @ Include/Money/HSBI_BrokerMarginModel.mqh:8; HSBI_CalculateProjectedProfit @ Include/Money/HSBI_BrokerMoneyModel.mqh:9; HSBI_ValidatePriceGrid @ Include/Planning/HSBI_BrokerGrid.mqh:19; HSBI_ValidateVolume @ Include/Planning/HSBI_BrokerGrid.mqh:35; HSBI_ValidateFutureSmallInput @ Include/Planning/HSBI_FutureSmallSolver.mqh:50; HSBI_SolveBigGeometry @ Include/Planning/HSBI_GeometrySolver.mqh:24 |
| Dependencies | HSBI_IsFiniteNumber @ Include/Money/HSBI_BrokerMoneyTypes.mqh:16; HSBI_IsFiniteNumber @ Include/Money/HSBI_BrokerMoneyTypes.mqh:16; HSBI_IsFiniteNumber @ Include/Money/HSBI_BrokerMoneyTypes.mqh:16; HSBI_IsFiniteNumber @ Include/Money/HSBI_BrokerMoneyTypes.mqh:16; HSBI_IsFiniteNumber @ Include/Money/HSBI_BrokerMoneyTypes.mqh:16; HSBI_IsFiniteNumber @ Include/Money/HSBI_BrokerMoneyTypes.mqh:16; HSBI_IsFiniteNumber @ Include/Money/HSBI_BrokerMoneyTypes.mqh:16 |
| Normative contract | Docs/24:3–11 |
| Formula IDs | F036/F041/F044/F048 |
| Error IDs | ERR024/029/039/040 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | LOCAL_PROPERTIES_VALIDATOR |
| Limitations / side effects | Не проверяет independent snapshot content/clock age,actual broker volume-origin; no universal native evidence |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{
   if(!p.valid)return HSBI_BROKER_PROPERTIES_UNAVAILABLE;
   if(!p.fresh)return HSBI_BROKER_PROPERTIES_STALE;
   if(p.symbol==""||p.digits<0||p.snapshotId==0||p.timestamp<=0)return HSBI_BROKER_PROPERTIES_INVALID;
   if(!HSBI_IsFiniteNumber(p.point)||!HSBI_IsFiniteNumber(p.tickSize)||!HSBI_IsFiniteNumber(p.volumeMin)||!HSBI_IsFiniteNumber(p.volumeMax)||!HSBI_IsFiniteNumber(p.volumeStep)||!HSBI_IsFiniteNumber(p.tickValueProfit)||!HSBI_IsFiniteNumber(p.tickValueLoss))return HSBI_BROKER_PROPERTIES_INVALID;
   if(p.point<=0.0||p.tickSize<=0.0||p.volumeMin<=0.0||p.volumeMax<p.volumeMin||p.volumeStep<=0.0||p.tickValueProfit<0.0||p.tickValueLoss<0.0)return HSBI_BROKER_PROPERTIES_INVALID;
   return HSBI_BROKER_PROPERTIES_VALID;
}
~~~

### FUNCTION HSBI_MoneyResult

| Field | Individual analysis |
|---|---|
| Function ID | Include/Money/HSBI_BrokerMoneyModel.mqh:5:HSBI_MoneyResult |
| Source | Include/Money/HSBI_BrokerMoneyModel.mqh:5–5 |
| Signature | HSBI_MoneyCalculationResult HSBI_MoneyResult(const HSBI_CalculationStatus status,const HSBI_ReasonCode reason,const string details) |
| Inputs | const HSBI_CalculationStatus status,const HSBI_ReasonCode reason,const string details |
| Outputs / Postconditions | ZeroMemory,projected=true,status/reason/details;validfalse/actualfalse |
| Domain | status/reason enums,text |
| Preconditions | Caller chooses valid typed status |
| Guards | Нет guard: constructor |
| Callers | HSBI_CalculateProjectedProfit @ Include/Money/HSBI_BrokerMoneyModel.mqh:8 |
| Dependencies | NONE project functions |
| Normative contract | Docs/24:5–11 |
| Formula IDs | F036/F060 |
| Error IDs | ERR027 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | DTO_CONSTRUCTOR |
| Limitations / side effects | Не financial validator, status arbitrary until caller computes |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{HSBI_MoneyCalculationResult r;ZeroMemory(r);r.status=status;r.reason=reason;r.details=details;r.projected=true;return r;}
~~~

### FUNCTION HSBI_CalculateProjectedProfit

| Field | Individual analysis |
|---|---|
| Function ID | Include/Money/HSBI_BrokerMoneyModel.mqh:6:HSBI_CalculateProjectedProfit |
| Source | Include/Money/HSBI_BrokerMoneyModel.mqh:6–21 |
| Signature | HSBI_MoneyCalculationResult HSBI_CalculateProjectedProfit(const HSBI_BrokerProperties &p,const HSBI_Direction direction,const double volume,const double openPrice,const double closePrice,const double bid,const double ask,const HSBI_CostSnapshot &cost,const double executionSafetyBuffer) |
| Inputs | const HSBI_BrokerProperties &p,const HSBI_Direction direction,const double volume,const double openPrice,const double closePrice,const double bid,const double ask,const HSBI_CostSnapshot &cost,const double executionSafetyBuffer |
| Outputs / Postconditions | Typed REJECT/UNAVAILABLE/ERROR or projectedPASS; no ledger/state writes |
| Domain | lots,price,money samecurrency;Buy/Sell;costsnapshot |
| Preconditions | Provided broker/quotes/costs independentlyfresh, provider available |
| Guards | properties;directionwhitelist;volumegrid;open/closepricegrid;finiteBidAsk/spread;closeside;cost;OrderCalcProfit bool;finitegross;TryProjectedNet finite |
| Callers | HSBI_EvaluateProjectedLegMoney @ Include/Money/HSBI_LevelMoneyEvaluator.mqh:11 |
| Dependencies | HSBI_MoneyResult @ Include/Money/HSBI_BrokerMoneyModel.mqh:8; HSBI_ValidateBrokerProperties @ Include/Money/HSBI_BrokerMoneyModel.mqh:9; HSBI_ValidateVolume @ Include/Money/HSBI_BrokerMoneyModel.mqh:11; HSBI_ValidatePriceGrid @ Include/Money/HSBI_BrokerMoneyModel.mqh:12; HSBI_ValidatePriceGrid @ Include/Money/HSBI_BrokerMoneyModel.mqh:12; HSBI_IsFiniteNumber @ Include/Money/HSBI_BrokerMoneyModel.mqh:12; HSBI_IsFiniteNumber @ Include/Money/HSBI_BrokerMoneyModel.mqh:12; HSBI_GridTolerance @ Include/Money/HSBI_BrokerMoneyModel.mqh:13; HSBI_ValidateCostSnapshot @ Include/Money/HSBI_BrokerMoneyModel.mqh:14; HSBI_IsFiniteNumber @ Include/Money/HSBI_BrokerMoneyModel.mqh:17; HSBI_TryProjectedNetMoney @ Include/Money/HSBI_BrokerMoneyModel.mqh:19 |
| Normative contract | Docs/24_BROKER_MONEY_MODEL_RU.md:3–11 |
| Formula IDs | F007/F008/F009/F036/F046 |
| Error IDs | ERR022/024/029/033/040 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | Native OrderCalcProfit — independent calculation API in source; supplied properties/quotes/costs remain external. Не actual deal/history authority; execution NOT_RUN. |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | PROJECTED_API_WRAPPER_NOT_SETTLEMENT |
| Limitations / side effects | Native API NOT_RUN; price/broker facts not authenticated byshape; cost overlap unresolved; !valid property returns REJECT not brokerAPI UNAVAILABLE |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{
   HSBI_MoneyCalculationResult r=HSBI_MoneyResult(HSBI_CALC_REJECT,HSBI_REASON_INVALID_IDENTITY,"INVALID_SYMBOL_PROPERTIES");r.symbol=p.symbol;r.direction=direction;r.volume=volume;r.openPrice=openPrice;r.closePrice=closePrice;r.snapshotId=p.snapshotId;
   if(HSBI_ValidateBrokerProperties(p)!=HSBI_BROKER_PROPERTIES_VALID)return r;
   if(direction!=HSBI_DIRECTION_BUY&&direction!=HSBI_DIRECTION_SELL){r.details="INVALID_DIRECTION";return r;}
   if(!HSBI_ValidateVolume(volume,p)){r.reason=HSBI_REASON_INVALID_VOLUME;r.details="INVALID_VOLUME";return r;}
   if(!HSBI_ValidatePriceGrid(openPrice,p)||!HSBI_ValidatePriceGrid(closePrice,p)||!HSBI_IsFiniteNumber(bid)||!HSBI_IsFiniteNumber(ask)||bid<=0.0||ask<bid){r.reason=HSBI_REASON_OFF_GRID_PRICE;r.details="INVALID_PRICE_GRID";return r;}
   double expectedClose=(direction==HSBI_DIRECTION_BUY?bid:ask);if(MathAbs(closePrice-expectedClose)>HSBI_GridTolerance(p.tickSize)){r.reason=HSBI_REASON_OFF_GRID_PRICE;r.details="WRONG_CLOSE_SIDE";return r;}
   if(!HSBI_ValidateCostSnapshot(cost,false)||executionSafetyBuffer<0.0){r.details="INVALID_COST_SNAPSHOT";return r;}
   double gross=0.0;ENUM_ORDER_TYPE orderType=(direction==HSBI_DIRECTION_BUY?ORDER_TYPE_BUY:ORDER_TYPE_SELL);
   if(!OrderCalcProfit(orderType,p.symbol,volume,openPrice,closePrice,gross)){r.status=HSBI_CALC_UNAVAILABLE;r.reason=HSBI_REASON_NOT_INITIALIZED;r.details="BROKER_MONEY_UNAVAILABLE";return r;}
   if(!HSBI_IsFiniteNumber(gross)){r.status=HSBI_CALC_ERROR;r.details="NONFINITE_MONEY";return r;}
   r.grossProfit=gross;r.commission=cost.commission;r.swap=cost.swap;r.fee=cost.fee;r.spreadCost=cost.spreadCost;r.slippageBuffer=cost.slippageBuffer;
   if(!HSBI_TryProjectedNetMoney(gross,cost,executionSafetyBuffer,r.netMoney)){r.status=HSBI_CALC_ERROR;r.details="NONFINITE_MONEY";return r;}
   r.status=HSBI_CALC_PASS;r.valid=true;r.actual=false;r.reason=HSBI_REASON_OK;r.details="PASS";return r;
}
~~~

### FUNCTION HSBI_CalculateProjectedMargin

| Field | Individual analysis |
|---|---|
| Function ID | Include/Money/HSBI_BrokerMarginModel.mqh:5:HSBI_CalculateProjectedMargin |
| Source | Include/Money/HSBI_BrokerMarginModel.mqh:5–17 |
| Signature | HSBI_MarginCalculationResult HSBI_CalculateProjectedMargin(const HSBI_BrokerProperties &p,const HSBI_Direction direction,const double volume,const double price) |
| Inputs | const HSBI_BrokerProperties &p,const HSBI_Direction direction,const double volume,const double price |
| Outputs / Postconditions | REJECT/UNAVAILABLE/ERROR or projected finite nonnegative margin |
| Domain | lots,price,money |
| Preconditions | properties/actualaccountcontext provided; no trade |
| Guards | properties;knownDirection;volume/pricegrid;OrderCalcMargin bool;finite/nonnegative output |
| Callers | HSBI_EvaluateProjectedLegMargin @ Include/Money/HSBI_LevelMarginEvaluator.mqh:9 |
| Dependencies | HSBI_ValidateBrokerProperties @ Include/Money/HSBI_BrokerMarginModel.mqh:8; HSBI_ValidateVolume @ Include/Money/HSBI_BrokerMarginModel.mqh:10; HSBI_ValidatePriceGrid @ Include/Money/HSBI_BrokerMarginModel.mqh:11; HSBI_IsFiniteNumber @ Include/Money/HSBI_BrokerMarginModel.mqh:14 |
| Normative contract | Docs/24:5; Docs/15_RISK_AND_MARGIN_CONTRACT_RU.md |
| Formula IDs | F032/F033/F036 |
| Error IDs | ERR023/029/034 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | Native OrderCalcMargin — standalone calculation API in source; не portfolio margin/actual fill receipt; execution NOT_RUN. |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | STANDALONE_PROJECTED_MARGIN |
| Limitations / side effects | Standalone margin не полный hedged/netting portfolio margin и prefix risk; nativeNOTRUN |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{
   HSBI_MarginCalculationResult r;ZeroMemory(r);r.status=HSBI_CALC_REJECT;r.projected=true;r.symbol=p.symbol;r.direction=direction;r.volume=volume;r.price=price;r.snapshotId=p.snapshotId;r.reason=HSBI_REASON_INVALID_IDENTITY;r.details="INVALID_SYMBOL_PROPERTIES";
   if(HSBI_ValidateBrokerProperties(p)!=HSBI_BROKER_PROPERTIES_VALID)return r;
   if(direction!=HSBI_DIRECTION_BUY&&direction!=HSBI_DIRECTION_SELL){r.details="INVALID_DIRECTION";return r;}
   if(!HSBI_ValidateVolume(volume,p)){r.reason=HSBI_REASON_INVALID_VOLUME;r.details="INVALID_VOLUME";return r;}
   if(!HSBI_ValidatePriceGrid(price,p)){r.reason=HSBI_REASON_OFF_GRID_PRICE;r.details="INVALID_PRICE_GRID";return r;}
   double margin=0.0;ENUM_ORDER_TYPE orderType=(direction==HSBI_DIRECTION_BUY?ORDER_TYPE_BUY:ORDER_TYPE_SELL);
   if(!OrderCalcMargin(orderType,p.symbol,volume,price,margin)){r.status=HSBI_CALC_UNAVAILABLE;r.reason=HSBI_REASON_NOT_INITIALIZED;r.details="BROKER_MARGIN_UNAVAILABLE";return r;}
   if(!HSBI_IsFiniteNumber(margin)){r.status=HSBI_CALC_ERROR;r.details="NONFINITE_MARGIN";return r;}
   if(margin<0.0){r.status=HSBI_CALC_ERROR;r.details="NEGATIVE_MARGIN";return r;}
   r.margin=margin;r.status=HSBI_CALC_PASS;r.valid=true;r.reason=HSBI_REASON_OK;r.details="PASS";return r;
}
~~~

### FUNCTION HSBI_EvaluateProjectedLegMoney

| Field | Individual analysis |
|---|---|
| Function ID | Include/Money/HSBI_LevelMoneyEvaluator.mqh:7:HSBI_EvaluateProjectedLegMoney |
| Source | Include/Money/HSBI_LevelMoneyEvaluator.mqh:7–15 |
| Signature | HSBI_BrokerMoneyEvaluationResult HSBI_EvaluateProjectedLegMoney(const HSBI_BrokerMoneyEvaluationInput &x) |
| Inputs | const HSBI_BrokerMoneyEvaluationInput &x |
| Outputs / Postconditions | Reject mismatchedsymbol/snapshot/time; delegateswrapper; copiesresults;valid error ifnonfinite/actual/wrongprojected |
| Domain | symbol,snapshotID,time,lots/price/costmoney |
| Preconditions | Provider source separately, identity filled externally |
| Guards | projected;timestamp>0;nonzerosamebrokerSnapshot;nonemptysamesymbol;wrapper;outputfiniteandflags |
| Callers | HSBI_EvaluateBasketMoney @ Include/Money/HSBI_BasketMoneyEvaluator.mqh:15; HSBI_EvaluateBasketMoney @ Include/Money/HSBI_BasketMoneyEvaluator.mqh:15; HSBI_EvaluateBasketMoney @ Include/Money/HSBI_BasketMoneyEvaluator.mqh:15; HSBI_EvaluateBasketMoney @ Include/Money/HSBI_BasketMoneyEvaluator.mqh:15 |
| Dependencies | HSBI_CalculateProjectedProfit @ Include/Money/HSBI_LevelMoneyEvaluator.mqh:11; HSBI_IsFiniteNumber @ Include/Money/HSBI_LevelMoneyEvaluator.mqh:13 |
| Normative contract | Docs/24:3–11; Docs/31_MONEY_PROOF_IDENTITY_RU.md |
| Formula IDs | F008/F036/F046/F053 |
| Error IDs | ERR013/022/024/033 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | Conditional delegated projected OrderCalcProfit/OrderCalcMargin; risk/ownership/EA-origin data остаются supplied DTO. Нет actual deals/history provider; native NOT_RUN. |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | LEG_PROJECTION_NOT_ACTUAL_PROOF |
| Limitations / side effects | Identity stayszero here; runtimeConfirmed signifies calculation success, not actual deals/provenance |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{
   HSBI_BrokerMoneyEvaluationResult r;ZeroMemory(r);r.status=HSBI_CALC_REJECT;r.projected=x.projected;r.actual=false;r.symbol=x.symbol;r.direction=x.direction;r.volume=x.volume;r.openPrice=x.openPrice;r.closePrice=x.closePrice;r.snapshotId=x.snapshotId;r.executionSafetyBuffer=x.executionSafetyBuffer;r.reason=HSBI_REASON_INTERNAL_INVARIANT_FAILED;r.details="INVALID_INPUT";
   if(!x.projected||x.timestamp<=0||x.snapshotId==0||x.snapshotId!=x.broker.snapshotId||x.symbol==""||x.symbol!=x.broker.symbol)return r;
   HSBI_MoneyCalculationResult source=HSBI_CalculateProjectedProfit(x.broker,x.direction,x.volume,x.openPrice,x.closePrice,x.bid,x.ask,x.costs,x.executionSafetyBuffer);
   r.status=source.status;r.valid=source.valid;r.runtimeConfirmed=source.valid&&source.status==HSBI_CALC_PASS;r.projected=source.projected;r.actual=source.actual;r.grossProfit=source.grossProfit;r.commission=source.commission;r.swap=source.swap;r.fee=source.fee;r.spreadCost=source.spreadCost;r.slippageBuffer=source.slippageBuffer;r.netMoney=source.netMoney;r.reason=source.reason;r.details=source.details;
   if(r.valid&&(!HSBI_IsFiniteNumber(r.netMoney)||r.actual||!r.projected)){r.valid=false;r.status=HSBI_CALC_ERROR;r.details="INVALID_RESULT_FLAGS_OR_MONEY";}
   return r;
}
~~~

### FUNCTION HSBI_EvaluateProjectedLegMargin

| Field | Individual analysis |
|---|---|
| Function ID | Include/Money/HSBI_LevelMarginEvaluator.mqh:5:HSBI_EvaluateProjectedLegMargin |
| Source | Include/Money/HSBI_LevelMarginEvaluator.mqh:5–12 |
| Signature | HSBI_MarginCalculationResult HSBI_EvaluateProjectedLegMargin(const HSBI_BrokerMoneyEvaluationInput &x) |
| Inputs | const HSBI_BrokerMoneyEvaluationInput &x |
| Outputs / Postconditions | Typed wrapper result;postcheck finite/nonnegative |
| Domain | sameunits as leg; outputaccountcurrency |
| Preconditions | Same snapshot/symbol gating, broker margin API required |
| Guards | projected;timestamp;IDs/symbolmatch;CalculateProjectedMargin;outputbounds |
| Callers | HSBI_EvaluateBasketMoney @ Include/Money/HSBI_BasketMoneyEvaluator.mqh:16; HSBI_EvaluateBasketMoney @ Include/Money/HSBI_BasketMoneyEvaluator.mqh:16; HSBI_EvaluateBasketMoney @ Include/Money/HSBI_BasketMoneyEvaluator.mqh:16; HSBI_EvaluateBasketMoney @ Include/Money/HSBI_BasketMoneyEvaluator.mqh:16 |
| Dependencies | HSBI_CalculateProjectedMargin @ Include/Money/HSBI_LevelMarginEvaluator.mqh:9; HSBI_IsFiniteNumber @ Include/Money/HSBI_LevelMarginEvaluator.mqh:10 |
| Normative contract | Docs/24:3–11; Docs/15_RISK_AND_MARGIN_CONTRACT_RU.md |
| Formula IDs | F032/F033/F036 |
| Error IDs | ERR023/029/034 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | Conditional delegated projected OrderCalcProfit/OrderCalcMargin; risk/ownership/EA-origin data остаются supplied DTO. Нет actual deals/history provider; native NOT_RUN. |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | LOCAL_PROJECTED_MARGIN |
| Limitations / side effects | Не totalaccount margin, no identity/batch/fullpath proof |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{
   HSBI_MarginCalculationResult r;ZeroMemory(r);r.status=HSBI_CALC_REJECT;r.projected=true;r.symbol=x.symbol;r.direction=x.direction;r.volume=x.volume;r.price=x.openPrice;r.snapshotId=x.snapshotId;r.reason=HSBI_REASON_INTERNAL_INVARIANT_FAILED;r.details="INVALID_INPUT";
   if(!x.projected||x.timestamp<=0||x.snapshotId==0||x.snapshotId!=x.broker.snapshotId||x.symbol==""||x.symbol!=x.broker.symbol)return r;
   r=HSBI_CalculateProjectedMargin(x.broker,x.direction,x.volume,x.openPrice);
   if(r.valid&&(!HSBI_IsFiniteNumber(r.margin)||r.margin<0.0)){r.valid=false;r.status=HSBI_CALC_ERROR;r.details="NONFINITE_OR_NEGATIVE_MARGIN";}
   return r;
}
~~~

### FUNCTION HSBI_EvaluateCandidateMoney

| Field | Individual analysis |
|---|---|
| Function ID | Include/Money/HSBI_CandidateMoneyEvaluator.mqh:10:HSBI_EvaluateCandidateMoney |
| Source | Include/Money/HSBI_CandidateMoneyEvaluator.mqh:10–27 |
| Signature | HSBI_CandidateMoneyEvaluationResult HSBI_EvaluateCandidateMoney(const HSBI_FutureSmallInput &candidateInput) |
| Inputs | const HSBI_FutureSmallInput &candidateInput |
| Outputs / Postconditions | UNAVAILABLE on flags/proofdepth<2/emptydigest; otherwisePASS |
| Domain | candidateDTO;perlevel money/margin/risk |
| Preconditions | FutureSmall provider assumptions обязательны, no injected/testonly |
| Guards | !testOnlyApproximation;!useInjected;SolveFutureSmall;valid/depth>=2;4digestnonempty |
| Callers | HSBI_SolveNewFar @ Include/Planning/HSBI_NewFarSolver.mqh:114 |
| Dependencies | HSBI_SolveFutureSmall @ Include/Money/HSBI_CandidateMoneyEvaluator.mqh:15; HSBI_FutureSmallProofDigest @ Include/Money/HSBI_CandidateMoneyEvaluator.mqh:17 |
| Normative contract | Docs/27_FUTURE_SMALL_SOLVER_RU.md; Docs/18:13 |
| Formula IDs | F037/F038/F057/F058/F060 |
| Error IDs | ERR013/021/026/031 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | Conditional delegated projected OrderCalcProfit/OrderCalcMargin; risk/ownership/EA-origin data остаются supplied DTO. Нет actual deals/history provider; native NOT_RUN. |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | DELEGATED_PREFIX_PROOF_ONLY |
| Limitations / side effects | Future proof validity наследует solver scope; nonempty strings не независимая proof completeness |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{
   HSBI_CandidateMoneyEvaluationResult r;ZeroMemory(r);r.status=HSBI_CALC_UNAVAILABLE;
   r.reason=HSBI_REASON_NOT_INITIALIZED;r.details="CANDIDATE_PROOF_UNAVAILABLE";
   if(candidateInput.testOnlyApproximation||candidateInput.useInjectedBrokerProofs)return r;
   r.futureSmallProof=HSBI_SolveFutureSmall(candidateInput);
   if(!r.futureSmallProof.valid||r.futureSmallProof.provenDepth<2)return r;
   r.futureSmallProofDigest=HSBI_FutureSmallProofDigest(r.futureSmallProof);
   r.moneyProofDigest="MONEY";r.marginProofDigest="MARGIN";r.riskProofDigest="RISK";
   for(int i=0;i<r.futureSmallProof.provenDepth;i++) {
      HSBI_FutureSmallLevelProof p=r.futureSmallProof.levels[i];
      r.moneyProofDigest+="|"+IntegerToString(i)+"|"+DoubleToString(p.projectedRecoveryMoney,8)+"|"+IntegerToString((int)p.moneyProofStatus);
      r.marginProofDigest+="|"+IntegerToString(i)+"|"+DoubleToString(p.projectedMargin,8)+"|"+IntegerToString((int)p.marginProofStatus);
      r.riskProofDigest+="|"+IntegerToString(i)+"|"+DoubleToString(p.projectedRisk,8)+"|"+IntegerToString((int)p.riskProofStatus);
   }
   if(r.futureSmallProofDigest==""||r.moneyProofDigest==""||r.marginProofDigest==""||r.riskProofDigest=="")return r;
   r.status=HSBI_CALC_PASS;r.valid=true;r.reason=HSBI_REASON_OK;r.details="PASS";return r;
}
~~~

### FUNCTION HSBI_ValidateAllocationPolicy

| Field | Individual analysis |
|---|---|
| Function ID | Include/Money/HSBI_AllocationPolicyTypes.mqh:16:HSBI_ValidateAllocationPolicy |
| Source | Include/Money/HSBI_AllocationPolicyTypes.mqh:16–24 |
| Signature | bool HSBI_ValidateAllocationPolicy(const HSBI_AllocationPolicySnapshot &p) |
| Inputs | const HSBI_AllocationPolicySnapshot &p |
| Outputs / Postconditions | true ifshape/domain andsum<=1+eps |
| Domain | 4ratios,policy/snapshotIDs,valid/fresh |
| Preconditions | Snapshot policy independently approved; not by boolflags |
| Guards | 2flags/2ids;4finite;reserve[0,1];partial/transition/carry>=0;sum<=1+1e-12 |
| Callers | HSBI_EvaluateReserveCatchUp @ Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:55; HSBI_ValidateFutureSmallInput @ Include/Planning/HSBI_FutureSmallSolver.mqh:47; HSBI_SolveNewFar @ Include/Planning/HSBI_NewFarSolver.mqh:99; HSBI_ValidateRuntimeDecisionContext @ Include/Runtime/HSBI_RuntimeDecisionValidator.mqh:24 |
| Dependencies | HSBI_IsFiniteNumber @ Include/Money/HSBI_AllocationPolicyTypes.mqh:19; HSBI_IsFiniteNumber @ Include/Money/HSBI_AllocationPolicyTypes.mqh:19; HSBI_IsFiniteNumber @ Include/Money/HSBI_AllocationPolicyTypes.mqh:20; HSBI_IsFiniteNumber @ Include/Money/HSBI_AllocationPolicyTypes.mqh:20 |
| Normative contract | Docs/08:12–24; Docs/32_RESERVE_ALLOCATION_CONSUMPTION_RU.md |
| Formula IDs | F012/F064 |
| Error IDs | ERR005/006/028 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | LOCAL_POLICY_SHAPE |
| Limitations / side effects | transitionShare negative guard EXISTS; прежняя гипотеза отсутствия WITHDRAWN; policyapproval/authenticity внешняя |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{
   if(!p.valid || !p.fresh || p.policyVersion==0 || p.snapshotId==0) return false;
   if(!HSBI_IsFiniteNumber(p.reserveShare) || !HSBI_IsFiniteNumber(p.partialFarShare) ||
      !HSBI_IsFiniteNumber(p.transitionShare) || !HSBI_IsFiniteNumber(p.carryShare)) return false;
   if(p.reserveShare<0.0 || p.reserveShare>1.0 || p.partialFarShare<0.0 ||
      p.transitionShare<0.0 || p.carryShare<0.0) return false;
   return p.reserveShare+p.partialFarShare+p.transitionShare+p.carryShare<=1.0+1e-12;
}
~~~

### FUNCTION HSBI_AllocationPolicyDigest

| Field | Individual analysis |
|---|---|
| Function ID | Include/Money/HSBI_AllocationPolicyTypes.mqh:25:HSBI_AllocationPolicyDigest |
| Source | Include/Money/HSBI_AllocationPolicyTypes.mqh:25–31 |
| Signature | string HSBI_AllocationPolicyDigest(const HSBI_AllocationPolicySnapshot &p) |
| Inputs | const HSBI_AllocationPolicySnapshot &p |
| Outputs / Postconditions | Fixed textual8fields |
| Domain | 4share12dec,IDs64,bools |
| Preconditions | Validation/approvedpolicy separately |
| Guards | Нет guards |
| Callers | HSBI_FutureSmallTemplateDigest @ Include/Planning/HSBI_NewFarSolver.mqh:37; HSBI_NewFarInputDigest @ Include/Planning/HSBI_NewFarSolver.mqh:56; HSBI_SolveNewFar @ Include/Planning/HSBI_NewFarSolver.mqh:144 |
| Dependencies | HSBI_UlongToString @ Include/Money/HSBI_AllocationPolicyTypes.mqh:29; HSBI_UlongToString @ Include/Money/HSBI_AllocationPolicyTypes.mqh:29 |
| Normative contract | Docs/16:8; NUM-CODEC proposed |
| Formula IDs | F042/F057/F060 |
| Error IDs | ERR003/024/040 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | POLICY_FINGERPRINT_ONLY |
| Limitations / side effects | Не canonicalexactcodec/signature; freshness flagнеindependentclock |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{
   return DoubleToString(p.reserveShare,12)+"|"+DoubleToString(p.partialFarShare,12)+"|"+
          DoubleToString(p.transitionShare,12)+"|"+DoubleToString(p.carryShare,12)+"|"+
          HSBI_UlongToString(p.policyVersion)+"|"+HSBI_UlongToString(p.snapshotId)+"|"+
          IntegerToString((int)p.valid)+"|"+IntegerToString((int)p.fresh);
}
~~~

### FUNCTION HSBI_BasketLegInput

| Field | Individual analysis |
|---|---|
| Function ID | Include/Money/HSBI_BasketMoneyEvaluator.mqh:7:HSBI_BasketLegInput |
| Source | Include/Money/HSBI_BasketMoneyEvaluator.mqh:7–10 |
| Signature | HSBI_BrokerMoneyEvaluationInput HSBI_BasketLegInput(const HSBI_BasketMoneyInput &x,const HSBI_Direction direction,const double volume,const double openPrice,const HSBI_CostSnapshot &cost) |
| Inputs | const HSBI_BasketMoneyInput &x,const HSBI_Direction direction,const double volume,const double openPrice,const HSBI_CostSnapshot &cost |
| Outputs / Postconditions | Copiesbroker/symbol/snapshot/costs,closeBUYBidelseAsk,projectedtrue |
| Domain | volume lots,open/closeprice,costmoney;Direction |
| Preconditions | Known direction caller; this is constructor |
| Guards | Нет own domain checks; directionternary |
| Callers | HSBI_EvaluateBasketMoney @ Include/Money/HSBI_BasketMoneyEvaluator.mqh:14; HSBI_EvaluateBasketMoney @ Include/Money/HSBI_BasketMoneyEvaluator.mqh:14; HSBI_EvaluateBasketMoney @ Include/Money/HSBI_BasketMoneyEvaluator.mqh:14; HSBI_EvaluateBasketMoney @ Include/Money/HSBI_BasketMoneyEvaluator.mqh:14 |
| Dependencies | NONE project functions |
| Normative contract | Docs/24:3–11; Docs/03:9 |
| Formula IDs | F008/F046 |
| Error IDs | ERR022/049 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | LEG_CONSTRUCTOR |
| Limitations / side effects | Unknown direction defaultsAsk здесь, но wrapper rejects; no standalone trade |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{
   HSBI_BrokerMoneyEvaluationInput leg;ZeroMemory(leg);leg.broker=x.broker;leg.symbol=x.symbol;leg.direction=direction;leg.volume=volume;leg.openPrice=openPrice;leg.bid=x.controlPrice.bid;leg.ask=x.controlPrice.ask;leg.closePrice=(direction==HSBI_DIRECTION_BUY?leg.bid:leg.ask);leg.costs=cost;leg.executionSafetyBuffer=x.executionSafetyBuffer;leg.snapshotId=x.snapshotId;leg.timestamp=x.controlPrice.timestamp;leg.projected=true;return leg;
}
~~~

### FUNCTION HSBI_EvaluateBasketMoney

| Field | Individual analysis |
|---|---|
| Function ID | Include/Money/HSBI_BasketMoneyEvaluator.mqh:11:HSBI_EvaluateBasketMoney |
| Source | Include/Money/HSBI_BasketMoneyEvaluator.mqh:11–19 |
| Signature | HSBI_BasketMoneyResult HSBI_EvaluateBasketMoney(const HSBI_BasketMoneyInput &x) |
| Inputs | const HSBI_BasketMoneyInput &x |
| Outputs / Postconditions | Typedreject/unavailable/error orPASS basket sums |
| Domain | 4lots,4price/costsets;sumcurrency |
| Preconditions | Actual source funding внеscope; broker APIs required |
| Guards | FarDirectionwhitelist;typedcontrolprice;4legvalid;4marginvalid;finite basket/totalmargin/gross |
| Callers | HSBI_EvaluateFutureSmallLevel @ Include/Planning/HSBI_FutureSmallSolver.mqh:80 |
| Dependencies | HSBI_ValidateTypedControlPrice @ Include/Money/HSBI_BasketMoneyEvaluator.mqh:13; HSBI_BasketLegInput @ Include/Money/HSBI_BasketMoneyEvaluator.mqh:14; HSBI_BasketLegInput @ Include/Money/HSBI_BasketMoneyEvaluator.mqh:14; HSBI_BasketLegInput @ Include/Money/HSBI_BasketMoneyEvaluator.mqh:14; HSBI_BasketLegInput @ Include/Money/HSBI_BasketMoneyEvaluator.mqh:14; HSBI_EvaluateProjectedLegMoney @ Include/Money/HSBI_BasketMoneyEvaluator.mqh:15; HSBI_EvaluateProjectedLegMoney @ Include/Money/HSBI_BasketMoneyEvaluator.mqh:15; HSBI_EvaluateProjectedLegMoney @ Include/Money/HSBI_BasketMoneyEvaluator.mqh:15; HSBI_EvaluateProjectedLegMoney @ Include/Money/HSBI_BasketMoneyEvaluator.mqh:15; HSBI_EvaluateProjectedLegMargin @ Include/Money/HSBI_BasketMoneyEvaluator.mqh:16; HSBI_EvaluateProjectedLegMargin @ Include/Money/HSBI_BasketMoneyEvaluator.mqh:16; HSBI_EvaluateProjectedLegMargin @ Include/Money/HSBI_BasketMoneyEvaluator.mqh:16; HSBI_EvaluateProjectedLegMargin @ Include/Money/HSBI_BasketMoneyEvaluator.mqh:16; HSBI_IsFiniteNumber @ Include/Money/HSBI_BasketMoneyEvaluator.mqh:18; HSBI_IsFiniteNumber @ Include/Money/HSBI_BasketMoneyEvaluator.mqh:18; HSBI_IsFiniteNumber @ Include/Money/HSBI_BasketMoneyEvaluator.mqh:18 |
| Normative contract | Docs/24:3–11; Docs/04_MATHEMATICAL_MODEL_RU.md |
| Formula IDs | F002/F005/F008/F009/F020/F030/F032/F047 |
| Error IDs | ERR015/022/034/043/047 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | Conditional delegated projected OrderCalcProfit/OrderCalcMargin; risk/ownership/EA-origin data остаются supplied DTO. Нет actual deals/history provider; native NOT_RUN. |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | PROJECTED_BASKET_PARTIAL_SEMANTICS |
| Limitations / side effects | Trend0неinactive money leg; reservegain включаетSmall; FarLoss absolute despiteIncrease name; totalmarginnotportfolio; safetycostbasis unresolved |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{
   HSBI_BasketMoneyResult r;ZeroMemory(r);r.status=HSBI_CALC_REJECT;r.reason=HSBI_REASON_INTERNAL_INVARIANT_FAILED;r.details="INVALID_BASKET";if(x.farDirection!=HSBI_DIRECTION_BUY&&x.farDirection!=HSBI_DIRECTION_SELL)return r;if(!HSBI_ValidateTypedControlPrice(x.controlPrice,x.symbol))return r;
   HSBI_Direction opposite=(x.farDirection==HSBI_DIRECTION_BUY?HSBI_DIRECTION_SELL:HSBI_DIRECTION_BUY);HSBI_BrokerMoneyEvaluationInput farIn=HSBI_BasketLegInput(x,x.farDirection,x.farVolume,x.farOpenPrice,x.farCosts),coreIn=HSBI_BasketLegInput(x,opposite,x.coreVolume,x.coreOpenPrice,x.coreCosts),trendIn=HSBI_BasketLegInput(x,opposite,x.trendVolume,x.trendOpenPrice,x.trendCosts),smallIn=HSBI_BasketLegInput(x,x.farDirection,x.smallVolume,x.smallOpenPrice,x.smallCosts);
   r.far=HSBI_EvaluateProjectedLegMoney(farIn);r.core=HSBI_EvaluateProjectedLegMoney(coreIn);r.trend=HSBI_EvaluateProjectedLegMoney(trendIn);r.small=HSBI_EvaluateProjectedLegMoney(smallIn);if(!r.far.valid||!r.core.valid||!r.trend.valid||!r.small.valid){r.status=(r.far.status==HSBI_CALC_UNAVAILABLE||r.core.status==HSBI_CALC_UNAVAILABLE||r.trend.status==HSBI_CALC_UNAVAILABLE||r.small.status==HSBI_CALC_UNAVAILABLE)?HSBI_CALC_UNAVAILABLE:HSBI_CALC_REJECT;r.details="LEG_MONEY_UNAVAILABLE";return r;}
   HSBI_MarginCalculationResult fm=HSBI_EvaluateProjectedLegMargin(farIn),cm=HSBI_EvaluateProjectedLegMargin(coreIn),tm=HSBI_EvaluateProjectedLegMargin(trendIn),sm=HSBI_EvaluateProjectedLegMargin(smallIn);if(!fm.valid||!cm.valid||!tm.valid||!sm.valid){r.status=(fm.status==HSBI_CALC_UNAVAILABLE||cm.status==HSBI_CALC_UNAVAILABLE||tm.status==HSBI_CALC_UNAVAILABLE||sm.status==HSBI_CALC_UNAVAILABLE)?HSBI_CALC_UNAVAILABLE:HSBI_CALC_REJECT;r.details="LEG_MARGIN_UNAVAILABLE";return r;}
   r.basketNetMoney=r.far.netMoney+r.core.netMoney+r.trend.netMoney+r.small.netMoney;r.recoveryMoney=r.basketNetMoney;r.totalMargin=fm.margin+cm.margin+tm.margin+sm.margin;r.grossExposure=x.farVolume+x.coreVolume+x.trendVolume+x.smallVolume;r.reserveGainMoney=MathMax(0.0,r.core.netMoney+r.trend.netMoney+r.small.netMoney);r.farLossIncreaseMoney=MathMax(0.0,-r.far.netMoney);r.transitionLoss=MathMax(0.0,-r.basketNetMoney);r.safetyBuffer=x.executionSafetyBuffer*4.0;
   if(!HSBI_IsFiniteNumber(r.basketNetMoney)||!HSBI_IsFiniteNumber(r.totalMargin)||!HSBI_IsFiniteNumber(r.grossExposure)){r.status=HSBI_CALC_ERROR;r.details="NONFINITE_BASKET";return r;}r.status=HSBI_CALC_PASS;r.valid=true;r.brokerRuntimeConfirmed=true;r.reason=HSBI_REASON_OK;r.details="PASS";return r;
}
~~~

### FUNCTION HSBI_BasketMoneyProofDigest

| Field | Individual analysis |
|---|---|
| Function ID | Include/Money/HSBI_BasketMoneyEvaluator.mqh:20:HSBI_BasketMoneyProofDigest |
| Source | Include/Money/HSBI_BasketMoneyEvaluator.mqh:20–28 |
| Signature | string HSBI_BasketMoneyProofDigest(const HSBI_BasketMoneyResult &r) |
| Inputs | const HSBI_BasketMoneyResult &r |
| Outputs / Postconditions | 11numeric/status fields +reason, no input changes |
| Domain | money/margin8dec,grosslots,status/reason |
| Preconditions | Immutable sourceproof отдельно |
| Guards | Нет guards |
| Callers | NO_CALLER_FOUND: all74 production source bodies, no dynamic/native proof |
| Dependencies | NONE project functions |
| Normative contract | Docs/16:8; Docs/24:3–11 |
| Formula IDs | F042/F057/F060 |
| Error IDs | ERR003/013/026 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | RESULT_FINGERPRINT_ONLY |
| Limitations / side effects | Не включаетполныйbroker/identity/costbasis, nonempty≠independence |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{
   return IntegerToString((int)r.status)+"|"+IntegerToString((int)r.valid)+"|"+
      DoubleToString(r.far.netMoney,8)+"|"+DoubleToString(r.core.netMoney,8)+"|"+
      DoubleToString(r.trend.netMoney,8)+"|"+DoubleToString(r.small.netMoney,8)+"|"+
      DoubleToString(r.basketNetMoney,8)+"|"+DoubleToString(r.recoveryMoney,8)+"|"+
      DoubleToString(r.totalMargin,8)+"|"+DoubleToString(r.grossExposure,8)+"|"+
      DoubleToString(r.transitionLoss,8)+"|"+IntegerToString((int)r.reason);
}
~~~

### FUNCTION HSBI_EvaluateCatchUp

| Field | Individual analysis |
|---|---|
| Function ID | Include/Money/HSBI_CatchUpModel.mqh:4:HSBI_EvaluateCatchUp |
| Source | Include/Money/HSBI_CatchUpModel.mqh:4–16 |
| Signature | HSBI_CatchUpResult HSBI_EvaluateCatchUp(const HSBI_CatchUpInput &x) |
| Inputs | const HSBI_CatchUpInput &x |
| Outputs / Postconditions | passed when2strictconditions andshape; zero constinputdelta |
| Domain | share ratio,lots,money,farDirection |
| Preconditions | Resource eligible and independent; lossbasis externally set |
| Guards | snapshotFresh;moneyAvailable;direction;6finite;sharebounds/positivevol/nonnegativebuffer;share*netBig>F;margin>0 |
| Callers | NO_CALLER_FOUND: all74 production source bodies, no dynamic/native proof |
| Dependencies | HSBI_IsFiniteNumber @ Include/Money/HSBI_CatchUpModel.mqh:10; HSBI_IsFiniteNumber @ Include/Money/HSBI_CatchUpModel.mqh:10; HSBI_IsFiniteNumber @ Include/Money/HSBI_CatchUpModel.mqh:10; HSBI_IsFiniteNumber @ Include/Money/HSBI_CatchUpModel.mqh:10; HSBI_IsFiniteNumber @ Include/Money/HSBI_CatchUpModel.mqh:10; HSBI_IsFiniteNumber @ Include/Money/HSBI_CatchUpModel.mqh:10 |
| Normative contract | Docs/24:9; D04/CR09 proposed |
| Formula IDs | F006/F020/F022/F023 |
| Error IDs | ERR018/033/043/048 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | LOCAL_CATCHUP_FILTER |
| Limitations / side effects | Lossnegative не отдельноотвергается; AvailableReserve authority/alllevels/globalfunding отсутствуют; не finalspend |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{
   HSBI_CatchUpResult r;ZeroMemory(r);r.reserveShare=x.reserveShare;r.netBigVolume=x.netBigVolume;r.farVolume=x.farVolume;r.reserveGainMoney=x.reserveGainMoney;r.farLossIncreaseMoney=x.farLossIncreaseMoney;r.executionSafetyBuffer=x.executionSafetyBuffer;r.status=HSBI_CALC_REJECT;r.reason=HSBI_REASON_INTERNAL_INVARIANT_FAILED;
   if(!x.snapshotFresh){r.reason=HSBI_REASON_STALE_SNAPSHOT;return r;}
   if(!x.moneyAvailable){r.status=HSBI_CALC_UNAVAILABLE;r.reason=HSBI_REASON_NOT_INITIALIZED;return r;}
   if(x.farDirection!=HSBI_DIRECTION_BUY&&x.farDirection!=HSBI_DIRECTION_SELL)return r;
   if(!HSBI_IsFiniteNumber(x.reserveShare)||!HSBI_IsFiniteNumber(x.netBigVolume)||!HSBI_IsFiniteNumber(x.farVolume)||!HSBI_IsFiniteNumber(x.reserveGainMoney)||!HSBI_IsFiniteNumber(x.farLossIncreaseMoney)||!HSBI_IsFiniteNumber(x.executionSafetyBuffer))return r;
   if(x.reserveShare<=0.0||x.reserveShare>1.0||x.netBigVolume<=0.0||x.farVolume<=0.0||x.executionSafetyBuffer<0.0)return r;
   if(x.reserveShare*x.netBigVolume<=x.farVolume)return r;
   r.catchUpMargin=x.reserveGainMoney-x.farLossIncreaseMoney-x.executionSafetyBuffer;
   if(r.catchUpMargin<=0.0)return r;
   r.passed=true;r.status=HSBI_CALC_PASS;r.reason=HSBI_REASON_OK;return r;
}
~~~

### FUNCTION HSBI_ValidateCostSnapshot

| Field | Individual analysis |
|---|---|
| Function ID | Include/Money/HSBI_CostModel.mqh:5:HSBI_ValidateCostSnapshot |
| Source | Include/Money/HSBI_CostModel.mqh:5–10 |
| Signature | bool HSBI_ValidateCostSnapshot(const HSBI_CostSnapshot &c,const bool expectedActual) |
| Inputs | const HSBI_CostSnapshot &c,const bool expectedActual |
| Outputs / Postconditions | true valid/type/time/snapshot and5finite/nonneg spread/slip |
| Domain | 3signedcosts,2nonneg deductions,IDs/time |
| Preconditions | CostID/basis/window coverage independent external |
| Guards | valid;actual==expected;time>0,id>0;5finite;2nonnegative |
| Callers | HSBI_CalculateProjectedProfit @ Include/Money/HSBI_BrokerMoneyModel.mqh:14; HSBI_TryActualDealNet @ Include/Money/HSBI_CostModel.mqh:13; HSBI_TryProjectedNetMoney @ Include/Money/HSBI_CostModel.mqh:17; HSBI_ValidateLevelCosts @ Include/Planning/HSBI_FutureSmallSolver.mqh:29; HSBI_ValidateLevelCosts @ Include/Planning/HSBI_FutureSmallSolver.mqh:30; HSBI_ValidateLevelCosts @ Include/Planning/HSBI_FutureSmallSolver.mqh:30; HSBI_ValidateLevelCosts @ Include/Planning/HSBI_FutureSmallSolver.mqh:30 |
| Dependencies | HSBI_IsFiniteNumber @ Include/Money/HSBI_CostModel.mqh:8; HSBI_IsFiniteNumber @ Include/Money/HSBI_CostModel.mqh:8; HSBI_IsFiniteNumber @ Include/Money/HSBI_CostModel.mqh:8; HSBI_IsFiniteNumber @ Include/Money/HSBI_CostModel.mqh:8; HSBI_IsFiniteNumber @ Include/Money/HSBI_CostModel.mqh:8 |
| Normative contract | Docs/24:7; D06 proposed |
| Formula IDs | F007/F008/F009/F036 |
| Error IDs | ERR022 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | COST_SHAPE_NOT_COVERAGE |
| Limitations / side effects | Неполный inventory/overlap/knownunknown не represented; valid flag не cost authority |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{
   if(!c.valid||c.actual!=expectedActual||c.timestamp<=0||c.snapshotId==0)return false;
   if(!HSBI_IsFiniteNumber(c.commission)||!HSBI_IsFiniteNumber(c.swap)||!HSBI_IsFiniteNumber(c.fee)||!HSBI_IsFiniteNumber(c.slippageBuffer)||!HSBI_IsFiniteNumber(c.spreadCost))return false;
   return c.slippageBuffer>=0.0&&c.spreadCost>=0.0;
}
~~~

### FUNCTION HSBI_TryActualDealNet

| Field | Individual analysis |
|---|---|
| Function ID | Include/Money/HSBI_CostModel.mqh:11:HSBI_TryActualDealNet |
| Source | Include/Money/HSBI_CostModel.mqh:11–14 |
| Signature | bool HSBI_TryActualDealNet(const double profit,const HSBI_CostSnapshot &c,double &netMoney) |
| Inputs | const double profit,const HSBI_CostSnapshot &c,double &netMoney |
| Outputs / Postconditions | setsoutput0 initially; on valid computes sum;returns finite resultbool |
| Domain | profit,swap,commission,fee samecurrency finite |
| Preconditions | actual cost snapshot independently sourced |
| Guards | profitfinite;ValidateCostSnapshot(true);sumfinite |
| Callers | NO_CALLER_FOUND: all74 production source bodies, no dynamic/native proof |
| Dependencies | HSBI_IsFiniteNumber @ Include/Money/HSBI_CostModel.mqh:13; HSBI_ValidateCostSnapshot @ Include/Money/HSBI_CostModel.mqh:13; HSBI_IsFiniteNumber @ Include/Money/HSBI_CostModel.mqh:13 |
| Normative contract | Docs/08:6; Docs/24:7 |
| Formula IDs | F007/F036/F049 |
| Error IDs | ERR022/033/040 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | LOCAL_ACTUAL_TYPED_ARITHMETIC |
| Limitations / side effects | Output byref изменяется даже при failed overflow; caller обязан читать bool, это не ledgerdelta; no broker authenticity |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{
   netMoney=0.0;if(!HSBI_IsFiniteNumber(profit)||!HSBI_ValidateCostSnapshot(c,true))return false;netMoney=profit+c.swap+c.commission+c.fee;return HSBI_IsFiniteNumber(netMoney);
}
~~~

### FUNCTION HSBI_TryProjectedNetMoney

| Field | Individual analysis |
|---|---|
| Function ID | Include/Money/HSBI_CostModel.mqh:15:HSBI_TryProjectedNetMoney |
| Source | Include/Money/HSBI_CostModel.mqh:15–19 |
| Signature | bool HSBI_TryProjectedNetMoney(const double grossProfit,const HSBI_CostSnapshot &c,const double executionSafetyBuffer,double &netMoney) |
| Inputs | const double grossProfit,const HSBI_CostSnapshot &c,const double executionSafetyBuffer,double &netMoney |
| Outputs / Postconditions | setsoutput0;computessum ifvalid;returnfinitebool |
| Domain | gross+signedcosts−spread−slippage−buffer samecurrency |
| Preconditions | Disjoint costbasis andprojected snapshot |
| Guards | gross/bufferfinite;buffer>=0;ValidateCostSnapshot(false);resultfinite |
| Callers | HSBI_CalculateProjectedProfit @ Include/Money/HSBI_BrokerMoneyModel.mqh:19 |
| Dependencies | HSBI_IsFiniteNumber @ Include/Money/HSBI_CostModel.mqh:17; HSBI_IsFiniteNumber @ Include/Money/HSBI_CostModel.mqh:17; HSBI_ValidateCostSnapshot @ Include/Money/HSBI_CostModel.mqh:17; HSBI_IsFiniteNumber @ Include/Money/HSBI_CostModel.mqh:18 |
| Normative contract | Docs/24:7 |
| Formula IDs | F008/F009/F036/F049 |
| Error IDs | ERR022/033/040 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | LOCAL_PROJECTION_ARITHMETIC |
| Limitations / side effects | Нельзя считать falseoutput0 доказанным moneyzero; outputnotcommittedbalance; overlap unresolved |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{
   netMoney=0.0;if(!HSBI_IsFiniteNumber(grossProfit)||!HSBI_IsFiniteNumber(executionSafetyBuffer)||executionSafetyBuffer<0.0||!HSBI_ValidateCostSnapshot(c,false))return false;
   netMoney=grossProfit+c.swap+c.commission+c.fee-c.spreadCost-c.slippageBuffer-executionSafetyBuffer;return HSBI_IsFiniteNumber(netMoney);
}
~~~

### FUNCTION HSBI_BuildRecoveryPL

| Field | Individual analysis |
|---|---|
| Function ID | Include/Money/HSBI_MoneyTypes.mqh:9:HSBI_BuildRecoveryPL |
| Source | Include/Money/HSBI_MoneyTypes.mqh:9–9 |
| Signature | HSBI_RecoveryPLSnapshot HSBI_BuildRecoveryPL(const double realized,const double openNet,const HSBI_FinalCloseThreshold &t) |
| Inputs | const double realized,const double openNet,const HSBI_FinalCloseThreshold &t |
| Outputs / Postconditions | sum=realized+openNet;allowed=sum>=t.threshold;copies fields |
| Domain | realized/openNet/threshold samecurrency |
| Preconditions | t.valid/components/authority/actualcoverage проверяетcaller |
| Guards | единственное thresholdcomparison;нетshape guard |
| Callers | NO_CALLER_FOUND: all74 production source bodies, no dynamic/native proof |
| Dependencies | NONE project functions |
| Normative contract | Docs/12_FINAL_CLOSE_SPECIFICATION_RU.md; Docs/04:18 |
| Formula IDs | F010/F011/F035 |
| Error IDs | ERR036/044 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | SCALAR_METRIC_NOT_FINAL_GATE |
| Limitations / side effects | t.valid ignored;threshold not recomputed;finite/cycleboundary/time/snapshot notbound; не FinalClose authorization |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{HSBI_RecoveryPLSnapshot r;r.realizedCycleNet=realized;r.openPositionsCloseNowNet=openNet;r.recoveryPLCloseNow=realized+openNet;r.minimumProfit=t.minimumProfit;r.executionBuffer=t.executionBuffer;r.tolerance=t.tolerance;r.threshold=t.threshold;r.allowed=r.recoveryPLCloseNow>=r.threshold;return r;}
~~~

### FUNCTION HSBI_BuildDiagnosticSnapshot

| Field | Individual analysis |
|---|---|
| Function ID | Include/Diagnostics/HSBI_Diagnostics.mqh:5:HSBI_BuildDiagnosticSnapshot |
| Source | Include/Diagnostics/HSBI_Diagnostics.mqh:5–5 |
| Signature | HSBI_DiagnosticSnapshot HSBI_BuildDiagnosticSnapshot(const HSBI_RecoveryContext &c) |
| Inputs | const HSBI_RecoveryContext &c |
| Outputs / Postconditions | Copiesfields;4slotfarcount;TimeCurrent timestamp |
| Domain | contextfields,counters,money,time |
| Preconditions | NOT_APPLICABLE financial authority: displayonly |
| Guards | Нетvalidation;delegatesCountFarRoles |
| Callers | HSBI_UpdateDiagnosticSnapshot @ Include/Diagnostics/HSBI_Diagnostics.mqh:6 |
| Dependencies | HSBI_CountFarRoles @ Include/Diagnostics/HSBI_Diagnostics.mqh:5 |
| Normative contract | Docs/18:6,28 |
| Formula IDs | F060 |
| Error IDs | ERR012/027 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | DIAGNOSTIC_READ_ONLY |
| Limitations / side effects | 4slotcount inheritslimitedscope; display timestamp не marketsnapshotfreshness |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{HSBI_DiagnosticSnapshot d;d.cycleId=c.cycleId;d.stateRevision=c.stateRevision;d.state=c.currentState;d.runtimeMode=c.runtimeMode;d.lastReason=c.lastReason;d.farCount=HSBI_CountFarRoles(c.far,c.bigCore,c.bigTrend,c.smallBase);d.realizedCycleNet=c.realizedCycleNet;d.finalReserve=c.finalReserve;d.tradingImplemented=HSBI_TRADING_IMPLEMENTED;d.timestamp=TimeCurrent();return d;}
~~~

### FUNCTION HSBI_UpdateDiagnosticSnapshot

| Field | Individual analysis |
|---|---|
| Function ID | Include/Diagnostics/HSBI_Diagnostics.mqh:6:HSBI_UpdateDiagnosticSnapshot |
| Source | Include/Diagnostics/HSBI_Diagnostics.mqh:6–6 |
| Signature | void HSBI_UpdateDiagnosticSnapshot(const HSBI_RecoveryContext &c) |
| Inputs | const HSBI_RecoveryContext &c |
| Outputs / Postconditions | BuildDiagnosticSnapshot thenPrint;noledger/state writes |
| Domain | constcontext;Print output |
| Preconditions | Diagnostics не финансовое действие |
| Guards | Нет guards:display |
| Callers | OnTimer @ Hybrid_Split_Big_Independent_EA.mq5:43 |
| Dependencies | HSBI_BuildDiagnosticSnapshot @ Include/Diagnostics/HSBI_Diagnostics.mqh:6 |
| Normative contract | Docs/18:28–30 |
| Formula IDs | F060 |
| Error IDs | ERR027 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | LOGGING_ONLY |
| Limitations / side effects | Имеет log sideeffect, не money/trade/persistence; native loggingNOTRUN |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{HSBI_DiagnosticSnapshot d=HSBI_BuildDiagnosticSnapshot(c);Print("HSBI_DIAG|cycle=",d.cycleId,"|rev=",d.stateRevision,"|state=",d.state,"|trade=",d.tradingImplemented);}
~~~

### FUNCTION HSBI_Log

| Field | Individual analysis |
|---|---|
| Function ID | Include/Diagnostics/HSBI_Logger.mqh:6:HSBI_Log |
| Source | Include/Diagnostics/HSBI_Logger.mqh:6–6 |
| Signature | void HSBI_Log(const string requirementId,const HSBI_ReasonCode reason,const string message) |
| Inputs | const string requirementId,const HSBI_ReasonCode reason,const string message |
| Outputs / Postconditions | Print text withReasonToString;noledger/state writes |
| Domain | strings,reason enum |
| Preconditions | NOT_APPLICABLE approval/provenance |
| Guards | Нетfinancialguards |
| Callers | OnInit @ Hybrid_Split_Big_Independent_EA.mq5:24; OnDeinit @ Hybrid_Split_Big_Independent_EA.mq5:32 |
| Dependencies | HSBI_ReasonToString @ Include/Diagnostics/HSBI_Logger.mqh:6 |
| Normative contract | Docs/18:6,28 |
| Formula IDs | F060 |
| Error IDs | ERR027/028 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | LOGGING_ONLY |
| Limitations / side effects | Logнеimmutable journal/receipt; not proof of guardexecution orbroker |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{Print("HSBI|",requirementId,"|",HSBI_ReasonToString(reason),"|",message);}
~~~

### FUNCTION HSBI_BuildPanelModel

| Field | Individual analysis |
|---|---|
| Function ID | Include/Diagnostics/HSBI_PanelModel.mqh:5:HSBI_BuildPanelModel |
| Source | Include/Diagnostics/HSBI_PanelModel.mqh:5–5 |
| Signature | HSBI_PanelModel HSBI_BuildPanelModel(const HSBI_RecoveryContext &c) |
| Inputs | const HSBI_RecoveryContext &c |
| Outputs / Postconditions | Copiesproject/stage/state/identity/reason/money/recon,hardcodednoTrade |
| Domain | contextscope,money2dec,text |
| Preconditions | NOT_APPLICABLE: not authoritative serializedbalance |
| Guards | Нетvalidationguards |
| Callers | NO_CALLER_FOUND: all74 production source bodies, no dynamic/native proof |
| Dependencies | HSBI_UlongToString @ Include/Diagnostics/HSBI_PanelModel.mqh:5; HSBI_ReasonToString @ Include/Diagnostics/HSBI_PanelModel.mqh:5 |
| Normative contract | Docs/18:6,28 |
| Formula IDs | F042/F060 |
| Error IDs | ERR003/027 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | DISPLAY_ONLY |
| Limitations / side effects | Displayroundingнеmoneycodec; hardcodedlabelнеruntimeapproval; not actualaccountprovider |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{HSBI_PanelModel p;p.projectName=HSBI_PROJECT_NAME;p.stage=HSBI_STAGE;p.runtimeMode=IntegerToString((int)c.runtimeMode);p.state=IntegerToString((int)c.currentState);p.identity=c.symbol+"/"+LongToString(c.magic)+"/"+HSBI_UlongToString(c.cycleId);p.noTradeStatus="TRADING_IMPLEMENTED=NO";p.lastReason=HSBI_ReasonToString(c.lastReason);p.moneySummary=DoubleToString(c.realizedCycleNet,2)+"|"+DoubleToString(c.finalReserve,2);p.reconciliationSummary=IntegerToString(c.reconciliationStatus);return p;}
~~~

### FUNCTION HSBI_ValidateActionRecord

| Field | Individual analysis |
|---|---|
| Function ID | Include/Execution/HSBI_ActionTypes.mqh:6:HSBI_ValidateActionRecord |
| Source | Include/Execution/HSBI_ActionTypes.mqh:6–6 |
| Signature | bool HSBI_ValidateActionRecord(const HSBI_ActionRecord &a) |
| Inputs | const HSBI_ActionRecord &a |
| Outputs / Postconditions | true iff6conjuncts |
| Domain | 4positiveIDs,actionType!=NONE,expectedVolume>=0 |
| Preconditions | Knownenum/finite/ownership/pending proof caller |
| Guards | 4positiveIDs;type!=NONE;volume>=0 |
| Callers | NO_CALLER_FOUND: all74 production source bodies, no dynamic/native proof |
| Dependencies | NONE project functions |
| Normative contract | Docs/07:9–24 |
| Formula IDs | F024/F036/F053 |
| Error IDs | ERR010/049 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | ACTION_DTO_PARTIAL |
| Limitations / side effects | Infinityvolume passes; unknown action enum!=NONE passes; status/time/role notvalidated |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{return a.actionId>0&&a.planId>0&&a.cycleId>0&&a.stateRevision>0&&a.actionType!=HSBI_ACTION_NONE&&a.expectedVolume>=0.0;}
~~~

### FUNCTION HSBI_SerializeActionIds

| Field | Individual analysis |
|---|---|
| Function ID | Include/Execution/HSBI_ActionTypes.mqh:7:HSBI_SerializeActionIds |
| Source | Include/Execution/HSBI_ActionTypes.mqh:7–7 |
| Signature | string HSBI_SerializeActionIds(const HSBI_ActionRecord &a) |
| Inputs | const HSBI_ActionRecord &a |
| Outputs / Postconditions | concatplan/action/parent/cycle/revision/ticket/identifier |
| Domain | 7ulongIDs |
| Preconditions | Not full bodydigest; valid record separately |
| Guards | No validation;unsignedformatter |
| Callers | HSBI_SerializeJournalIds @ Include/Persistence/HSBI_JournalTypes.mqh:7; HSBI_SerializeSnapshotIds @ Include/Persistence/HSBI_SnapshotTypes.mqh:10 |
| Dependencies | HSBI_UlongToString @ Include/Execution/HSBI_ActionTypes.mqh:7; HSBI_UlongToString @ Include/Execution/HSBI_ActionTypes.mqh:7; HSBI_UlongToString @ Include/Execution/HSBI_ActionTypes.mqh:7; HSBI_UlongToString @ Include/Execution/HSBI_ActionTypes.mqh:7; HSBI_UlongToString @ Include/Execution/HSBI_ActionTypes.mqh:7; HSBI_UlongToString @ Include/Execution/HSBI_ActionTypes.mqh:7; HSBI_UlongToString @ Include/Execution/HSBI_ActionTypes.mqh:7 |
| Normative contract | Docs/07:9; Docs/16:8 |
| Formula IDs | F042/F053/F060 |
| Error IDs | ERR003/013/030 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | ID_TEXT_ONLY |
| Limitations / side effects | Excludesvolume/type/status/time; notimmutablepayload equality/sourceauthority |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{return HSBI_UlongToString(a.planId)+"|"+HSBI_UlongToString(a.actionId)+"|"+HSBI_UlongToString(a.parentActionId)+"|"+HSBI_UlongToString(a.cycleId)+"|"+HSBI_UlongToString(a.stateRevision)+"|"+HSBI_UlongToString(a.expectedTicket)+"|"+HSBI_UlongToString(a.expectedIdentifier);}
~~~

### FUNCTION HSBI_ValidateEventRecord

| Field | Individual analysis |
|---|---|
| Function ID | Include/Execution/HSBI_EventTypes.mqh:6:HSBI_ValidateEventRecord |
| Source | Include/Execution/HSBI_EventTypes.mqh:6–6 |
| Signature | bool HSBI_ValidateEventRecord(const HSBI_EventRecord &e) |
| Inputs | const HSBI_EventRecord &e |
| Outputs / Postconditions | true iff4conditions |
| Domain | event/actionIDs>0,eventType!=NONE,actualVolume>=0 |
| Preconditions | Actualdeal/history independent caller |
| Guards | 2nonzeroIDs;type!=NONE;volume>=0 |
| Callers | NO_CALLER_FOUND: all74 production source bodies, no dynamic/native proof |
| Dependencies | NONE project functions |
| Normative contract | Docs/07:9–24 |
| Formula IDs | F024/F036/F053 |
| Error IDs | ERR010/049 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | EVENT_DTO_PARTIAL |
| Limitations / side effects | Unknownenum/Infinity accepted; noactualprice/deal/ticket/timestamp/schema check |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{return e.eventId>0&&e.actionId>0&&e.eventType!=HSBI_EVENT_NONE&&e.actualVolume>=0.0;}
~~~

### FUNCTION HSBI_SerializeEventIds

| Field | Individual analysis |
|---|---|
| Function ID | Include/Execution/HSBI_EventTypes.mqh:7:HSBI_SerializeEventIds |
| Source | Include/Execution/HSBI_EventTypes.mqh:7–7 |
| Signature | string HSBI_SerializeEventIds(const HSBI_EventRecord &e) |
| Inputs | const HSBI_EventRecord &e |
| Outputs / Postconditions | concat5IDs;inputunchanged |
| Domain | event/action/order/deal/positionulong |
| Preconditions | Full immutablebodyindependentjournal separately |
| Guards | No validation;unsignedformatter |
| Callers | HSBI_SerializeJournalIds @ Include/Persistence/HSBI_JournalTypes.mqh:7 |
| Dependencies | HSBI_UlongToString @ Include/Execution/HSBI_EventTypes.mqh:7; HSBI_UlongToString @ Include/Execution/HSBI_EventTypes.mqh:7; HSBI_UlongToString @ Include/Execution/HSBI_EventTypes.mqh:7; HSBI_UlongToString @ Include/Execution/HSBI_EventTypes.mqh:7; HSBI_UlongToString @ Include/Execution/HSBI_EventTypes.mqh:7 |
| Normative contract | Docs/07:9; Docs/16:8 |
| Formula IDs | F042/F053/F060 |
| Error IDs | ERR003/013/030 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | ID_TEXT_ONLY |
| Limitations / side effects | Excludesvolume/price/outcome/time; notreceipt/provenanceproof |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{return HSBI_UlongToString(e.eventId)+"|"+HSBI_UlongToString(e.actionId)+"|"+HSBI_UlongToString(e.orderTicket)+"|"+HSBI_UlongToString(e.dealTicket)+"|"+HSBI_UlongToString(e.positionIdentifier);}
~~~


## R2 — индивидуальные journal/recovery/outcome функции, продолжение без замены43 карт

### FUNCTION HSBI_ExecutionJournalEntryDigest

| Field | Individual analysis |
|---|---|
| Function ID | Include/Persistence/HSBI_ExecutionJournal.mqh:12:HSBI_ExecutionJournalEntryDigest |
| Source | Include/Persistence/HSBI_ExecutionJournal.mqh:12–17 |
| Signature | string HSBI_ExecutionJournalEntryDigest(const HSBI_ExecutionJournalEntry &x) |
| Inputs | const HSBI_ExecutionJournalEntry &x |
| Outputs / Postconditions | Concats14fields; no mutation |
| Domain | IDs,entry enums,time,namespace,previous/payloadtext |
| Preconditions | Full source/journal authority separately |
| Guards | No validation guards |
| Callers | HSBI_ValidateJournalEntry @ Include/Persistence/HSBI_ExecutionJournal.mqh:20 |
| Dependencies | HSBI_UlongToString @ Include/Persistence/HSBI_ExecutionJournal.mqh:13; HSBI_UlongToString @ Include/Persistence/HSBI_ExecutionJournal.mqh:13; HSBI_UlongToString @ Include/Persistence/HSBI_ExecutionJournal.mqh:13; HSBI_UlongToString @ Include/Persistence/HSBI_ExecutionJournal.mqh:14; HSBI_UlongToString @ Include/Persistence/HSBI_ExecutionJournal.mqh:14; HSBI_UlongToString @ Include/Persistence/HSBI_ExecutionJournal.mqh:14; HSBI_UlongToString @ Include/Persistence/HSBI_ExecutionJournal.mqh:15 |
| Normative contract | Docs/16:8–19; Docs/HSB.2C_Journal_Persistence_Reconciliation.md:3 |
| Formula IDs | F042/F053/F057/F060 |
| Error IDs | ERR003/017/030 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | JOURNAL_FINGERPRINT_ONLY |
| Limitations / side effects | Text concatenation не cryptographic SHA256; unknown enum вdigest не validation |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{return HSBI_UlongToString(x.journalEntryId)+"|"+HSBI_UlongToString(x.intentId)+"|"+HSBI_UlongToString(x.planId)+"|"+
   HSBI_UlongToString(x.cycleId)+"|"+HSBI_UlongToString(x.stateRevision)+"|"+HSBI_UlongToString(x.actionId)+"|"+
   HSBI_UlongToString(x.eventId)+"|"+IntegerToString((int)x.entryType)+"|"+IntegerToString((int)x.entryStatus)+"|"+
   LongToString((long)x.timestamp)+"|"+LongToString(x.accountLogin)+"|"+x.symbol+"|"+LongToString(x.magic)+"|"+
   x.previousEntryDigest+"|"+x.payloadDigest;}
~~~

### FUNCTION HSBI_ValidateJournalEntry

| Field | Individual analysis |
|---|---|
| Function ID | Include/Persistence/HSBI_ExecutionJournal.mqh:18:HSBI_ValidateJournalEntry |
| Source | Include/Persistence/HSBI_ExecutionJournal.mqh:18–20 |
| Signature | bool HSBI_ValidateJournalEntry(const HSBI_ExecutionJournalEntry &x,const string expectedPrevious,const ulong cycleId,const ulong planId,const ulong revision) |
| Inputs | const HSBI_ExecutionJournalEntry &x,const string expectedPrevious,const ulong cycleId,const ulong planId,const ulong revision |
| Outputs / Postconditions | true iff9group clauses |
| Domain | positiveIDs/time,expectedcycle/plan/revision/digest |
| Preconditions | Expectedprevious and scope derived independently durablejournal |
| Guards | 3IDs>0,time>0;3scopeequalities;previous equality;payloadnonempty;currentDigest recompute |
| Callers | HSBI_ClassifyJournalAppend @ Include/Persistence/HSBI_ExecutionJournal.mqh:29; HSBI_ValidateJournalChain @ Include/Persistence/HSBI_ExecutionJournal.mqh:36 |
| Dependencies | HSBI_ExecutionJournalEntryDigest @ Include/Persistence/HSBI_ExecutionJournal.mqh:20 |
| Normative contract | Docs/16:8–19; Docs/07:9 |
| Formula IDs | F053/F057/F062 |
| Error IDs | ERR017/030/049 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | ENTRY_SHAPE_PARTIAL |
| Limitations / side effects | No enum/namespace/status/event validation, digest source not authenticity |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{return x.journalEntryId>0&&x.intentId>0&&x.actionId>0&&x.timestamp>0&&x.cycleId==cycleId&&x.planId==planId&&x.stateRevision==revision&&
   x.previousEntryDigest==expectedPrevious&&x.payloadDigest!=""&&x.currentEntryDigest==HSBI_ExecutionJournalEntryDigest(x);}
~~~

### FUNCTION HSBI_IsDuplicateJournalEntry

| Field | Individual analysis |
|---|---|
| Function ID | Include/Persistence/HSBI_ExecutionJournal.mqh:21:HSBI_IsDuplicateJournalEntry |
| Source | Include/Persistence/HSBI_ExecutionJournal.mqh:21–22 |
| Signature | bool HSBI_IsDuplicateJournalEntry(const HSBI_ExecutionJournalEntry &a,const HSBI_ExecutionJournalEntry &b) |
| Inputs | const HSBI_ExecutionJournalEntry &a,const HSBI_ExecutionJournalEntry &b |
| Outputs / Postconditions | true iff5exactequalities |
| Domain | 5fields journal/intent/action/event/currentdigest |
| Preconditions | Both candidate/last bodyvalid independently |
| Guards | 5exactequalities |
| Callers | HSBI_ClassifyJournalAppend @ Include/Persistence/HSBI_ExecutionJournal.mqh:27 |
| Dependencies | NONE project functions |
| Normative contract | Docs/07:21; Docs/16:8–19 |
| Formula IDs | F053/F057 |
| Error IDs | ERR030 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | REPLAY_KEY_DIGEST_ONLY |
| Limitations / side effects | Candidate body could differ with stalecopied currentdigest; validation not insidehelper |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{return a.journalEntryId==b.journalEntryId&&a.intentId==b.intentId&&a.actionId==b.actionId&&a.eventId==b.eventId&&a.currentEntryDigest==b.currentEntryDigest;}
~~~

### FUNCTION HSBI_IsJournalEntryConflict

| Field | Individual analysis |
|---|---|
| Function ID | Include/Persistence/HSBI_ExecutionJournal.mqh:23:HSBI_IsJournalEntryConflict |
| Source | Include/Persistence/HSBI_ExecutionJournal.mqh:23–24 |
| Signature | bool HSBI_IsJournalEntryConflict(const HSBI_ExecutionJournalEntry &a,const HSBI_ExecutionJournalEntry &b) |
| Inputs | const HSBI_ExecutionJournalEntry &a,const HSBI_ExecutionJournalEntry &b |
| Outputs / Postconditions | 3keyequalities &&digestdiff |
| Domain | journalEntry/intent/action IDs,currentdigest |
| Preconditions | Bodyvalidity and eventnamespace expected separately |
| Guards | 4clauses |
| Callers | HSBI_ClassifyJournalAppend @ Include/Persistence/HSBI_ExecutionJournal.mqh:28 |
| Dependencies | NONE project functions |
| Normative contract | Docs/07:21; Docs/16:8–19 |
| Formula IDs | F053/F057 |
| Error IDs | ERR030 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | LOCAL_CONFLICT_CLASSIFIER |
| Limitations / side effects | Same eventonlycollision no conflict here; stale unchanged digest canhide alteredbody beforevalidation |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{return a.journalEntryId==b.journalEntryId&&a.intentId==b.intentId&&a.actionId==b.actionId&&a.currentEntryDigest!=b.currentEntryDigest;}
~~~

### FUNCTION HSBI_ClassifyJournalAppend

| Field | Individual analysis |
|---|---|
| Function ID | Include/Persistence/HSBI_ExecutionJournal.mqh:25:HSBI_ClassifyJournalAppend |
| Source | Include/Persistence/HSBI_ExecutionJournal.mqh:25–30 |
| Signature | HSBI_JournalAppendStatus HSBI_ClassifyJournalAppend(const HSBI_ExecutionJournalEntry &candidate,const HSBI_ExecutionJournalEntry &last,const string expectedPrevious,const ulong cycleId,const ulong planId,const ulong revision) |
| Inputs | const HSBI_ExecutionJournalEntry &candidate,const HSBI_ExecutionJournalEntry &last,const string expectedPrevious,const ulong cycleId,const ulong planId,const ulong revision |
| Outputs / Postconditions | duplicate→NOOP beforebodyvalidation;conflict→CONFLICT;elsevalid+consecutiveid+fresh event→APPENDED |
| Domain | candidate,last,expectedprevious/scope |
| Preconditions | Durable/immutable last independentlytrusted |
| Guards | 2earlyclassifierbranches;entryvalidator;idlast+1;event>last |
| Callers | NO_CALLER_FOUND: all74 production source bodies, no dynamic/native proof |
| Dependencies | HSBI_IsDuplicateJournalEntry @ Include/Persistence/HSBI_ExecutionJournal.mqh:27; HSBI_IsJournalEntryConflict @ Include/Persistence/HSBI_ExecutionJournal.mqh:28; HSBI_ValidateJournalEntry @ Include/Persistence/HSBI_ExecutionJournal.mqh:29 |
| Normative contract | Docs/07:21; Docs/16:8–19 |
| Formula IDs | F053/F057/F065 |
| Error IDs | ERR017/025/030 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | LOCAL_CLASSIFIER_SOURCE_DEFECT_SCOPE |
| Limitations / side effects | ERR030 earlyNOOP doesnotvalidate candidatebody; ulong increment overflow unguarded; function writesnothing |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{
   if(HSBI_IsDuplicateJournalEntry(candidate,last))return HSBI_JOURNAL_NO_OP;
   if(HSBI_IsJournalEntryConflict(candidate,last))return HSBI_JOURNAL_CONFLICT;
   return HSBI_ValidateJournalEntry(candidate,expectedPrevious,cycleId,planId,revision)&&candidate.journalEntryId==last.journalEntryId+1&&candidate.eventId>last.eventId?HSBI_JOURNAL_APPENDED:HSBI_JOURNAL_REJECTED;
}
~~~

### FUNCTION HSBI_ValidateJournalChain

| Field | Individual analysis |
|---|---|
| Function ID | Include/Persistence/HSBI_ExecutionJournal.mqh:31:HSBI_ValidateJournalChain |
| Source | Include/Persistence/HSBI_ExecutionJournal.mqh:31–44 |
| Signature | bool HSBI_ValidateJournalChain(const HSBI_ExecutionJournalEntry &entries[],const int count,const ulong cycleId,const ulong planId,const ulong revision) |
| Inputs | const HSBI_ExecutionJournalEntry &entries[],const int count,const ulong cycleId,const ulong planId,const ulong revision |
| Outputs / Postconditions | allentrychecks;consecutiveid/freshevent;reconciliation-before-complete;no postcompletecreation |
| Domain | entries[],countpositive,scopedIDs |
| Preconditions | Caller ensures count<=ArraySize and independentcompletehistory |
| Guards | count>0;perentryvalidator;sequence;2phaseflags;4forbiddenpostcompleteentrytypes |
| Callers | NO_CALLER_FOUND: all74 production source bodies, no dynamic/native proof |
| Dependencies | HSBI_ValidateJournalEntry @ Include/Persistence/HSBI_ExecutionJournal.mqh:36 |
| Normative contract | Docs/16:8–19; Docs/HSB.2C_Journal_Persistence_Reconciliation.md:3–7 |
| Formula IDs | F024/F053/F057/F063 |
| Error IDs | ERR017/025/030/049 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | LOCAL_CHAIN_ORDER_ONLY |
| Limitations / side effects | No arrayboundscheck/countmax inside; sourcecompleteness/authenticity/durableordering notvalidated; native runtimeNOTRUN |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{
   if(count<=0)return false;string previous="";bool reconciliationPassed=false,completed=false;
   for(int i=0;i<count;i++){
      HSBI_ExecutionJournalEntry e=entries[i];
      if(!HSBI_ValidateJournalEntry(e,previous,cycleId,planId,revision))return false;
      if(i>0&&(e.journalEntryId!=entries[i-1].journalEntryId+1||e.eventId<=entries[i-1].eventId))return false;
      if(e.entryType==HSBI_JE_RECONCILIATION_PASSED){if(completed)return false;reconciliationPassed=true;}
      if(e.entryType==HSBI_JE_INTENT_COMPLETED){if(!reconciliationPassed||completed)return false;completed=true;}
      if(completed&&(e.entryType==HSBI_JE_INTENT_CREATED||e.entryType==HSBI_JE_PREFLIGHT_RESULT||e.entryType==HSBI_JE_INTENT_PERSISTED||e.entryType==HSBI_JE_EXTERNAL_OUTCOME_RECEIVED))return false;
      previous=e.currentEntryDigest;
   }
   return true;
}
~~~

### FUNCTION HSBI_ValidateJournalRecord

| Field | Individual analysis |
|---|---|
| Function ID | Include/Persistence/HSBI_JournalTypes.mqh:6:HSBI_ValidateJournalRecord |
| Source | Include/Persistence/HSBI_JournalTypes.mqh:6–6 |
| Signature | bool HSBI_ValidateJournalRecord(const HSBI_JournalRecord &r) |
| Inputs | const HSBI_JournalRecord &r |
| Outputs / Postconditions | true iff5conditions |
| Domain | 3positive revisions/IDs,time>0,recordDigestnonempty |
| Preconditions | Fullaction/event/body/journalchain caller responsibility |
| Guards | revision/cycle/stateRevision/time/digest |
| Callers | NO_CALLER_FOUND: all74 production source bodies, no dynamic/native proof |
| Dependencies | NONE project functions |
| Normative contract | Docs/16:8–19 |
| Formula IDs | F053/F057 |
| Error IDs | ERR017/030 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | MINIMAL_RECORD_SHAPE |
| Limitations / side effects | committed flag/nested action/event/previous/currentdigest correctness notvalidated |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{return r.revision>0&&r.cycleId>0&&r.stateRevision>0&&r.timestamp>0&&r.recordDigest!="";}
~~~

### FUNCTION HSBI_SerializeJournalIds

| Field | Individual analysis |
|---|---|
| Function ID | Include/Persistence/HSBI_JournalTypes.mqh:7:HSBI_SerializeJournalIds |
| Source | Include/Persistence/HSBI_JournalTypes.mqh:7–7 |
| Signature | string HSBI_SerializeJournalIds(const HSBI_JournalRecord &r) |
| Inputs | const HSBI_JournalRecord &r |
| Outputs / Postconditions | 3journalIDs plusnestedIDserializers |
| Domain | ulong IDs,text |
| Preconditions | Not fullrecordcodec; valid nestedrecordseparate |
| Guards | No guards;2serializerdelegations |
| Callers | NO_CALLER_FOUND: all74 production source bodies, no dynamic/native proof |
| Dependencies | HSBI_UlongToString @ Include/Persistence/HSBI_JournalTypes.mqh:7; HSBI_UlongToString @ Include/Persistence/HSBI_JournalTypes.mqh:7; HSBI_UlongToString @ Include/Persistence/HSBI_JournalTypes.mqh:7; HSBI_SerializeActionIds @ Include/Persistence/HSBI_JournalTypes.mqh:7; HSBI_SerializeEventIds @ Include/Persistence/HSBI_JournalTypes.mqh:7 |
| Normative contract | Docs/16:8–19 |
| Formula IDs | F042/F053/F060 |
| Error IDs | ERR003/017/030 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | ID_TEXT_ONLY |
| Limitations / side effects | Excludes actualbody/committed/previousdigest; not durable/authenticjournal |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{return HSBI_UlongToString(r.revision)+"|"+HSBI_UlongToString(r.cycleId)+"|"+HSBI_UlongToString(r.stateRevision)+"|"+HSBI_SerializeActionIds(r.action)+"|"+HSBI_SerializeEventIds(r.event);}
~~~

### FUNCTION HSBI_PersistSnapshotStub

| Field | Individual analysis |
|---|---|
| Function ID | Include/Persistence/HSBI_PersistenceInterface.mqh:7:HSBI_PersistSnapshotStub |
| Source | Include/Persistence/HSBI_PersistenceInterface.mqh:7–7 |
| Signature | HSBI_PersistenceResult HSBI_PersistSnapshotStub(const HSBI_SnapshotRecord &s) |
| Inputs | const HSBI_SnapshotRecord &s |
| Outputs / Postconditions | successfalse,PERSISTENCE_NOT_IMPLEMENTED,revisioncopied,digestempty |
| Domain | snapshotconst→result |
| Preconditions | No backend implemented, no IOexpected |
| Guards | Alwaysfailure |
| Callers | NO_CALLER_FOUND: all74 production source bodies, no dynamic/native proof |
| Dependencies | NONE project functions |
| Normative contract | Docs/16:5–19; Docs/18:6 |
| Formula IDs | F057/F065 |
| Error IDs | ERR017 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | UNIMPLEMENTED_BACKEND_EXPLICIT |
| Limitations / side effects | Does notsave snapshot/journal; correct stub cannotprove crashrecovery |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{HSBI_PersistenceResult r;r.success=false;r.reason=HSBI_REASON_PERSISTENCE_NOT_IMPLEMENTED;r.revision=s.stateRevision;r.digest="";return r;}
~~~

### FUNCTION HSBI_CompareReconciliation

| Field | Individual analysis |
|---|---|
| Function ID | Include/Persistence/HSBI_ReconciliationTypes.mqh:7:HSBI_CompareReconciliation |
| Source | Include/Persistence/HSBI_ReconciliationTypes.mqh:7–7 |
| Signature | HSBI_ReconciliationResult HSBI_CompareReconciliation(const HSBI_ReconciliationInput &x) |
| Inputs | const HSBI_ReconciliationInput &x |
| Outputs / Postconditions | 3emptyobservations→CLEANSTART;invalididentity→REJECT;economic!=allocationdigest→CONFLICT;elsePENDING;nevernewTradingAllowed |
| Domain | digeststrings+identityDTO |
| Preconditions | Complete actual broker observations/journals not readinside |
| Guards | empty3shortcut;identityvalidator;2digestinequality |
| Callers | NO_CALLER_FOUND: all74 production source bodies, no dynamic/native proof |
| Dependencies | HSBI_IsValidIdentity @ Include/Persistence/HSBI_ReconciliationTypes.mqh:7 |
| Normative contract | Docs/17:3–22 |
| Formula IDs | F053/F057/F062 |
| Error IDs | ERR013/017/033 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | RECONCILIATION_SKELETON_NOT_PROVIDER |
| Limitations / side effects | Emptystrings cannotprove completeemptyhistory; equaldifferentledgerdigests not economicreconciliation; no RECONCILED pathimplemented |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{HSBI_ReconciliationResult r;r.mismatchMask=0;r.newTradingAllowed=false;r.manualInterventionRequired=false;r.reason=HSBI_REASON_OK;if(x.persistedSnapshotDigest==""&&x.observedPositionsDigest==""&&x.observedEventsDigest==""){r.outcome=HSBI_RECON_CLEAN_START;r.requiredAction="NONE";return r;}if(!HSBI_IsValidIdentity(x.identityScope)){r.outcome=HSBI_RECON_REJECTED;r.reason=HSBI_REASON_INVALID_IDENTITY;r.requiredAction="MANUAL_REVIEW";r.manualInterventionRequired=true;return r;}if(x.economicLedgerDigest!=x.allocationLedgerDigest){r.outcome=HSBI_RECON_CONFLICT;r.mismatchMask=1;r.reason=HSBI_REASON_RECONCILIATION_REQUIRED;r.requiredAction="TERMINAL_SAFE";r.manualInterventionRequired=true;return r;}r.outcome=HSBI_RECON_PENDING;r.reason=HSBI_REASON_RECONCILIATION_REQUIRED;r.requiredAction="OBSERVE";return r;}
~~~

### FUNCTION HSBI_ValidateSnapshotSchema

| Field | Individual analysis |
|---|---|
| Function ID | Include/Persistence/HSBI_SnapshotTypes.mqh:8:HSBI_ValidateSnapshotSchema |
| Source | Include/Persistence/HSBI_SnapshotTypes.mqh:8–8 |
| Signature | bool HSBI_ValidateSnapshotSchema(const HSBI_SnapshotRecord &s) |
| Inputs | const HSBI_SnapshotRecord &s |
| Outputs / Postconditions | true iff2versions/revision>0/time>0 |
| Domain | schemaversion/moneyversion,revision/time |
| Preconditions | Snapshotcontent/namespace/digest independentlyvalidated elsewhere |
| Guards | 4conditions |
| Callers | NO_CALLER_FOUND: all74 production source bodies, no dynamic/native proof |
| Dependencies | NONE project functions |
| Normative contract | Docs/16:8–19 |
| Formula IDs | F057/F060 |
| Error IDs | ERR017 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | SCHEMA_HEADER_ONLY |
| Limitations / side effects | Money/state/roles/ownership/checksum/pendingbody notvalidated |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{return s.schemaVersion==HSBI_SNAPSHOT_SCHEMA_VERSION&&s.moneyStateVersion==HSBI_MONEY_STATE_VERSION&&s.stateRevision>0&&s.timestamp>0;}
~~~

### FUNCTION HSBI_TestDigest

| Field | Individual analysis |
|---|---|
| Function ID | Include/Persistence/HSBI_SnapshotTypes.mqh:9:HSBI_TestDigest |
| Source | Include/Persistence/HSBI_SnapshotTypes.mqh:9–9 |
| Signature | ulong HSBI_TestDigest(const HSBI_SnapshotRecord &s) |
| Inputs | const HSBI_SnapshotRecord &s |
| Outputs / Postconditions | FNV-style XOR/multiply overtextselectedfields |
| Domain | 4selectedfields,stringchars→ulong |
| Preconditions | Explicittestname,notproductionSHA256 |
| Guards | LoopStringLen;char truncateduchar |
| Callers | NO_CALLER_FOUND: all74 production source bodies, no dynamic/native proof |
| Dependencies | HSBI_UlongToString @ Include/Persistence/HSBI_SnapshotTypes.mqh:9; HSBI_UlongToString @ Include/Persistence/HSBI_SnapshotTypes.mqh:9 |
| Normative contract | Docs/16:8–11 contradicts useasproductionSHA; implementation nameTest only |
| Formula IDs | F042/F057/F060 |
| Error IDs | ERR003/017/040 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | TEST_DIGEST_NOT_PRODUCTION_AUTHENTICITY |
| Limitations / side effects | Not fullsnapshotcontent/UTF8canonical/SHA256; hash collision/overflow nottrustedproof |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{string v=IntegerToString(s.schemaVersion)+"|"+HSBI_UlongToString(s.cycleId)+"|"+HSBI_UlongToString(s.stateRevision)+"|"+s.candidatePlanDigest;ulong h=2166136261;for(int i=0;i<StringLen(v);i++){h^=(uchar)StringGetCharacter(v,i);h*=16777619;}return h;}
~~~

### FUNCTION HSBI_SerializeSnapshotIds

| Field | Individual analysis |
|---|---|
| Function ID | Include/Persistence/HSBI_SnapshotTypes.mqh:10:HSBI_SerializeSnapshotIds |
| Source | Include/Persistence/HSBI_SnapshotTypes.mqh:10–10 |
| Signature | string HSBI_SerializeSnapshotIds(const HSBI_SnapshotRecord &s) |
| Inputs | const HSBI_SnapshotRecord &s |
| Outputs / Postconditions | 2IDs+nestedactionIDs |
| Domain | ulong IDs |
| Preconditions | Snapshotfullbodyvalidation separately |
| Guards | No guards |
| Callers | NO_CALLER_FOUND: all74 production source bodies, no dynamic/native proof |
| Dependencies | HSBI_UlongToString @ Include/Persistence/HSBI_SnapshotTypes.mqh:10; HSBI_UlongToString @ Include/Persistence/HSBI_SnapshotTypes.mqh:10; HSBI_SerializeActionIds @ Include/Persistence/HSBI_SnapshotTypes.mqh:10 |
| Normative contract | Docs/16:8–19 |
| Formula IDs | F042/F053/F060 |
| Error IDs | ERR003/017 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | ID_TEXT_ONLY |
| Limitations / side effects | Not contentbinding ofbalances/roles/volumes; notfullcodec |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{return HSBI_UlongToString(s.cycleId)+"|"+HSBI_UlongToString(s.stateRevision)+"|"+HSBI_SerializeActionIds(s.pendingAction);}
~~~

### FUNCTION HSBI_ExternalOutcomeDigest

| Field | Individual analysis |
|---|---|
| Function ID | Include/Execution/HSBI_ExternalOutcome.mqh:13:HSBI_ExternalOutcomeDigest |
| Source | Include/Execution/HSBI_ExternalOutcome.mqh:13–19 |
| Signature | string HSBI_ExternalOutcomeDigest(const HSBI_ExternalTransactionOutcome &x) |
| Inputs | const HSBI_ExternalTransactionOutcome &x |
| Outputs / Postconditions | Concatsalllisted20fields,notmutableinput |
| Domain | IDs/namespace,role/direction,volume8dec,price12dec,flags/time/status |
| Preconditions | Actual read/expectedcontext independentlyverified |
| Guards | No guards |
| Callers | HSBI_ReconcileExecutionOutcome @ Include/Execution/HSBI_ExternalOutcome.mqh:25 |
| Dependencies | HSBI_UlongToString @ Include/Execution/HSBI_ExternalOutcome.mqh:14; HSBI_UlongToString @ Include/Execution/HSBI_ExternalOutcome.mqh:14; HSBI_UlongToString @ Include/Execution/HSBI_ExternalOutcome.mqh:14; HSBI_UlongToString @ Include/Execution/HSBI_ExternalOutcome.mqh:15; HSBI_UlongToString @ Include/Execution/HSBI_ExternalOutcome.mqh:15; HSBI_UlongToString @ Include/Execution/HSBI_ExternalOutcome.mqh:17; HSBI_UlongToString @ Include/Execution/HSBI_ExternalOutcome.mqh:17; HSBI_UlongToString @ Include/Execution/HSBI_ExternalOutcome.mqh:17 |
| Normative contract | Docs/07:9–24; Docs/HSB.2C_Journal_Persistence_Reconciliation.md:7 |
| Formula IDs | F042/F053/F060 |
| Error IDs | ERR003/013/026 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | EXTERNAL_DTO_FINGERPRINT_ONLY |
| Limitations / side effects | Nonempty self-derivedstring не independent brokerrecord/authentication; fixedprecision collisions |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{return HSBI_UlongToString(x.actionId)+"|"+HSBI_UlongToString(x.eventId)+"|"+HSBI_UlongToString(x.dealId)+"|"+
   HSBI_UlongToString(x.positionIdentifier)+"|"+HSBI_UlongToString(x.ticket)+"|"+LongToString(x.accountLogin)+"|"+x.symbol+"|"+
   LongToString(x.magic)+"|"+IntegerToString((int)x.direction)+"|"+IntegerToString((int)x.role)+"|"+DoubleToString(x.volume,8)+"|"+
   DoubleToString(x.price,12)+"|"+HSBI_UlongToString(x.stateRevision)+"|"+HSBI_UlongToString(x.cycleId)+"|"+HSBI_UlongToString(x.planId)+"|"+
   IntegerToString((int)x.source)+"|"+IntegerToString((int)x.runtimeConfirmed)+"|"+IntegerToString((int)x.positionActuallyRead)+"|"+
   IntegerToString((int)x.dealActuallyRead)+"|"+LongToString((long)x.readTimestamp)+"|"+IntegerToString((int)x.status);}
~~~

### FUNCTION HSBI_ReconcileExecutionOutcome

| Field | Individual analysis |
|---|---|
| Function ID | Include/Execution/HSBI_ExternalOutcome.mqh:22:HSBI_ReconcileExecutionOutcome |
| Source | Include/Execution/HSBI_ExternalOutcome.mqh:22–32 |
| Signature | HSBI_ExecutionReconciliationResult HSBI_ReconcileExecutionOutcome(const HSBI_ExecutionReconciliationInput &x) |
| Inputs | const HSBI_ExecutionReconciliationInput &x |
| Outputs / Postconditions | Default reconcilingfalse;onlyallmatch→completionAllowedtrue,targetCOMPLETED;noMutationBeforeCommittrue |
| Domain | intent/outcome,expectedlastEvent,tolerances lots/price |
| Preconditions | Independent runtime terminal source andactualread flags; fullintentstructure separately |
| Guards | CompletionSourceAllowed;intentdigest;outcomedigest;conflict/fresh/ownershipflags;COMPLETED+3runtimeflags;14identity/volume/pricecomparisons |
| Callers | NO_CALLER_FOUND: all74 production source bodies, no dynamic/native proof |
| Dependencies | HSBI_IsCompletionSourceAllowed @ Include/Execution/HSBI_ExternalOutcome.mqh:25; HSBI_ValidateExecutionIntentDigest @ Include/Execution/HSBI_ExternalOutcome.mqh:25; HSBI_ExternalOutcomeDigest @ Include/Execution/HSBI_ExternalOutcome.mqh:25 |
| Normative contract | Docs/07:6–24; Docs/HSB.2C_Journal_Persistence_Reconciliation.md:7 |
| Formula IDs | F024/F036/F053/F063 |
| Error IDs | ERR010/013/017/024/049 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | LOCAL_COMPLETION_PROOF_INCOMPLETE |
| Limitations / side effects | DoesnotcallStructure;nonfinitevolume/price/tolerances notvalidated; matchingunknownenumspossible; readTimestamp notfreshwindowchecked; no durableapply |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{
   HSBI_ExecutionReconciliationResult r;ZeroMemory(r);r.targetStatus=HSBI_INTENT_RECONCILING;r.reason=HSBI_REASON_INTERNAL_INVARIANT_FAILED;r.details="RECONCILIATION_REJECTED";r.noMutationBeforeCommit=true;
   if(!HSBI_IsCompletionSourceAllowed(x.runtimeMode,(int)x.outcome.source)||!HSBI_ValidateExecutionIntentDigest(x.intent)||x.outcome.digest!=HSBI_ExternalOutcomeDigest(x.outcome)||x.reconciliationConflict||!x.snapshotFresh||!x.ownershipPassed)return r;
   if(x.outcome.status!=HSBI_EXTERNAL_COMPLETED||!x.outcome.runtimeConfirmed||!x.outcome.positionActuallyRead||!x.outcome.dealActuallyRead)return r;
   if(x.outcome.actionId!=x.intent.expectedActionId||x.outcome.eventId<=x.lastAppliedEventId||x.outcome.dealId==0||x.outcome.positionIdentifier!=x.intent.sourcePositionIdentifier||
      x.outcome.ticket!=x.intent.sourceTicket||x.outcome.accountLogin!=x.intent.accountLogin||x.outcome.symbol!=x.intent.symbol||x.outcome.magic!=x.intent.magic||
      x.outcome.direction!=x.intent.direction||x.outcome.role!=x.intent.role||x.outcome.stateRevision!=x.intent.stateRevision||x.outcome.cycleId!=x.intent.cycleId||
      x.outcome.planId!=x.intent.planId||MathAbs(x.outcome.volume-x.intent.normalizedVolume)>x.volumeTolerance||MathAbs(x.outcome.price-x.intent.controlPrice)>x.priceTolerance)return r;
   r.valid=true;r.completionAllowed=true;r.targetStatus=HSBI_INTENT_COMPLETED;r.reason=HSBI_REASON_OK;r.details="RECONCILIATION_PASSED";r.digest=x.intent.digest+"|"+x.outcome.digest;return r;
}
~~~

## R2 — индивидуальные grid/geometry/candidate функции, продолжение без замены43 карт

### FUNCTION HSBI_GridTolerance

| Field | Individual analysis |
|---|---|
| Function ID | Include/Planning/HSBI_BrokerGrid.mqh:7:HSBI_GridTolerance |
| Source | Include/Planning/HSBI_BrokerGrid.mqh:7–7 |
| Signature | double HSBI_GridTolerance(const double step) |
| Inputs | const double step |
| Outputs / Postconditions | max(1e-10,abs(step)*1e-8) |
| Domain | step lot/price;return sameunit |
| Preconditions | stepfinitepositive callerprecondition |
| Guards | No directguard;MathMax/Abs |
| Callers | HSBI_ValidateExecutionPreflight @ Include/Execution/HSBI_ExecutionPreflight.mqh:31; HSBI_CalculateProjectedProfit @ Include/Money/HSBI_BrokerMoneyModel.mqh:13; HSBI_IsPriceOnTickGrid @ Include/Planning/HSBI_BrokerGrid.mqh:11; HSBI_IsVolumeOnGrid @ Include/Planning/HSBI_BrokerGrid.mqh:24; HSBI_ValidateVolume @ Include/Planning/HSBI_BrokerGrid.mqh:36; HSBI_ValidateVolume @ Include/Planning/HSBI_BrokerGrid.mqh:36; HSBI_ValidateTypedControlPrice @ Include/Planning/HSBI_ControlPrices.mqh:21; HSBI_ValidateTypedControlPrice @ Include/Planning/HSBI_ControlPrices.mqh:22; HSBI_ValidateLevelMarket @ Include/Planning/HSBI_FutureSmallSolver.mqh:22; HSBI_ValidateLevelMarket @ Include/Planning/HSBI_FutureSmallSolver.mqh:23; HSBI_ValidateLevelMarket @ Include/Planning/HSBI_FutureSmallSolver.mqh:24; HSBI_EvaluateFutureSmallLevel @ Include/Planning/HSBI_FutureSmallSolver.mqh:68; HSBI_EvaluateFutureSmallLevel @ Include/Planning/HSBI_FutureSmallSolver.mqh:69; HSBI_SolveFutureSmall @ Include/Planning/HSBI_FutureSmallSolver.mqh:142; HSBI_SolveFutureSmall @ Include/Planning/HSBI_FutureSmallSolver.mqh:144; HSBI_SolveBigGeometry @ Include/Planning/HSBI_GeometrySolver.mqh:31; HSBI_SolveBigGeometry @ Include/Planning/HSBI_GeometrySolver.mqh:31; HSBI_SolveBigGeometry @ Include/Planning/HSBI_GeometrySolver.mqh:31; HSBI_SolveBigGeometry @ Include/Planning/HSBI_GeometrySolver.mqh:34; HSBI_SolveNewFar @ Include/Planning/HSBI_NewFarSolver.mqh:109 |
| Dependencies | NONE project functions |
| Normative contract | Docs/05_GEOMETRY_MODEL_RU.md; Docs/24:3 |
| Formula IDs | F001/F003/F044/F048 |
| Error IDs | ERR039/040 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | NUMERIC_TOLERANCE_PROFILE |
| Limitations / side effects | Fixedabsolute floor tolerance requiresdomain;not brokerpolicy itself |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{return MathMax(1.0e-10,MathAbs(step)*1.0e-8);}
~~~

### FUNCTION HSBI_IsPriceOnTickGrid

| Field | Individual analysis |
|---|---|
| Function ID | Include/Planning/HSBI_BrokerGrid.mqh:8:HSBI_IsPriceOnTickGrid |
| Source | Include/Planning/HSBI_BrokerGrid.mqh:8–12 |
| Signature | bool HSBI_IsPriceOnTickGrid(const double price,const double tickSize) |
| Inputs | const double price,const double tickSize |
| Outputs / Postconditions | falseinvalid;elseabs(price/tick−round)<=tol/tick |
| Domain | finitepositiveprice/tick |
| Preconditions | Declaredorigin0/toleranceprofile, broker origin independentlyfixed |
| Guards | 2finite/2positive guards;gridresidual |
| Callers | HSBI_NormalizePriceToTick @ Include/Planning/HSBI_BrokerGrid.mqh:17; HSBI_ValidatePriceGrid @ Include/Planning/HSBI_BrokerGrid.mqh:19; HSBI_ValidateTypedControlPrice @ Include/Planning/HSBI_ControlPrices.mqh:20; HSBI_ValidateLevelMarket @ Include/Planning/HSBI_FutureSmallSolver.mqh:22 |
| Dependencies | HSBI_IsFiniteNumber @ Include/Planning/HSBI_BrokerGrid.mqh:10; HSBI_IsFiniteNumber @ Include/Planning/HSBI_BrokerGrid.mqh:10; HSBI_GridTolerance @ Include/Planning/HSBI_BrokerGrid.mqh:11 |
| Normative contract | Docs/05:16; Docs/24:3–5 |
| Formula IDs | F036/F044/F048 |
| Error IDs | ERR039/040 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | LOCAL_PRICE_LATTICE |
| Limitations / side effects | Intermediate division/multiplication domain not separatelybounded; not universal brokerrounding policy |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{
   if(!HSBI_IsFiniteNumber(price)||!HSBI_IsFiniteNumber(tickSize)||price<=0.0||tickSize<=0.0)return false;
   double ticks=price/tickSize;return MathAbs(ticks-MathRound(ticks))<=HSBI_GridTolerance(tickSize)/tickSize;
}
~~~

### FUNCTION HSBI_ValidatePriceGrid

| Field | Individual analysis |
|---|---|
| Function ID | Include/Planning/HSBI_BrokerGrid.mqh:19:HSBI_ValidatePriceGrid |
| Source | Include/Planning/HSBI_BrokerGrid.mqh:19–19 |
| Signature | bool HSBI_ValidatePriceGrid(const double price,const HSBI_BrokerProperties &p) |
| Inputs | const double price,const HSBI_BrokerProperties &p |
| Outputs / Postconditions | VALID properties &&IsPriceOnTickGrid |
| Domain | price,p.tickSize |
| Preconditions | Broker properties authentic separately |
| Guards | 2delegated requiredcalls |
| Callers | HSBI_CalculateProjectedMargin @ Include/Money/HSBI_BrokerMarginModel.mqh:11; HSBI_CalculateProjectedProfit @ Include/Money/HSBI_BrokerMoneyModel.mqh:12; HSBI_CalculateProjectedProfit @ Include/Money/HSBI_BrokerMoneyModel.mqh:12 |
| Dependencies | HSBI_ValidateBrokerProperties @ Include/Planning/HSBI_BrokerGrid.mqh:19; HSBI_IsPriceOnTickGrid @ Include/Planning/HSBI_BrokerGrid.mqh:19 |
| Normative contract | Docs/24:3–5 |
| Formula IDs | F036/F044/F048 |
| Error IDs | ERR024/039/040 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | LOCAL_GRID_COMPOSITION |
| Limitations / side effects | Shape/grid не quote freshness/content; origin0 assumption |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{return HSBI_ValidateBrokerProperties(p)==HSBI_BROKER_PROPERTIES_VALID&&HSBI_IsPriceOnTickGrid(price,p.tickSize);}
~~~

### FUNCTION HSBI_PriceDistanceInTicks

| Field | Individual analysis |
|---|---|
| Function ID | Include/Planning/HSBI_BrokerGrid.mqh:20:HSBI_PriceDistanceInTicks |
| Source | Include/Planning/HSBI_BrokerGrid.mqh:20–20 |
| Signature | double HSBI_PriceDistanceInTicks(const double first,const double second,const double tickSize) |
| Inputs | const double first,const double second,const double tickSize |
| Outputs / Postconditions | invalidfirst/second or tick<=0→0;elseabs(second-first)/tick |
| Domain | priceprice difference dividedbytick→dimensionless |
| Preconditions | tickfinitepositive andsubtractnoflowcaller |
| Guards | 2finiteprices;tick>0 only |
| Callers | NO_CALLER_FOUND: all74 production source bodies, no dynamic/native proof |
| Dependencies | HSBI_IsFiniteNumber @ Include/Planning/HSBI_BrokerGrid.mqh:20; HSBI_IsFiniteNumber @ Include/Planning/HSBI_BrokerGrid.mqh:20 |
| Normative contract | Docs/01_GLOSSARY_AND_DIMENSIONS_RU.md; exact error sentinel CONTRACT_NOT_FOUND |
| Formula IDs | F044/F048 |
| Error IDs | ERR024/040 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | DISTANCE_HELPER_LIMITED_DOMAIN |
| Limitations / side effects | NaN/Infinity ticknotexplicitfinite; error0 not known actualzero; nonfiniteintermediate possible |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{if(!HSBI_IsFiniteNumber(first)||!HSBI_IsFiniteNumber(second)||tickSize<=0.0)return 0.0;return MathAbs(second-first)/tickSize;}
~~~

### FUNCTION HSBI_IsVolumeOnGrid

| Field | Individual analysis |
|---|---|
| Function ID | Include/Planning/HSBI_BrokerGrid.mqh:21:HSBI_IsVolumeOnGrid |
| Source | Include/Planning/HSBI_BrokerGrid.mqh:21–25 |
| Signature | bool HSBI_IsVolumeOnGrid(const double volume,const double step) |
| Inputs | const double volume,const double step |
| Outputs / Postconditions | falseinvalid;elseabs(units-round)<=tol/step |
| Domain | finitepositivevolume/step |
| Preconditions | Origin/tolerance approved independently |
| Guards | 2finite/2positive;gridresidual |
| Callers | HSBI_ValidateVolume @ Include/Planning/HSBI_BrokerGrid.mqh:36; HSBI_SolveBigGeometry @ Include/Planning/HSBI_GeometrySolver.mqh:32; HSBI_SolveBigGeometry @ Include/Planning/HSBI_GeometrySolver.mqh:32 |
| Dependencies | HSBI_IsFiniteNumber @ Include/Planning/HSBI_BrokerGrid.mqh:23; HSBI_IsFiniteNumber @ Include/Planning/HSBI_BrokerGrid.mqh:23; HSBI_GridTolerance @ Include/Planning/HSBI_BrokerGrid.mqh:24 |
| Normative contract | Docs/04:9; Docs/24:3–5 |
| Formula IDs | F001/F003/F004/F048 |
| Error IDs | ERR039/040 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | LOCAL_LOT_LATTICE |
| Limitations / side effects | Min/max notscope; don'ttreatgridpass asbrokertradability |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{
   if(!HSBI_IsFiniteNumber(volume)||!HSBI_IsFiniteNumber(step)||volume<=0.0||step<=0.0)return false;
   double units=volume/step;return MathAbs(units-MathRound(units))<=HSBI_GridTolerance(step)/step;
}
~~~

### FUNCTION HSBI_FloorVolumeToStep

| Field | Individual analysis |
|---|---|
| Function ID | Include/Planning/HSBI_BrokerGrid.mqh:26:HSBI_FloorVolumeToStep |
| Source | Include/Planning/HSBI_BrokerGrid.mqh:26–26 |
| Signature | double HSBI_FloorVolumeToStep(const double volume,const double step) |
| Inputs | const double volume,const double step |
| Outputs / Postconditions | invalid→0;floor(volume/step+1e-12)*step |
| Domain | volume/stepfinitepositive |
| Preconditions | origin0 profile+bounded intermediates |
| Guards | 2finite/2positive guards |
| Callers | HSBI_NormalizeVolume @ Include/Planning/HSBI_BrokerGrid.mqh:31; HSBI_SolveBigGeometry @ Include/Planning/HSBI_GeometrySolver.mqh:30; HSBI_SolveBigGeometry @ Include/Planning/HSBI_GeometrySolver.mqh:30 |
| Dependencies | HSBI_IsFiniteNumber @ Include/Planning/HSBI_BrokerGrid.mqh:26; HSBI_IsFiniteNumber @ Include/Planning/HSBI_BrokerGrid.mqh:26 |
| Normative contract | Docs/04:9; Docs/05:16 |
| Formula IDs | F001/F002/F004/F048 |
| Error IDs | ERR014/039/040 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | FLOOR_PRIMITIVE |
| Limitations / side effects | No min/max/outputfinite check; exactrealfloor proof doesnotautomaticallycoverepsilon/nativebinary64 |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{if(!HSBI_IsFiniteNumber(volume)||!HSBI_IsFiniteNumber(step)||volume<=0.0||step<=0.0)return 0.0;return MathFloor(volume/step+1.0e-12)*step;}
~~~

### FUNCTION HSBI_CeilVolumeToStep

| Field | Individual analysis |
|---|---|
| Function ID | Include/Planning/HSBI_BrokerGrid.mqh:27:HSBI_CeilVolumeToStep |
| Source | Include/Planning/HSBI_BrokerGrid.mqh:27–27 |
| Signature | double HSBI_CeilVolumeToStep(const double volume,const double step) |
| Inputs | const double volume,const double step |
| Outputs / Postconditions | invalid→0;ceil(volume/step−1e-12)*step |
| Domain | volume/stepfinitepositive |
| Preconditions | origin0 profile+bounded intermediates |
| Guards | 2finite/2positive guards |
| Callers | HSBI_NormalizeVolume @ Include/Planning/HSBI_BrokerGrid.mqh:30; HSBI_SolveBigGeometry @ Include/Planning/HSBI_GeometrySolver.mqh:30 |
| Dependencies | HSBI_IsFiniteNumber @ Include/Planning/HSBI_BrokerGrid.mqh:27; HSBI_IsFiniteNumber @ Include/Planning/HSBI_BrokerGrid.mqh:27 |
| Normative contract | Docs/04:9; Docs/05:16 |
| Formula IDs | F003/F004/F048 |
| Error IDs | ERR014/039/040 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | CEIL_PRIMITIVE |
| Limitations / side effects | No min/max/outputfinite; roundedeconomics requirepostgates |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{if(!HSBI_IsFiniteNumber(volume)||!HSBI_IsFiniteNumber(step)||volume<=0.0||step<=0.0)return 0.0;return MathCeil(volume/step-1.0e-12)*step;}
~~~

### FUNCTION HSBI_NormalizeVolume

| Field | Individual analysis |
|---|---|
| Function ID | Include/Planning/HSBI_BrokerGrid.mqh:28:HSBI_NormalizeVolume |
| Source | Include/Planning/HSBI_BrokerGrid.mqh:28–32 |
| Signature | double HSBI_NormalizeVolume(const double volume,const double step,const HSBI_VolumePurpose purpose) |
| Inputs | const double volume,const double step,const HSBI_VolumePurpose purpose |
| Outputs / Postconditions | SMALL_BASE→ceil,elsefloor |
| Domain | volume/step lots,purposeenum |
| Preconditions | Knownpurposecaller |
| Guards | onepurposeequality;delegatesgridfunctions |
| Callers | HSBI_SolveNewFar @ Include/Planning/HSBI_NewFarSolver.mqh:110 |
| Dependencies | HSBI_CeilVolumeToStep @ Include/Planning/HSBI_BrokerGrid.mqh:30; HSBI_FloorVolumeToStep @ Include/Planning/HSBI_BrokerGrid.mqh:31 |
| Normative contract | Docs/04:9; Docs/05:16 |
| Formula IDs | F001/F002/F003/F048 |
| Error IDs | ERR014/039/049 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | PURPOSE_SELECTOR_PARTIAL |
| Limitations / side effects | Unknownpurpose defaultsfloor, so closed-domain guardmissinglocally; min/maxseparate |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{
   if(purpose==HSBI_VOLUME_SMALL_BASE)return HSBI_CeilVolumeToStep(volume,step);
   return HSBI_FloorVolumeToStep(volume,step);
}
~~~

### FUNCTION HSBI_ValidateVolume

| Field | Individual analysis |
|---|---|
| Function ID | Include/Planning/HSBI_BrokerGrid.mqh:33:HSBI_ValidateVolume |
| Source | Include/Planning/HSBI_BrokerGrid.mqh:33–37 |
| Signature | bool HSBI_ValidateVolume(const double volume,const HSBI_BrokerProperties &p) |
| Inputs | const double volume,const HSBI_BrokerProperties &p |
| Outputs / Postconditions | validproperties &&finite &&min−tol<=V<=max+tol &&onGrid |
| Domain | finitevolume lots,properties |
| Preconditions | Independentbrokervolume facts |
| Guards | properties;finite;2bounds;grid |
| Callers | HSBI_ValidateExecutionPreflight @ Include/Execution/HSBI_ExecutionPreflight.mqh:30; HSBI_CalculateProjectedMargin @ Include/Money/HSBI_BrokerMarginModel.mqh:10; HSBI_CalculateProjectedProfit @ Include/Money/HSBI_BrokerMoneyModel.mqh:11; HSBI_ValidateFarProjection @ Include/Planning/HSBI_FutureSmallSolver.mqh:35; HSBI_SolveBigGeometry @ Include/Planning/HSBI_GeometrySolver.mqh:27; HSBI_SolveBigGeometry @ Include/Planning/HSBI_GeometrySolver.mqh:33; HSBI_ValidateNewFarSource @ Include/Planning/HSBI_NewFarSolver.mqh:72; HSBI_SolveNewFar @ Include/Planning/HSBI_NewFarSolver.mqh:112 |
| Dependencies | HSBI_ValidateBrokerProperties @ Include/Planning/HSBI_BrokerGrid.mqh:35; HSBI_IsFiniteNumber @ Include/Planning/HSBI_BrokerGrid.mqh:35; HSBI_GridTolerance @ Include/Planning/HSBI_BrokerGrid.mqh:36; HSBI_GridTolerance @ Include/Planning/HSBI_BrokerGrid.mqh:36; HSBI_IsVolumeOnGrid @ Include/Planning/HSBI_BrokerGrid.mqh:36 |
| Normative contract | Docs/24:3–5; Docs/14_NEW_FAR_SOLVER_SPECIFICATION_RU.md:9 |
| Formula IDs | F004/F048 |
| Error IDs | ERR039/040 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | LOCAL_BROKER_VOLUME_ADMISSION |
| Limitations / side effects | Doesnotproveactualfill/ownership/source;origin0 andtolerance profiles pending |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{
   if(HSBI_ValidateBrokerProperties(p)!=HSBI_BROKER_PROPERTIES_VALID||!HSBI_IsFiniteNumber(volume))return false;
   return volume>=p.volumeMin-HSBI_GridTolerance(p.volumeStep)&&volume<=p.volumeMax+HSBI_GridTolerance(p.volumeStep)&&HSBI_IsVolumeOnGrid(volume,p.volumeStep);
}
~~~

### FUNCTION HSBI_ValidateCandidatePlan

| Field | Individual analysis |
|---|---|
| Function ID | Include/Planning/HSBI_CandidatePlan.mqh:6:HSBI_ValidateCandidatePlan |
| Source | Include/Planning/HSBI_CandidatePlan.mqh:6–6 |
| Signature | bool HSBI_ValidateCandidatePlan(const HSBI_CandidatePlan &p) |
| Inputs | const HSBI_CandidatePlan &p |
| Outputs / Postconditions | true iff6requirements |
| Domain | plan/cycle/rev/marketsnapshotpositive,immutable,FarIdentity |
| Preconditions | Fullproofs/independentplancontent external |
| Guards | 4positiveIDs;immutable;validIdentity |
| Callers | NO_CALLER_FOUND: all74 production source bodies, no dynamic/native proof |
| Dependencies | HSBI_IsValidIdentity @ Include/Planning/HSBI_CandidatePlan.mqh:6 |
| Normative contract | Docs/18:10–15; Docs/07:6–12 |
| Formula IDs | F053/F057/F060 |
| Error IDs | ERR013/026/049 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | PLAN_HEADER_ONLY |
| Limitations / side effects | Lots/geometry/controls/digests/gates notchecked; immutable bool not immutable storage |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{return p.planId>0&&p.cycleId>0&&p.stateRevision>0&&p.marketSnapshotId>0&&p.immutable&&HSBI_IsValidIdentity(p.farIdentity);}
~~~

### FUNCTION HSBI_CandidatePlanFingerprint

| Field | Individual analysis |
|---|---|
| Function ID | Include/Planning/HSBI_CandidatePlan.mqh:7:HSBI_CandidatePlanFingerprint |
| Source | Include/Planning/HSBI_CandidatePlan.mqh:7–7 |
| Signature | string HSBI_CandidatePlanFingerprint(const HSBI_CandidatePlan &p) |
| Inputs | const HSBI_CandidatePlan &p |
| Outputs / Postconditions | concat5fields |
| Domain | plan/cycle/revision/marketID,positionFingerprint |
| Preconditions | Do not useasfullplancodec |
| Guards | No domain/bodyguard |
| Callers | HSBI_SameCandidatePlan @ Include/Planning/HSBI_CandidatePlan.mqh:8; HSBI_SameCandidatePlan @ Include/Planning/HSBI_CandidatePlan.mqh:8 |
| Dependencies | HSBI_UlongToString @ Include/Planning/HSBI_CandidatePlan.mqh:7; HSBI_UlongToString @ Include/Planning/HSBI_CandidatePlan.mqh:7; HSBI_UlongToString @ Include/Planning/HSBI_CandidatePlan.mqh:7; HSBI_UlongToString @ Include/Planning/HSBI_CandidatePlan.mqh:7 |
| Normative contract | Docs/16:8; Docs/HSB.2C_Execution_Intent_Spec.md:3 |
| Formula IDs | F057/F060 |
| Error IDs | ERR026 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | PARTIAL_PLAN_FINGERPRINT |
| Limitations / side effects | Changing ratios/lots/moneyPreview withsamemetadata leavesfingerprint; source fullbodyauthorityabsent |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{return HSBI_UlongToString(p.planId)+"|"+HSBI_UlongToString(p.cycleId)+"|"+HSBI_UlongToString(p.stateRevision)+"|"+p.positionFingerprint+"|"+HSBI_UlongToString(p.marketSnapshotId);}
~~~

### FUNCTION HSBI_SameCandidatePlan

| Field | Individual analysis |
|---|---|
| Function ID | Include/Planning/HSBI_CandidatePlan.mqh:8:HSBI_SameCandidatePlan |
| Source | Include/Planning/HSBI_CandidatePlan.mqh:8–8 |
| Signature | bool HSBI_SameCandidatePlan(const HSBI_CandidatePlan &a,const HSBI_CandidatePlan &b) |
| Inputs | const HSBI_CandidatePlan &a,const HSBI_CandidatePlan &b |
| Outputs / Postconditions | fingerprints equal→true |
| Domain | 2constplans |
| Preconditions | Fullpayload comparison independentlymandatory elsewhere |
| Guards | singlefingerprintequality |
| Callers | NO_CALLER_FOUND: all74 production source bodies, no dynamic/native proof |
| Dependencies | HSBI_CandidatePlanFingerprint @ Include/Planning/HSBI_CandidatePlan.mqh:8; HSBI_CandidatePlanFingerprint @ Include/Planning/HSBI_CandidatePlan.mqh:8 |
| Normative contract | Docs/07:6–12; Docs/16:8 |
| Formula IDs | F057/F060 |
| Error IDs | ERR026 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | METADATA_EQUALITY_ONLY |
| Limitations / side effects | Не fullimmutablepayload equality; cannotclaimplanunchanged if lots/gateschanged |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{return HSBI_CandidatePlanFingerprint(a)==HSBI_CandidatePlanFingerprint(b);}
~~~

### FUNCTION HSBI_IsSnapshotFresh

| Field | Individual analysis |
|---|---|
| Function ID | Include/Planning/HSBI_ControlPrices.mqh:11:HSBI_IsSnapshotFresh |
| Source | Include/Planning/HSBI_ControlPrices.mqh:11–11 |
| Signature | bool HSBI_IsSnapshotFresh(const HSBI_MarketSnapshot &s,const datetime now) |
| Inputs | const HSBI_MarketSnapshot &s,const datetime now |
| Outputs / Postconditions | timestamp>0 &&limit>=0 &&now−timestamp<=limit |
| Domain | timestamp/now seconds,freshnessSeconds>=0 |
| Preconditions | Clockauthority/skew policycaller |
| Guards | 3conditions |
| Callers | NO_CALLER_FOUND: all74 production source bodies, no dynamic/native proof |
| Dependencies | NONE project functions |
| Normative contract | Docs/27_CONTROL_PRICES_AND_COSTS_RU.md; SNAP-FIXTURE-1 proposed |
| Formula IDs | F057/F060 |
| Error IDs | ERR024 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | CLOCK_WINDOW_PARTIAL |
| Limitations / side effects | Futuretimestamp canpasswithoutskewbound; doesn'tbindcontentorbrokerreceipt |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{return s.timestamp>0&&s.freshnessSeconds>=0&&(now-s.timestamp)<=s.freshnessSeconds;}
~~~

### FUNCTION HSBI_ResolveCloseSide

| Field | Individual analysis |
|---|---|
| Function ID | Include/Planning/HSBI_ControlPrices.mqh:13:HSBI_ResolveCloseSide |
| Source | Include/Planning/HSBI_ControlPrices.mqh:13–13 |
| Signature | double HSBI_ResolveCloseSide(const HSBI_Direction d,const HSBI_MarketSnapshot &s) |
| Inputs | const HSBI_Direction d,const HSBI_MarketSnapshot &s |
| Outputs / Postconditions | BUYbid,SELLask,unknown0 |
| Domain | knownDirection,prices |
| Preconditions | Snapshotshape/freshness independentlyvalidated |
| Guards | 2enumexactbranches |
| Callers | NO_CALLER_FOUND: all74 production source bodies, no dynamic/native proof |
| Dependencies | NONE project functions |
| Normative contract | Docs/03:9; Docs/24:5 |
| Formula IDs | F046 |
| Error IDs | ERR024/049 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | CLOSE_SIDE_SELECTOR |
| Limitations / side effects | No finitequote guard; returned0errornotactualprice |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{if(d==HSBI_DIRECTION_BUY)return s.bid;if(d==HSBI_DIRECTION_SELL)return s.ask;return 0.0;}
~~~

### FUNCTION HSBI_ValidateMarketSnapshot

| Field | Individual analysis |
|---|---|
| Function ID | Include/Planning/HSBI_ControlPrices.mqh:14:HSBI_ValidateMarketSnapshot |
| Source | Include/Planning/HSBI_ControlPrices.mqh:14–14 |
| Signature | HSBI_ValidationResult HSBI_ValidateMarketSnapshot(const HSBI_MarketSnapshot &s) |
| Inputs | const HSBI_MarketSnapshot &s |
| Outputs / Postconditions | passed positiveorderedquotes/point/tick/nonemptyID |
| Domain | symbol,bid/ask,point,tick,snapshotID |
| Preconditions | Actualfreshness/grid separate |
| Guards | 6scalarconditions |
| Callers | NO_CALLER_FOUND: all74 production source bodies, no dynamic/native proof |
| Dependencies | HSBI_Result @ Include/Planning/HSBI_ControlPrices.mqh:14 |
| Normative contract | Docs/24:3; Docs/05:16 |
| Formula IDs | F036/F044/F046 |
| Error IDs | ERR024/040 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | SNAPSHOT_SHAPE_PARTIAL |
| Limitations / side effects | Infinitycanpass, timestamp/digits/freshness/origin notvalidated |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{bool ok=s.symbol!=""&&s.bid>0&&s.ask>=s.bid&&s.point>0&&s.tickSize>0&&s.snapshotId>0;return HSBI_Result(ok,ok?HSBI_REASON_OK:HSBI_REASON_STALE_SNAPSHOT,"HSBI-GEO-005","");}
~~~

### FUNCTION HSBI_ValidateControlPriceSet

| Field | Individual analysis |
|---|---|
| Function ID | Include/Planning/HSBI_ControlPrices.mqh:15:HSBI_ValidateControlPriceSet |
| Source | Include/Planning/HSBI_ControlPrices.mqh:15–15 |
| Signature | HSBI_ValidationResult HSBI_ValidateControlPriceSet(const HSBI_ControlPriceSet &p) |
| Inputs | const HSBI_ControlPriceSet &p |
| Outputs / Postconditions | passed iffcurrent/nextBig/small/final valid |
| Domain | 4pricepointvalidbools |
| Preconditions | Actualprice/grid/contentproof separately |
| Guards | 4flags |
| Callers | NO_CALLER_FOUND: all74 production source bodies, no dynamic/native proof |
| Dependencies | HSBI_Result @ Include/Planning/HSBI_ControlPrices.mqh:15 |
| Normative contract | Docs/05:19–22; Docs/27_CONTROL_PRICES_AND_COSTS_RU.md |
| Formula IDs | F044/F045/F052 |
| Error IDs | ERR024/026 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | CONTROL_SET_FLAGS_ONLY |
| Limitations / side effects | Adverse/gapstressfields notchecked; flags not amount/priceauthority |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{bool ok=p.currentClosePrice.valid&&p.nextBigControlPrice.valid&&p.smallTransitionControlPrice.valid&&p.finalClosePrice.valid;return HSBI_Result(ok,ok?HSBI_REASON_OK:HSBI_REASON_OFF_GRID_PRICE,"HSBI-DEC-003","");}
~~~

### FUNCTION HSBI_ValidateTypedControlPrice

| Field | Individual analysis |
|---|---|
| Function ID | Include/Planning/HSBI_ControlPrices.mqh:16:HSBI_ValidateTypedControlPrice |
| Source | Include/Planning/HSBI_ControlPrices.mqh:16–24 |
| Signature | bool HSBI_ValidateTypedControlPrice(const HSBI_ControlPrice &p,const string expectedSymbol) |
| Inputs | const HSBI_ControlPrice &p,const string expectedSymbol |
| Outputs / Postconditions | trueonlyshape+finitequotes/grid+BUYBid/SELLAsk |
| Domain | price/symbol/side/direction,tickpoint,IDs/time/flags |
| Preconditions | Independentfreshsnapshot andclock policy |
| Guards | 3flags;time/id/symbol;3finitequotes;positivebid/orderask/tick/point;grid;2directionbranches |
| Callers | HSBI_ValidateExecutionPreflight @ Include/Execution/HSBI_ExecutionPreflight.mqh:31; HSBI_EvaluateBasketMoney @ Include/Money/HSBI_BasketMoneyEvaluator.mqh:13 |
| Dependencies | HSBI_IsFiniteNumber @ Include/Planning/HSBI_ControlPrices.mqh:19; HSBI_IsFiniteNumber @ Include/Planning/HSBI_ControlPrices.mqh:19; HSBI_IsFiniteNumber @ Include/Planning/HSBI_ControlPrices.mqh:19; HSBI_IsPriceOnTickGrid @ Include/Planning/HSBI_ControlPrices.mqh:20; HSBI_GridTolerance @ Include/Planning/HSBI_ControlPrices.mqh:21; HSBI_GridTolerance @ Include/Planning/HSBI_ControlPrices.mqh:22 |
| Normative contract | Docs/24:3–5; Docs/27_CONTROL_PRICES_AND_COSTS_RU.md |
| Formula IDs | F036/F044/F046/F060 |
| Error IDs | ERR024/040 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | TYPED_LOCAL_PRICE_PROOF |
| Limitations / side effects | Pointfinite notexplicit checked; tickfinite delegated; noindependentcontentreceipt/timeage; expectedSymbol maybecopy |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{
   if(!p.valid||!p.fresh||!p.normalized||p.timestamp<=0||p.snapshotId==0||p.symbol==""||p.symbol!=expectedSymbol)return false;
   if(!HSBI_IsFiniteNumber(p.bid)||!HSBI_IsFiniteNumber(p.ask)||!HSBI_IsFiniteNumber(p.selectedPrice)||p.bid<=0.0||p.ask<p.bid||p.tickSize<=0.0||p.point<=0.0)return false;
   if(!HSBI_IsPriceOnTickGrid(p.selectedPrice,p.tickSize))return false;
   if(p.direction==HSBI_DIRECTION_BUY)return p.side==HSBI_PRICE_SIDE_BID&&MathAbs(p.selectedPrice-p.bid)<=HSBI_GridTolerance(p.tickSize);
   if(p.direction==HSBI_DIRECTION_SELL)return p.side==HSBI_PRICE_SIDE_ASK&&MathAbs(p.selectedPrice-p.ask)<=HSBI_GridTolerance(p.tickSize);
   return false;
}
~~~

### FUNCTION HSBI_ValidateRecoverySlope

| Field | Individual analysis |
|---|---|
| Function ID | Include/Planning/HSBI_GeometrySolver.mqh:6:HSBI_ValidateRecoverySlope |
| Source | Include/Planning/HSBI_GeometrySolver.mqh:6–11 |
| Signature | bool HSBI_ValidateRecoverySlope(const double coreVolume,const double trendVolume,const double smallVolume,const double farVolume,const bool brokerGridPassed,double &slope) |
| Inputs | const double coreVolume,const double trendVolume,const double smallVolume,const double farVolume,const bool brokerGridPassed,double &slope |
| Outputs / Postconditions | output0initial;finite/domainguards;thenC+T−S−F>0finite |
| Domain | 4lots,slopebyref |
| Preconditions | brokerGridPassed independentlyestablished |
| Guards | gridflag;4finite;C/T>=0,S/F>0;finitepositiveoutput |
| Callers | HSBI_SolveBigGeometry @ Include/Planning/HSBI_GeometrySolver.mqh:34 |
| Dependencies | HSBI_IsFiniteNumber @ Include/Planning/HSBI_GeometrySolver.mqh:8; HSBI_IsFiniteNumber @ Include/Planning/HSBI_GeometrySolver.mqh:8; HSBI_IsFiniteNumber @ Include/Planning/HSBI_GeometrySolver.mqh:8; HSBI_IsFiniteNumber @ Include/Planning/HSBI_GeometrySolver.mqh:8; HSBI_IsFiniteNumber @ Include/Planning/HSBI_GeometrySolver.mqh:10 |
| Normative contract | Docs/04:12; Docs/05:22 |
| Formula IDs | F005/F006/F038/F039 |
| Error IDs | ERR014/015/037/046 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | LOCAL_LINEAR_SLOPE |
| Limitations / side effects | DoesnotrequireeconomicCoremin;positive lot-slope notmoneyprofit theorem |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{
   slope=0.0;if(!brokerGridPassed||!HSBI_IsFiniteNumber(coreVolume)||!HSBI_IsFiniteNumber(trendVolume)||!HSBI_IsFiniteNumber(smallVolume)||!HSBI_IsFiniteNumber(farVolume))return false;
   if(coreVolume<0.0||trendVolume<0.0||smallVolume<=0.0||farVolume<=0.0)return false;
   slope=coreVolume+trendVolume-smallVolume-farVolume;return HSBI_IsFiniteNumber(slope)&&slope>0.0;
}
~~~

### FUNCTION HSBI_EvaluateRecoveryMoneyDirection

| Field | Individual analysis |
|---|---|
| Function ID | Include/Planning/HSBI_GeometrySolver.mqh:12:HSBI_EvaluateRecoveryMoneyDirection |
| Source | Include/Planning/HSBI_GeometrySolver.mqh:12–20 |
| Signature | HSBI_RecoveryDirectionResult HSBI_EvaluateRecoveryMoneyDirection(const HSBI_Direction farDirection,const double baseMoney,const double nextTickMoney,const bool moneyAvailable,const bool priceFresh) |
| Inputs | const HSBI_Direction farDirection,const double baseMoney,const double nextTickMoney,const bool moneyAvailable,const bool priceFresh |
| Outputs / Postconditions | finiteknownnumbers;delta>0 passes |
| Domain | moneybase/next inonecurrency,directionenum |
| Preconditions | Nexttick mustfavorable price movement, independentvaluation |
| Guards | priceFresh;moneyAvailable;2finite;directionwhitelist;delta>0 |
| Callers | NO_CALLER_FOUND: all74 production source bodies, no dynamic/native proof |
| Dependencies | HSBI_IsFiniteNumber @ Include/Planning/HSBI_GeometrySolver.mqh:17; HSBI_IsFiniteNumber @ Include/Planning/HSBI_GeometrySolver.mqh:17 |
| Normative contract | Docs/05:22; Docs/03:12 |
| Formula IDs | F038/F039/F050 |
| Error IDs | ERR037/046 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | TWO_VALUE_COMPARISON |
| Limitations / side effects | PricecoordinatesnotinputsoFarBUYmirrorcallerresponsibility; two-point delta notrange/globalmonotonicity |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{
   HSBI_RecoveryDirectionResult r;ZeroMemory(r);r.baseMoney=baseMoney;r.nextTickMoney=nextTickMoney;r.moneyAvailable=moneyAvailable;r.priceFresh=priceFresh;r.status=HSBI_CALC_REJECT;r.reason=HSBI_REASON_INTERNAL_INVARIANT_FAILED;
   if(!priceFresh){r.reason=HSBI_REASON_STALE_SNAPSHOT;return r;}
   if(!moneyAvailable){r.status=HSBI_CALC_UNAVAILABLE;r.reason=HSBI_REASON_NOT_INITIALIZED;return r;}
   if(!HSBI_IsFiniteNumber(baseMoney)||!HSBI_IsFiniteNumber(nextTickMoney)){r.status=HSBI_CALC_ERROR;return r;}
   if(farDirection!=HSBI_DIRECTION_BUY&&farDirection!=HSBI_DIRECTION_SELL)return r;
   r.deltaMoney=nextTickMoney-baseMoney;r.directionCorrect=r.deltaMoney>0.0;r.status=r.directionCorrect?HSBI_CALC_PASS:HSBI_CALC_REJECT;r.reason=r.directionCorrect?HSBI_REASON_OK:HSBI_REASON_INTERNAL_INVARIANT_FAILED;return r;
}
~~~

### FUNCTION HSBI_SolveBigGeometry

| Field | Individual analysis |
|---|---|
| Function ID | Include/Planning/HSBI_GeometrySolver.mqh:21:HSBI_SolveBigGeometry |
| Source | Include/Planning/HSBI_GeometrySolver.mqh:21–37 |
| Signature | HSBI_GeometryResult HSBI_SolveBigGeometry(const double farVolume,const double coreRatio,const double trendRatio,const double smallRatio,const HSBI_BrokerProperties &p,const bool moneyPrerequisite,const bool riskPrerequisite) |
| Inputs | const double farVolume,const double coreRatio,const double trendRatio,const double smallRatio,const HSBI_BrokerProperties &p,const bool moneyPrerequisite,const bool riskPrerequisite |
| Outputs / Postconditions | typed geometryresult;PASSnormalizedvolumes/slope |
| Domain | Far lots,3ratios,brokergrid |
| Preconditions | Money/risk prerequisites true notindependentactualproof |
| Guards | properties;2prereqflags;3finiteratio/range;Farvolume;3rawfinite;floor/floor/ceil;Core/Trendzeroorgrid/max;Smallfullvolume;netBig/slope |
| Callers | HSBI_EvaluateFutureSmallLevel @ Include/Planning/HSBI_FutureSmallSolver.mqh:63 |
| Dependencies | HSBI_ValidateBrokerProperties @ Include/Planning/HSBI_GeometrySolver.mqh:24; HSBI_IsFiniteNumber @ Include/Planning/HSBI_GeometrySolver.mqh:26; HSBI_IsFiniteNumber @ Include/Planning/HSBI_GeometrySolver.mqh:26; HSBI_IsFiniteNumber @ Include/Planning/HSBI_GeometrySolver.mqh:26; HSBI_ValidateVolume @ Include/Planning/HSBI_GeometrySolver.mqh:27; HSBI_IsFiniteNumber @ Include/Planning/HSBI_GeometrySolver.mqh:29; HSBI_IsFiniteNumber @ Include/Planning/HSBI_GeometrySolver.mqh:29; HSBI_IsFiniteNumber @ Include/Planning/HSBI_GeometrySolver.mqh:29; HSBI_FloorVolumeToStep @ Include/Planning/HSBI_GeometrySolver.mqh:30; HSBI_FloorVolumeToStep @ Include/Planning/HSBI_GeometrySolver.mqh:30; HSBI_CeilVolumeToStep @ Include/Planning/HSBI_GeometrySolver.mqh:30; HSBI_GridTolerance @ Include/Planning/HSBI_GeometrySolver.mqh:31; HSBI_GridTolerance @ Include/Planning/HSBI_GeometrySolver.mqh:31; HSBI_GridTolerance @ Include/Planning/HSBI_GeometrySolver.mqh:31; HSBI_IsVolumeOnGrid @ Include/Planning/HSBI_GeometrySolver.mqh:32; HSBI_IsVolumeOnGrid @ Include/Planning/HSBI_GeometrySolver.mqh:32; HSBI_ValidateVolume @ Include/Planning/HSBI_GeometrySolver.mqh:33; HSBI_ValidateRecoverySlope @ Include/Planning/HSBI_GeometrySolver.mqh:34; HSBI_GridTolerance @ Include/Planning/HSBI_GeometrySolver.mqh:34 |
| Normative contract | Docs/04:9–12; Docs/05:16–22 |
| Formula IDs | F001/F002/F003/F004/F005 |
| Error IDs | ERR014/015/039/040 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | GEOMETRY_SOURCE_DEFECT_CORE_MIN |
| Limitations / side effects | Core0/minnotchecked;Trendzero downstreammoneyincompatible;origin/range/native precision pending |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{
   HSBI_GeometryResult r;ZeroMemory(r);r.status=HSBI_CALC_REJECT;r.reason=HSBI_REASON_INVALID_VOLUME;r.details="INVALID_GEOMETRY";r.farVolume=farVolume;r.snapshotId=p.snapshotId;
   if(HSBI_ValidateBrokerProperties(p)!=HSBI_BROKER_PROPERTIES_VALID){r.status=HSBI_CALC_UNAVAILABLE;r.details="INVALID_BROKER_GRID";return r;}
   if(!moneyPrerequisite||!riskPrerequisite){r.details="FAILED_MONEY_OR_RISK_PREREQUISITE";return r;}
   if(!HSBI_IsFiniteNumber(coreRatio)||!HSBI_IsFiniteNumber(trendRatio)||!HSBI_IsFiniteNumber(smallRatio)||coreRatio<=0.0||trendRatio<0.0||smallRatio<=0.0){r.details="INVALID_RATIO";return r;}
   if(!HSBI_ValidateVolume(farVolume,p)){r.details="INVALID_FAR_VOLUME";return r;}
   r.rawCoreVolume=farVolume*coreRatio;r.rawTrendVolume=farVolume*trendRatio;r.rawSmallVolume=farVolume*smallRatio;
   if(!HSBI_IsFiniteNumber(r.rawCoreVolume)||!HSBI_IsFiniteNumber(r.rawTrendVolume)||!HSBI_IsFiniteNumber(r.rawSmallVolume)){r.status=HSBI_CALC_ERROR;r.details="VOLUME_OVERFLOW";return r;}
   r.coreVolume=HSBI_FloorVolumeToStep(r.rawCoreVolume,p.volumeStep);r.trendVolume=(r.rawTrendVolume==0.0?0.0:HSBI_FloorVolumeToStep(r.rawTrendVolume,p.volumeStep));r.smallVolume=HSBI_CeilVolumeToStep(r.rawSmallVolume,p.volumeStep);
   r.coreRoundedDown=r.coreVolume<=r.rawCoreVolume+HSBI_GridTolerance(p.volumeStep);r.trendRoundedDown=r.trendVolume<=r.rawTrendVolume+HSBI_GridTolerance(p.volumeStep);r.smallRoundedUp=r.smallVolume+HSBI_GridTolerance(p.volumeStep)>=r.rawSmallVolume;
   bool coreGrid=(r.coreVolume==0.0||(HSBI_IsVolumeOnGrid(r.coreVolume,p.volumeStep)&&r.coreVolume<=p.volumeMax));bool trendGrid=(r.trendVolume==0.0||(HSBI_IsVolumeOnGrid(r.trendVolume,p.volumeStep)&&r.trendVolume<=p.volumeMax));
   r.brokerGridPassed=coreGrid&&trendGrid&&HSBI_ValidateVolume(r.smallVolume,p);if(!r.brokerGridPassed){r.details="INVALID_NORMALIZED_VOLUME";return r;}
   r.netBigVolume=r.coreVolume+r.trendVolume-r.smallVolume;r.slopePassed=HSBI_ValidateRecoverySlope(r.coreVolume,r.trendVolume,r.smallVolume,r.farVolume,r.brokerGridPassed,r.recoverySlopeLots)&&r.recoverySlopeLots>HSBI_GridTolerance(p.volumeStep);
   if(r.netBigVolume<=0.0||!r.slopePassed){r.details="RECOVERY_SLOPE_FAILED";return r;}
   r.status=HSBI_CALC_PASS;r.valid=true;r.reason=HSBI_REASON_OK;r.details="PASS";return r;
}
~~~

### FUNCTION HSBI_ValidateNewFarCandidateStructure

| Field | Individual analysis |
|---|---|
| Function ID | Include/Planning/HSBI_NewFarCandidate.mqh:19:HSBI_ValidateNewFarCandidateStructure |
| Source | Include/Planning/HSBI_NewFarCandidate.mqh:19–23 |
| Signature | HSBI_ValidationResult HSBI_ValidateNewFarCandidateStructure(const HSBI_NewFarCandidate &c) |
| Inputs | const HSBI_NewFarCandidate &c |
| Outputs / Postconditions | normalized>0<oldFar,compression>0,2IDs>0 |
| Domain | normalized/oldFar/compressionLots lots;sourceIDs |
| Preconditions | Independentactualresidual/source separately |
| Guards | 5scalarpredicates |
| Callers | NO_CALLER_FOUND: all74 production source bodies, no dynamic/native proof |
| Dependencies | HSBI_Result @ Include/Planning/HSBI_NewFarCandidate.mqh:22 |
| Normative contract | Docs/14_NEW_FAR_SOLVER_SPECIFICATION_RU.md:9–22 |
| Formula IDs | F027/F028/F053 |
| Error IDs | ERR013/041/045 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | CANDIDATE_SHAPE_ONLY |
| Limitations / side effects | Finite/ratio/equation/grid/allproofs notvalidated; structureshape≠candidateauthorization |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{
   bool ok=c.normalizedVolume>0.0&&c.normalizedVolume<c.oldFarVolume&&c.compressionLots>0.0&&c.sourceBigCoreIdentifier>0&&c.sourceBigCoreTicket>0;
   return HSBI_Result(ok,ok?HSBI_REASON_OK:HSBI_REASON_INVALID_VOLUME,"HSBI-NF-001","");
}
~~~

### FUNCTION HSBI_IsCandidateSourceValid

| Field | Individual analysis |
|---|---|
| Function ID | Include/Planning/HSBI_NewFarCandidate.mqh:24:HSBI_IsCandidateSourceValid |
| Source | Include/Planning/HSBI_NewFarCandidate.mqh:24–25 |
| Signature | bool HSBI_IsCandidateSourceValid(const HSBI_NewFarCandidate &c,const ulong id,const ulong ticket) |
| Inputs | const HSBI_NewFarCandidate &c,const ulong id,const ulong ticket |
| Outputs / Postconditions | true iff2equalities |
| Domain | 2sourceIDs |
| Preconditions | Expectedindependentnonzeroorigin notcopied |
| Guards | 2exactequalities |
| Callers | NO_CALLER_FOUND: all74 production source bodies, no dynamic/native proof |
| Dependencies | NONE project functions |
| Normative contract | Docs/02:27; Docs/14_NEW_FAR_SOLVER_SPECIFICATION_RU.md |
| Formula IDs | F053/F062 |
| Error IDs | ERR013/041 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | SOURCE_EQUALITY_ONLY |
| Limitations / side effects | 0/0canmatch; notdescriptor/historyvolumeproof |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{return c.sourceBigCoreIdentifier==id&&c.sourceBigCoreTicket==ticket;}
~~~

### FUNCTION HSBI_IsCompleteCandidateProof

| Field | Individual analysis |
|---|---|
| Function ID | Include/Planning/HSBI_NewFarCandidate.mqh:26:HSBI_IsCompleteCandidateProof |
| Source | Include/Planning/HSBI_NewFarCandidate.mqh:26–32 |
| Signature | bool HSBI_IsCompleteCandidateProof(const HSBI_NewFarCandidate &c) |
| Inputs | const HSBI_NewFarCandidate &c |
| Outputs / Postconditions | trueonlylistedflags/status/digests |
| Domain | status,12bools,digeststrings |
| Preconditions | Independentproducer/provider validatescontent,numbers,source |
| Guards | VALIDstatus,feasible,proof/allocation/snapshot/fullDigestflags;9nonemptydigests |
| Callers | HSBI_CompareCandidateTieBreak @ Include/Planning/HSBI_NewFarCandidate.mqh:35; HSBI_CompareCandidateTieBreak @ Include/Planning/HSBI_NewFarCandidate.mqh:35; HSBI_SolveNewFar @ Include/Planning/HSBI_NewFarSolver.mqh:146; HSBI_ValidateRuntimeDecisionContext @ Include/Runtime/HSBI_RuntimeDecisionValidator.mqh:20 |
| Dependencies | NONE project functions |
| Normative contract | Docs/14_NEW_FAR_SOLVER_SPECIFICATION_RU.md; Docs/18:14 |
| Formula IDs | F053/F057/F060/F062 |
| Error IDs | ERR013/026 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | PROOF_COMPLETENESS_FLAGS_ONLY |
| Limitations / side effects | Doesnotrecomputecontents/finite/source/equations; nonempty/fullDigestValid notauthenticproof |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{
   return c.validationStatus==HSBI_STATUS_VALID&&c.nextCycleFeasible&&c.moneyProofValid&&c.marginProofValid&&c.riskProofValid&&
      c.futureSmallProofValid&&c.catchUpProofValid&&c.aggregateProofValid&&c.aggregateRuntimeConfirmed&&c.aggregateProofDigest!=""&&c.allocationPolicyValid&&c.controlSnapshotsValid&&c.costSnapshotsValid&&
      c.fullDigestValid&&c.moneyProofDigest!=""&&c.marginProofDigest!=""&&c.riskProofDigest!=""&&c.futureSmallProofDigest!=""&&
      c.catchUpProofDigest!=""&&c.allocationPolicyDigest!=""&&c.controlPriceDigest!=""&&c.costSnapshotDigest!=""&&c.candidateDigest!="";
}
~~~

### FUNCTION HSBI_CompareCandidateTieBreak

| Field | Individual analysis |
|---|---|
| Function ID | Include/Planning/HSBI_NewFarCandidate.mqh:33:HSBI_CompareCandidateTieBreak |
| Source | Include/Planning/HSBI_NewFarCandidate.mqh:33–41 |
| Signature | int HSBI_CompareCandidateTieBreak(const HSBI_NewFarCandidate &a,const HSBI_NewFarCandidate &b) |
| Inputs | const HSBI_NewFarCandidate &a,const HSBI_NewFarCandidate &b |
| Outputs / Postconditions | completefirst;minrisk,minmargin,minfuturecount,maxbuffer,minvolume,digest |
| Domain | finite risk/margin/moneybuffer,volume,count,digest |
| Preconditions | Allproofs/domain validatedbefore comparison |
| Guards | completepredicate;5comparisons;StringCompare |
| Callers | HSBI_SolveNewFar @ Include/Planning/HSBI_NewFarSolver.mqh:149 |
| Dependencies | HSBI_IsCompleteCandidateProof @ Include/Planning/HSBI_NewFarCandidate.mqh:35; HSBI_IsCompleteCandidateProof @ Include/Planning/HSBI_NewFarCandidate.mqh:35 |
| Normative contract | Docs/14_NEW_FAR_SOLVER_SPECIFICATION_RU.md:22–23; Docs/29_CANDIDATE_OBJECTIVE_AND_TIEBREAK_RU.md |
| Formula IDs | F047 |
| Error IDs | ERR019/045 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | POLICY_PRECEDENCE_UNRESOLVED |
| Limitations / side effects | Risk-first conflictsminN-first normativeversion; NaNorderingunverified; ordering not financialfeasibility |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{
   bool av=HSBI_IsCompleteCandidateProof(a),bv=HSBI_IsCompleteCandidateProof(b);if(av!=bv)return av?-1:1;
   if(a.riskNext!=b.riskNext)return a.riskNext<b.riskNext?-1:1;if(a.marginNext!=b.marginNext)return a.marginNext<b.marginNext?-1:1;
   if(a.futureTransitionCount!=b.futureTransitionCount)return a.futureTransitionCount<b.futureTransitionCount?-1:1;
   if(a.safetyBuffer!=b.safetyBuffer)return a.safetyBuffer>b.safetyBuffer?-1:1;
   if(a.normalizedVolume!=b.normalizedVolume)return a.normalizedVolume<b.normalizedVolume?-1:1;
   return StringCompare(a.candidateDigest,b.candidateDigest);
}
~~~


## R2 — индивидуальные FutureSmall/NewFar/risk функции, продолжение без замены43 карт

### FUNCTION HSBI_CalculateFutureSmallDepth

| Field | Individual analysis |
|---|---|
| Function ID | Include/Planning/HSBI_FutureSmallSolver.mqh:5:HSBI_CalculateFutureSmallDepth |
| Source | Include/Planning/HSBI_FutureSmallSolver.mqh:5–11 |
| Signature | bool HSBI_CalculateFutureSmallDepth(const double f,const double vmin,const double q,const double step,int &depth) |
| Inputs | const double f,const double vmin,const double q,const double step,int &depth |
| Outputs / Postconditions | depth0oninputerror;ceil(log(vmin/f)/logq)if0..INT_MAXfinite |
| Domain | f>=vmin>0,0<q<1,steppositivefinite;depthint32 |
| Preconditions | Uniformcontract каждого реального transition отдельно |
| Guards | 4finite;f/vmin/q/stepranges;logresultfinite/int32bounds |
| Callers | HSBI_SolveFutureSmall @ Include/Planning/HSBI_FutureSmallSolver.mqh:117 |
| Dependencies | HSBI_IsFiniteNumber @ Include/Planning/HSBI_FutureSmallSolver.mqh:7; HSBI_IsFiniteNumber @ Include/Planning/HSBI_FutureSmallSolver.mqh:7; HSBI_IsFiniteNumber @ Include/Planning/HSBI_FutureSmallSolver.mqh:7; HSBI_IsFiniteNumber @ Include/Planning/HSBI_FutureSmallSolver.mqh:8; HSBI_IsFiniteNumber @ Include/Planning/HSBI_FutureSmallSolver.mqh:9 |
| Normative contract | Docs/04:33–36; Docs/27_FUTURE_SMALL_SOLVER_RU.md |
| Formula IDs | F037/F058 |
| Error IDs | ERR021/031/032 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | CONDITIONAL_DEPTH_ARITHMETIC |
| Limitations / side effects | stepлишьвалидируется, не доказываетgrid contraction; boundнеwallclocktimeилиactualclose |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{
   depth=0; if(!HSBI_IsFiniteNumber(f)||!HSBI_IsFiniteNumber(vmin)||!HSBI_IsFiniteNumber(q)||
      !HSBI_IsFiniteNumber(step)||f<=0.0||vmin<=0.0||vmin>f||q<=0.0||q>=1.0||step<=0.0) return false;
   double value=MathLog(vmin/f)/MathLog(q); if(!HSBI_IsFiniteNumber(value)||value<0.0||value>2147483647.0) return false;
   depth=(int)MathCeil(value); return true;
}
~~~

### FUNCTION HSBI_ValidateConservativeBound

| Field | Individual analysis |
|---|---|
| Function ID | Include/Planning/HSBI_FutureSmallSolver.mqh:12:HSBI_ValidateConservativeBound |
| Source | Include/Planning/HSBI_FutureSmallSolver.mqh:12–17 |
| Signature | bool HSBI_ValidateConservativeBound(const double initialFar,const double observedFar,const double q,const int depth, const bool rounding,const bool costs,const bool margin,const bool risk,const bool loss) |
| Inputs | const double initialFar,const double observedFar,const double q,const int depth, const bool rounding,const bool costs,const bool margin,const bool risk,const bool loss |
| Outputs / Postconditions | bool conjunction+observed<=initial*q^depth+eps |
| Domain | initial/observedlots,qratio,depth>=2,5flags |
| Preconditions | Uniformfuturemodel иcompleteproviders не выводятсяизflags |
| Guards | depth/qdomain;5coverageflags;positiveFar;endpointbound |
| Callers | HSBI_SolveFutureSmall @ Include/Planning/HSBI_FutureSmallSolver.mqh:146 |
| Dependencies | NONE project functions |
| Normative contract | Docs/27_FUTURE_SMALL_SOLVER_RU.md; Docs/04:33–36 |
| Formula IDs | F037/F038/F058 |
| Error IDs | ERR021/031/032 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | PREFIX_BOUND_NOT_UNIVERSAL_PROOF |
| Limitations / side effects | No allfuture quantifier/finitechecks; finiteprefix cannotprove tail; no actualterminalroute |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{
   return depth>=2&&q>0.0&&q<1.0&&rounding&&costs&&margin&&risk&&loss&&initialFar>0.0&&observedFar>0.0&&
      observedFar<=initialFar*MathPow(q,depth)+1e-10;
}
~~~

### FUNCTION HSBI_ValidateLevelMarket

| Field | Individual analysis |
|---|---|
| Function ID | Include/Planning/HSBI_FutureSmallSolver.mqh:18:HSBI_ValidateLevelMarket |
| Source | Include/Planning/HSBI_FutureSmallSolver.mqh:18–26 |
| Signature | bool HSBI_ValidateLevelMarket(const HSBI_FutureSmallLevelMarketSnapshot &m,const int level,const HSBI_BrokerProperties &b,const HSBI_Direction d) |
| Inputs | const HSBI_FutureSmallLevelMarketSnapshot &m,const int level,const HSBI_BrokerProperties &b,const HSBI_Direction d |
| Outputs / Postconditions | false mismatch;knownBUYBid/SELLAsk only |
| Domain | levelindex,quotesprice,tick,snapshot/time/flags |
| Preconditions | Independent immutable snapshot authority/clock |
| Guards | index/flags/ID/time/symbol;3finitequotes;quoteorder;tickdelta;grid;side/priceequalities |
| Callers | HSBI_EvaluateFutureSmallLevel @ Include/Planning/HSBI_FutureSmallSolver.mqh:61 |
| Dependencies | HSBI_IsFiniteNumber @ Include/Planning/HSBI_FutureSmallSolver.mqh:21; HSBI_IsFiniteNumber @ Include/Planning/HSBI_FutureSmallSolver.mqh:21; HSBI_IsFiniteNumber @ Include/Planning/HSBI_FutureSmallSolver.mqh:21; HSBI_GridTolerance @ Include/Planning/HSBI_FutureSmallSolver.mqh:22; HSBI_IsPriceOnTickGrid @ Include/Planning/HSBI_FutureSmallSolver.mqh:22; HSBI_GridTolerance @ Include/Planning/HSBI_FutureSmallSolver.mqh:23; HSBI_GridTolerance @ Include/Planning/HSBI_FutureSmallSolver.mqh:24 |
| Normative contract | Docs/25_BROKER_GRID_AND_ROUNDING_RU.md; Docs/27_CONTROL_PRICES_AND_COSTS_RU.md |
| Formula IDs | F036/F044/F046/F060 |
| Error IDs | ERR024/040 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | LOCAL_LEVEL_PRICE_BINDING |
| Limitations / side effects | Clockage/independentcontent notproven; timestamp>0 неfreshwindow; normsidedomainpassedcaller |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{
   if(m.levelIndex!=level||!m.valid||!m.fresh||!m.normalized||m.snapshotId==0||m.timestamp<=0||m.symbol!=b.symbol||
      !HSBI_IsFiniteNumber(m.bid)||!HSBI_IsFiniteNumber(m.ask)||!HSBI_IsFiniteNumber(m.selectedPrice)||m.bid<=0.0||m.ask<m.bid||
      MathAbs(m.tickSize-b.tickSize)>HSBI_GridTolerance(b.tickSize)||!HSBI_IsPriceOnTickGrid(m.selectedPrice,m.tickSize)) return false;
   if(d==HSBI_DIRECTION_BUY) return m.side==HSBI_PRICE_SIDE_BID&&MathAbs(m.selectedPrice-m.bid)<=HSBI_GridTolerance(m.tickSize);
   if(d==HSBI_DIRECTION_SELL) return m.side==HSBI_PRICE_SIDE_ASK&&MathAbs(m.selectedPrice-m.ask)<=HSBI_GridTolerance(m.tickSize);
   return false;
}
~~~

### FUNCTION HSBI_ValidateLevelCosts

| Field | Individual analysis |
|---|---|
| Function ID | Include/Planning/HSBI_FutureSmallSolver.mqh:27:HSBI_ValidateLevelCosts |
| Source | Include/Planning/HSBI_FutureSmallSolver.mqh:27–31 |
| Signature | bool HSBI_ValidateLevelCosts(const HSBI_FutureSmallLevelCostSnapshot &c,const int level) |
| Inputs | const HSBI_FutureSmallLevelCostSnapshot &c,const int level |
| Outputs / Postconditions | true index/valid/fresh/id plus4ValidateCostSnapshot(false) |
| Domain | levelID,costsnapshotID,boolflags,moneycosts |
| Preconditions | Costinventory/basiscoverage external |
| Guards | 4headerchecks;4costvalidators |
| Callers | HSBI_EvaluateFutureSmallLevel @ Include/Planning/HSBI_FutureSmallSolver.mqh:62 |
| Dependencies | HSBI_ValidateCostSnapshot @ Include/Planning/HSBI_FutureSmallSolver.mqh:29; HSBI_ValidateCostSnapshot @ Include/Planning/HSBI_FutureSmallSolver.mqh:30; HSBI_ValidateCostSnapshot @ Include/Planning/HSBI_FutureSmallSolver.mqh:30; HSBI_ValidateCostSnapshot @ Include/Planning/HSBI_FutureSmallSolver.mqh:30 |
| Normative contract | Docs/24:7; Docs/27_CONTROL_PRICES_AND_COSTS_RU.md |
| Formula IDs | F008/F009/F036 |
| Error IDs | ERR015/022 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | FOUR_COST_SHAPES_ONLY |
| Limitations / side effects | Notcompletecostcoverage/window/sourceauthenticity; empty/inapplicablelegpolicyseparate |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{
   return c.levelIndex==level&&c.valid&&c.fresh&&c.snapshotId>0&&HSBI_ValidateCostSnapshot(c.farCosts,false)&&
      HSBI_ValidateCostSnapshot(c.coreCosts,false)&&HSBI_ValidateCostSnapshot(c.trendCosts,false)&&HSBI_ValidateCostSnapshot(c.smallCosts,false);
}
~~~

### FUNCTION HSBI_ValidateFarProjection

| Field | Individual analysis |
|---|---|
| Function ID | Include/Planning/HSBI_FutureSmallSolver.mqh:32:HSBI_ValidateFarProjection |
| Source | Include/Planning/HSBI_FutureSmallSolver.mqh:32–38 |
| Signature | bool HSBI_ValidateFarProjection(const HSBI_FutureFarProjection &p,const HSBI_BrokerProperties &b,const double before) |
| Inputs | const HSBI_FutureFarProjection &p,const HSBI_BrokerProperties &b,const double before |
| Outputs / Postconditions | OnlyBIGCORE_RESIDUAL withid+deal orEXPLICIT_MODEL withid accepted |
| Domain | finitebrokerlotgrid,0<next<before;sourceenum |
| Preconditions | Explicitmodel/residual origin independentlycertified |
| Guards | 4flags;source!=unavailable;positive/strictreduction;volumevalidator;2knownsourcebranches |
| Callers | HSBI_EvaluateFutureSmallLevel @ Include/Planning/HSBI_FutureSmallSolver.mqh:62 |
| Dependencies | HSBI_ValidateVolume @ Include/Planning/HSBI_FutureSmallSolver.mqh:35 |
| Normative contract | Docs/27_FUTURE_SMALL_SOLVER_RU.md; Docs/14:6–26 |
| Formula IDs | F027/F028/F053 |
| Error IDs | ERR013/021/041/045 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | PROJECTED_REDUCTION_ONLY |
| Limitations / side effects | confirmed bool notactualreceipt; projected!=actual; beforedomain dependscaller |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{
   if(!p.valid||!p.projected||p.actual||!p.confirmed||p.source==HSBI_FAR_PROJECTION_UNAVAILABLE||p.projectedFar<=0.0||
      p.projectedFar>=before||!HSBI_ValidateVolume(p.projectedFar,b)) return false;
   if(p.source==HSBI_FAR_PROJECTION_BIGCORE_RESIDUAL) return p.sourceIdentifier>0&&p.sourceDealId>0;
   return p.source==HSBI_FAR_PROJECTION_EXPLICIT_MODEL&&p.sourceIdentifier>0;
}
~~~

### FUNCTION HSBI_LevelControlPrice

| Field | Individual analysis |
|---|---|
| Function ID | Include/Planning/HSBI_FutureSmallSolver.mqh:39:HSBI_LevelControlPrice |
| Source | Include/Planning/HSBI_FutureSmallSolver.mqh:39–44 |
| Signature | HSBI_ControlPrice HSBI_LevelControlPrice(const HSBI_FutureSmallLevelMarketSnapshot &m,const HSBI_BrokerProperties &b,const HSBI_Direction d) |
| Inputs | const HSBI_FutureSmallLevelMarketSnapshot &m,const HSBI_BrokerProperties &b,const HSBI_Direction d |
| Outputs / Postconditions | Copyfields;mid=(bid+ask)/2;valid copied |
| Domain | quotesprice,point/tick/digits,levelsourceflags |
| Preconditions | Levelmarketshape validatedcaller |
| Guards | No independentguards |
| Callers | HSBI_EvaluateFutureSmallLevel @ Include/Planning/HSBI_FutureSmallSolver.mqh:77 |
| Dependencies | NONE project functions |
| Normative contract | Docs/27_CONTROL_PRICES_AND_COSTS_RU.md; Docs/24:3 |
| Formula IDs | F044/F046 |
| Error IDs | ERR024/040 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | PRICE_DTO_CONSTRUCTOR |
| Limitations / side effects | Midadditioncouldoverflow; selectedpricevalidator distinct;constructor doesn'tauthorize |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{
   HSBI_ControlPrice p; ZeroMemory(p); p.symbol=m.symbol;p.bid=m.bid;p.ask=m.ask;p.mid=(m.bid+m.ask)/2.0;
   p.selectedPrice=m.selectedPrice;p.direction=d;p.side=m.side;p.point=b.point;p.tickSize=m.tickSize;p.digits=b.digits;
   p.timestamp=m.timestamp;p.snapshotId=m.snapshotId;p.fresh=m.fresh;p.normalized=m.normalized;p.valid=m.valid;return p;
}
~~~

### FUNCTION HSBI_ValidateFutureSmallInput

| Field | Individual analysis |
|---|---|
| Function ID | Include/Planning/HSBI_FutureSmallSolver.mqh:45:HSBI_ValidateFutureSmallInput |
| Source | Include/Planning/HSBI_FutureSmallSolver.mqh:45–56 |
| Signature | bool HSBI_ValidateFutureSmallInput(const HSBI_FutureSmallInput &x) |
| Inputs | const HSBI_FutureSmallInput &x |
| Outputs / Postconditions | true ifflistedflags/ids/ranges+directionknown |
| Domain | depth2..128,counts>=depth,ratios/q/lots,currency/risk/marginflags |
| Preconditions | Arraysactualsizes/provider/freshness/coverageindependentcaller |
| Guards | staticmode/test/injectionpolicy;allocation;8availability/fresh flags;broker;3IDs;depth/countbounds;positiveFar/step;Q/compressionranges;directionwhitelist |
| Callers | HSBI_SolveFutureSmall @ Include/Planning/HSBI_FutureSmallSolver.mqh:116 |
| Dependencies | HSBI_IsStaticCalculationAllowed @ Include/Planning/HSBI_FutureSmallSolver.mqh:47; HSBI_IsInjectedProofAllowed @ Include/Planning/HSBI_FutureSmallSolver.mqh:47; HSBI_ValidateAllocationPolicy @ Include/Planning/HSBI_FutureSmallSolver.mqh:47; HSBI_ValidateBrokerProperties @ Include/Planning/HSBI_FutureSmallSolver.mqh:50 |
| Normative contract | Docs/27_FUTURE_SMALL_SOLVER_RU.md; Docs/14:6–26 |
| Formula IDs | F036/F037/F038/F048/F058 |
| Error IDs | ERR021/024/031/040 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | INPUT_SHAPE_NOT_GLOBAL_FEASIBILITY |
| Limitations / side effects | Counts notactualArraySize; severalconfigfields nofinite; terminalRouteAllowed unread; commonstep notboundbrokerstep |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{
   if(!HSBI_IsStaticCalculationAllowed(x.runtimeMode)||x.testOnlyApproximation||(x.useInjectedBrokerProofs&&!HSBI_IsInjectedProofAllowed(x.runtimeMode))||!HSBI_ValidateAllocationPolicy(x.allocationPolicy)||!x.brokerPropertiesValid||!x.snapshotsFresh||
      !x.roundingIncluded||!x.costsIncluded||!x.moneyState.available||!x.moneyState.fresh||!x.riskState.available||
      !x.riskState.fresh||!x.marginState.available||!x.marginState.fresh) return false;
   if(HSBI_ValidateBrokerProperties(x.broker)!=HSBI_BROKER_PROPERTIES_VALID||x.cycleId==0||x.stateRevision==0||x.planId==0||
      x.maximumDepth<2||x.maximumDepth>128||x.levelMarketSnapshotCount<x.maximumDepth||x.levelCostSnapshotCount<x.maximumDepth||
      x.farProjectionCount<x.maximumDepth||x.currentFar<=0.0||x.volumeStep<=0.0||x.conservativeQ<=0.0||x.conservativeQ>=1.0) return false;
   if(x.maxNewFarRatio<=0.0||x.maxNewFarRatio>=1.0||x.minimumCompressionLots<=0.0||
      x.minimumCompressionRatio<=0.0||x.minimumCompressionRatio>=1.0) return false;
   return x.farDirection==HSBI_DIRECTION_BUY||x.farDirection==HSBI_DIRECTION_SELL;
}
~~~

### FUNCTION HSBI_EvaluateFutureSmallLevel

| Field | Individual analysis |
|---|---|
| Function ID | Include/Planning/HSBI_FutureSmallSolver.mqh:57:HSBI_EvaluateFutureSmallLevel |
| Source | Include/Planning/HSBI_FutureSmallSolver.mqh:57–92 |
| Signature | HSBI_FutureSmallLevelResult HSBI_EvaluateFutureSmallLevel(const HSBI_FutureSmallLevelInput &x) |
| Inputs | const HSBI_FutureSmallLevelInput &x |
| Outputs / Postconditions | UNPROVEN onfailure;EXACT_LEVEL iflocalgates accepted |
| Domain | lots/recoverymoney/margin/risk,independentmarketcostsourceDTO |
| Preconditions | Projectedbrokerresults notactualfills; actualpromotefollowslater |
| Guards | mode/injection/market/cost/farprojection;geometry;compression;basket;runtime risk;moneyincrease/margin/grossexposure/netBig-vs-priorBig/loss cap |
| Callers | HSBI_SolveFutureSmall @ Include/Planning/HSBI_FutureSmallSolver.mqh:130 |
| Dependencies | HSBI_IsStaticCalculationAllowed @ Include/Planning/HSBI_FutureSmallSolver.mqh:61; HSBI_IsInjectedProofAllowed @ Include/Planning/HSBI_FutureSmallSolver.mqh:61; HSBI_ValidateLevelMarket @ Include/Planning/HSBI_FutureSmallSolver.mqh:61; HSBI_ValidateLevelCosts @ Include/Planning/HSBI_FutureSmallSolver.mqh:62; HSBI_ValidateFarProjection @ Include/Planning/HSBI_FutureSmallSolver.mqh:62; HSBI_SolveBigGeometry @ Include/Planning/HSBI_FutureSmallSolver.mqh:63; HSBI_GridTolerance @ Include/Planning/HSBI_FutureSmallSolver.mqh:68; HSBI_GridTolerance @ Include/Planning/HSBI_FutureSmallSolver.mqh:69; HSBI_LevelControlPrice @ Include/Planning/HSBI_FutureSmallSolver.mqh:77; HSBI_EvaluateBasketMoney @ Include/Planning/HSBI_FutureSmallSolver.mqh:80; HSBI_EvaluateFutureSmallRisk @ Include/Planning/HSBI_FutureSmallSolver.mqh:86 |
| Normative contract | Docs/27_FUTURE_SMALL_SOLVER_RU.md; Docs/04:21; Docs/15_RISK_AND_MARGIN_CONTRACT_RU.md |
| Formula IDs | F005/F027/F028/F029/F030/F031/F037 |
| Error IDs | ERR013/020/021/031/041 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | Conditional delegated projected OrderCalcProfit/OrderCalcMargin; risk/ownership/EA-origin data остаются supplied DTO. Нет actual deals/history provider; native NOT_RUN. |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | LOCAL_FORECAST_LEVEL_SOURCE_MISMATCH |
| Limitations / side effects | ERR020 compareNet vspriorBigGross; prefixlossbasis notactualbatch; exactlevel notuniversal/finalclose |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{
   HSBI_FutureSmallLevelResult r; ZeroMemory(r);r.levelIndex=x.levelIndex;r.farBefore=x.farBefore;
   r.status=HSBI_FS_UNPROVEN;r.reason=HSBI_REASON_INTERNAL_INVARIANT_FAILED;r.details="LEVEL_UNPROVEN";
   if(!HSBI_IsStaticCalculationAllowed(x.runtimeMode)||x.testOnlyApproximation||(x.useInjectedBrokerProof&&!HSBI_IsInjectedProofAllowed(x.runtimeMode))||!HSBI_ValidateLevelMarket(x.market,x.levelIndex,x.broker,x.farDirection)||
      !HSBI_ValidateLevelCosts(x.costs,x.levelIndex)||!HSBI_ValidateFarProjection(x.farProjection,x.broker,x.farBefore)) return r;
   HSBI_GeometryResult g=HSBI_SolveBigGeometry(x.farBefore,x.coreRatio,x.trendRatio,x.smallRatio,x.broker,true,true);
   if(!g.valid){r.details="GEOMETRY_FAILED";return r;}
   r.coreVolume=g.coreVolume;r.trendVolume=g.trendVolume;r.smallVolume=g.smallVolume;r.netBigVolume=g.netBigVolume;
   r.recoverySlopeLots=g.recoverySlopeLots;r.farAfter=x.farProjection.projectedFar;
   r.compressionLots=x.farBefore-r.farAfter;r.compressionRatio=r.compressionLots/x.farBefore;
   if(r.farAfter>x.maxNewFarRatio*x.farBefore+HSBI_GridTolerance(x.broker.volumeStep)||
      r.compressionLots<x.minimumCompressionLots-HSBI_GridTolerance(x.broker.volumeStep)||r.compressionRatio<x.minimumCompressionRatio-1e-10) {
      r.details="COMPRESSION_FAILED";return r;
   }
   HSBI_BasketMoneyResult basket;
   if(x.useInjectedBrokerProof){basket=x.injectedBrokerProof;if(!basket.valid||!basket.brokerRuntimeConfirmed){r.details="INJECTED_PROOF_UNCONFIRMED";return r;}}
   else {
      HSBI_BasketMoneyInput bi;ZeroMemory(bi);bi.farVolume=x.farBefore;bi.coreVolume=g.coreVolume;bi.trendVolume=g.trendVolume;bi.smallVolume=g.smallVolume;
      bi.farDirection=x.farDirection;bi.symbol=x.broker.symbol;bi.broker=x.broker;
      bi.controlPrice=HSBI_LevelControlPrice(x.market,x.broker,bi.farDirection);bi.farOpenPrice=x.farOpenPrice;bi.coreOpenPrice=x.coreOpenPrice;
      bi.trendOpenPrice=x.trendOpenPrice;bi.smallOpenPrice=x.smallOpenPrice;bi.farCosts=x.costs.farCosts;bi.coreCosts=x.costs.coreCosts;
      bi.trendCosts=x.costs.trendCosts;bi.smallCosts=x.costs.smallCosts;bi.executionSafetyBuffer=x.executionSafetyBuffer;bi.snapshotId=x.market.snapshotId;
      basket=HSBI_EvaluateBasketMoney(bi);
   }
   r.basketProof=basket;if(!basket.valid){r.details="BROKER_MONEY_OR_MARGIN_UNAVAILABLE";return r;}
   HSBI_FutureSmallRiskInput ri;ZeroMemory(ri);ri.basket=basket;ri.priorRisk=x.riskState.currentRisk;ri.tolerance=x.riskState.riskTolerance;
   ri.evaluatedRisk=x.evaluatedRisk;ri.source=x.riskProofSource;ri.runtimeConfirmed=x.riskRuntimeConfirmed;ri.testOnly=x.riskTestOnly;
   ri.fresh=x.riskState.fresh;ri.snapshotId=x.riskProofSnapshotId;
   HSBI_FutureSmallRiskResult risk=HSBI_EvaluateFutureSmallRisk(ri);if(!risk.valid){r.details="RISK_RUNTIME_PROOF_UNAVAILABLE_OR_FAILED";return r;}
   r.recoveryMoney=basket.recoveryMoney;r.totalMargin=basket.totalMargin;r.grossExposure=basket.grossExposure;r.transitionLoss=basket.transitionLoss;
   r.riskValue=risk.riskValue;r.moneyIncluded=true;r.marginIncluded=true;r.riskIncluded=true;r.transitionLossIncluded=true;r.controlSnapshotValid=true;r.costSnapshotValid=true;r.farProjectionValid=true;r.runtimeConfirmed=basket.brokerRuntimeConfirmed&&risk.runtimeConfirmed;
   if(r.recoveryMoney<=x.moneyState.recoveryMoney||r.totalMargin>x.marginState.allowedMargin||r.grossExposure>=x.priorGrossExposure||
      r.netBigVolume>=x.priorBigGross||r.transitionLoss>x.transitionLossCap){r.details="LEVEL_GATES_FAILED";return r;}
   r.valid=true;r.status=HSBI_FS_EXACT_PROOF;r.reason=HSBI_REASON_OK;r.details="EXACT_LEVEL";return r;
}
~~~

### FUNCTION HSBI_FutureSmallLevelDigest

| Field | Individual analysis |
|---|---|
| Function ID | Include/Planning/HSBI_FutureSmallSolver.mqh:93:HSBI_FutureSmallLevelDigest |
| Source | Include/Planning/HSBI_FutureSmallSolver.mqh:93–105 |
| Signature | string HSBI_FutureSmallLevelDigest(const HSBI_FutureSmallLevelProof &p) |
| Inputs | const HSBI_FutureSmallLevelProof &p |
| Outputs / Postconditions | Fixedfieldstring |
| Domain | 30selectedIDs/status/lots/money8dec/ratio12dec |
| Preconditions | Fullimmutableproofindependentoriginseparate |
| Guards | No guards |
| Callers | HSBI_AggregateFutureSmallProof @ Include/Planning/HSBI_FutureSmallProofAggregator.mqh:47; HSBI_FutureSmallProofDigest @ Include/Planning/HSBI_FutureSmallSolver.mqh:109; HSBI_SolveFutureSmall @ Include/Planning/HSBI_FutureSmallSolver.mqh:140 |
| Dependencies | HSBI_UlongToString @ Include/Planning/HSBI_FutureSmallSolver.mqh:101; HSBI_UlongToString @ Include/Planning/HSBI_FutureSmallSolver.mqh:101; HSBI_UlongToString @ Include/Planning/HSBI_FutureSmallSolver.mqh:101; HSBI_UlongToString @ Include/Planning/HSBI_FutureSmallSolver.mqh:102; HSBI_UlongToString @ Include/Planning/HSBI_FutureSmallSolver.mqh:102 |
| Normative contract | Docs/16:8; Docs/27_FUTURE_SMALL_SOLVER_RU.md |
| Formula IDs | F042/F057/F060 |
| Error IDs | ERR003/013/026/040 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | LEVEL_FINGERPRINT_ONLY |
| Limitations / side effects | Flags/sourceprooffullbodynotincluded; roundinghashnotexactcodec |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{
   return IntegerToString(p.levelIndex)+"|"+DoubleToString(p.farBefore,8)+"|"+DoubleToString(p.farAfter,8)+"|"+
      DoubleToString(p.coreVolume,8)+"|"+DoubleToString(p.trendVolume,8)+"|"+DoubleToString(p.smallVolume,8)+"|"+
      DoubleToString(p.netBigVolume,8)+"|"+DoubleToString(p.recoverySlopeLots,8)+"|"+DoubleToString(p.projectedRecoveryMoney,8)+"|"+
      DoubleToString(p.projectedMargin,8)+"|"+DoubleToString(p.grossExposure,8)+"|"+DoubleToString(p.projectedRisk,8)+"|"+
      DoubleToString(p.transitionLoss,8)+"|"+DoubleToString(p.compressionLots,8)+"|"+DoubleToString(p.compressionRatio,12)+"|"+
      DoubleToString(p.controlPrice,8)+"|"+DoubleToString(p.bid,8)+"|"+DoubleToString(p.ask,8)+"|"+DoubleToString(p.tickSize,8)+"|"+
      HSBI_UlongToString(p.controlSnapshotId)+"|"+HSBI_UlongToString(p.farCostSnapshotId)+"|"+HSBI_UlongToString(p.coreCostSnapshotId)+"|"+
      HSBI_UlongToString(p.trendCostSnapshotId)+"|"+HSBI_UlongToString(p.smallCostSnapshotId)+"|"+IntegerToString((int)p.moneyProofStatus)+"|"+
      IntegerToString((int)p.marginProofStatus)+"|"+IntegerToString((int)p.riskProofStatus)+"|"+IntegerToString((int)p.transitionLossProofStatus)+"|"+
      IntegerToString((int)p.proofStatus)+"|"+IntegerToString((int)p.reason);
}
~~~

### FUNCTION HSBI_FutureSmallProofDigest

| Field | Individual analysis |
|---|---|
| Function ID | Include/Planning/HSBI_FutureSmallSolver.mqh:106:HSBI_FutureSmallProofDigest |
| Source | Include/Planning/HSBI_FutureSmallSolver.mqh:106–112 |
| Signature | string HSBI_FutureSmallProofDigest(const HSBI_FutureSmallResult &r) |
| Inputs | const HSBI_FutureSmallResult &r |
| Outputs / Postconditions | FS OR plan/rev+eachlevel+endstatus/depth/terminalflags |
| Domain | deptharrayindex,IDs,levelstrings,terminalfields |
| Preconditions | provenDepth<=128 andcompletearraycaller |
| Guards | fori<provenDepth nointernalbounds |
| Callers | HSBI_EvaluateCandidateMoney @ Include/Money/HSBI_CandidateMoneyEvaluator.mqh:17; HSBI_SolveFutureSmall @ Include/Planning/HSBI_FutureSmallSolver.mqh:130; HSBI_SolveFutureSmall @ Include/Planning/HSBI_FutureSmallSolver.mqh:149 |
| Dependencies | HSBI_UlongToString @ Include/Planning/HSBI_FutureSmallSolver.mqh:108; HSBI_UlongToString @ Include/Planning/HSBI_FutureSmallSolver.mqh:108; HSBI_FutureSmallLevelDigest @ Include/Planning/HSBI_FutureSmallSolver.mqh:109 |
| Normative contract | Docs/16:8; Docs/27_FUTURE_SMALL_SOLVER_RU.md |
| Formula IDs | F042/F057/F060 |
| Error IDs | ERR013/026 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | CHAIN_FINGERPRINT_ONLY |
| Limitations / side effects | Publichelper trustsdepth; nonemptyfingerprintnotproof; noindependentauthority |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{
   string d="FS|"+HSBI_UlongToString(r.planId)+"|"+HSBI_UlongToString(r.stateRevision);
   for(int i=0;i<r.provenDepth;i++) d+="|L|"+HSBI_FutureSmallLevelDigest(r.levels[i]);
   return d+"|END|"+IntegerToString((int)r.status)+"|"+IntegerToString(r.provenDepth)+"|"+
      DoubleToString(r.terminalFar,8)+"|"+IntegerToString((int)r.finiteSequence)+"|"+IntegerToString((int)r.plateauDetected);
}
~~~

### FUNCTION HSBI_SolveFutureSmall

| Field | Individual analysis |
|---|---|
| Function ID | Include/Planning/HSBI_FutureSmallSolver.mqh:113:HSBI_SolveFutureSmall |
| Source | Include/Planning/HSBI_FutureSmallSolver.mqh:113–150 |
| Signature | HSBI_FutureSmallResult HSBI_SolveFutureSmall(const HSBI_FutureSmallInput &x) |
| Inputs | const HSBI_FutureSmallInput &x |
| Outputs / Postconditions | Rejectbadinput/depth/failedlevel; exactifterminalorconservativebound+depth>=2 |
| Domain | maximumDepth2..128;projectedlots/money/risk arrays |
| Preconditions | Validatedproviders/terminalroute/approvednumericaldomain independentlyrequired |
| Guards | Inputvalidator;depthcalc;boundedloop;eachlevel;observedQbound;terminalFar<=Vmin+tolerance;finaldepth/status |
| Callers | HSBI_EvaluateCandidateMoney @ Include/Money/HSBI_CandidateMoneyEvaluator.mqh:15 |
| Dependencies | HSBI_ValidateFutureSmallInput @ Include/Planning/HSBI_FutureSmallSolver.mqh:116; HSBI_CalculateFutureSmallDepth @ Include/Planning/HSBI_FutureSmallSolver.mqh:117; HSBI_EvaluateFutureSmallLevel @ Include/Planning/HSBI_FutureSmallSolver.mqh:130; HSBI_FutureSmallProofDigest @ Include/Planning/HSBI_FutureSmallSolver.mqh:130; HSBI_FutureSmallLevelDigest @ Include/Planning/HSBI_FutureSmallSolver.mqh:140; HSBI_GridTolerance @ Include/Planning/HSBI_FutureSmallSolver.mqh:142; HSBI_GridTolerance @ Include/Planning/HSBI_FutureSmallSolver.mqh:144; HSBI_ValidateConservativeBound @ Include/Planning/HSBI_FutureSmallSolver.mqh:146; HSBI_FutureSmallProofDigest @ Include/Planning/HSBI_FutureSmallSolver.mqh:149 |
| Normative contract | Docs/27_FUTURE_SMALL_SOLVER_RU.md; Docs/04:21,33–36 |
| Formula IDs | F029/F037/F038/F058 |
| Error IDs | ERR020/021/031/032/041 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | Conditional delegated projected OrderCalcProfit/OrderCalcMargin; risk/ownership/EA-origin data остаются supplied DTO. Нет actual deals/history provider; native NOT_RUN. |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | BOUNDED_PLANNER_NOT_CYCLE_TERMINATION |
| Limitations / side effects | priorBig overwrittennet ERR020; prefixnotuniversaltail ERR021;terminalRouteAllowedunused ERR031; no financialexecution |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{
   HSBI_FutureSmallResult r;ZeroMemory(r);r.status=HSBI_FS_REJECTED;r.reason=HSBI_REASON_INTERNAL_INVARIANT_FAILED;
   r.planId=x.planId;r.stateRevision=x.stateRevision;r.details="INVALID_INPUT";if(!HSBI_ValidateFutureSmallInput(x))return r;
   if(!HSBI_CalculateFutureSmallDepth(x.currentFar,x.volumeMin,x.conservativeQ,x.volumeStep,r.theoreticalDepth)){r.details="NONFINITE_DEPTH";return r;}
   double far=x.currentFar,priorBig=x.currentBigGross,priorExposure=x.currentGrossExposure;HSBI_MoneyStateSnapshot money=x.moneyState;
   HSBI_RiskSnapshot risk=x.riskState;HSBI_MarginSnapshot margin=x.marginState;bool terminal=false,boundConditions=true;
   for(int k=0;k<x.maximumDepth;k++) {
      HSBI_FutureSmallLevelInput li;ZeroMemory(li);li.runtimeMode=x.runtimeMode;li.levelIndex=k+1;li.farBefore=far;li.coreRatio=x.coreRatio;li.trendRatio=x.trendRatio;
      li.smallRatio=x.smallRatio;li.farDirection=x.farDirection;li.broker=x.broker;li.market=x.levelMarketSnapshots[k];li.costs=x.levelCostSnapshots[k];li.farProjection=x.farProjections[k];
      li.farOpenPrice=x.farOpenPrice;li.coreOpenPrice=x.coreOpenPrice;li.trendOpenPrice=x.trendOpenPrice;li.smallOpenPrice=x.smallOpenPrice;
      li.moneyState=money;li.riskState=risk;li.marginState=margin;li.minimumCompressionLots=x.minimumCompressionLots;
      li.minimumCompressionRatio=x.minimumCompressionRatio;li.maxNewFarRatio=x.maxNewFarRatio;li.transitionLossCap=x.transitionLossCap;
      li.executionSafetyBuffer=x.executionSafetyBuffer;li.priorBigGross=priorBig;li.priorGrossExposure=priorExposure;li.planId=x.planId;li.stateRevision=x.stateRevision;
      li.evaluatedRisk=x.evaluatedRisks[k];li.riskProofSource=x.riskProofSources[k];li.riskRuntimeConfirmed=x.riskRuntimeConfirmed[k];
      li.riskTestOnly=x.riskTestOnly[k];li.riskProofSnapshotId=x.riskProofSnapshotIds[k];li.useInjectedBrokerProof=x.useInjectedBrokerProofs;
      li.testOnlyApproximation=x.testOnlyApproximation;if(x.useInjectedBrokerProofs)li.injectedBrokerProof=x.injectedBrokerProofs[k];
      HSBI_FutureSmallLevelResult level=HSBI_EvaluateFutureSmallLevel(li);if(!level.valid){r.details=level.details;r.proofDigest=HSBI_FutureSmallProofDigest(r);return r;}
      HSBI_FutureSmallLevelProof p;ZeroMemory(p);p.levelIndex=level.levelIndex;p.farBefore=level.farBefore;p.farAfter=level.farAfter;
      p.coreVolume=level.coreVolume;p.trendVolume=level.trendVolume;p.smallVolume=level.smallVolume;p.netBigVolume=level.netBigVolume;
      p.compressionLots=level.compressionLots;p.compressionRatio=level.compressionRatio;p.recoverySlopeLots=level.recoverySlopeLots;
      p.projectedRecoveryMoney=level.recoveryMoney;p.projectedReserve=x.expectedReserve;p.projectedMargin=level.totalMargin;p.projectedRisk=level.riskValue;
      p.transitionLoss=level.transitionLoss;p.grossExposure=level.grossExposure;p.controlPrice=li.market.selectedPrice;p.bid=li.market.bid;p.ask=li.market.ask;
      p.tickSize=li.market.tickSize;p.controlSnapshotId=li.market.snapshotId;p.farCostSnapshotId=li.costs.farCosts.snapshotId;
      p.coreCostSnapshotId=li.costs.coreCosts.snapshotId;p.trendCostSnapshotId=li.costs.trendCosts.snapshotId;p.smallCostSnapshotId=li.costs.smallCosts.snapshotId;
      p.valid=level.valid;p.moneyIncluded=level.moneyIncluded;p.marginIncluded=level.marginIncluded;p.riskIncluded=level.riskIncluded;p.transitionLossIncluded=level.transitionLossIncluded;p.controlSnapshotValid=level.controlSnapshotValid;p.costSnapshotValid=level.costSnapshotValid;p.farProjectionValid=level.farProjectionValid;p.runtimeConfirmed=level.runtimeConfirmed;
      p.moneyProofStatus=level.basketProof.status;p.marginProofStatus=level.basketProof.status;p.riskProofStatus=HSBI_CALC_PASS;
      p.transitionLossProofStatus=level.basketProof.status;p.reserveSourceProof=level.basketProof.core;p.farLossProof=level.basketProof.far;p.proofStatus=HSBI_FS_EXACT_PROOF;p.reason=HSBI_REASON_OK;p.levelDigest=HSBI_FutureSmallLevelDigest(p);
      r.levels[k]=p;r.provenDepth=k+1;
      if(level.farAfter>x.conservativeQ*level.farBefore+HSBI_GridTolerance(x.volumeStep))boundConditions=false;
      far=level.farAfter;priorBig=level.netBigVolume;priorExposure=level.grossExposure;money.recoveryMoney=level.recoveryMoney;
      risk.currentRisk=level.riskValue;margin.currentMargin=level.totalMargin;if(far<=x.volumeMin+HSBI_GridTolerance(x.volumeStep)){terminal=true;break;}
   }
   r.terminalFar=far;r.finiteSequence=terminal;bool bound=boundConditions&&HSBI_ValidateConservativeBound(x.currentFar,far,x.conservativeQ,r.provenDepth,x.roundingIncluded,x.costsIncluded,true,true,true);
   r.valid=r.provenDepth>=2&&(terminal||bound);r.status=terminal&&r.provenDepth>=2?HSBI_FS_EXACT_PROOF:(bound?HSBI_FS_CONSERVATIVE_BOUND:HSBI_FS_UNPROVEN);
   r.reason=r.valid?HSBI_REASON_OK:HSBI_REASON_INTERNAL_INVARIANT_FAILED;r.details=r.valid?(r.status==HSBI_FS_EXACT_PROOF?"EXACT_PROOF":"CONSERVATIVE_BOUND"):"UNPROVEN";
   r.proofDigest=HSBI_FutureSmallProofDigest(r);return r;
}
~~~

### FUNCTION HSBI_AggregateDigest

| Field | Individual analysis |
|---|---|
| Function ID | Include/Planning/HSBI_FutureSmallProofAggregator.mqh:16:HSBI_AggregateDigest |
| Source | Include/Planning/HSBI_FutureSmallProofAggregator.mqh:16–22 |
| Signature | string HSBI_AggregateDigest(const HSBI_FutureSmallAggregateProof &a,const string levelsDigest) |
| Inputs | const HSBI_FutureSmallAggregateProof &a,const string levelsDigest |
| Outputs / Postconditions | TextAGG fields+levelsDigest |
| Domain | money/margin/risk/lots/indices+levelsDigest |
| Preconditions | Validatedlevelchainseparately |
| Guards | No guards |
| Callers | HSBI_AggregateFutureSmallProof @ Include/Planning/HSBI_FutureSmallProofAggregator.mqh:58 |
| Dependencies | NONE project functions |
| Normative contract | Docs/30_FUTURE_SMALL_AGGREGATE_PROOF_RU.md |
| Formula IDs | F023/F042/F057/F060 |
| Error IDs | ERR018/026 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | AGGREGATE_FINGERPRINT |
| Limitations / side effects | Notindependentfullproof/fullrawcodec; extrema don'treplacealllevelCatchUp |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{return "AGG|"+IntegerToString((int)a.selectionPolicy)+"|"+IntegerToString(a.levelCount)+"|"+DoubleToString(a.minimumRecoveryMoney,8)+"|"+
   DoubleToString(a.maximumMargin,8)+"|"+DoubleToString(a.maximumRisk,8)+"|"+DoubleToString(a.maximumGrossExposure,8)+"|"+
   DoubleToString(a.maximumTransitionLoss,8)+"|"+DoubleToString(a.minimumCompressionLots,8)+"|"+DoubleToString(a.minimumCompressionRatio,12)+"|"+
   DoubleToString(a.finalFar,8)+"|"+IntegerToString(a.worstRecoveryLevel)+"|"+IntegerToString(a.worstMarginLevel)+"|"+
   IntegerToString(a.worstRiskLevel)+"|"+IntegerToString(a.worstExposureLevel)+"|"+IntegerToString(a.worstTransitionLossLevel)+"|"+
   IntegerToString(a.catchUpControlLevel)+"|"+levelsDigest;}
~~~

### FUNCTION HSBI_AggregateFutureSmallProof

| Field | Individual analysis |
|---|---|
| Function ID | Include/Planning/HSBI_FutureSmallProofAggregator.mqh:23:HSBI_AggregateFutureSmallProof |
| Source | Include/Planning/HSBI_FutureSmallProofAggregator.mqh:23–59 |
| Signature | HSBI_FutureSmallAggregateProof HSBI_AggregateFutureSmallProof(const HSBI_FutureSmallResult &p,const HSBI_ProofSelectionPolicy policy,const int explicitControlLevel) |
| Inputs | const HSBI_FutureSmallResult &p,const HSBI_ProofSelectionPolicy policy,const int explicitControlLevel |
| Outputs / Postconditions | validifalllevelcompleteness/status/coverage flags andcontrolinrange |
| Domain | depth2..128;enumselectionpolicy,1-basedcontrolindex |
| Preconditions | Alllevelsproducerproof+finitefields independent; no hiddenbridgefromflags |
| Guards | p.valid/depth;perlevel11completeclauses;4statuscoveragegroups;3snapshot/projectionflags;runtime;5extrema;compressionmin;controlindexrange |
| Callers | HSBI_SolveNewFar @ Include/Planning/HSBI_NewFarSolver.mqh:116 |
| Dependencies | HSBI_FutureSmallLevelDigest @ Include/Planning/HSBI_FutureSmallProofAggregator.mqh:47; HSBI_AggregateDigest @ Include/Planning/HSBI_FutureSmallProofAggregator.mqh:58 |
| Normative contract | Docs/30_FUTURE_SMALL_AGGREGATE_PROOF_RU.md; CR09 proposed |
| Formula IDs | F023/F036/F057/F062 |
| Error IDs | ERR013/018/049 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | AGGREGATE_SCOPE_SINGLE_CONTROL |
| Limitations / side effects | No separatefinitechecks publicentry; unknownpolicy falls explicit branch; WORST selectsmaxTransition notminCatchupMargin; producer≠arbitraryDTOcaller |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{
   HSBI_FutureSmallAggregateProof a;ZeroMemory(a);a.levelCount=p.provenDepth;a.selectionPolicy=policy;a.reason=HSBI_REASON_INTERNAL_INVARIANT_FAILED;
   a.details="PROOF_INCOMPLETE";a.allMoneyProofsValid=true;a.allMarginProofsValid=true;a.allRiskProofsValid=true;
   a.allTransitionLossProofsValid=true;a.allControlSnapshotsValid=true;a.allCostSnapshotsValid=true;a.allFarProjectionsValid=true;a.runtimeConfirmed=true;
   if(!p.valid||p.provenDepth<2||p.provenDepth>128)return a;string chain="";
   for(int i=0;i<p.provenDepth;i++){
      HSBI_FutureSmallLevelProof l=p.levels[i];a.evaluatedLevelCount++;
      bool complete=l.valid&&l.levelIndex==i+1&&l.moneyIncluded&&l.marginIncluded&&l.riskIncluded&&l.transitionLossIncluded&&
         l.controlSnapshotValid&&l.costSnapshotValid&&l.farProjectionValid&&l.proofStatus==HSBI_FS_EXACT_PROOF&&l.runtimeConfirmed;
      if(!complete)a.rejectedLevelCount++;
      a.allMoneyProofsValid&=l.valid&&l.moneyIncluded&&l.moneyProofStatus==HSBI_CALC_PASS;
      a.allMarginProofsValid&=l.valid&&l.marginIncluded&&l.marginProofStatus==HSBI_CALC_PASS;
      a.allRiskProofsValid&=l.valid&&l.riskIncluded&&l.riskProofStatus==HSBI_CALC_PASS;
      a.allTransitionLossProofsValid&=l.valid&&l.transitionLossIncluded&&l.transitionLossProofStatus==HSBI_CALC_PASS;
      a.allControlSnapshotsValid&=l.controlSnapshotValid;a.allCostSnapshotsValid&=l.costSnapshotValid;
      a.allFarProjectionsValid&=l.farProjectionValid;a.runtimeConfirmed&=l.runtimeConfirmed;
      if(i==0||l.projectedRecoveryMoney<a.minimumRecoveryMoney){a.minimumRecoveryMoney=l.projectedRecoveryMoney;a.worstRecoveryMoney=l.projectedRecoveryMoney;a.worstRecoveryLevel=l.levelIndex;}
      if(i==0||l.projectedMargin>a.maximumMargin){a.maximumMargin=l.projectedMargin;a.worstMargin=l.projectedMargin;a.worstMarginLevel=l.levelIndex;}
      if(i==0||l.projectedRisk>a.maximumRisk){a.maximumRisk=l.projectedRisk;a.worstRisk=l.projectedRisk;a.worstRiskLevel=l.levelIndex;}
      if(i==0||l.grossExposure>a.maximumGrossExposure){a.maximumGrossExposure=l.grossExposure;a.worstGrossExposure=l.grossExposure;a.worstExposureLevel=l.levelIndex;}
      if(i==0||l.transitionLoss>a.maximumTransitionLoss){a.maximumTransitionLoss=l.transitionLoss;a.worstTransitionLoss=l.transitionLoss;a.worstTransitionLossLevel=l.levelIndex;}
      if(i==0||l.compressionLots<a.minimumCompressionLots)a.minimumCompressionLots=l.compressionLots;
      if(i==0||l.compressionRatio<a.minimumCompressionRatio)a.minimumCompressionRatio=l.compressionRatio;
      chain+="|"+HSBI_FutureSmallLevelDigest(l);
   }
   a.finalFar=p.levels[p.provenDepth-1].farAfter;a.maximumFutureTransitions=p.theoreticalDepth;
   if(policy==HSBI_PROOF_POLICY_WORST_CASE)a.catchUpControlLevel=a.worstTransitionLossLevel;
   else if(policy==HSBI_PROOF_POLICY_FINAL_LEVEL)a.catchUpControlLevel=p.provenDepth;
   else a.catchUpControlLevel=explicitControlLevel;
   if(a.catchUpControlLevel<1||a.catchUpControlLevel>p.provenDepth)a.rejectedLevelCount++;
   a.exactProof=p.status==HSBI_FS_EXACT_PROOF;a.conservativeBound=p.status==HSBI_FS_CONSERVATIVE_BOUND;
   a.valid=a.rejectedLevelCount==0&&a.allMoneyProofsValid&&a.allMarginProofsValid&&a.allRiskProofsValid&&
      a.allTransitionLossProofsValid&&a.allControlSnapshotsValid&&a.allCostSnapshotsValid&&a.allFarProjectionsValid&&a.runtimeConfirmed;
   a.reason=a.valid?HSBI_REASON_OK:HSBI_REASON_INTERNAL_INVARIANT_FAILED;a.details=a.valid?"AGGREGATE_VALID":"PROOF_INCOMPLETE";
   a.aggregateDigest=HSBI_AggregateDigest(a,chain);return a;
}
~~~

### FUNCTION HSBI_FutureSmallTemplateDigest

| Field | Individual analysis |
|---|---|
| Function ID | Include/Planning/HSBI_NewFarSolver.mqh:35:HSBI_FutureSmallTemplateDigest |
| Source | Include/Planning/HSBI_NewFarSolver.mqh:35–46 |
| Signature | string HSBI_FutureSmallTemplateDigest(const HSBI_FutureSmallInput &f) |
| Inputs | const HSBI_FutureSmallInput &f |
| Outputs / Postconditions | Concatsselectedscalar/perlevelsnapshot/price/projection/riskIDs |
| Domain | maxDepthbounded0..128;IDs/quotes/ratios |
| Preconditions | Caller mustvalidateboundsbeforepublichelper |
| Guards | fori<maximumDepth;nointernalshapeguard |
| Callers | HSBI_NewFarInputDigest @ Include/Planning/HSBI_NewFarSolver.mqh:56; HSBI_SolveNewFar @ Include/Planning/HSBI_NewFarSolver.mqh:145 |
| Dependencies | HSBI_AllocationPolicyDigest @ Include/Planning/HSBI_NewFarSolver.mqh:37; HSBI_UlongToString @ Include/Planning/HSBI_NewFarSolver.mqh:39; HSBI_UlongToString @ Include/Planning/HSBI_NewFarSolver.mqh:41; HSBI_UlongToString @ Include/Planning/HSBI_NewFarSolver.mqh:41; HSBI_UlongToString @ Include/Planning/HSBI_NewFarSolver.mqh:42; HSBI_UlongToString @ Include/Planning/HSBI_NewFarSolver.mqh:42; HSBI_UlongToString @ Include/Planning/HSBI_NewFarSolver.mqh:43; HSBI_UlongToString @ Include/Planning/HSBI_NewFarSolver.mqh:44 |
| Normative contract | Docs/16:8; Docs/27_FUTURE_SMALL_SOLVER_RU.md |
| Formula IDs | F042/F057/F060 |
| Error IDs | ERR024/026 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | INCOMPLETE_TEMPLATE_BINDING |
| Limitations / side effects | Notalltemplatefieldsincluded; actualvaluesofcosts/risks maychangeundersameIDs; NewFarInputDigestcallsbeforefulltemplatevalidation |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{
   string d=HSBI_AllocationPolicyDigest(f.allocationPolicy)+"|"+DoubleToString(f.currentFar,8)+"|"+DoubleToString(f.coreRatio,12)+"|"+
      DoubleToString(f.trendRatio,12)+"|"+DoubleToString(f.smallRatio,12)+"|"+IntegerToString(f.maximumDepth);
   for(int i=0;i<f.maximumDepth;i++) d+="|M"+IntegerToString(i)+"|"+HSBI_UlongToString(f.levelMarketSnapshots[i].snapshotId)+"|"+
      DoubleToString(f.levelMarketSnapshots[i].bid,8)+"|"+DoubleToString(f.levelMarketSnapshots[i].ask,8)+"|"+
      HSBI_UlongToString(f.levelCostSnapshots[i].snapshotId)+"|"+HSBI_UlongToString(f.levelCostSnapshots[i].farCosts.snapshotId)+"|"+
      HSBI_UlongToString(f.levelCostSnapshots[i].coreCosts.snapshotId)+"|"+HSBI_UlongToString(f.levelCostSnapshots[i].trendCosts.snapshotId)+"|"+
      HSBI_UlongToString(f.levelCostSnapshots[i].smallCosts.snapshotId)+"|"+DoubleToString(f.farProjections[i].projectedFar,8)+"|"+
      HSBI_UlongToString(f.riskProofSnapshotIds[i]);
   return d;
}
~~~

### FUNCTION HSBI_NewFarInputDigest

| Field | Individual analysis |
|---|---|
| Function ID | Include/Planning/HSBI_NewFarSolver.mqh:47:HSBI_NewFarInputDigest |
| Source | Include/Planning/HSBI_NewFarSolver.mqh:47–58 |
| Signature | string HSBI_NewFarInputDigest(const HSBI_NewFarSolverInput &x) |
| Inputs | const HSBI_NewFarSolverInput &x |
| Outputs / Postconditions | Concatsnamedsubset+TemplateDigest |
| Domain | namespace/IDs/lots/grid/control/template/policy,digests |
| Preconditions | Fullshape/bounds beforedigest requiredcaller |
| Guards | No localguards |
| Callers | HSBI_FinalizeNewFarPlanDigest @ Include/Planning/HSBI_NewFarSolver.mqh:59; HSBI_SolveNewFar @ Include/Planning/HSBI_NewFarSolver.mqh:106 |
| Dependencies | HSBI_UlongToString @ Include/Planning/HSBI_NewFarSolver.mqh:50; HSBI_UlongToString @ Include/Planning/HSBI_NewFarSolver.mqh:50; HSBI_UlongToString @ Include/Planning/HSBI_NewFarSolver.mqh:50; HSBI_UlongToString @ Include/Planning/HSBI_NewFarSolver.mqh:51; HSBI_UlongToString @ Include/Planning/HSBI_NewFarSolver.mqh:52; HSBI_UlongToString @ Include/Planning/HSBI_NewFarSolver.mqh:55; HSBI_AllocationPolicyDigest @ Include/Planning/HSBI_NewFarSolver.mqh:56; HSBI_FutureSmallTemplateDigest @ Include/Planning/HSBI_NewFarSolver.mqh:56; HSBI_ReserveAllocationSourceDigest @ Include/Planning/HSBI_NewFarSolver.mqh:57; HSBI_ReserveConsumptionKeyDigest @ Include/Planning/HSBI_NewFarSolver.mqh:57; HSBI_UlongToString @ Include/Planning/HSBI_NewFarSolver.mqh:57; HSBI_UlongToString @ Include/Planning/HSBI_NewFarSolver.mqh:57 |
| Normative contract | Docs/14:6–26; Docs/16:8 |
| Formula IDs | F042/F053/F057/F060 |
| Error IDs | ERR013/026/040 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | PARTIAL_INPUT_FINGERPRINT |
| Limitations / side effects | maximumDepthusedbeforededicatedinputvalidation; caps/confignotallbound; expectedPlanDigest mayempty |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{
   return LongToString(x.oldFarDescriptor.identity.accountLogin)+"|"+x.oldFarDescriptor.identity.symbol+"|"+LongToString(x.oldFarDescriptor.identity.magic)+"|"+
      HSBI_UlongToString(x.cycleId)+"|"+HSBI_UlongToString(x.planId)+"|"+HSBI_UlongToString(x.stateRevision)+"|"+
      DoubleToString(x.oldFarDescriptor.actualVolume,8)+"|"+HSBI_UlongToString(x.originalBigCoreDescriptor.identifier)+"|"+
      HSBI_UlongToString(x.originalBigCoreDescriptor.ticket)+"|"+DoubleToString(x.actualBigCoreResidual.actualVolume,8)+"|"+
      DoubleToString(x.projectedVolume,8)+"|"+DoubleToString(x.brokerProperties.volumeMin,8)+"|"+DoubleToString(x.brokerProperties.volumeMax,8)+"|"+
      DoubleToString(x.brokerProperties.volumeStep,8)+"|"+DoubleToString(x.brokerProperties.tickSize,8)+"|"+
      DoubleToString(x.controlPrice.selectedPrice,8)+"|"+HSBI_UlongToString(x.controlPrice.snapshotId)+"|"+
      HSBI_AllocationPolicyDigest(x.allocationPolicy)+"|"+HSBI_FutureSmallTemplateDigest(x.futureSmallTemplate)+"|"+
      IntegerToString((int)x.proofSelectionPolicy)+"|"+IntegerToString(x.explicitCatchUpControlLevel)+"|"+HSBI_ReserveAllocationSourceDigest(x.reserveAllocationSource)+"|"+HSBI_ReserveConsumptionKeyDigest(x.consumptionKey)+"|"+x.moneyProofDigest+"|"+x.marginProofDigest+"|"+x.riskProofDigest+"|"+HSBI_UlongToString(x.riskState.snapshotId)+"|"+HSBI_UlongToString(x.marginState.snapshotId);
}
~~~

### FUNCTION HSBI_FinalizeNewFarPlanDigest

| Field | Individual analysis |
|---|---|
| Function ID | Include/Planning/HSBI_NewFarSolver.mqh:59:HSBI_FinalizeNewFarPlanDigest |
| Source | Include/Planning/HSBI_NewFarSolver.mqh:59–59 |
| Signature | string HSBI_FinalizeNewFarPlanDigest(const HSBI_NewFarSolverInput &x,const string list) |
| Inputs | const HSBI_NewFarSolverInput &x,const string list |
| Outputs / Postconditions | NewFarInputDigest +CANDIDATES+list |
| Domain | inputDTO,listtext |
| Preconditions | Listcomplete/immutableindependentacceptedproducer |
| Guards | No guards |
| Callers | HSBI_SolveNewFar @ Include/Planning/HSBI_NewFarSolver.mqh:148 |
| Dependencies | HSBI_NewFarInputDigest @ Include/Planning/HSBI_NewFarSolver.mqh:59 |
| Normative contract | Docs/14:26; Docs/16:8 |
| Formula IDs | F057/F060 |
| Error IDs | ERR013/026 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | PLAN_TEXT_FINGERPRINT |
| Limitations / side effects | Notfullcontent/provenance; no durablestorage/immutableplanapproval |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{return HSBI_NewFarInputDigest(x)+"|CANDIDATES|"+list;}
~~~

### FUNCTION HSBI_ValidateNewFarSource

| Field | Individual analysis |
|---|---|
| Function ID | Include/Planning/HSBI_NewFarSolver.mqh:60:HSBI_ValidateNewFarSource |
| Source | Include/Planning/HSBI_NewFarSolver.mqh:60–73 |
| Signature | bool HSBI_ValidateNewFarSource(const HSBI_NewFarSolverInput &x) |
| Inputs | const HSBI_NewFarSolverInput &x |
| Outputs / Postconditions | trueonlylistedrole/owner/id/oppositedirection/volumeconditions |
| Domain | oldFar/Core/residualDTOs,closingflags/IDs,brokerlotgrid |
| Preconditions | Actualhistory/residual independentproviderrequired |
| Guards | closingactual/fills/nonzeroIDs;3roles;SamePositionOwner;4namespacechecks;2nonzero/equalIDs;nonNONEdistinctdirections;0<residual<oldFar;actualCorehelper;volumevalidator |
| Callers | HSBI_SolveNewFar @ Include/Planning/HSBI_NewFarSolver.mqh:102 |
| Dependencies | HSBI_SamePositionOwner @ Include/Planning/HSBI_NewFarSolver.mqh:64; HSBI_IsActualBigCoreResidual @ Include/Planning/HSBI_NewFarSolver.mqh:72; HSBI_ValidateVolume @ Include/Planning/HSBI_NewFarSolver.mqh:72 |
| Normative contract | Docs/02:23–34; Docs/14:6–26 |
| Formula IDs | F027/F028/F053/F062 |
| Error IDs | ERR013/041/045/049 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | RESIDUAL_DTO_MATCH_NOT_BROKER_AUTHORITY |
| Limitations / side effects | UnknownnonNONEdistinctdirectionsmaypass; oldFaractualvolume finite separately; flagsnotprovider; plannedNnotactualpromotion |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{
   if(!x.actualClosingDeals.actual||!x.actualClosingDeals.fillsConfirmed||x.actualClosingDeals.sourceDealId==0||x.actualClosingDeals.sourceEventId==0)return false;
   if(x.oldFarDescriptor.role!=HSBI_ROLE_FAR||x.originalBigCoreDescriptor.role!=HSBI_ROLE_BIG_CORE||x.actualBigCoreResidual.role!=HSBI_ROLE_BIG_CORE)return false;
   if(!HSBI_SamePositionOwner(x.originalBigCoreDescriptor.identity,x.actualBigCoreResidual.identity))return false;
   if(x.originalBigCoreDescriptor.identity.accountLogin!=x.oldFarDescriptor.identity.accountLogin||x.originalBigCoreDescriptor.identity.symbol!=x.oldFarDescriptor.identity.symbol||
      x.originalBigCoreDescriptor.identity.magic!=x.oldFarDescriptor.identity.magic||x.originalBigCoreDescriptor.identity.cycleId!=x.cycleId)return false;
   if(x.originalBigCoreDescriptor.identifier==0||x.originalBigCoreDescriptor.identifier!=x.actualBigCoreResidual.identifier||
      x.originalBigCoreDescriptor.ticket==0||x.originalBigCoreDescriptor.ticket!=x.actualBigCoreResidual.ticket)return false;
   if(x.oldFarDescriptor.direction==HSBI_DIRECTION_NONE||x.actualBigCoreResidual.direction==HSBI_DIRECTION_NONE||
      x.oldFarDescriptor.direction==x.actualBigCoreResidual.direction||x.actualBigCoreResidual.actualVolume<=0.0||
      x.actualBigCoreResidual.actualVolume>=x.oldFarDescriptor.actualVolume)return false;
   return HSBI_IsActualBigCoreResidual(x.actualBigCoreResidual,x.originalBigCoreDescriptor.identifier)&&HSBI_ValidateVolume(x.actualBigCoreResidual.actualVolume,x.brokerProperties);
}
~~~

### FUNCTION HSBI_AllowedTransitionLoss

| Field | Individual analysis |
|---|---|
| Function ID | Include/Planning/HSBI_NewFarSolver.mqh:74:HSBI_AllowedTransitionLoss |
| Source | Include/Planning/HSBI_NewFarSolver.mqh:74–74 |
| Signature | double HSBI_AllowedTransitionLoss(const HSBI_NewFarSolverInput &x) |
| Inputs | const HSBI_NewFarSolverInput &x |
| Outputs / Postconditions | MathMin4values |
| Domain | 4moneycaps samebasis |
| Preconditions | Finite/nonnegativecaps verifiedmandatorycaller |
| Guards | No own guards |
| Callers | HSBI_SolveNewFar @ Include/Planning/HSBI_NewFarSolver.mqh:107 |
| Dependencies | NONE project functions |
| Normative contract | Docs/15_RISK_AND_MARGIN_CONTRACT_RU.md:15 |
| Formula IDs | F026 |
| Error IDs | ERR035/040 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | CAP_AGGREGATOR_ONLY |
| Limitations / side effects | minvalidation notsubstitutevalidatingeachcap; lossmetric/basisD05 pending |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{return MathMin(MathMin(x.absoluteLossCap,x.equityPercentCap),MathMin(x.oldFarRiskCap,x.cumulativeCycleLossCap));}
~~~

### FUNCTION HSBI_BuildCandidateFutureSmallInput

| Field | Individual analysis |
|---|---|
| Function ID | Include/Planning/HSBI_NewFarSolver.mqh:75:HSBI_BuildCandidateFutureSmallInput |
| Source | Include/Planning/HSBI_NewFarSolver.mqh:75–79 |
| Signature | HSBI_FutureSmallInput HSBI_BuildCandidateFutureSmallInput(const HSBI_NewFarSolverInput &x,const double candidate) |
| Inputs | const HSBI_NewFarSolverInput &x,const double candidate |
| Outputs / Postconditions | Copieswholetemplate;setsCurrentFar/plan/rev/policy;injection/testflagsfalse |
| Domain | candidate lot,IDs,policy |
| Preconditions | Candidate/domain andtemplateproofs separatelyvalidated |
| Guards | No guards |
| Callers | HSBI_SolveNewFar @ Include/Planning/HSBI_NewFarSolver.mqh:114 |
| Dependencies | NONE project functions |
| Normative contract | Docs/14:6–26; Docs/27_FUTURE_SMALL_SOLVER_RU.md |
| Formula IDs | F027/F028/F053 |
| Error IDs | ERR013/021 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | FORECAST_INPUT_CONSTRUCTOR |
| Limitations / side effects | Clearingtestflags doesn'tauthenticatecopieddata; no actualsourceacquisition |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{
   HSBI_FutureSmallInput fs=x.futureSmallTemplate;fs.currentFar=candidate;fs.planId=x.planId;fs.stateRevision=x.stateRevision;
   fs.allocationPolicy=x.allocationPolicy;fs.useInjectedBrokerProofs=false;fs.testOnlyApproximation=false;return fs;
}
~~~

### FUNCTION HSBI_NewFarProofIdentity

| Field | Individual analysis |
|---|---|
| Function ID | Include/Planning/HSBI_NewFarSolver.mqh:80:HSBI_NewFarProofIdentity |
| Source | Include/Planning/HSBI_NewFarSolver.mqh:80–83 |
| Signature | HSBI_MoneyProofIdentity HSBI_NewFarProofIdentity(const HSBI_NewFarSolverInput &x,const HSBI_PositionDescriptor &position,const HSBI_Role role,const HSBI_Direction direction,const ulong dealId,const ulong eventId,const ulong snapshotId) |
| Inputs | const HSBI_NewFarSolverInput &x,const HSBI_PositionDescriptor &position,const HSBI_Role role,const HSBI_Direction direction,const ulong dealId,const ulong eventId,const ulong snapshotId |
| Outputs / Postconditions | Copiesfields;no independentlookup |
| Domain | namespace/pos/role/direction/deal/event/snapshot/plan/revIDs |
| Preconditions | Actualsourceprovenance externallyrequired |
| Guards | ZeroMemory thenassignments, no validation |
| Callers | HSBI_SolveNewFar @ Include/Planning/HSBI_NewFarSolver.mqh:119; HSBI_SolveNewFar @ Include/Planning/HSBI_NewFarSolver.mqh:120 |
| Dependencies | NONE project functions |
| Normative contract | Docs/31_MONEY_PROOF_IDENTITY_RU.md; D08 pending |
| Formula IDs | F053/F062 |
| Error IDs | ERR013/033 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | IDENTITY_CONSTRUCTOR_NOT_AUTHORITY |
| Limitations / side effects | Usedtooverwritepresentedproofidentity;copyingresultasexpectednotindependentproof |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{
   HSBI_MoneyProofIdentity i;ZeroMemory(i);i.accountLogin=position.identity.accountLogin;i.symbol=position.identity.symbol;i.magic=position.identity.magic;i.cycleId=x.cycleId;i.positionIdentifier=position.identifier;i.role=role;i.direction=direction;i.sourceDealId=dealId;i.sourceEventId=eventId;i.snapshotId=snapshotId;i.planId=x.planId;i.stateRevision=x.stateRevision;return i;
}
~~~

### FUNCTION HSBI_CandidateProofDigest

| Field | Individual analysis |
|---|---|
| Function ID | Include/Planning/HSBI_NewFarSolver.mqh:84:HSBI_CandidateProofDigest |
| Source | Include/Planning/HSBI_NewFarSolver.mqh:84–93 |
| Signature | string HSBI_CandidateProofDigest(const HSBI_NewFarCandidate &c,const HSBI_NewFarSolverInput &x) |
| Inputs | const HSBI_NewFarCandidate &c,const HSBI_NewFarSolverInput &x |
| Outputs / Postconditions | Concatsnumericfields+policy+proofstrings |
| Domain | volumes/moneyrisk/extremaindices,digests |
| Preconditions | Candidatefieldsfullyvalidatedandindependentproofproducer |
| Guards | No localguards |
| Callers | HSBI_SolveNewFar @ Include/Planning/HSBI_NewFarSolver.mqh:145 |
| Dependencies | NONE project functions |
| Normative contract | Docs/14:26; Docs/16:8 |
| Formula IDs | F042/F057/F060 |
| Error IDs | ERR003/013/026/040 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | CANDIDATE_FINGERPRINT_ONLY |
| Limitations / side effects | Nonempty≠full content validity; fixeddecimalsnotexactcodec; noindependentreceipt |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{
   return DoubleToString(c.normalizedVolume,8)+"|"+DoubleToString(x.actualBigCoreResidual.actualVolume,8)+"|"+DoubleToString(x.oldFarDescriptor.actualVolume,8)+"|"+
      DoubleToString(c.compressionLots,8)+"|"+DoubleToString(c.compressionRatio,12)+"|"+DoubleToString(c.aggregateMinimumRecoveryMoney,8)+"|"+
      DoubleToString(c.aggregateWorstMargin,8)+"|"+DoubleToString(c.aggregateWorstRisk,8)+"|"+DoubleToString(c.aggregateWorstGrossExposure,8)+"|"+
      DoubleToString(c.aggregateWorstTransitionLoss,8)+"|"+IntegerToString(c.aggregateWorstMarginLevel)+"|"+IntegerToString(c.aggregateWorstRiskLevel)+"|"+
      IntegerToString(c.aggregateWorstExposureLevel)+"|"+IntegerToString(c.aggregateWorstTransitionLossLevel)+"|"+IntegerToString((int)x.proofSelectionPolicy)+"|"+
      c.aggregateProofDigest+"|"+c.futureSmallProofDigest+"|"+c.moneyProofDigest+"|"+c.marginProofDigest+"|"+c.riskProofDigest+"|"+
      c.catchUpProofDigest+"|"+c.allocationPolicyDigest+"|"+c.controlPriceDigest+"|"+c.costSnapshotDigest;
}
~~~

### FUNCTION HSBI_SolveNewFar

| Field | Individual analysis |
|---|---|
| Function ID | Include/Planning/HSBI_NewFarSolver.mqh:94:HSBI_SolveNewFar |
| Source | Include/Planning/HSBI_NewFarSolver.mqh:94–153 |
| Signature | HSBI_NewFarSolverResult HSBI_SolveNewFar(const HSBI_NewFarSolverInput &x) |
| Inputs | const HSBI_NewFarSolverInput &x |
| Outputs / Postconditions | Typedrejectstatuses orSELECTED forecast; no promotion/ledger/trade |
| Domain | brokergridfinite,actualresidual,forecastproofs/caps |
| Preconditions | Independentactualsource/completehistory andnormativechoice beforepromotion |
| Guards | mode/unit/injection/policy;fresh5;secondFar;source;money;plan/persist;optionaldigest;cap;gridloop;compression;futureproof;aggregate;CatchUp;NewFarGates;completeness;ranking |
| Callers | NO_CALLER_FOUND: all74 production source bodies, no dynamic/native proof |
| Dependencies | HSBI_IsStaticCalculationAllowed @ Include/Planning/HSBI_NewFarSolver.mqh:99; HSBI_ValidateAllocationPolicy @ Include/Planning/HSBI_NewFarSolver.mqh:99; HSBI_ValidateNewFarSource @ Include/Planning/HSBI_NewFarSolver.mqh:102; HSBI_NewFarInputDigest @ Include/Planning/HSBI_NewFarSolver.mqh:106; HSBI_AllowedTransitionLoss @ Include/Planning/HSBI_NewFarSolver.mqh:107; HSBI_IsFiniteNumber @ Include/Planning/HSBI_NewFarSolver.mqh:107; HSBI_GridTolerance @ Include/Planning/HSBI_NewFarSolver.mqh:109; HSBI_NormalizeVolume @ Include/Planning/HSBI_NewFarSolver.mqh:110; HSBI_ValidateVolume @ Include/Planning/HSBI_NewFarSolver.mqh:112; HSBI_BuildCandidateFutureSmallInput @ Include/Planning/HSBI_NewFarSolver.mqh:114; HSBI_EvaluateCandidateMoney @ Include/Planning/HSBI_NewFarSolver.mqh:114; HSBI_AggregateFutureSmallProof @ Include/Planning/HSBI_NewFarSolver.mqh:116; HSBI_NewFarProofIdentity @ Include/Planning/HSBI_NewFarSolver.mqh:119; HSBI_NewFarProofIdentity @ Include/Planning/HSBI_NewFarSolver.mqh:120; HSBI_EvaluateReserveCatchUp @ Include/Planning/HSBI_NewFarSolver.mqh:127; HSBI_EvaluateNewFarGates @ Include/Planning/HSBI_NewFarSolver.mqh:134; HSBI_ReserveCatchUpDigest @ Include/Planning/HSBI_NewFarSolver.mqh:143; HSBI_AllocationPolicyDigest @ Include/Planning/HSBI_NewFarSolver.mqh:144; HSBI_FutureSmallTemplateDigest @ Include/Planning/HSBI_NewFarSolver.mqh:145; HSBI_CandidateProofDigest @ Include/Planning/HSBI_NewFarSolver.mqh:145; HSBI_IsCompleteCandidateProof @ Include/Planning/HSBI_NewFarSolver.mqh:146; HSBI_FinalizeNewFarPlanDigest @ Include/Planning/HSBI_NewFarSolver.mqh:148; HSBI_CompareCandidateTieBreak @ Include/Planning/HSBI_NewFarSolver.mqh:149 |
| Normative contract | Docs/14:6–26; Docs/29_CANDIDATE_OBJECTIVE_AND_TIEBREAK_RU.md |
| Formula IDs | F023/F027/F028/F047/F048/F057 |
| Error IDs | ERR013/018/019/026/040/041/045 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | Conditional delegated projected OrderCalcProfit/OrderCalcMargin; risk/ownership/EA-origin data остаются supplied DTO. Нет actual deals/history provider; native NOT_RUN. |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | PURE_SOLVER_NOT_ACTUAL_PROMOTION |
| Limitations / side effects | Expectedidentity copiedfromrewrittenproof ERR013;selectedN may<actualresidual ERR045;singleCatchUpcontrol ERR018;ERR051: missinggriditerationprogress atlargeULP; no actualcommit |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{
   HSBI_NewFarSolverResult r;ZeroMemory(r);r.status=HSBI_SOLVER_NO_SAFE_CANDIDATE;r.reason=HSBI_REASON_INTERNAL_INVARIANT_FAILED;
   r.oldFarVolume=x.oldFarDescriptor.actualVolume;r.actualResidualVolume=x.actualBigCoreResidual.actualVolume;r.projectedVolume=x.projectedVolume;
   r.planId=x.planId;r.stateRevision=x.stateRevision;r.sourceIdentifier=x.originalBigCoreDescriptor.identifier;r.sourceDealId=x.actualClosingDeals.sourceDealId;r.details="NO_SAFE_CANDIDATE";
   if(!HSBI_IsStaticCalculationAllowed(x.futureSmallTemplate.runtimeMode)||x.futureSmallTemplate.runtimeMode==HSBI_RUNTIME_UNIT_TEST||x.testOnlyApproximation||x.futureSmallTemplate.useInjectedBrokerProofs||!HSBI_ValidateAllocationPolicy(x.allocationPolicy)){r.status=HSBI_SOLVER_PROOF_FAILED;r.details="ALLOCATION_OR_APPROXIMATION_INVALID";return r;}
   if(!x.controlPrice.fresh||!x.riskState.fresh||!x.marginState.fresh||!x.moneyState.fresh||!x.allocationState.fresh){r.status=HSBI_SOLVER_STALE_SNAPSHOT;r.details="STALE_SNAPSHOT";return r;}
   if(x.secondFarPresent){r.status=HSBI_SOLVER_RECONCILIATION_REQUIRED;r.details="SECOND_FAR";return r;}
   if(!HSBI_ValidateNewFarSource(x)){r.status=HSBI_SOLVER_SOURCE_MISMATCH;r.reason=HSBI_REASON_INVALID_IDENTITY;r.details="NEW_FAR_SOURCE_MISMATCH";return r;}
   if(!x.brokerMoneyAvailable){r.status=HSBI_SOLVER_PROOF_FAILED;r.details="BROKER_MONEY_UNAVAILABLE";return r;}
   if(x.planId==0||x.stateRevision==0||x.smallTransitionPlan.planId!=x.planId||x.smallTransitionPlan.stateRevision!=x.stateRevision||
      !x.smallTransitionPlan.immutable||!x.smallTransitionPlan.persisted){r.status=HSBI_SOLVER_RECONCILIATION_REQUIRED;r.details="PLAN_IDENTITY_MISMATCH";return r;}
   string inputDigest=HSBI_NewFarInputDigest(x);if(x.expectedPlanDigest!=""&&x.expectedPlanDigest!=inputDigest){r.status=HSBI_SOLVER_RECONCILIATION_REQUIRED;r.details="PLAN_DIGEST_MISMATCH";return r;}
   r.allowedTransitionLoss=HSBI_AllowedTransitionLoss(x);if(!HSBI_IsFiniteNumber(r.allowedTransitionLoss)||r.allowedTransitionLoss<0.0){r.status=HSBI_SOLVER_TRANSITION_LOSS_FAILED;r.details="TRANSITION_CAP_UNAVAILABLE";return r;}
   HSBI_NewFarCandidate safe[];int safeCount=0;double upper=MathMin(x.brokerProperties.volumeMax,x.actualBigCoreResidual.actualVolume);string listDigest="";
   for(double n=x.brokerProperties.volumeMin;n<=upper+HSBI_GridTolerance(x.brokerProperties.volumeStep);n+=x.brokerProperties.volumeStep) {
      r.candidateCount++;double candidate=HSBI_NormalizeVolume(n,x.brokerProperties.volumeStep,HSBI_VOLUME_PARTIAL_FAR);
      double compression=x.oldFarDescriptor.actualVolume-candidate,ratio=compression/x.oldFarDescriptor.actualVolume;
      if(!HSBI_ValidateVolume(candidate,x.brokerProperties)||candidate<=0.0||candidate>=x.oldFarDescriptor.actualVolume||candidate>x.maximumNewFarRatio*x.oldFarDescriptor.actualVolume||
         compression<x.minimumCompressionLots||ratio<x.minimumCompressionRatio){r.rejectedCandidateCount++;continue;}
      HSBI_FutureSmallInput fs=HSBI_BuildCandidateFutureSmallInput(x,candidate);HSBI_CandidateMoneyEvaluationResult cp=HSBI_EvaluateCandidateMoney(fs);
      if(!cp.valid){r.rejectedCandidateCount++;continue;}HSBI_FutureSmallResult proof=cp.futureSmallProof;
      HSBI_FutureSmallAggregateProof aggregate=HSBI_AggregateFutureSmallProof(proof,x.proofSelectionPolicy,x.explicitCatchUpControlLevel);
      if(!aggregate.valid||!aggregate.runtimeConfirmed||!aggregate.allMoneyProofsValid||!aggregate.allMarginProofsValid||!aggregate.allRiskProofsValid||!aggregate.allTransitionLossProofsValid){r.rejectedCandidateCount++;continue;}
      int controlIndex=aggregate.catchUpControlLevel-1;HSBI_FutureSmallLevelProof control=proof.levels[controlIndex];
      control.reserveSourceProof.identity=HSBI_NewFarProofIdentity(x,x.originalBigCoreDescriptor,HSBI_ROLE_BIG_CORE,x.originalBigCoreDescriptor.direction,x.reserveSourceDealId,x.reserveSourceEventId,control.controlSnapshotId);
      control.farLossProof.identity=HSBI_NewFarProofIdentity(x,x.oldFarDescriptor,HSBI_ROLE_FAR,x.oldFarDescriptor.direction,x.farLossSourceDealId,x.farLossSourceEventId,control.controlSnapshotId);
      HSBI_ReserveCatchUpInput ci;ZeroMemory(ci);ci.runtimeMode=fs.runtimeMode;ci.testOnlySource=false;ci.allocationPolicy=x.allocationPolicy;ci.reserveEligibleMoney=MathMax(0.0,control.reserveSourceProof.netMoney);
      ci.reserveEligibleMoneyAlreadyAllocated=x.reserveAllocationSource.reserveAllocated>0.0;ci.farLossIncreaseMoney=MathMax(0.0,-control.farLossProof.netMoney);ci.executionSafetyBuffer=fs.executionSafetyBuffer;
      ci.netBigVolume=control.netBigVolume;ci.farVolume=candidate;ci.farDirection=x.oldFarDescriptor.direction;ci.reserveSourceProof=control.reserveSourceProof;ci.farLossProof=control.farLossProof;
      ci.expectedReserveIdentity=control.reserveSourceProof.identity;ci.expectedFarIdentity=control.farLossProof.identity;ci.reserveAllocationSource=x.reserveAllocationSource;
      ci.consumptionKey=x.consumptionKey;ci.priorConsumptionKey=x.priorConsumptionKey;ci.hasPriorConsumption=x.hasPriorConsumption;
      ci.sourceDealId=x.reserveSourceDealId;ci.sourceEventId=x.reserveSourceEventId;ci.planId=x.planId;ci.stateRevision=x.stateRevision;ci.snapshotId=control.controlSnapshotId;
      ci.projected=true;ci.moneyAvailable=control.moneyIncluded;ci.fresh=fs.snapshotsFresh;HSBI_ReserveCatchUpResult catchResult=HSBI_EvaluateReserveCatchUp(ci);
      if(!catchResult.valid){r.rejectedCandidateCount++;continue;}
      HSBI_NewFarGateInput gate;ZeroMemory(gate);gate.marginNext=aggregate.maximumMargin;gate.allowedMargin=x.marginState.allowedMargin;gate.riskNext=aggregate.maximumRisk;
      gate.riskOld=x.riskState.currentRisk;gate.riskTolerance=x.riskState.riskTolerance;gate.grossExposureNext=aggregate.maximumGrossExposure;
      gate.grossExposureOld=x.riskState.currentGrossExposure;gate.transitionLoss=aggregate.maximumTransitionLoss;gate.absoluteLossCap=x.absoluteLossCap;
      gate.equityPercentCap=x.equityPercentCap;gate.oldFarRiskCap=x.oldFarRiskCap;gate.cumulativeCycleLossCap=x.cumulativeCycleLossCap;
      gate.marginAvailable=aggregate.allMarginProofsValid;gate.riskAvailable=aggregate.allRiskProofsValid;gate.transitionCapAvailable=aggregate.allTransitionLossProofsValid;
      gate.moneyAvailable=aggregate.allMoneyProofsValid;gate.snapshotFresh=fs.snapshotsFresh;if(!HSBI_EvaluateNewFarGates(gate).passed){r.rejectedCandidateCount++;continue;}
      HSBI_NewFarCandidate c;ZeroMemory(c);c.candidateVolume=n;c.normalizedVolume=candidate;c.oldFarVolume=x.oldFarDescriptor.actualVolume;
      c.compressionLots=compression;c.compressionRatio=ratio;c.riskNext=aggregate.maximumRisk;c.marginNext=aggregate.maximumMargin;c.futureSmallStatus=HSBI_STATUS_VALID;
      c.finiteCatchUpStatus=HSBI_STATUS_VALID;c.nextCycleFeasible=true;c.moneyProofValid=true;c.marginProofValid=true;c.riskProofValid=aggregate.allRiskProofsValid;
      c.futureSmallProofValid=proof.valid;c.aggregateProofValid=aggregate.valid;c.aggregateRuntimeConfirmed=aggregate.runtimeConfirmed;c.aggregateMinimumRecoveryMoney=aggregate.minimumRecoveryMoney;c.aggregateWorstMargin=aggregate.maximumMargin;c.aggregateWorstRisk=aggregate.maximumRisk;c.aggregateWorstGrossExposure=aggregate.maximumGrossExposure;c.aggregateWorstTransitionLoss=aggregate.maximumTransitionLoss;c.aggregateWorstMarginLevel=aggregate.worstMarginLevel;c.aggregateWorstRiskLevel=aggregate.worstRiskLevel;c.aggregateWorstExposureLevel=aggregate.worstExposureLevel;c.aggregateWorstTransitionLossLevel=aggregate.worstTransitionLossLevel;c.aggregateProofDigest=aggregate.aggregateDigest;c.catchUpProofValid=catchResult.valid;c.allocationPolicyValid=true;c.controlSnapshotsValid=true;c.costSnapshotsValid=true;
      c.sourceBigCoreIdentifier=x.originalBigCoreDescriptor.identifier;c.sourceBigCoreTicket=x.originalBigCoreDescriptor.ticket;c.validationStatus=HSBI_STATUS_VALID;
      c.reason=HSBI_REASON_OK;c.futureTransitionCount=proof.theoreticalDepth;c.safetyBuffer=catchResult.catchUpMargin;c.reserveShare=catchResult.reserveShare;
      c.reserveEligibleMoney=catchResult.reserveEligibleMoney;c.reserveGainMoney=catchResult.reserveGainMoney;c.farLossIncreaseMoney=catchResult.farLossIncreaseMoney;
      c.moneyProofDigest=cp.moneyProofDigest;c.marginProofDigest=cp.marginProofDigest;c.riskProofDigest=cp.riskProofDigest;
      c.futureSmallProofDigest=cp.futureSmallProofDigest;c.catchUpProofDigest=HSBI_ReserveCatchUpDigest(catchResult);
      c.allocationPolicyDigest=HSBI_AllocationPolicyDigest(x.allocationPolicy);c.controlPriceDigest=cp.futureSmallProofDigest+"|CONTROL";
      c.costSnapshotDigest=HSBI_FutureSmallTemplateDigest(fs)+"|COST";c.candidateDigest=HSBI_CandidateProofDigest(c,x);c.fullDigestValid=c.candidateDigest!="";
      if(!HSBI_IsCompleteCandidateProof(c)){r.rejectedCandidateCount++;continue;}listDigest+=c.candidateDigest+";";ArrayResize(safe,safeCount+1);safe[safeCount++]=c;
   }
   r.candidateListDigest=listDigest;r.planDigest=HSBI_FinalizeNewFarPlanDigest(x,listDigest);if(safeCount==0)return r;
   int best=0;for(int i=1;i<safeCount;i++)if(HSBI_CompareCandidateTieBreak(safe[i],safe[best])<0)best=i;HSBI_NewFarCandidate selected=safe[best];
   r.valid=true;r.status=HSBI_SOLVER_SELECTED;r.selectedVolume=selected.normalizedVolume;r.compressionLots=selected.compressionLots;
   r.compressionRatio=selected.compressionRatio;r.riskNext=selected.riskNext;r.marginNext=selected.marginNext;r.transitionLoss=selected.farLossIncreaseMoney;
   r.candidateDigest=selected.candidateDigest;r.proofDigest=selected.futureSmallProofDigest;r.reason=HSBI_REASON_OK;r.details="SELECTED";return r;
}
~~~

### FUNCTION HSBI_FailClosed

| Field | Individual analysis |
|---|---|
| Function ID | Include/Risk/HSBI_CalculationGateTypes.mqh:6:HSBI_FailClosed |
| Source | Include/Risk/HSBI_CalculationGateTypes.mqh:6–9 |
| Signature | HSBI_CalculationGateResult HSBI_FailClosed(const HSBI_CalculationStatus status,const HSBI_CalculationFailure failure,const HSBI_ReasonCode reason,const string details) |
| Inputs | const HSBI_CalculationStatus status,const HSBI_CalculationFailure failure,const HSBI_ReasonCode reason,const string details |
| Outputs / Postconditions | passed=(status==PASS),copiesotherfields |
| Domain | status/failure/reason enums,details |
| Preconditions | Caller mustchooseappropriatefailurestatus |
| Guards | singlePASScomparison |
| Callers | NO_CALLER_FOUND: all74 production source bodies, no dynamic/native proof |
| Dependencies | NONE project functions |
| Normative contract | CONTRACT_NOT_FOUND standalonefactory; Docs/24:11 statusfamily |
| Formula IDs | F036/F060 |
| Error IDs | ERR027 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | STATUS_CONSTRUCTOR |
| Limitations / side effects | Названиенеguarantee unconditionalreject:constructorcalledwithPASSreturns passedtrue; notindependentvalidator |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{
   HSBI_CalculationGateResult r;r.status=status;r.passed=(status==HSBI_CALC_PASS);r.failure=failure;r.reason=reason;r.details=details;return r;
}
~~~

### FUNCTION HSBI_CalculationResultFlagsValid

| Field | Individual analysis |
|---|---|
| Function ID | Include/Risk/HSBI_CalculationGateTypes.mqh:10:HSBI_CalculationResultFlagsValid |
| Source | Include/Risk/HSBI_CalculationGateTypes.mqh:10–13 |
| Signature | bool HSBI_CalculationResultFlagsValid(const bool valid,const bool projected,const bool actual,const HSBI_CalculationStatus status) |
| Inputs | const bool valid,const bool projected,const bool actual,const HSBI_CalculationStatus status |
| Outputs / Postconditions | false ifprojected&&actual orvalid!=(statusPASS);else true |
| Domain | valid/projected/actualbool,statusenum |
| Preconditions | Knownstatus/domain/typepolicy separate |
| Guards | 2consistencyconditions |
| Callers | NO_CALLER_FOUND: all74 production source bodies, no dynamic/native proof |
| Dependencies | NONE project functions |
| Normative contract | Docs/24:3–11 |
| Formula IDs | F036/F060 |
| Error IDs | ERR049 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | FLAGS_COHERENCE_ONLY |
| Limitations / side effects | Bothactual/projectedfalse permitted; unknownstatuswithvalidfalsemaypass; helperнеfullmoneykindproof |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{
   if(projected&&actual)return false;if(valid!=(status==HSBI_CALC_PASS))return false;return true;
}
~~~

### FUNCTION HSBI_EvaluateFutureSmallRisk

| Field | Individual analysis |
|---|---|
| Function ID | Include/Risk/HSBI_FutureSmallRiskEvaluator.mqh:29:HSBI_EvaluateFutureSmallRisk |
| Source | Include/Risk/HSBI_FutureSmallRiskEvaluator.mqh:29–51 |
| Signature | HSBI_FutureSmallRiskResult HSBI_EvaluateFutureSmallRisk(const HSBI_FutureSmallRiskInput &x) |
| Inputs | const HSBI_FutureSmallRiskInput &x |
| Outputs / Postconditions | UNAVAILABLE forbadflags/proxy;ERRORnonfinite;REJECTnotreduced;PASSstrictreduction |
| Domain | riskmoney/tolerance,snapshot/sourceenum,basket |
| Preconditions | Independentriskproviderandapprovedriskbasisneeded |
| Guards | fresh/id/basket;runtimeexactsource/confirmed/!test;3finite;tolerance>=0;risk<prior−tol |
| Callers | HSBI_EvaluateFutureSmallLevel @ Include/Planning/HSBI_FutureSmallSolver.mqh:86 |
| Dependencies | HSBI_IsFiniteNumber @ Include/Risk/HSBI_FutureSmallRiskEvaluator.mqh:42; HSBI_IsFiniteNumber @ Include/Risk/HSBI_FutureSmallRiskEvaluator.mqh:42; HSBI_IsFiniteNumber @ Include/Risk/HSBI_FutureSmallRiskEvaluator.mqh:43 |
| Normative contract | Docs/15_RISK_AND_MARGIN_CONTRACT_RU.md; Docs/27_FUTURE_SMALL_SOLVER_RU.md |
| Formula IDs | F031/F036/F062 |
| Error IDs | ERR009/013/034 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | RUNTIME_LABELLED_RISK_NOT_PROVIDER |
| Limitations / side effects | Negativerisknotexplicitrejected; no independentcontentbinding; proxy mixedunit expression returnedonlyUNAVAILABLE,notacceptedproof |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{
   HSBI_FutureSmallRiskResult r; ZeroMemory(r); r.status=HSBI_CALC_UNAVAILABLE;
   r.priorRisk=x.priorRisk; r.tolerance=x.tolerance; r.source=x.source;
   r.runtimeConfirmed=x.runtimeConfirmed; r.testOnly=x.testOnly;
   r.reason=HSBI_REASON_NOT_INITIALIZED; r.details="RISK_RUNTIME_PROOF_UNAVAILABLE";
   if(!x.fresh || x.snapshotId==0 || !x.basket.valid) return r;
   if(x.source!=HSBI_RISK_SOURCE_RUNTIME || !x.runtimeConfirmed || x.testOnly) {
      r.riskValue=(x.source==HSBI_RISK_SOURCE_PROXY_TEST_ONLY) ?
         x.basket.transitionLoss+x.basket.totalMargin+x.basket.grossExposure : x.evaluatedRisk;
      r.details="RISK_PROXY_OR_TEST_ONLY_FORBIDDEN"; return r;
   }
   r.riskValue=x.evaluatedRisk;
   if(!HSBI_IsFiniteNumber(r.riskValue)||!HSBI_IsFiniteNumber(x.priorRisk)||
      !HSBI_IsFiniteNumber(x.tolerance)||x.tolerance<0.0) {
      r.status=HSBI_CALC_ERROR; r.details="NONFINITE_RISK"; return r;
   }
   if(r.riskValue>=x.priorRisk-x.tolerance) {
      r.status=HSBI_CALC_REJECT; r.reason=HSBI_REASON_INTERNAL_INVARIANT_FAILED;
      r.details="RISK_NOT_REDUCED"; return r;
   }
   r.status=HSBI_CALC_PASS; r.valid=true; r.reason=HSBI_REASON_OK; r.details="PASS"; return r;
}
~~~

### FUNCTION HSBI_EvaluateNewFarGates

| Field | Individual analysis |
|---|---|
| Function ID | Include/Risk/HSBI_NewFarGateTypes.mqh:6:HSBI_EvaluateNewFarGates |
| Source | Include/Risk/HSBI_NewFarGateTypes.mqh:6–17 |
| Signature | HSBI_NewFarGateResult HSBI_EvaluateNewFarGates(const HSBI_NewFarGateInput &x) |
| Inputs | const HSBI_NewFarGateInput &x |
| Outputs / Postconditions | typedfailureorPASS, no sideeffects |
| Domain | moneycaps,risk/margin,grosslots,flags |
| Preconditions | Allcurrent/allowedboundsfiniteandindependentcaller |
| Guards | fresh;4available;4finite/nonnegativecaps;mincap;marginNextfinite/bound;riskNext/grossNextfinite+reduction;transitionfinite<=cap |
| Callers | HSBI_SolveNewFar @ Include/Planning/HSBI_NewFarSolver.mqh:134 |
| Dependencies | HSBI_IsFiniteNumber @ Include/Risk/HSBI_NewFarGateTypes.mqh:11; HSBI_IsFiniteNumber @ Include/Risk/HSBI_NewFarGateTypes.mqh:11; HSBI_IsFiniteNumber @ Include/Risk/HSBI_NewFarGateTypes.mqh:11; HSBI_IsFiniteNumber @ Include/Risk/HSBI_NewFarGateTypes.mqh:11; HSBI_IsFiniteNumber @ Include/Risk/HSBI_NewFarGateTypes.mqh:13; HSBI_IsFiniteNumber @ Include/Risk/HSBI_NewFarGateTypes.mqh:14; HSBI_IsFiniteNumber @ Include/Risk/HSBI_NewFarGateTypes.mqh:14; HSBI_IsFiniteNumber @ Include/Risk/HSBI_NewFarGateTypes.mqh:15 |
| Normative contract | Docs/15_RISK_AND_MARGIN_CONTRACT_RU.md |
| Formula IDs | F026/F030/F031/F032/F036 |
| Error IDs | ERR009/013/034/040 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | LOCAL_GATE_CONFIG_DOMAIN_PARTIAL |
| Limitations / side effects | allowedMargin/riskOld/riskTolerance/grossOldfinite/domain notvalidatedlocally; negativeinputs maynotexcluded; noglobalprovider |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{
   HSBI_NewFarGateResult r;ZeroMemory(r);r.status=HSBI_CALC_REJECT;r.reason=HSBI_REASON_INTERNAL_INVARIANT_FAILED;
   if(!x.snapshotFresh){r.failure=HSBI_STALE_SNAPSHOT;r.reason=HSBI_REASON_STALE_SNAPSHOT;return r;}
   if(!x.marginAvailable||!x.riskAvailable||!x.transitionCapAvailable||!x.moneyAvailable){r.status=HSBI_CALC_UNAVAILABLE;r.failure=HSBI_BROKER_MONEY_UNAVAILABLE;return r;}
   if(!HSBI_IsFiniteNumber(x.absoluteLossCap)||!HSBI_IsFiniteNumber(x.equityPercentCap)||!HSBI_IsFiniteNumber(x.oldFarRiskCap)||!HSBI_IsFiniteNumber(x.cumulativeCycleLossCap)||x.absoluteLossCap<0.0||x.equityPercentCap<0.0||x.oldFarRiskCap<0.0||x.cumulativeCycleLossCap<0.0){r.failure=HSBI_CATCH_UP_FAILED;return r;}
   r.allowedTransitionLoss=MathMin(MathMin(x.absoluteLossCap,x.equityPercentCap),MathMin(x.oldFarRiskCap,x.cumulativeCycleLossCap));
   if(!HSBI_IsFiniteNumber(x.marginNext)||x.marginNext>x.allowedMargin){r.failure=HSBI_NONFINITE_MARGIN;return r;}
   if(!HSBI_IsFiniteNumber(x.riskNext)||x.riskNext>=x.riskOld-x.riskTolerance||!HSBI_IsFiniteNumber(x.grossExposureNext)||x.grossExposureNext>=x.grossExposureOld){r.failure=HSBI_RECOVERY_SLOPE_FAILED;return r;}
   if(!HSBI_IsFiniteNumber(x.transitionLoss)||x.transitionLoss>r.allowedTransitionLoss){r.failure=HSBI_CATCH_UP_FAILED;return r;}
   r.passed=true;r.status=HSBI_CALC_PASS;r.failure=HSBI_CALC_FAILURE_NONE;r.reason=HSBI_REASON_OK;return r;
}
~~~

### FUNCTION HSBI_RuntimeDecisionContextDigest

| Field | Individual analysis |
|---|---|
| Function ID | Include/Runtime/HSBI_RuntimeDecisionTypes.mqh:17:HSBI_RuntimeDecisionContextDigest |
| Source | Include/Runtime/HSBI_RuntimeDecisionTypes.mqh:17–17 |
| Signature | string HSBI_RuntimeDecisionContextDigest(const HSBI_RuntimeDecisionContext &x) |
| Inputs | const HSBI_RuntimeDecisionContext &x |
| Outputs / Postconditions | Concatsselected21fields |
| Domain | namespace/state/IDs,actualresiduallots,proof/alloc/snapshotstrings |
| Preconditions | Completecontent/actualauthority checkedseparately |
| Guards | No validationguards |
| Callers | HSBI_ValidateRuntimeDecisionContext @ Include/Runtime/HSBI_RuntimeDecisionValidator.mqh:27 |
| Dependencies | HSBI_UlongToString @ Include/Runtime/HSBI_RuntimeDecisionTypes.mqh:17; HSBI_UlongToString @ Include/Runtime/HSBI_RuntimeDecisionTypes.mqh:17; HSBI_UlongToString @ Include/Runtime/HSBI_RuntimeDecisionTypes.mqh:17; HSBI_UlongToString @ Include/Runtime/HSBI_RuntimeDecisionTypes.mqh:17; HSBI_UlongToString @ Include/Runtime/HSBI_RuntimeDecisionTypes.mqh:17; HSBI_UlongToString @ Include/Runtime/HSBI_RuntimeDecisionTypes.mqh:17; HSBI_UlongToString @ Include/Runtime/HSBI_RuntimeDecisionTypes.mqh:17; HSBI_ReserveCatchUpDigest @ Include/Runtime/HSBI_RuntimeDecisionTypes.mqh:17; HSBI_ReserveAllocationSourceDigest @ Include/Runtime/HSBI_RuntimeDecisionTypes.mqh:17; HSBI_ReserveConsumptionKeyDigest @ Include/Runtime/HSBI_RuntimeDecisionTypes.mqh:17 |
| Normative contract | Docs/16:8; Docs/18:28–30 |
| Formula IDs | F042/F053/F057/F060 |
| Error IDs | ERR003/013/026 |
| Proof boundary | Локальный body; accepted path не заменяет independent action boundary Docs/02:23. Все статические callers перечислены отдельно. |
| Actual authority | NONE inside helper: supplied DTO/config, не самостоятельный broker/provider authority |
| Fail-closed | Отказ/результат ровно по перечисленным guards; const input helpers zero state delta; initializer/reset effects указаны отдельно. |
| Implementation status | CONTEXT_FINGERPRINT_ONLY |
| Limitations / side effects | Flags/manynestedfieldsnotincluded; supplieddigestnonemptyrecomputed≠independentexpected; fixedprecisionnotfullcodec |

Полное source body для сверки clauses (цитата, не executable artifact):

~~~text
{return LongToString(x.accountLogin)+"|"+x.symbol+"|"+LongToString(x.magic)+"|"+HSBI_UlongToString(x.cycleId)+"|"+HSBI_UlongToString(x.planId)+"|"+HSBI_UlongToString(x.stateRevision)+"|"+IntegerToString(x.schemaVersion)+"|"+IntegerToString(x.moneyStateVersion)+"|"+IntegerToString((int)x.runtimeMode)+"|"+IntegerToString((int)x.state)+"|"+HSBI_UlongToString(x.eventId)+"|"+HSBI_UlongToString(x.actionId)+"|"+HSBI_UlongToString(x.actualResidual.identifier)+"|"+HSBI_UlongToString(x.actualResidual.ticket)+"|"+DoubleToString(x.actualResidual.actualVolume,8)+"|"+x.aggregate.aggregateDigest+"|"+x.candidate.candidateDigest+"|"+HSBI_ReserveCatchUpDigest(x.catchUp)+"|"+HSBI_ReserveAllocationSourceDigest(x.allocationSource)+"|"+HSBI_ReserveConsumptionKeyDigest(x.consumptionKey)+"|"+x.persistence.snapshotDigest;}
~~~


## R2 — перегрузки NormalizePriceToTick: две декларации, не одна функция

### FUNCTION HSBI_NormalizePriceToTick

| Field | Individual analysis |
|---|---|
| Function ID | Include/Planning/HSBI_BrokerGrid.mqh:13:HSBI_NormalizePriceToTick |
| Source | Include/Planning/HSBI_BrokerGrid.mqh:13–18 |
| Signature | double HSBI_NormalizePriceToTick(const double price,const double tickSize,const HSBI_GridRoundingMode mode) |
| Inputs | const double price,const double tickSize,const HSBI_GridRoundingMode mode |
| Outputs | double price; invalid returns0; no context/ledger effects |
| Domain | finitepositive price/tick; known roundingmode |
| Preconditions | Origin0 brokerlattice and approved tie/domain policy; no nativeexecution |
| Postconditions | FLOOR/CEIL/NEAREST normalized then output-grid recheck |
| Guards | finiteprice/tick;2positive;mode FLOOR/CEIL else NEAREST;outputgrid |
| Callers | NO_CALLER_FOUND: full text search all74 production sources; only2overloaded declarations |
| Dependencies | HSBI_IsFiniteNumber;HSBI_IsPriceOnTickGrid;MathRound/Floor/Ceil |
| Normative contract | Docs/25_BROKER_GRID_AND_ROUNDING_RU.md:3; Docs/05_GEOMETRY_MODEL_RU.md:16 |
| Formula IDs | F036/F044/F048 |
| Error IDs | ERR024/039/040/049 |
| Proof boundary | Primitive only; min/max/side/freshness/provider validation mustfollow; no mandatory financialcaller |
| Actual authority | NONE: supplied numbers, no brokerread |
| Fail-closed | Invalidprice/tick rejected0;unknownmode silently NEAREST |
| Implementation status | THREE_ARG_LOCAL_GRID_NORMALIZER |

~~~text
{
   if(!HSBI_IsFiniteNumber(price)||!HSBI_IsFiniteNumber(tickSize)||price<=0.0||tickSize<=0.0)return 0.0;
   double ticks=price/tickSize;double units=MathRound(ticks);if(mode==HSBI_GRID_FLOOR)units=MathFloor(ticks+1.0e-12);else if(mode==HSBI_GRID_CEIL)units=MathCeil(ticks-1.0e-12);
   double normalized=units*tickSize;return HSBI_IsPriceOnTickGrid(normalized,tickSize)?normalized:0.0;
}
~~~

### FUNCTION HSBI_NormalizePriceToTick

| Field | Individual analysis |
|---|---|
| Function ID | Include/Planning/HSBI_ControlPrices.mqh:12:HSBI_NormalizePriceToTick |
| Source | Include/Planning/HSBI_ControlPrices.mqh:12–12 |
| Signature | double HSBI_NormalizePriceToTick(const double price,const double tickSize) |
| Inputs | const double price,const double tickSize |
| Outputs | double price; invalid returns0; no context/ledger effects |
| Domain | finitepositive price/tick requiredcaller, though finite notcheckedinside |
| Preconditions | Origin0 brokerlattice and approved tie/domain policy; no nativeexecution |
| Postconditions | MathRound(price/tick)*tick; no output recheck |
| Guards | tick<=0→0 only |
| Callers | NO_CALLER_FOUND: full text search all74 production sources; only2overloaded declarations |
| Dependencies | MathRound |
| Normative contract | Docs/25_BROKER_GRID_AND_ROUNDING_RU.md:3; Docs/05_GEOMETRY_MODEL_RU.md:16 |
| Formula IDs | F036/F044/F048 |
| Error IDs | ERR024/039/040/049 |
| Proof boundary | Primitive only; min/max/side/freshness/provider validation mustfollow; no mandatory financialcaller |
| Actual authority | NONE: supplied numbers, no brokerread |
| Fail-closed | Nonfinite input/output not guarded; zero sentinelnotactualprice |
| Implementation status | TWO_ARG_WEAKER_PRIMITIVE_NOT_EQUIVALENT |

~~~text
{if(tickSize<=0.0)return 0.0;return MathRound(price/tickSize)*tickSize;}
~~~
