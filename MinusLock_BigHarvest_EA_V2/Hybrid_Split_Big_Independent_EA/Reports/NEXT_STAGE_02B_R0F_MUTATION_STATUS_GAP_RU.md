# R0F — формальный status contract и C3 gap

BASE_SHA=ad5ce78d74c53b34358cd7508982aa888976057a

PROPOSED / AWAITING_ADMIN_APPROVAL. CONTRACT-DECISION-PREPARATION / TEST-ONLY. Не разрешение production или торговли.

Source: frozen C2 `cost_coverage` и `C2-MUT-cost-shape-caller`; новые фактические outcomes — STATUS_GAP.json. Минимальный input: independent fact OverlapKnown=1 (int), все claim поля нормальны. Positive control COVERED в original/mutant. Pure original CONFLICT, mutant UNAVAILABLE; authorize/apply оба REJECT, zero deltas и input unchanged. Это status coverage gap, не unsafe spend и не глобально избыточный guard.

| API / факт | Outcome | State |
|---|---|---|
| Pure cost malformed/противоречивый authoritative fact | CONFLICT | Pure/zero delta |
| Pure cost authority отсутствует или overlap неизвестен | UNAVAILABLE | Pure/zero delta; не known zero |
| Spending request malformed/неразрешён | REJECT | zero balances/journal/revision delta |
| Changed known event payload/source immutable conflict | CONFLICT | zero delta |
| Независимая history/provider недоступна | UNAVAILABLE | zero delta |
| Exact verified receipt/payload | NO_OP | zero delta, не новое eligibility |

Обязательные callers: direct cost_coverage; authorize->_authorize; apply_for_test->authorize. Public spending prevalidation предотвращает этот malformed fact до pure helper. Она не заменяет самостоятельный direct-helper status contract. R0F candidate cost_status сначала проверяет формы/точные bool types, затем различает malformed и unknown. Это новый test-only профиль, не исправление C2/C3.

Будущий план: в новом versioned test-only suite добавить independent OverlapKnown1 и complete/unknown controls; повторить exact source mutation; сохранить old C2/C3 rows и новую классификацию отдельно; не утверждать redundant по одному bool-policy input. Любое дальнейшее production изменение требует отдельного approved scope. Tests R0F-COST-malformed/unknown/known и STATUS_GAP.json не используют evaluator как expected.
