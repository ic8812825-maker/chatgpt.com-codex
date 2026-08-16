# HSB.2D — финальный static audit

```text
TEST_RANGE=T01-T464
DECLARED_TESTS=464
NO_GAPS=YES
NO_DUPLICATES=YES
FORBIDDEN_TRADE_CALLS=0
LINEAR_SHORTCUTS=0
FILES_OUTSIDE_SCOPE=0
METAEDITOR_COMPILE=USER_VERIFICATION_REQUIRED
MQL5_RUNTIME_TESTS=USER_VERIFICATION_REQUIRED
BROKER_MONEY_RUNTIME_PROOF=USER_VERIFICATION_REQUIRED
```

T455–T464 дополняют restart coverage: valid recovery, revision/plan/ticket/volume mutation, reused source, duplicate NO_OP, conflicting payload, missing snapshot и pending conflict.
