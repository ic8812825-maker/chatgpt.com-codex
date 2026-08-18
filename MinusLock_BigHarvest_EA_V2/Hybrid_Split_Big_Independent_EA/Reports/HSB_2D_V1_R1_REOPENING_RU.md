# Переоткрытие HSB.2D-V1-R1

Baseline и GitHub SHA: `974792307c0cd2a736fca8edfa1befa8d347c556`.

Независимый контрпример заменил `if(x.stateRevision!=revision)` на `if(false && x.stateRevision!=revision)` и обновил SHA manifest. Старый S028 искал подстроку, поэтому нейтрализованный guard сохранил текст и получил ложный PASS; S045 также закономерно прошёл после rehash. Старый suite не запускал основной verifier на реальных копиях: duplicate guard из списка `SAME`, удаления в локальной строке, literal status и искусственный outside path были декоративными. Presence-only были S023–S039; поэтому заявленные `15/15` не являются end-to-end доказательством.

```text
HSB.2D_V1_PREVIOUS_ACCEPTANCE=HISTORICAL_SUPERSEDED
SUPERSEDED_REASON=INDEPENDENT_MUTATION_COUNTEREXAMPLE
HSB.2D_V1_R1=REOPENED
HSB.2D_V2_ALLOWED=NO
HSB.2E_ALLOWED=NO
```

Scope R1: только verifier, mutation runner/catalog, manifest, evidence, отчёты и status docs внутри этого проекта. Торговая математика, production broker dispatch и MQL5 runtime не изменяются. Переход к HSB.2D-V2/HSB.2E запрещён до публикации и решения администратора.
