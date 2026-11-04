# 02B-R0D — нормативное дополнение, PROPOSED

База `ec7ae40fe22e1d6e5bed035450750502a1162ab5`. Старые документы не переписываются. D-01–D-08/CR-09/R0C и новые R0D уточнения ожидают явного утверждения администратора.

| Clause | Характер изменения | Требуемый выбор | Влияние на R1.1 |
|---|---|---|---|
| NUM-EXACT-1 / NUM-DOMAIN-1 | Исправляет неверную арифметическую реализацию conservation/CR-09; новый явный fixture representation/domain | Утвердить только test-only профиль либо предложить другой доказанный домен; не broker precision policy | Fraction не переносится автоматически в MQL5; raw source codec/posted reconciliation остаются отдельными зависимостями |
| SNAP-FIXTURE-1 | Уточняет отсутствовавшие fingerprint type/schema и unknown semantics | Непустая opaque строка; None=unknown; missing/wrong type=malformed; schema version обязательно | Только future DTO/provider specification; не расширяет allowlist EconomicLedger phase |
| NUM-CODEC | Новые typed tokens исключают str/number и bool/int коллизии | Утвердить fixture codec отдельно от MQL5 raw64/NFC codec | Не переинтерпретировать historical roots/receipts; source identity migration append-only по отдельному решению |
| NUM-APPLY / SCOPE-FREEZE | Обязательная post-state validation и точный prefix trace; scoped acceptance | Утвердить scope/typed outcomes; не считать eligibility commit или trading permission | R1.1 по-прежнему отдельное задание после решений D-01–D-08/CR-09; NewFar/geometry/dispatch запрещены |

Рабочая формула posted net и source roles здесь не меняется. HALF_EVEN остаётся только candidate local mode после независимой сверки с fixture receipt; реальная broker verification NOT_RUN. Projected loss/buffer в CR-09 не округляются до minor units ради PASS. Для settled grants/consumption grid обязателен.

R0C COMPLETE переоценивается отдельным новым verdict из-за воспроизведённых локальных математических дефектов. Исторические221PASS/30KILLED остаются фактами своих каталогов. R0D не утверждает глобальную source-level conservation, durable restart/CAS/concurrency, real fills или broker authenticity.

Никакого production remediation M01/M02/L01/L02/ZeroCore. Никакой автоматической миграции схем, подстановки текущего account или изменения immutable evidence. После test-only публикации — остановиться и представить решения администратору. Источники: новые Numeric/Snapshot ContractID, R0C Oracle Contract, Docs/08/24/31/32, действующая R1.1 specification.
