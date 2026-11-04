# 02B-R0D — независимое воспроизведение R0C

База `ec7ae40fe22e1d6e5bed035450750502a1162ab5`. Изменялись только disposable reference copies. Production и исторические тесты не менялись.

| FindingID | Факт | Independent expected | Статус |
|---|---|---|---|
| R0D-01 | R0C worst: Available1e28, Loss.010, Buffer9999999999999999999999999999.995 => ALL_LEVEL_POSITIVE,+.005 | Integer coefficient/scale calculation =>−.005, REJECT | CONFIRMED |
| R0D-02 | R0C sequential1e28 с двумя расходами.01 сохраняет исходный остаток и сообщает CONSERVATION_ONLY | Integer hundredths:10^30−2; итог9999999999999999999999999999.98 | CONFIRMED |
| R0D-03 | Snapshot string"1"→Decimal1, receipt не меняется; canonical равен, commit Remaining40/revision2 | Поддерживаемые разные типы нельзя случайно отождествлять; тип поля требует schema decision | CONFIRMED encoding collision; SCHEMA_DECISION_REQUIRED |
| R0D-04 | Четыре weakened R0C copies дают221PASS и принимают свои запрещённые случаи | Negative amount/locked funds/off-grid post/unverified policy должны отвергаться | CONFIRMED |

R0D-01 positive control margin29 проходит. Высокая Decimal precision старого worst даёт−.005, но это только наблюдение: expected построен отдельно integer arithmetic, не повторным evaluator. Все значения входят в заявленный numeric domain R0C, currency fixture KWD precision3.

Для R0D-03 None/empty/bool/int/dict исследованы отдельно: frozen string receipt даёт CONFLICT; self-consistent fixture receipt может дать commit. Без прежней явной схемы это SCHEMA_DECISION_REQUIRED, не автоматически пять дефектов и не broker provider bypass.

Original R0C amount−10 отвергается, mutant допускает Remaining60/Consumed−10. Remaining50/Reserved45/amount10: original REJECT, mutant Remaining40/Reserved45. Posted1.005/digits2: original UNAVAILABLE, mutant POSTED. LOCAL_VERIFIED с flagFalse: original UNAVAILABLE, mutant POSTED. В каждом случае old221 suite продолжает PASS. Это coverage gap, а не утверждение, что оригинал разрешал отрицательное списание.

Точные source edits/hashes/controls/outcomes в `Tests/Evidence/NEXT_STAGE_02B_R0D_REPRODUCTION.json`; producer `check_hsbi_02b_r0d_mutations.py:reproduction`. Frozen functions: R0C worst:294, sequential:311, canonical:33/context_shape:167. Новая verification matrix отделяет OLD_MODEL_FINDING от NEW_REFERENCE_FIXTURE и EXTERNAL_NOT_PROVEN.
