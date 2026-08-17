# Аудит Restart Validator HSB.2D-V1

Проверены snapshot presence/schema/identity/digest, plan/revision/event/action, неизменность history, source reuse, duplicate consumption, payload conflict, pending action, broker-money/reconciliation, persisted residual identifier/ticket/volume/role/direction и allocation/consumption digests. Duplicate с тем же persisted contract даёт идемпотентный `NO_OP`; конфликт и неизвестное состояние блокируются.

`actualVolume` сравнивается точно. Контракт HSB.2D хранит уже broker-grid-normalized volume в snapshot и требует бит-в-бит детерминированное представление; тест T459 доказывает блокировку изменённого volume. Произвольный epsilon не добавлялся. Повторная сериализация с иной двоичной формой остаётся fail-closed и требует reconciliation; grid-aware изменение требует отдельного нормативного решения с `SYMBOL_VOLUME_STEP`.

`RESTART_STATIC_AUDIT=PASS`; runtime serialization не выполнялась.
