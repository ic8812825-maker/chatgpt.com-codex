# Архитектура MQL5 lexer R2

Lexer конечным автоматом разделяет ACTIVE_CODE, comments, string/char literals и disabled preprocessor code. Строки обрабатываются до comment delimiters; незакрытые literals/comments и неоднозначные conditional blocks дают fail-closed `LexerError`. Include guard верхнего уровня сохраняет body активным. L001–L010 вызывают реальные lexer-функции.
