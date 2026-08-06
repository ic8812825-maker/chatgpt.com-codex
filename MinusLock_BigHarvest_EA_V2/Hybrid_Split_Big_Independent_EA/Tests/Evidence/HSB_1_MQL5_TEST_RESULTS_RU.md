# Результат MQL5 unit tests HSB.1

```text
MQL5_UNIT_TESTS=NOT_RUN_ENVIRONMENT_UNAVAILABLE
```

MT5 и MetaEditor в доступной среде отсутствуют. PASS не объявляется. Создан `Tests/MQL5/HSBI_Skeleton_Tests.mq5` с 26 тестами:

1. enum uniqueness;
2. runtime mode validation;
3. real mode rejection;
4. identity validation;
5. SameCycle;
6. ownership mismatch;
7. one Far;
8. duplicate Far reject;
9–12. role promotion и actual BigCore source;
13–14. FSM transitions;
15–17. PLACED/PARTIAL/TIMEOUT barriers;
18–20. allocation conservation и Reserve isolation;
21. NewFar tie-break;
22. snapshot schema;
23. revision monotonicity;
24. reconciliation;
25. no-trade guard;
26. запрет real trading.

Каждый тест выводит TEST_ID, Requirement ID, Expected, Actual и PASS/FAIL. Для будущего evidence необходимо запустить скрипт в MT5 и сохранить Experts log, Journal и итог `HSBI_TEST_SUMMARY`.