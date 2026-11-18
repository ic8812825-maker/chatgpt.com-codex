# Воспроизведение HALR-03

Из Git checkout с веткой HALR-03 подготовить неизменяемый архив HALR-02. URL и SHA контрольных PR приведены в 01_BASELINE_MANIFEST.json.

```sh
git fetch origin refs/pull/7/head
RESEARCH=MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Research
export HALR02_DIR="$(mktemp -d)"
git archive "ac17e6a365ec97457b3fd358163f5aab91f15924:$RESEARCH/HALR02" | tar -x -C "$HALR02_DIR"
cd "$RESEARCH/HALR03"
python -B reproduce_baseline.py "$HALR02_DIR" /tmp/halr03-baseline --run
python -B baseline_audit.py
python -B stress_audit.py
python -B core_ablation.py
python -B meta_audit.py
python -B experiments.py
python -B bridge.py
python -B viability.py
python -B select_policy.py
python -B verify_halr03.py
python -B render_report.py
```

Обычный прогон эксперимента заново фиксирует training/validation; флаг `--frozen` повторно применяет замороженные настройки без подбора. Главные статистики на Python 3.11+ строятся стандартной библиотекой.

Для исторического прогона использовать неизменённые ZIP с опубликованными SHA-256. Команда получения обращается к общедоступной форме провайдера отдельно от офлайн-анализа. Источники могут изменить байты; при расхождении хэша использовать сохранённый снимок либо пометить новую версию данных.

```sh
(cd .. && python -B HALR03/fetch_histdata.py 202301 202307 202401 202003 202407)
python -B scan_historical.py
python -B historical_replay.py
```

Скачивание и промежуточные слоты создают файлы рядом с каталогом исследования. Эти архивы и промежуточные файлы остаются вне Git. Проверки воспроизводимости отслеживают опубликованные агрегаты, исходный SHA и журнал модельных fill. Положительный mark при открытой корзине не входит в Recovery.
