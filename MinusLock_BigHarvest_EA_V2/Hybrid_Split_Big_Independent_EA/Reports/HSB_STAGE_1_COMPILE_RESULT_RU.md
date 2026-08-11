# HSB.1V — фактический результат MetaEditor compile

Дата попытки: `2026-08-10T11:04:58Z`.

## Поиск среды

Выполнены `command -v metaeditor64`, `command -v metaeditor`, `command -v terminal64`, `command -v wine`, а также ограниченный поиск `metaeditor*`, `terminal64*`, `metatester64*` в `/opt`, `/usr`, `/workspace`. Исполняемые MetaEditor, MT5 Terminal и Wine не найдены. Build MetaEditor: `UNAVAILABLE`.

Компиляция обоих targets фактически запланирована, но не могла быть запущена в данной среде. Сторонний parser и Python как заменитель не использовались; compile log отсутствует по причине отсутствия компилятора.

| Target | SHA-256 | Результат |
|---|---|---|
| `Hybrid_Split_Big_Independent_EA.mq5` | `2f58dfc9d8a35d9e90de1b7d61324f1a7a08cc6e403d5b49cd5d71556ea20f4a` | NOT_RUN_ENVIRONMENT_UNAVAILABLE |
| `Tests/MQL5/HSBI_Skeleton_Tests.mq5` | `868f60a9acc8b8c3a72fe7650780cb235eb4525bd20b88be1313327cac11cb1f` | NOT_RUN_ENVIRONMENT_UNAVAILABLE |

```text
METAEDITOR_COMPILE=NOT_RUN_ENVIRONMENT_UNAVAILABLE
METAEDITOR_COMPILE=NOT_RUN_ENVIRONMENT_UNAVAILABLE
COMPILE_RESULT=NOT_RUN_ENVIRONMENT_UNAVAILABLE
ERRORS=NOT_AVAILABLE
WARNINGS=NOT_AVAILABLE
```

`PASS` и требование `0 errors / 0 warnings` не объявляются без фактического MetaEditor log.
