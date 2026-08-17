# Аудит include-графа HSB.2D-V1

Машинный граф: `Tests/Static/hsb_2d_v1_include_graph.json` (пути относительно project root).

- Корни: главный EA и `Tests/MQL5/HSBI_Skeleton_Tests.mq5`.
- Узлы: 75 MQL5-файлов; include-рёбра: 157; guards: 73.
- Все include разрешаются внутри project root; абсолютных, внешних и отсутствующих include нет.
- Циклы отсутствуют; guard каждого `.mqh` присутствует и уникален, закрывающий `#endif` присутствует.
- Конфликтующих определений runtime policy не найдено; consumers используют `Include/Core/HSBI_RuntimePolicy.mqh`.
- Harness достигает `HSBI_RuntimeDecisionValidator.mqh`, `HSBI_RuntimeRestartValidator.mqh` и `HSBI_RuntimeTransactionBarrier.mqh` по ожидаемому графу.
- Include соседних EA и общей торговой библиотеки отсутствуют.

`INCLUDE_GRAPH=PASS`; `INCLUDE_GUARDS=PASS`; `NO_EXTERNAL_INCLUDE=PASS`.
