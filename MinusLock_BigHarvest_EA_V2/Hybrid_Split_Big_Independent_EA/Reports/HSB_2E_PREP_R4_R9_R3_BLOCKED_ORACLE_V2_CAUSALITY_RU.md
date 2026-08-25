# R9-R3 — блокировка Oracle V2 после model-independent confrontation

```text
HSB.2E_PREP_R4_R9_R3=BLOCKED_OR_FAILED
PASS_DECLARATION_ALLOWED=NO
IMPLEMENTATION_HANDOFF=NOT_READY
TRADING_LOGIC_START_ALLOWED=NO
REAL_TRADING_ALLOWED=NO
```

После freeze обнаружено, что certificate adversarial cases не изолируют certificate provenance. Например `CERT_FORGERY_ECONOMIC_PROPOSAL` меняет `availableMoney` и тем самым раньше certificate reconstruction нарушает money conservation; `CERT_FORGERY_ALLOCATION` создаёт Reserve misuse; `CERT_FORGERY_FSM` создаёт persistence revision mismatch. Qualification V2 ошибочно проверяла только declared path и anchor, но не отсутствие второго нормативного дефекта.

```text
CHECK_ID=R9_ORACLE_V2_SINGLE_CAUSE_CERTIFICATE_ECONOMIC
EXPECTED=CERTIFICATE_PROVENANCE_MISMATCH
ACTUAL=MONEY_CONSERVATION
CHECK_ID=R9_ORACLE_V2_SINGLE_CAUSE_CERTIFICATE_ALLOCATION
EXPECTED=CERTIFICATE_PROVENANCE_MISMATCH
ACTUAL=RESERVE_MISUSE
```

Oracle V2 и frozen fixtures не изменялись. Требуется отдельное административное переоткрытие qualification contract.
