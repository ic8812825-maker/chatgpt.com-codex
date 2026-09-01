# HSB.2E-PREP-R4-R9-R4A-R5 — результат исправления

## Результат

Исправленный, версионированный R5-контур schema и positive bases прошёл вычисляемую приёмку. Исторические R4/R4-AUDIT artifacts сохранены. Это не Oracle freeze и не доказательство полной экономической корректности.

## Дефект аудита → исправление → воспроизводимый тест

| Дефект R4 | Исправление R5 | Исполнимый тест |
|---|---|---|
| 64 нуля принимались как certificate digest | Канонический пересчёт собственного digest без поля `digest` | `CERT_ZERO_DIGEST`, `CERT_BODY_CHANGED` |
| Не было phase applicability | Явное `phase=PRE_COMMIT/COMMITTED/REPLAY`; certificate forbidden/required по phase | `VALID_PRECOMMIT_NO_CERT`, `CERT_MISSING_COMMITTED`, `PHASE_DOWNGRADE_WITH_EVIDENCE` |
| Claims не связывались с sources | Пересчёт broker/economic/allocation/persistence/FSM/output/identity digests и revisions | `CERT_CLAIM_RESEALED`, `CERT_OTHER_OPERATION` |
| Far ticket указывал на не-FAR position | Явный active Far, unique owned FAR position, volume/direction binding; inactive Far без фиктивных полей | `FAR_FOREIGN`, `FAR_DUPLICATE`, 24 runtime validations |
| LIFECYCLE был одним переходом | Четыре sequence containers с 11 шагами и полным state-object continuity | lifecycle validation всех четырёх chains |
| `KeyError`/`TypeError` засчитывались как CAUGHT | `NormativeError(checkId, reason, inputPath)` отделён от `INFRASTRUCTURE_ERROR` | `HARNESS_KEYERROR`, `HARNESS_TYPEERROR` |
| Варианты различались главным образом metadata/scalars | Вычисляемые min-volume/cost, nontrivial tick/multi-fill, recovery edge, phases, persistence и lifecycle-chain cases | acceptance `coverageTable` и `DIVERSITY` |

## Объём

- 28 верхнеуровневых fixtures: 6 runtime-групп × 4 и 4 lifecycle containers.
- 11 связанных lifecycle steps.
- Phase coverage: `PRE_COMMIT`, `COMMITTED`, `REPLAY`.
- 28 regression cases; required и executed вычислены из каталога.
- Normative rejections: 22; wrong failures: 0; unexpected infrastructure errors: 0.
- Два намеренных harness probes корректно классифицированы как infrastructure, но не засчитаны нормативными отказами.

## Certificate proof boundary

SHA-256 доказывает соответствие содержимого заявленному хешу, но сам по себе не доказывает подлинность брокерских данных. R5 доказывает внутреннюю целостность и предусмотренные source bindings, но не защиту от одновременной подмены всех источников и хешей без независимого trusted source.

## Статус

```text
R4A_R4_ACCEPTANCE=REJECTED_BY_AUDIT
R4A_R5_SCHEMA_AND_INTERNAL_CONSISTENCY=PASS
R4A_R5_INDEPENDENT_ACCEPTANCE=PASS
CERTIFICATE_INTERNAL_INTEGRITY=PASS
CERTIFICATE_SOURCE_BINDING=PASS
CERTIFICATE_PHASE_APPLICABILITY=PASS
FAR_ROLE_CONSISTENCY=PASS
LIFECYCLE_DECLARED_CHAIN_VALIDATED=YES
LIFECYCLE_EXECUTED_BY_NATIVE_MODEL=NO
FULL_ECONOMIC_CORRECTNESS=NOT_PROVEN
QUALIFICATION_CORE_READY=NO
ORACLE_V3_CANDIDATE=NOT_YET_FROZEN
MODEL_CHANGES_ALLOWED=NO
TRADING_LOGIC_START_ALLOWED=NO
REAL_TRADING_ALLOWED=NO
```

MetaEditor, MQL5 runtime, Strategy Tester и broker-money runtime proof не запускались. Следующий допустимый шаг — независимый аудит R5; negative qualification fixtures и Oracle freeze пока запрещены.
