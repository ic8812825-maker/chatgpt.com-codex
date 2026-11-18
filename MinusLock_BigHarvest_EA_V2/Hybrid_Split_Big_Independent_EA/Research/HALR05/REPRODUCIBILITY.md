# Воспроизведение HALR-05

Нужны Git и Python 3.11+. HALR02_DIR, HALR03_DIR и HALR04_DIR — отдельные каталоги архивов. Архивы изменяются только как локальные копии воспроизведения, исходные ветки сохраняются.

```sh
git fetch origin refs/pull/7/head refs/pull/8/head refs/pull/9/head
P=MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Research
export HALR02_DIR="$(mktemp -d)"
export HALR03_DIR="$(mktemp -d)"
export HALR04_DIR="$(mktemp -d)"
git archive "ac17e6a365ec97457b3fd358163f5aab91f15924:$P/HALR02" | tar -x -C "$HALR02_DIR"
git archive "7d12c24192730b27dac92bb8a5bad0c0efa900cc:$P/HALR03" | tar -x -C "$HALR03_DIR"
git archive "dd957384a43253964c906379cf37c0ec80de0828:$P/HALR04" | tar -x -C "$HALR04_DIR"
cd "$P/HALR05"
```

Для повторения старого контроля передайте каталог с HALR-04 episodes.json из его закреплённого [протокола](https://github.com/ic8812825-maker/chatgpt.com-codex/pull/9). Команды baseline_check и margin_audit используют только прежние данные. baseline_check без аргумента обновляет локальный манифест, поэтому сравнивать время манифеста побайтно не следует.

```sh
python -B baseline_check.py /path/to/old_halr04_data
python -B margin_audit.py /path/to/old_halr04_data
python -B oracle_audit.py /path/to/old_halr04_data
```

Для нового календаря каталогу DATA нужны исходные HistData ZIP. При отсутствии локального файла причинный сборщик выполняет объявленную загрузку с общедоступной формы и сохраняет контрольные суммы. Для строго офлайн-повтора предварительно разместите в DATA 36 ZIP с указанными SHA-256. Код загрузки не отправляет торговых поручений. Если источник поменял архив, не считать новый байтовый результат повтором прежнего.

```sh
DATA="$(mktemp -d)"
python -B 04_CAUSAL_REPLAY.py "$DATA"
python -B data_checks.py "$DATA"
python -B main_test.py "$DATA"
python -B stress_test.py "$DATA"
python -B independent_audit.py "$DATA"
python -B final_checks.py "$DATA"
python -B render_report.py
```

Первичный артефакт 07_CONFIRMED_JOURNALS.jsonl.gz раскрывает порядок QUOTE, CREATE, ACK и FILL и временную метку доступного quote. Матрица 08 отдельно хранит открытые marks, gross и pending при отсутствии FLAT. Формат брокерского импорта локальный: `python -B 05_FILL_IMPORT.py anonymized.csv`. Тестированные журналы импорта искусственные, отдельно от исторических Bid/Ask.
