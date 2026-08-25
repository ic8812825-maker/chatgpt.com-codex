# HSB.2E-PREP-R4-R9-R2 — остановка на проверке Native Economic Oracle

```text
HSB.2E_PREP_R4_R9_R2=BLOCKED_OR_FAILED
ORACLE_REOPENING_REQUIRED=YES
MODEL_CHANGES_ALLOWED=NO
PASS_DECLARATION_ALLOWED=NO
IMPLEMENTATION_HANDOFF=NOT_READY
TRADING_LOGIC_START_ALLOWED=NO
REAL_TRADING_ALLOWED=NO
```

После immutable commit Economic Oracle обнаружена несогласованность `R9_*_CERTIFICATE_FORGERY`: fixture отличается от положительной только metadata-полем `kind=CERTIFICATE_FORGERY`, но persisted certificate/source records не подделаны. Builder объявляет `REJECT` по `kind`, а native engine не имеет права ветвиться по test metadata. Ожидаемое невозможно получить из нормативного transaction input.

```text
CHECK_ID=R9_NATIVE_CERTIFICATE_FORGERY_FIXTURE_COMPLETENESS
EXPECTED=fixture contains an independently forged persisted source/certificate relation
ACTUAL=only kind metadata marks forgery; certificateDigest remains empty and no source digest is altered
```

В соответствии с stop rule immutable fixtures/oracle не изменялись после начала следующей фазы. Требуется отдельное административное переоткрытие Oracle.
