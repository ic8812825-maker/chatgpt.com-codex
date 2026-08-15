# HSB.1V — фактический результат MetaEditor compile

Дата попытки: `2026-08-11T11:26:28Z`.

Выполнены без подмены компилятора:

```bash
command -v metaeditor64
command -v metaeditor
command -v wine
find /opt /usr /workspace -maxdepth 5 -type f \( -iname 'metaeditor64*' -o -iname 'metaeditor*' \) -print
```

Все команды поиска вернули пустой результат. MetaEditor и Wine недоступны, поэтому запустить компиляцию невозможно. Python, сторонний parser, ручной syntax review или иной компилятор не использовались как evidence.

| Target | SHA-256 | Фактический результат |
|---|---|---|
| `Hybrid_Split_Big_Independent_EA.mq5` | `2f58dfc9d8a35d9e90de1b7d61324f1a7a08cc6e403d5b49cd5d71556ea20f4a` | NOT_RUN_ENVIRONMENT_UNAVAILABLE |
| `Tests/MQL5/HSBI_Skeleton_Tests.mq5` | `8d7a691bc7b9de688a9f73d2f456bfdeddea0cc5f4699804aba74d519ab93e6c` | NOT_RUN_ENVIRONMENT_UNAVAILABLE |

```text
METAEDITOR_BUILD=UNAVAILABLE
METAEDITOR_COMPILE=NOT_RUN_ENVIRONMENT_UNAVAILABLE
ERRORS=NOT_AVAILABLE
WARNINGS=NOT_AVAILABLE
```

Compile PASS и `0 errors / 0 warnings` не заявляются; compile logs отсутствуют именно из-за отсутствия MetaEditor.
