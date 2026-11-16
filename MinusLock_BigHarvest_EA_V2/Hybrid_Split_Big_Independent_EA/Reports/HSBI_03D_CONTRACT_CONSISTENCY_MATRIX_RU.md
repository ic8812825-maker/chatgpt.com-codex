# HSBI-03D — Матрица согласованности контрактов

Версия HSBI-03D-REMOTE-R1; PROPOSED; source SHA6543bc2c0d125f5f7e02f78a092b0412a2e34626.
16 полных текстов: [ballot](HSBI_03D_OWNER_APPROVAL_BALLOT_RU.md). Sources: [independent review](HSBI_03D_INDEPENDENT_CONTRACT_REVIEW_RU.md).
N normative dependency; A architectural interface; E evidence requirement.
Arrow означает «использует решение», не независимый линейный approval order. Исходные зависимости карточек сохранены; новые уточнения не удаляют реальные cycles.

## Зависимости, порядок, совместное утверждение

| Решение | Зависимости и тип | Порядок/совместное утверждение и R1.1 |
|---|---|---|
| D01 | D10 N,D14 A,D16 N | Grant semantics вместе с registry/migration interfaces; numeric freeze отдельно |
| D02 | D08 N,D13 E,D14 A | Согласовать evidence/source interface; bool не activates funding |
| D03 | D02 N,D14 A | Eligibility/registry attribution совместны |
| D04 | D02 N,D06 N,CR09 N | Loss/cost basis и all-level gates согласовать вместе |
| D05 | D06 N,D07 A,D13 E | Reset policy explicit approval; ordered history/restart evidence до implementation |
| D06 | D02 N,D13 E; дополнительно D11 N | Initial A/B first; posting/cost scope отдельно |
| D07 | D08 N,D10 N,D13 E,D14 A | Effect/receipt/registry transaction единый interface |
| D08 | D02 N,D12 A,D13 E,D16 N | Logical identity отдельно от bytes; migration сохраняет K |
| CR09 | D04 N,D06 N,D13 E,D14 A | Every required level до objective; tail unproven |
| D10 | D11 N,D12 A,D15 E | Numeric bundle, principles не concrete freeze |
| D11 | D10 N,D13 E,D15 E | Currency/posting profile и native boundaries |
| D12 | D08 N,D10 N,D11 N,D15 E | Codec не новый source; native before freeze |
| D13 | D08 N,D12 A,D15 E | Provider/clock/receipt profile before freshness use |
| D14 | D01 N,D02 N,D07 A,D08 N | Atomic funding+source semantics jointly specified |
| D15 | D10 E,D11 E,D12 E | Квалифицирует конкретный numeric manifest |
| D16 | D01 N,D07 A,D08 N,D10 N | Mapping после определения balances/receipt semantics |

Для каждой перечисленной пары совместимость требует выполнения обоих предложенных текстов, общего interface manifest и соответствующих evidence gates. Противоположные варианты из следующей таблицы несовместимы; незакрытая evidence dependency запрещает implementation-ready claim, даже если принцип одобрен.

## Реальные cycles

В исходном графе большая strongly connected group: {D01,D02,D07,D08,D10,D11,D12,D13,D14,D15,D16}; малый cycle {D04,CR09}. Разделение N/A/E организует решения, но не превращает graph в DAG. Новые D06 posting links также нельзя скрывать.

Обязательный numeric approval bundle:
NUM-EXACT-1 + NUM-DOMAIN-1 + NUM-CODEC + MQL-DOMAIN.
Единый frozen manifest: currency/profile,scale,posting stage,rounding,range/intermediate checks,zero/subnormal policy,schema,codec,framing,UTF-8/size limits,native goldens.
Можно утвердить principles/test requirements отдельно; конкретный bundle ещё не qualified. Evidence не заменяется совместным голосованием.

Funding/source/journal/migration interfaces требуют совместно согласованного manifest, сохраняя отдельные owner decisions. D05 safety policy отдельный явный выбор. D06 Initial choice и NewFar objective conflict не скрываются numeric bundle.

## Несовместимые комбинации и допустимые альтернативы

| Комбинация | Причина | Совместимая альтернатива |
|---|---|---|
| Original grants + добавление consumed к их сумме | double accounting | lifecycle identity отдельно |
| Projected scalar + spendable grant | no actual funding | actual receipt+registry |
| Small в BigReserve + отдельная Big eligibility | attribution violation | separate Small или approved transfer |
| Incremental FarLoss + absolute coverage | undercoverage | absolute obligation |
| Sticky + reset по final net>0 | erased safety history | owner reset receipt, no autoresume |
| All realized включая Initial + Docs/09:20 | normative conflict | D06-A либо explicit amendment B |
| UNKNOWN + resend/release | repeated/late effect | independent reconciliation |
| Codec/schema как новый source | double funding | codec-independent K |
| Max TransitionLoss + all-level margin claim | minimum elsewhere | check each required level |
| Exact minor units + early preview rounding | lost small loss | separate preview/posted domains |
| Component rounding + aggregate posting receipt | amounts differ | evidenced posting stage |
| F64Z reference PASS + native-qualified claim | no native evidence | native bundle |
| Snapshot ID/digest + caller freshness | no provider authority | clock/content receipt profile |
| Local duplicate map + global funding | no completeness/atomicity | durable serializable registry |
| Unknown legacy + zero/default fill | invented facts | quarantine |
| Bounded lots + global bounded money loss | absent market bounds | separate limited risk model |

## Дополнительные нормативные конфликты

Docs/14_NEW_FAR_SOLVER_SPECIFICATION_RU.md:22–23 minimum-safe-first против Docs/29_CANDIDATE_OBJECTIVE_AND_TIEBREAK_RU.md:3 risk-first; production S07:149 risk-first. CR09 approval не выбирает objective автоматически.
Docs/09_INITIAL_LOCK_SPECIFICATION_RU.md:20 Initial exclusion против общего all-realized RecoveryResult — D06 CONFLICTING.
Docs/14:9 grid Vmin+nstep против production S18:21–36 zero-origin — D11 evidence/profile issue.
Docs/16:6–12 crash consistency нельзя усилить недоказанным atomic rename/fsync-equivalent из Docs/HSB_2E_PERSISTENCE_SCHEMA_RU.md:8–10.

R11_IMPLEMENTATION_ALLOWED=NO; OWNER_APPROVAL_COMPLETE=NO.
