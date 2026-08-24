# R4-R4: анализ новых ложных PASS

На baseline R4-R3 воспроизведены 9/9 дефектов: zero position settlement, off-grid volume, negative price, строковый confirmed, multiple intents, negative revision, потеря partial registry, non-bijective persisted binding и неправильные registry types.

Первопричина — сокращённая R4-R3 модель не сохранила primitive/grid контракты R4-R2 и не реализовала настоящий persisted partial/restart lifecycle. R4-R4 устраняет дефекты монотонным объединением требований.
