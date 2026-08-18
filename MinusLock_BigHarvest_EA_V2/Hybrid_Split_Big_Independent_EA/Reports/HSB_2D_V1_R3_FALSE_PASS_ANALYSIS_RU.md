# Анализ ложных PASS R3

## A: unreachable guard
R2 подтверждал presence внутри функции, но `if(false){guard}` не доминирует success. R3 принимает только exact top-level `if` с непосредственно связанным `return HSBI_RuntimeReject`, точным status/reason и без предшествующего top-level return.

## B: comment/preprocessor order
R2 искал directives до comments. R3 сначала маскирует literals/comments, затем распознаёт directives только на физически активных строках. Поэтому `#else` внутри `/* */` не меняет `#if 0` state.

```text
M104_EXPECTED=S028
M110_EXPECTED=S028
PRODUCTION_MQL5_CHANGED=NO
```
