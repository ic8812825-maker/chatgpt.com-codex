# C2 — предлагаемый контракт вложенных DTO

BASE_SHA=fae7dfc18ca2d61af2f3446826ef3031825bbfd8

PROPOSED / AWAITING_ADMIN_APPROVAL. Арифметика R0D неизменна. Денежные и wire schemas C1/R0E сохраняются; новый validation profile HSBI-C2-SCHEMAS-1 задаётся отдельным inventory. Это не утверждение экономической политики.

Исполнимый первичный schema inventory: Tests/Reference/hsbi_02b_r0e_c2_schemas.py:M. Его точная JSON-проекция — Tests/Contracts/NEXT_STAGE_02B_R0E_C2_DTO_SCHEMAS.json. Для каждого поля указаны обязательность, тип/диапазон, nullable, единицы, identity participation, provider boundary и результат ошибки. Unknown fields отвергаются, extension-пространства в профиле нет.

Bool не integer. Account: int 1..2^63−1; Magic: signed int64 nonzero; ulong identities: int 1..2^64−1. Money: frozen R0D number domain, без float/bool. Digits: R0D 0..8; неизвестная precision/domain UNAVAILABLE. Unknown schema/operation UNAVAILABLE. Missing required field, неверный тип/enum — Malformed; authorize/apply REJECT, recovery/available/batch/cost CONFLICT. Authority=None или nullable unavailable provider возвращает UNAVAILABLE. Присутствующий malformed объект не превращается в unknown fact.

Полная вложенная shape validation перед lookup/hash/изменением — обязательная часть публичных proof API. Trusted provider не освобождает DTO от проверки схемы. Request identity полностью typed до replay; неполная identity теперь REJECT, а не исторический C1 CONFLICT: это явное уточнение синтаксического приоритета, не изменение экономики. Валидный изменённый replay остаётся CONFLICT.

Текущие nullable provider containers могут отсутствовать как факт (None) для исторического replay; missing key остаётся malformed. Valid изменившиеся current Plan/Revision/Snapshot не отменяют exact исторический NO_OP. Новое событие всегда проверяет текущие mandatory gates. Receipt digest/equations и source reconciliation проверяются независимо от формы DTO.

Неожиданные RuntimeError/ошибки реализации не перехватываются blanket except. Harness показывает INFRASTRUCTURE_ERROR. Mathematical helpers не являются consumption authorization; публичные proof API: authorize, apply_for_test, available, assess_batch, cost_coverage, verify_allocation_identity, recover_store. Конструкторы snapshot/new_store не удостоверяют provenance.

Область схем — конечные деревья DTO с глубиной меньше48; arbitrary Python object graphs не являются wire DTO. Все обязательные C2 JSON artifacts читаются strict loader до семантической проверки. TestedSHA в evidence — Git HEAD базового рабочего дерева при запуске; новые C2 sources однозначно задаются SourceHashes и последующим опубликованным commit, без невозможного self-referential final hash.
