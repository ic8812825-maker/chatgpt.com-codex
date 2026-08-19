# R4: mutation audit

Каталог содержит непрерывный обязательный диапазон M001--M135. Размер suite
вычисляется из записей с `required=true`; runner сравнивает required, executed и
caught ID sets. M101--M103 вновь обязательны. M124--M135 проверяют conditional
success, неизвестные returns, persistence/digest bypass, reject constructor и
множественные success paths. Итоговые числа публикуются только из реального
end-to-end прогона.
