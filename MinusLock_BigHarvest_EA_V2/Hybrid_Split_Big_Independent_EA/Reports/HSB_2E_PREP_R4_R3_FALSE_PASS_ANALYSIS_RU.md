# Анализ шести ложных PASS R4-R2

На точном baseline воспроизведены 6/6 контрпримеров: повторный `dealId` с другим event, устаревший deal timestamp, чужой intent, чужая managed position, отсутствие Small leg в Big и full-close request меньше authoritative position volume.

Первопричина: R4-R2 связывал deal лишь с частью context/position и не доказывал независимые position/context, intent/context, intent/position, deal/intent bindings, уникальность deal/event по отдельности, временное окно, обязательные role multiplicities и authoritative full-close volume.

`FALSE_PASS_REPRODUCTION=PASS`; полные входы, actual результаты и SHA-256 сохранены в evidence JSON.
