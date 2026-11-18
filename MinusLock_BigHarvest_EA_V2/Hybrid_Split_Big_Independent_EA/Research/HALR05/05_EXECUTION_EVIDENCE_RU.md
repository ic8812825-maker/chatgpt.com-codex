# Свидетельства исполнения

Подтверждённых анонимизированных брокерских журналов среди входов и закреплённых исследований нет. EXECUTION_EVIDENCE=MODEL_ONLY; BROKER_FILL_EVIDENCE_UNAVAILABLE. Нет калибровки capacity, задержки, hedged margin или stop-out реального брокера.

QUOTE_FILL использует наблюдаемый Bid/Ask и предполагаемую общую capacity 1000 единиц на событие без задержки. BOUNDED_SLIPPAGE добавляет 2 points на fill. DELAYED_PARTIAL и COMPOUND_STRESS — точные соответствующие режимы HALR-04. DELAY_ONLY/PARTIAL_ONLY и REJECT_ONLY/UNKNOWN_ONLY — диагностические выключения отдельных факторов разрешённых семей. REJECT_UNKNOWN и LOW_LIQUIDITY заданы в предрегистрации. Цена и подтверждение сделки принадлежат событию фактического fill. Нельзя считать отправленную заявку закрытием. Модели общие для всех политик, без подбора под отложенные результаты.
