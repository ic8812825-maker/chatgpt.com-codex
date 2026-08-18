# Архитектура reachability/dominance proof R3

Verifier извлекает только требуемую функцию из comment/literal/preprocessor-filtered ACTIVE_CODE. Затем разбирает top-level compound body, связывая один узел `if(condition)` с его непосредственной true-ветвью `return HSBI_RuntimeReject(args)`.

PASS требует exact condition, exact argument positions status/reason, top-level reachability и отсутствие предшествующего unconditional top-level return. Guards внутри `if/while/for`, optional blocks и unused helpers имеют depth > 0 и не являются candidates. Unsupported structure даёт FAIL.
