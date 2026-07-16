# Historical tests

These source-assertion tests describe superseded architecture and are retained for audit, not collected by pytest.

- Reserve idempotency tests expected the removed `ReserveEventAlreadyApplied(eventKeyHash)` API. Active replacements: `reserve_ledger_credit_debit_check.py`, `reserve_apply_once_check.py`, and `test_reserve_ledger_idempotency.py` coverage is superseded by transaction/ledger persistence checks.
- `test_restart_recovery` expected the old per-row EventKeyHash persistence spelling; active recovery checks cover the current split high/low model.
- `test_split_geometry_blocked_until_full` expected a compile-time feature guard removed when Split was implemented; active split architecture and scenario tests replace it.

No assertion was weakened or deleted; original files are preserved with `.historical.py` suffix so pytest does not import obsolete module-level assertions.
