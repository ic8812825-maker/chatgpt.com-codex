# 02B-R0C — независимое воспроизведение и findings

База `8903f7ba5d376dc642024ac8ab4400b884466c55`. Только новые R0C artifacts. Все выводы ограничены Python reference API, без production remediation и broker execution.

| FindingID | Независимый результат | Классификация | Новый контракт/тест |
|---|---|---|---|
| R0C-01 | Каждая из четырёх копий без digest/raw sum/posted-state/source identity проходит141 R0B tests и принимает свой запрещённый consumption10 | CONFIRMED, P1 coverage gap | R0C-MONEY; DIGEST-forged, RAW-net-mismatch, POSTED-net-mismatch, RECORD-Magic |
| R0C-02 | snapshot.id999 при request/expected SnapshotID1 допускает COMMITTED_IN_MEMORY, Remaining40, revision2 | CONFIRMED, P1 binding gap | R0C-SNAPSHOT; SNAPSHOT-id/content/unknown |
| R0C-03 | EventTrue и Event2^64 принимаются; после True event1 конфликтует с тем же Python key | CONFIRMED, P2 type/range | R0C-ID; EVENT-invalid-True / ULONG overflow / boundary controls |
| R0C-04 | Missing event/Plan/receipt.posted вызывает исключения; неверные DTO types не имеют единообразного typed outcome | CONFIRMED, P2 boundary | R0C-SHAPE; MISSING-*, SHAPE-*, DTO-type-* |
| R0C-05 | now100/historyObservedAt1000 проходит одностороннюю freshness проверку | CONFIRMED, P2 time consistency | R0C-TIME; TIME-future / boundaries |

Для original четыре отрицательных исхода: REJECT, CONFLICT, CONFLICT, REJECT. Для соответствующих mutants — COMMITTED_IN_MEMORY. Положительные original/mutant controls также COMMITTED_IN_MEMORY. Negative payloads raw/posted/record resealed независимым encoder, чтобы digest не маскировал удалённый guard. Точные edits/hashes/outcomes/state/revision deltas: `Tests/Evidence/NEXT_STAGE_02B_R0C_REPRODUCTION.json#fourMutations`.

Не всякий отрицательный input R0B имеет дефект. False/0/negative event могут корректно отвергаться; matching outcomes отмечены NOT_REPRODUCED **для конкретного контрпримера**, без отмены FindingID в целом. R0B content receipt/clock-domain extras не поддерживаются: там UNPROVEN. Одно отсутствие проверки extra field не объявлено обходом production layer.

Дополнительная гипотеза неправильного regex escaping архивного no-trade scan проверена AST literal и payload OrderSend: NOT_REPRODUCED, старый regex распознаёт token. Новый static scan имеет7 positive/3 negative scanner controls,74 файлов и0 forbidden matches. Это не runtime proof no-trade.

Новая модель устраняет перечисленные reference-boundary gaps только в PROPOSED fixture profile. R0B/production/history не меняются. Изменение внутреннего allocation ID отдельно получает CONFLICT. Origin Plan/Revision/Snapshot могут отличаться от current context — положительный контроль ORIGIN-context-distinct; новая модель не вводит неверное равенство origin/current.

Полный mapping SourceFunction/SourceLine/TestID/MutationID в `Tests/Contracts/NEXT_STAGE_02B_R0C_VERIFICATION_MATRIX.json`. R0B source: `Tests/Reference/hsbi_02b_r0b_independent_oracle.py`, authorize:104, apply_for_test:156. R0C: request_shape, context_shape, record_shape, _authorize, apply_for_test; строки вычислены из текущего AST в matrix.
