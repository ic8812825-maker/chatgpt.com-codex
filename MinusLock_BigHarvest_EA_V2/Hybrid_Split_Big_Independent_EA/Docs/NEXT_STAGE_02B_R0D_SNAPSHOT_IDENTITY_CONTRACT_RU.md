# 02B-R0D — PROPOSED схема snapshot до выбора encoder

База `ec7ae40fe22e1d6e5bed035450750502a1162ab5`. SCHEMA_DECISION_REQUIRED / AWAITING_ADMIN_APPROVAL. Не универсальный broker fingerprint и не production codec.

## SNAP-FIXTURE-1

Все поля обязательны, неизвестные extra fields запрещены.

| Поле | Тип/допустимость | Семантика и identity | Authority |
|---|---|---|---|
| schemaVersion | exact str `HSBI-SNAPSHOT-FIXTURE-1` | Версия полного payload | Independent fixture provider |
| id | exact int1..2^64-1, bool запрещён | Snapshot ID, связан с expected/request | Immutable context mapping |
| validUntil | exact int>=0 | Inclusive endpoint fixture tick | Provider receipt |
| clockDomain | exact str `FIXTURE_MONOTONIC` | Только fixture clock; другой domain UNAVAILABLE | Provider clock metadata |
| timeUnit | exact str `tick` | Без guessed seconds/UTC conversion | Provider clock metadata |
| marketFingerprint | exact nonempty str; None — явный unknown | Opaque fixture tag, участвует в полном content identity | Независимый frozen snapshot receipt |

Missing field/wrong type/empty fingerprint =>REJECT; fingerprint=None =>UNAVAILABLE; unknown schema/domain/unit =>UNAVAILABLE. Ни presence, ни caller boolean не подтверждают source.

Typed canonical tokens различают string "1", integer1, boolTrue, numeric Decimal1, None/missing и list/tuple. Для marketFingerprint допускается только строка: остальные типы отвергаются до сравнения receipt; None не становится fingerprint. Decimal1/Fraction1 — одинаковое numeric value только в numeric-typed DTO, не строка. Extra field не игнорируется.

Независимый receipt = typed canonical encoding полного первоначального snapshot. Отрицательный content test меняет только snapshot; receipt не пересчитывается. ID объекта/request/expected должны совпасть; receipt по ID обязан существовать. Same ID/changed legal content =>CONFLICT. Предъявленный proof или self-consistent snapshot не создаёт registry/history.

В R0C marketFingerprint type не определён явно, поэтому acceptance None/пустых/других типов сначала SCHEMA_DECISION_REQUIRED; доказанная string/Decimal encoding collision отделяется от объявления универсальной брокерской схемы. Новый профиль становится действующим нормативом только после explicit approval.
