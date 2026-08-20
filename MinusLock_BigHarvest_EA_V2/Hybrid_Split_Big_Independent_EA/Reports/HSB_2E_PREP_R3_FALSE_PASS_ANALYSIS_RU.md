# PREP-R2 semantic false PASS

Во временной fixture первая formula получила `VARIABLES=["banana"]` и бессмысленные example objects. `verify_hsb_2e_prep_r2.py --skip-integrity` вернул 120/120, `FORMULA_CONTRACTS=PASS`, `RESULT=PASS`, exit 0. Причина: R2 проверял форму и непустоту, но не исполнял expression/reference и не сравнивал immutable expected output.

```text
PREP_R2_FALSE_PASS_REPRODUCED=YES
FALSE_PASS_CLASS=NON_EXECUTABLE_FORMULA_ACCEPTED
```
