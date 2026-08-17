# Traceability matrix HSB.2D-V1

| Requirement ID | Требование | Реализация/доказательство | Static check | Negative fixture | Статус |
|---|---|---|---|---|---|
| HSBI-2D-V1-SCOPE | Только project root | verifier path/symlink/git scope | S001,S002,S048 | outside_scope | PASS |
| HSBI-2D-V1-BASELINE | Точный baseline | pre-audit + Git evidence | manual Git | — | PASS |
| HSBI-2D-V1-INCLUDE | Полный безопасный граф/guards | include JSON/report | S005–S009 | external/missing/cycle/guard | PASS |
| HSBI-2D-V1-NO-TRADE | Нет dispatch/side effects | disabled no-trade stub | S016–S022 | OrderSend,CTrade | PASS |
| HSBI-2D-V1-TEST-ID | T01–T464 | harness audit | S011–S015 | missing/duplicate | PASS |
| HSBI-2D-V1-DECISION | Fail-closed decision | runtime audit | S023,S026–S039 | revision/ownership | PASS |
| HSBI-2D-V1-RESTART | Restart/idempotency | restart audit | S024,S027–S039 | persistence | PASS |
| HSBI-2D-V1-BARRIER | Pre-advance barrier | barrier audit | S025,S028–S039 | persistence | PASS |
| HSBI-2D-V1-MONEY | Actual broker proof | money audit | S032–S036 | ownership | STATIC PASS; RUNTIME PENDING_USER |
| HSBI-2D-V1-ALLOCATION | Conservation/consumption | money audit | S036,S037 | persistence | PASS |
| HSBI-2D-V1-PERSISTENCE | Prepared + digest | runtime contracts | S038,S039 | persistence removed | PASS |
| HSBI-2D-V1-DOCUMENTATION | Честный canonical status | 7 status docs | S040–S044 | false status x3 | PASS |
| HSBI-2D-V1-MANIFEST | SHA-256 | file manifest | S045 | hash mismatch supported | PASS после финального запуска |
| HSBI-2D-V1-HANDOFF | MetaEditor/MT5 инструкция | user verification doc | file/status checks | false runtime status | PASS |
| HSBI-2D-V1-PUBLICATION | Fast-forward + parity | publication record | Git post-push | outside_scope | PENDING до публикации |

`METAEDITOR_COMPILE`, `MQL5_RUNTIME_TESTS` и broker runtime proof не получают PASS без пользовательских журналов.
