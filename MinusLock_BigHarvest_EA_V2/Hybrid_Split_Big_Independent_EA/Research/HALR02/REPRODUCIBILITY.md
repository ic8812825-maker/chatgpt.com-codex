# Воспроизведение

Из каталога HALR02 запустить на Python 3.11 или новее:

```sh
python -B -m unittest -v
python -B study2.py
python -B audit2.py
python -B render_report.py
```

Прогон содержит поиск параметров и точное дерево. Прямое перечисление малого горизонта встроено в тесты. Точный повтор дерева для сохранённых настроек работает отдельно командой `python -B replay_exact.py`. Matplotlib используется только для диаграммы `python -B budget_plot.py`. Сравнение с опубликованными данными выполняется через `git diff -- '*.csv' '*.json' '*.md'`. Версия Python фиксируется в TEST_RESULTS.json.

Из корня репозитория повтор исходного аудита:

```sh
git fetch origin refs/pull/6/head
BASE=$(mktemp -d)
P=MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Research
git archive 0da896a615b47771d9cf66b6bf7c55cc782b74fc "$P/HALR01" | tar -x -C "$BASE"
(cd "$BASE/$P/HALR01" && python -B -m unittest -q)
python -B "$P/HALR02/audit_baseline.py" "$BASE/$P/HALR01"
python -B "$P/HALR02/audit_ports.py" "$BASE/$P/HALR01"
```

Сценарии по индексам из ADVERSARIAL_RESULTS.csv воспроизводятся функцией scenarios2.stress(horizon). Индекс начинается с нуля. Для адаптивного случая ценовой путь зависит от подтверждённого Net, поэтому общий сценарий задаёт одинаковую функцию противника. Полные журналы выбранных нарушений распаковываются `gzip -dc COUNTEREXAMPLE_JOURNALS.jsonl.gz`. MINIMAL_COUNTEREXAMPLES.json содержит исходные параметры коротких случаев, события и итоговый снимок. Список событий и логика fill опубликованы рядом с кодом. Total Cost в сводках относится к фактически уплаченным новым расходам; полные фактические расходы цикла включают ещё исторические $29 на испытание.

Вся вычисляемая статистика относится к симулятору. Seed и правила разделения зафиксированы в [протоколе](OPTIMIZATION_PROTOCOL.md).
