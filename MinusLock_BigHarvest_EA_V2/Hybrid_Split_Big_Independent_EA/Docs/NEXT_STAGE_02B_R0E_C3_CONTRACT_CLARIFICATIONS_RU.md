# C3 — уточнения для административного рассмотрения

BASE_SHA=3737116bff6e2275d674b3dd7b816de93715f27c

AUDIT / PROPOSED / AWAITING_ADMIN_APPROVAL. Production, trading и dispatch запрещены.

Нормативная иерархия: первичные Docs08/16/31/32 задают исторические требования; proposed R0E/C1/C2 не утверждаются тестами. Фактический MQL5 source — поведение, а не автоматическое нормативное разрешение. Административные поля прежних16 решений остаются пустыми. Никакой исторический статус не переписан.

## Имена баланса: существенное противоречие

В задании C3 Gross=Consumed+Reserved+Free. В R0E/C2 документах G означает OriginalGrant, а Gross-view означает Reserved+Free. Это две разные величины. Рекомендуется запретить bare Gross и использовать:

OriginalGrant=Consumed+Reserved+RemainingFree; RemainingGross=Reserved+RemainingFree; Available=RemainingFree только после обязательной authority/journal reconciliation. Числа50,10,15,25 дают RemainingGross40; 10+15+40=65 ошибочно. Если Gross в C3 понимается как исходный grant50, его равенство верно; если как RemainingGross40 — неверно. Это naming/schema decision D01/BALANCE-SCHEMA-MAPPING, не ошибка точной арифметики. Никакой новый смысл не вступает в силу автоматически.

## Scope и отсутствующие переходы

C2 публичная composed операция — CONSUME_FREE. Reserve/release/consume-reserved доступны как математические private registry transforms; JournalPayload C2 store допускает только FUND/CONSUME_FREE. C3 проверяет owner algebra отдельно, но не выдаёт это за публичный production reservation lifecycle. Source-local multi-allocation cap не доказывает global economic debit attribution.

C2 Snapshot ID/fresh берутся из independent fixture evaluation context. В Authority нет текущего snapshot-object/receipt registry. Поэтому current C2 proof подтверждает ID binding, не полный snapshot content proof. R0D отдельный snapshot-content тест не доказывает его интеграцию в C2/NewFar. Coherent ID999 в request/context может разрешить fixture debit; authenticity/content остаются UNPROVEN.

## D05 и costs

Префикс fills -15,+100 при cap12: signed loss15→0; current final CONFIRMED совместим с C2 profile, но sticky breach остаётся true, peak cumulative loss15. Выбор signed/peak/sticky — решение администратора. Подтверждённый deal не доказывает batch membership; повторный reference не увеличивает unique volume. Changed history payload между assessments не превращается автоматически в CONFLICT без immutable provider journal.

AdditionalRisk — headroom, не actual debit. Неизвестный cost или risk overlap не0. Малформированный OverlapKnown1 должен быть CONFLICT в pure cost API; C3 показывает, что один C2 survivor не эквивалентен по этому правилу. Денежное небезопасное списание этим не доказано.

## Геометрия и числа

Zero Core недопустим при обязательной BigCore-ноге даже при positive slope. Необходимы min<=Core<=max, допустимая сетка/step/origin, positive required legs, correct ratios/direction и recovery/risk/margin gates. Одно Core>=min недостаточно: min.03/step.02 при origin0 не на сетке, при origin.03 может быть допустимо. Broker volume origin нельзя угадывать; недостаток данных UNPROVEN/UNAVAILABLE.

R0D lattice10^-64, abs<10^65 не является MQL-domain. Settled integer minor units требуют checked overflow; projected subunit losses нельзя округлять до0. Unknown broker precision policy не заменяется HALF_EVEN. Критерии0 и отрицательного margin сохраняются точными.
