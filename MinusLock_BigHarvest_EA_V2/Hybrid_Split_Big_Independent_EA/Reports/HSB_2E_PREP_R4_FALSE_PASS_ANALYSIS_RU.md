# PREP-R4: воспроизведение ложного PASS PREP-R3

Во временной копии одновременно внедрены неизвестный `EXPECTED_INVARIANTS`, операция `do arbitrary thing` и план `close unknown ticket twice`.

Исторический verifier завершился `RESULT=PASS`, `EXIT=0`, `SCENARIO_SEMANTIC_COMPLETENESS=PASS`, `SCENARIO_VECTORS_FAILED=0`. Следовательно, `PREP_R3_FALSE_PASS_REPRODUCED=YES`.

R4 устраняет дефект исполнением каждого invariant ID, типизированного scenario step и сериализованного broker intent.
