# R4: анализ условного раннего success

R3 ошибочно приравнивал наличие exact guard к dominance. Контрпример M124
возвращал `valid=true` по условию mismatch до S028 и оставлял штатный guard
физически неизменным. R4 перечисляет каждый `return` в префиксе guard,
классифицирует присваивания `.valid=true`, `.status=HSBI_DECISION_VALID`,
valid-status constructor и неизвестные helpers. Любой такой путь даёт
`GUARD_ON_ALL_SUCCESS_PATHS=false` и `DOMINATES_SUCCESS=false`.

M124_EXPECTED=S028
M124_MANIFEST=PASS
M124_EXPECTED_RESULT=CAUGHT
