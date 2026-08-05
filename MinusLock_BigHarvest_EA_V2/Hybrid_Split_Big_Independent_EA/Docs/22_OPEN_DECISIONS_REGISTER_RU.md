# Реестр открытых нормативных решений

Версия 1.0. Статус: OPEN. Решения нельзя выдумывать молча.

| ID | Тема | Варианты | Влияние/риск | Рекомендация | Пользователь | Статус |
|---|---|---|---|---|---|---|
| HSBI-DEC-001 | Production ratios C/T/S | fixed, solver range, profile set | catch-up/slope/margin; P1 | утвердить после money search | YES | OPEN P1 |
| HSBI-DEC-002 | Allocation shares | reserve/partial/transition/carry | Final/Partial capability; P1 | conservation + scenario study | YES | OPEN P1 |
| HSBI-DEC-003 | Control price/range | level, Far distance, stress range | proof validity; P1 | broker-valid bounded grid | YES | OPEN P1 |
| HSBI-DEC-004 | Future Small depth | 1, bounded N, finite proof | hidden dead-end; P1 | bounded multi-step proof | YES | OPEN P1 |
| HSBI-DEC-005 | NewFar objective | minimum-safe, weighted score, lexicographic | compression/risk; P1 | lexicographic safety then min N | YES | OPEN P1 |
| HSBI-DEC-006 | Emergency policy | freeze, protective close, account stop | loss/control; P1 | separate authority, no recovery PASS | YES | OPEN P1 |
| HSBI-DEC-007 | Maximum transition loss | zero or money limit | reversal feasibility; P1 | money cap + budget source | YES | OPEN P1 |
| HSBI-DEC-008 | Minimum Final profit | fixed/dynamic | close timing; P1 | money threshold incl costs | YES | OPEN P1 |
| HSBI-DEC-009 | Margin/drawdown limits | broker/account policy | survival; P1 | conservative demo limits | YES | OPEN P1 |
| HSBI-DEC-010 | Symbols/cycles | whitelist, one/multi-cycle | isolation/margin; P1 | one cycle per Symbol+Magic initially | YES | OPEN P1 |
| HSBI-DEC-011 | Persistence backend | files/common files/append log | atomicity/recovery; P1 | versioned temp+promote files | YES | OPEN P1 |
| HSBI-DEC-012 | Real limitations | deposit/leverage/lot/duration | capital risk; P1 | decide only after demo | YES | DEFERRED |
| HSBI-DEC-013 | Small confirmation | touch, retrace, time confirmation | false reversal | typed configurable rule | YES | OPEN P2 |
| HSBI-DEC-014 | Retry/timeouts | bounded retries/manual | duplicates/stuck action | no resend before reconciliation | YES | OPEN P2 |

## Requirements

- `HSBI-GEN-050`: OPEN P1 запрещает начать production implementation, зависящую от решения.
- `HSBI-GEN-051`: решение фиксируется новой revision с rationale, formulas, tests и affected IDs.
- `HSBI-GEN-052`: default не создаётся без пользовательского решения.

Контракт: вход — unresolved policy points; выход — explicit decision queue. Preconditions: no silent assumptions. Postconditions: каждое решение имеет owner/risk. Restart не применим. Owner: Administrator + architecture. Тест: все config constants ссылаются на APPROVED decision. Открытые вопросы перечислены таблицей.