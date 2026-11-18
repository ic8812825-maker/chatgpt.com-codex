# Воспроизведение

Требуется Python 3.11+ и Git. HALR02_DIR и HALR03_DIR должны указывать на зависимости из двух точных git archive. Воспроизводящий процесс записывает результаты контрольного прогона только в отдельный архив, поэтому рабочие исходные ветки не затрагиваются.

```sh
git fetch origin refs/pull/7/head refs/pull/8/head
P=MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Research
export HALR02_DIR="$(mktemp -d)"
export HALR03_DIR="$(mktemp -d)"
git archive "ac17e6a365ec97457b3fd358163f5aab91f15924:$P/HALR02" | tar -x -C "$HALR02_DIR"
git archive "7d12c24192730b27dac92bb8a5bad0c0efa900cc:$P/HALR03" | tar -x -C "$HALR03_DIR"
cd "$P/HALR04"
python -B baseline.py --run
python -B economic_audit.py
python -B risk_audit.py
```

Скачать ZIP отдельно. Имена и хэши из 03_DATA_MANIFEST.json. Если провайдер изменил файл, повтор пометить новым снимком.

```sh
DATA="$(mktemp -d)"
(cd "$DATA" && python -B "$HALR03_DIR/fetch_histdata.py" \
  201902 202004 202105 202210 202302 202310 202403 202406 202409 202502 202505 202508 202407 202003)
python -B data_scan.py "$DATA"
python -B 04_CAUSAL_REPLAY.py "$DATA"
python -B verify_s1.py "$DATA/episodes.json"
```

Замороженные конфигурация и таблицы опубликованы до исполнения final. Повтор с ними допускается для проверки работы. Локальная проверка обучения отдельно вызывает learning.py и сравнивает SHA-256 trained.json с 08_TRAINED_TABLES.json. Она использует только train/validation.

```sh
python -B learning.py "$DATA"
cmp trained.json 08_TRAINED_TABLES.json
python -B holdout.py "$DATA"
gzip -n -c 08_PRIMARY_PATHS.csv > 08_PRIMARY_PATHS.csv.gz
python -B activation_diagnostic.py "$DATA"
python -B frontier.py "$DATA"
python -B final_audit.py "$DATA"
python -B render_final.py
```

Брокерский импортёр отдельно: `python -B 05_EXECUTION_EVIDENCE.py anonymized.csv`. Полноценные журналы брокера в данном исследовании недоступны. Загрузка источников единственная сетевая операция анализа. Все расчёты выполняются офлайн. Большие ZIP, локальные .ticks и episodes.json не отслеживаются Git.
