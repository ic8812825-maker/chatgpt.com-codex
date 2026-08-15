# HSB.2C-R1-P1: publication contract

Publication metadata append-only. Исторический transport `dcafb222081dfef6686275fb32d8c7ffa0c60d59` не является текущим HEAD. Remote baseline P1: `42c4d418bdd9cb56785cffee4b5abc0221c2974b`.

Различаются: содержательный commit, commit записи публикации и проверенный post-push tip. SHA записи не может самоссылочно содержать собственный SHA; поэтому каждая запись подтверждает уже опубликованный предшествующий tip, а новый tip подтверждается следующей append-only записью и внешней GitHub API проверкой. История не переписывается, push только normal.
