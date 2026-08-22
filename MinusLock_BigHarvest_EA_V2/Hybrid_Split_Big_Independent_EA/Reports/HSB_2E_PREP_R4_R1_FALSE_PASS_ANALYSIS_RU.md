# PREP-R4-R1: ложный PASS mutation oracle

В полной временной fixture строка BUY close `Bid` заменена на `Ask`. Исторический полный PREP-R4 verifier вернул `CHECKS_FAILED=0`, `T465_T1149_PASS=685`, `RESULT=PASS`, exit 0.

```text
PREP_R4_FALSE_PASS_REPRODUCED=YES
FALSE_PASS_MUTATION=BUY_CLOSE_SIDE_BID_TO_ASK
FULL_VERIFIER_EXIT=0
MUTATION_SURVIVED=YES
ROOT_CAUSE=MUTATION_SEMANTIC_DIFF_USED_AS_CAUGHT_RESULT
```

R1 принимает code mutation только при ненулевом exit полного verifier и наличии ожидаемого Check ID.
