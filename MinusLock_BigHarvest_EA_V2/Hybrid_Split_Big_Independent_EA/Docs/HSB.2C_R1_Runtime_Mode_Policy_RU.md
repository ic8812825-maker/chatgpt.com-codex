# HSB.2C-R1 — runtime mode policy

`UNSPECIFIED` fail-closed. `UNIT_TEST` допускает injected fixtures исключительно в solver tests, но NewFar production selection/preflight/completion их не принимают. `PRODUCTION` и `SHADOW` запрещают injected proof; `ADMIN_VERIFICATION` принимает только фактически прочитанный terminal outcome. Торговый dispatch отсутствует во всех режимах.
