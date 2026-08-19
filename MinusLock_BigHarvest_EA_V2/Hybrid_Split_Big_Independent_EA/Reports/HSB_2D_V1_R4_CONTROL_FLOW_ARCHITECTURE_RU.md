# R4: архитектура control-flow proof

Анализ выполняется над comment/literal/preprocessor-aware active token stream.
Для каждого S023--S039 строится связанная запись function → top-level if →
immediate reject → status → reason. До позиции guard безопасными считаются
только уже доказанные immediate `return HSBI_RuntimeReject(...)`. Остальные
returns имеют fail-closed семантику; признаки valid-result считаются success.

Отдельные доказательства проверяют constructor `HSBI_RuntimeReject`, единственный
final success, его top-level положение и нахождение после всех обязательных
guards. Неподдерживаемый control flow означает FAIL, а не оптимистичный PASS.
