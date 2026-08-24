# PREP-R4-R2: анализ четырёх ложных PASS

Историческая R4-R1 модель воспроизвела `PASS` для недостаточных Big fills `0.01/0.01`, partial winner fill Initial Lock `0.01`, partial Small/Old Far fills `0.01/0.01` и отрицательного deal volume `-1`.

Первопричина: `net_deals()` проверял identity и money, но не доказывал cumulative volume против requested intent, не требовал `volume > 0` и volume-grid alignment. Поэтому money ошибочно использовался как достаточное доказательство исполнения.

`FALSE_PASS_COUNTEREXAMPLES_REPRODUCED=4/4`. Полные requested/deal volumes, historical actual, expected, source SHA и exit сохранены в JSON evidence.
