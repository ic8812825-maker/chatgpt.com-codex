# Финальная offline-приёмка HSB.2D-V1

Baseline и scope подтверждены. Include graph/guards, no-trade, T01–T464, runtime decision, restart, transaction barrier, money/allocation/consumption/persistence, документация, negative fixtures и user handoff проверены статически.

Verifier должен быть запущен из project root и из `Tests/Static`; полный финальный вывод хранится в `Tests/Evidence/HSB_2D_V1_OFFLINE_VERIFICATION_RESULT.txt`.

```text
HSB.2D_STATIC_IMPLEMENTATION=PASS
HSB.2D_OFFLINE_VERIFICATION=PASS
HSB.2D_METAEDITOR_VERIFICATION=PENDING_USER
METAEDITOR_COMPILE=NOT_EXECUTED_MT5_UNAVAILABLE
MQL5_RUNTIME_TESTS=NOT_EXECUTED_MT5_UNAVAILABLE
BROKER_MONEY_RUNTIME_PROOF=NOT_EXECUTED_MT5_UNAVAILABLE
HSB.2E_START_ALLOWED=NO
TRADING_LOGIC_START_ALLOWED=NO
REAL_TRADING_ALLOWED=NO
NEXT_ALLOWED_STAGE=HSB.2D-V2_USER_METAEDITOR_VERIFICATION
```

Open P0/P1 статического этапа: 0. MT5/MetaEditor unavailable остаётся обязательным runtime blocker, а не дефектом offline-пакета.
