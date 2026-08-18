# Evidence integrity R2

S046E требует точный набор из семи sealed files и проверяет SHA-256 каждого. Seal не включает себя. Обычные запуски не пишут tracked evidence; публикация требует `--publish-evidence`/explicit outputs. M101–M103 изменяют sealed evidence либо seal и обязаны дать S046E FAIL при S045 PASS.
