# R1.1 — неприменённые patch proposals

BASE_SHA=398da88424f3fb7b30e5315fbc3bf89219dd9ad2. Все diffs **PROPOSED, UNAPPLIED, PARTIAL PoC**, не готовое полное исправление пакета. Production не изменяется.

- `Tests/Close/patches/A_identity.patch` — R1.1-A. PoC сравнивает существующий полный payload; account/server/schema в legacy record отсутствуют. Поэтому этот diff НЕ является полным исправлением A.
- `Tests/Close/patches/B_allocation.patch` — R1.1-B. PoC устраняет vector-only equality gap и negative/nonfinite buckets. Source registry, lifecycle и durable consumption потребуют отдельно reviewed additive provider interface; production backend не реализуется в R1.1.
- `Tests/Close/patches/C_numeric.patch` — R1.1-C. PoC finite guards только в трёх headers. Все перечисленные domain/caller tests обязательны для acceptance; это не готовый полный numeric fix.
- `Tests/Close/patches/D_binding.patch` — R1.1-D. PoC только public scalar binding и output finite. Full provenance/spendability нельзя получить локальным equality; provider отсутствует → funding unavailable.
- `Tests/Close/patches/E_retry.patch` — R1.1-E. PoC блокирует UNKNOWN/TIMEOUT retry. Не создаёт durable storage или full FSM и не доказывает loss bound ERR-038. Торговая интеграция исключена.

Diffs привязаны к exact base. `git apply --check` проверяет только применимость текста, не MQL compile, runtime correctness или утверждение денежной политики. Сейчас production остаётся прежним. C и E затрагивают один header: последовательное применение требует recomposition E на базе C без потери finite guard и отдельного review. Каждая patch проверена отдельно на BASE, не как бесконфликтная серия.

Порядок будущей работы: owner утверждает формулировки и ограниченный allowlist; устранить audit gaps для затронутых clauses/callers; составить полный versioned diff с providers unavailable по умолчанию; независимый review; только затем отдельное разрешение реализации, native testing и acceptance. PoC A не решает новый namespace; B не создаёт глобальный registry; D не подтверждает broker provenance; E не создаёт journal backend. Автоматически применять эти файлы запрещено в текущем задании.
