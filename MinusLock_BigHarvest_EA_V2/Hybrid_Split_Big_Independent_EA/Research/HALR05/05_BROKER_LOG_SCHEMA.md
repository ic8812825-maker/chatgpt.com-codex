# Формат брокерского журнала

Локальный CSV/JSON с timezone timestamp, order_id и deal_id, направлением BUY/SELL, requested_lots, filled_lots, requested_price и execution_price. События SEND, ACK, FILL, REJECT, CANCEL_SENT, CANCEL_ACK, UNKNOWN, RESTART, RECONCILE, SWAP. FILL может быть частичным. Подтверждённый остаток сохраняется при UNKNOWN и после RESTART. Снимок RECONCILE не заменяет отсутствующий deal. Сделки дедуплицируются; late fill до подтверждения отмены учитывается. Комиссия и swap — подписанные денежные поля. Времена с одинаковой меткой идут в исходном порядке. Имена счёта, токены и пароли не нужны.

Send→fill и signed slippage измеряются для подтверждённых сделок, с цензурированием отказов. Максимальный наблюдённый объём не даёт гарантии будущей ликвидности. Импортёр работает без сети.
