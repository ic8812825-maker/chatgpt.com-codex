# Синхронизация полного системного мануала HSB.0R

Нормативное дополнение к `Docs/03_FULL_SYSTEM_MANUAL_RU.md`. При расхождении применяется `Docs/23_NORMATIVE_DECISIONS_RESOLUTION_RU.md` и evidence HSB.0R.

Закреплено без альтернатив по усмотрению программиста: Hybrid-only runtime; ratios через broker-normalized gates; configurable allocation с conservation; единые control prices; recursive Future Small; minimum-safe NewFar; отдельная Emergency Liquidation; transition loss caps; money Final Close threshold; fail-closed margin/drawdown; one cycle per symbol; file-based persistence; REAL_LIMITED contract.

Полный lifecycle: IDLE→Initial plan/actions→actual lock→actual plus close→FAR→CandidatePlan→actual C/T/S basket→Big Harvest→allocation→Partial Far или единственный Final Close; либо confirmed Small trigger→persist plan→actual closes S/F/T→actual Core reduction→actual residual Core=NEW_FAR→reconciliation→new FAR cycle.

BUY/SELL полностью зеркальны по ролям, но broker money всегда использует BUY close Bid и SELL close Ask. Необратимые действия выполняются только Plan→Persist Action→Request→OnTradeTransaction→fills→actual state→ledger→persist→FSM advance.

Emergency не считается recovery; after critical error auto-resume запрещён. Production profile, real defaults и trading code на HSB.0R отсутствуют.
