# R0F — реестр разрешения противоречий

BASE_SHA=ad5ce78d74c53b34358cd7508982aa888976057a

PROPOSED / AWAITING_ADMIN_APPROVAL. CONTRACT-DECISION-PREPARATION / TEST-ONLY. Не разрешение production или торговли.

| ConflictID | Старый источник/правило | Кандидат R0F | Что остаётся |
|---|---|---|---|
| BAL-GROSS | C3 request Gross=grant, R0E/C2 Gross-view=remaining | OriginalGrant и RemainingGross раздельно | D01/MAPPING approval; legacy ownership/units |
| MONEY-TYPE | Projected positive и actual деньги одной формой | Шесть disjoint money types/independent receipts | Provider/broker/runtime UNPROVEN |
| SMALL-ROLE | LevelMoney projected sum содержит Small | A Small residual; B explicit transfer | D03 не утверждён, production формула сохранена |
| FAR-METRIC | Incremental с baseline может быть меньшеabsolute | Absolute working forecast; incremental diagnostic | D04/baseline/native pricing proof |
| TRANSITION | C2 final signed loss не sticky/peak | Полные A/B/C, no default | Выбор D05 и reset/backend/ordered history |
| COST-STATUS | C2 survivor объявлен redundant на одном input | malformed pure fact CONFLICT vs unknown UNAVAILABLE | Новая fixture coverage; C2/C3 не меняются |
| CODEC | raw64/NFC старый proposal vs typed fixture | A/B explicit UTF8/no implicit normalization, Z equivalence | Native codec и zero policy approval |
| R1-SCOPE | Старый spec+2 helper headers vs C3 single file | Minimal inline vs explicitly Extended3 helpers | Admin scope/API choice; no headers created |
| ALLOCATION | Equal total игнорирует bucket vector | Immutable grant vector отдельно от consumed state | L02 production остаётся открытым |
| FUNDING | Source-local cap != account economic funding | Explicit scope; full account all roles/external debits required | Backend/global data UNPROVEN |

Структурные противоречия сформулированы непротиворечиво в candidate profile; это не означает их административного разрешения. CONTRACT_CONFLICTS_RESOLVED не YES: D05, codec, actual domain, scope и approvals остаются открыты. Никакой proposed профиль не переписал действующий historical норматив или acceptance status.
