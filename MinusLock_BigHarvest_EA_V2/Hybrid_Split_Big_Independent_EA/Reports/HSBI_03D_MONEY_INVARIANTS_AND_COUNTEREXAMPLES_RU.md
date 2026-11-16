# HSBI-03D — Денежные инварианты и контрпримеры

Версия HSBI-03D-REMOTE-R1; PROPOSED; source SHA 6543bc2c0d125f5f7e02f78a092b0412a2e34626.
Источник публикации — полный предыдущий ответ HSBI-03D в этой беседе. Это не новый runtime test.
Точные production sources S01–S20: [independent review](HSBI_03D_INDEPENDENT_CONTRACT_REVIEW_RU.md#зафиксированные-источники).
Нормативный текст: [ballot](HSBI_03D_OWNER_APPROVAL_BALLOT_RU.md).

## 1. Economic identity — условия и пределы доказательства

При assumptions о стабильном broker/server namespace, независимом actual source и trusted EA association:
K=(BrokerNamespace,ServerNamespace,AccountLogin,DealTicket).
Две записи одного immutable attributed fact эквивалентны iff совпадает authenticated K и полный mandatory semantic body в одном утверждённом numeric domain, без противоречащего association evidence. Это условие относится к представлениям с подтверждённым происхождением. Совпадение двух caller DTO не доказывает существования физического deal.

Полный 29-field envelope: SchemaVersion,Broker,Server,AccountLogin,Symbol,Magic,CycleID,DealTicket,OrderTicket,PositionIdentifier,ActionID,EventID,Role,EntryType,DealType,TimestampMsc,Volume,Price,Profit,Swap,Commission,Fee,DealNet,Currency,Precision,SourcePlanApplicable,SourcePlan,SourcePolicyApplicable,SourcePolicyVersion.
Immutable origin EconomicEventID не равен ObservationID повторного импорта. EA Cycle/Action/Role/Plan/Policy не выводятся из broker history без association. Derived DealNet не является самостоятельным broker DEAL_NET полем.

| Случай | Ожидаемый вывод |
|---|---|
| Equal net, different components | same K/changed body CONFLICT |
| Same ticket, other account/server | different K; attribution отдельно |
| Same amount, other role/position | changed attributed fact; не equal |
| Changed price/volume | CONFLICT, не epsilon replay |
| Different ObservationIDs, same physical deal | один K, без нового grant |
| Repeat import exact source/body | replay, funding effect0 |
| Correction/reversal | append linked fact, original receipt immutable |
| Incomplete broker/EA history | no proof of completeness/NEW funding |

Logical identity отделена от wire serialization: schema/codec change не новый income. Z-profile явно отождествляет ±0 и не raw-bit identity. На отсутствие registry нельзя ссылаться как на невозможность сравнить два уже authenticated факта; registry completeness необходима отдельно для NEW/spendable классификации. S01:7–11 и S06:10–28 текущие predicates недостаточны для independent authority. STATIC_REVIEWED.

## 2. Conservation и draft→commit

Два разных уровня:
G=Σ_b Grant_b=C+P+T+K+R.
Для каждого b: Grant_b=Consumed_b+Reserved_b+Free_b.
Символ C в первой формуле — bucket grant; Consumed_b во второй — lifecycle amount. Смешивать значения запрещено.

Все amounts nonnegative, exact, один currency/profile. Draft: Σdraft_b+Unassigned=G, Unassigned≥0. Draft не spendable. Atomic commit требует Unassigned0, полный manifest, уникальную регистрацию source и expected revision. Cancel draft не создаёт/освобождает ранее несуществовавших funds.

| Event | ΔConsumed | ΔReserved | ΔFree | Условие |
|---|---:|---:|---:|---|
| reserve a | 0 | +a | −a | 0≤a≤Free; authority valid |
| consume a | +a | −a | 0 | actual independently confirmed effect; a≤Reserved |
| release a | 0 | −a | +a | independently proven no further corresponding effect; a≤Reserved |

Сумма приращений каждой строки0, поэтому identity сохраняется. Предусловия сохраняют nonnegativity. Это MATH_DERIVED, не реализация atomicity.

Transfer: все debit/credit legs в одной transaction; общий capacity не растёт, attribution сохраняется. Partial fill: consumed actual part; remainder release только после подтверждения отсутствия future execution. Timeout/UNKNOWN не доказывает cancellation и не позволяет release.

Concurrent case: Free50, requests30+30 одной revision. Serializable CAS balance+receipt допускает не более одного commit: итог Free20; второй conflict. Два отдельных read/check/write могут оба пройти на Free50 — математическое равенство в одиночной модели concurrency не квалифицирует.

Restart должен восстановить полный committed balance+receipts+registry и broker reconciliation либо blocked. In-memory replay map/checkpoint не доказательство durable transaction. S02:5–10,S04:44–70,S12:18–43,S13:7. STATIC_REVIEWED/MATH_DERIVED.

## 3. Correction/reversal без фиктивного funding

Исходный G50,Consumed40,BookFree10. Correction уменьшает economic capacity до30.
Нельзя переписать grant в30 с consumed40 и объявить conservation успешной. Исходное50=40+10 сохраняется как history; correction−20 append-only; deficit10 регистрируется отдельно, affected free/reservations blocked. BookFree10 не spendable.
До отдельного approved adjustment settlement contract используется quarantine. Иной event/schema/reversal key не обходит source hold. Не заявляется доказанная глобальная funding conservation при незакрытом deficit.

## 4. Reserve и публичные scalars

Projected≠Confirmed≠Allocated. Allocated=Consumed+Reserved+Free; spendable дополнительно требует authority. S16:12 runtimeConfirmed — successful calculation, не actual source proof.

Обязательное binding: scalar amount==proof-derived amount; currency/profile/basis equal; proof source==registry source; consumption source/allocation/operation==authorised receipt.

Контрпример S04: proof eligible10, caller scalar100,share0.8,FarLoss20,buffer1:
caller margin=80−20−1=59; source-consistent margin=8−20−1=−13.
Expected CONFLICT до расчёта. COUNTEREXAMPLE_CONFIRMED как арифметика/contract, native NOT_RUN.
Ограничение вывода: S07:121–122 выводит scalars из proofs; это не автоматически доказанный solver exploit.

Exhausted-source shape: net50,alreadyConsumed50,buckets0,reserveAllocated0,scalarEligible50,share0.8; unallocated branch S04:67–70 не содержит allocated-branch запрет consumed из63–66 и может вычислить gain40. Требуется global inventory rejection; это static counterexample, не runtime PASS.

## 5. D05 — current, peak, sticky, reset, restart

Для immutable OperationID/CapEpoch,H:
S_n=ΣactualNet_i;
L_n=max(0,−S_n);
Peak_n=max(Peak_(n−1),L_n);
Sticky_n=Sticky_(n−1) OR (L_n>H).

| Fills | H | Net | Current | Peak | Sticky |
|---|---:|---:|---:|---:|---|
| −15,+100 | 12 | 85 | 0 | 15 | true |
| +100,−15 | 12 | 85 | 0 | 0 | false |
| −12 | 12 | −12 | 12 | 12 | false |

Final net недостаточен для ordered safety history. Cap equality не breach. Current не заменяется peak; sticky сохраняет факт breach.

Reset только authenticated owner principal отдельного control plane: complete independently verified history, no pending/unknown,Current≤H,safety review,expected revision. Receipt включает principal/reason/operation/cap epoch/history root/old revision/new monitoring epoch. Очищается только latch; fills/net/consumed/replay/archive peak неизменны; auto-resume запрещён. Unconfigured principal → reset unavailable.

Restart восстанавливает committed sticky до обычного продолжения и сверяет actual fills. Broker chronology и observation order различаются; EventID не независимый broker sequence. Неполная/повреждённая history → UNAVAILABLE/manual-safe, не sticky=false.
Sticky blocks NewFar/new risk/normal transition/routine FinalClose authority. Отдельная SAFE/emergency risk-reducing authority не означает recovery success и sticky не снимает. S19:8,Docs/04:24,Docs/13:9. Policy PROPOSED; реализации не заявлено.

## 6. Cycle result и costs

EconomicCyclePnL=all defined actual realized net+defined open net−not-yet-included costs.
NormativeRecoveryResult имеет отдельный membership: вариант D06-A сохраняет Initial exclusion Docs/09:20.
Initial50,other−10,open−5 → Economic35,Recovery−15. Это нормативный конфликт, не исправляется переименованием всех сумм в CyclePnL.

Actual net=Profit+Swap+Commission+Fee; gross100,commission−2,swap−1,fee−1 →96. Не92.
Spread/slippage могут уже отражаться в entry/exit prices; future estimates/buffers не actual broker expenses.
RemainingCosts — только disjoint ещё не включённые costs; close-now net с close expenses нельзя уменьшать ими повторно.
Buckets — распределение результата, не новая прибыль.

Positive BigHarvest не означает positive CyclePnL. Пример: BigHarvest100,прочие defined net−150 → cycle−50.
Positive cycle metric не равно FinalClose authorization; authorization не равно actual CLOSED. Docs/12:7–15 требует coverage,freshness,no pending/unknown,ownership/revision,actual zero residual,ledger,persist. S14:11–18,S19:9 не вся authority.

## 7. All-level и unchecked tail

Losses(10,5),Margins(9,−11): max loss level1 не minimum margin level2. Candidate reject. При margins(9,2) и остальных valid proofs finite required set feasible.
Required set задаётся явно; missing required proof→UNAVAILABLE; unchecked tail→UNPROVEN.
Objective после feasibility. Дополнительный conflict Docs/14:22–23 minimum-safe-first / Docs/29:3 risk-first остаётся owner question. S07:149 risk-first.
S08:23–58 не доказывает global infinite-depth profit.

## 8. Numeric mathematics

signed64 MIN=−9223372036854775808,MAX=9223372036854775807.
MAX+1,MIN−1,abs(MIN),−MIN,MIN×−1 invalid. MAX+MAX−MAX−MAX mathematically0,но intermediate overflow; checks до операции.
Balances≤MAX и nonnegative bounds позволяют safe bounded subtraction, но не оправдывают произвольные промежуточные суммы.
Scale100 max main92233720368547758.07. Для fixture scale10^8 max92233720368.54775807. Ни один scale не объявляется фактом currency без profile.

HALF_EVEN cents component0.005+0.005→0; aggregate→0.01; negative analog0 против−0.01. Posting stage обязателен.
Projected0.004 loss не исчезает как economic obligation от cents rounding.
NaN/Inf forbidden; negative-zero semantic policy явна; underflow changing decision reject.
Oracle unlimited integer/Fraction или grid10^-64 не доказывает native MQL5 range.

## 9. ERR038: bounded lots не bounded monetary loss

Контрмодель фиксированного SELL: Volume1,MoneyPerPriceUnit1,Price=P0+M → Loss=M. При неограниченном M loss не bounded, хотя lots constant.
Это COUNTEREXAMPLE_CONFIRMED к универсальной импликации; не утверждение, что каждый BUY имеет ту же модель.
Нужны отдельные price/gap/time/cost,liquidity,slippage,margin/stop-out/execution assumptions и математическое доказательство выбранной ограниченной модели. Даже q-contraction требует uniform assumptions,rounded grids и доказанного termination/close policy.
ERR-038=OPEN. Денежные контракты отдельно его не закрывают.
