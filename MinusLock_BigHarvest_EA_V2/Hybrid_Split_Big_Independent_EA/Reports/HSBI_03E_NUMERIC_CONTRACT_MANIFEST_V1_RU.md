# HSBI-03E-C — HSBI_NUMERIC_CONTRACT_MANIFEST_V1

Версия: **HSBI-03E-R1**. SOURCE_COMMIT_SHA=`b5ca9d377d454dfbec63ece76dd1c759abc3656d`.
Репозиторий `ic8812825-maker/chatgpt.com-codex`, ветка `work`, все относительные source paths внутри `MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/`.
Статус: **PROPOSED / AWAITING_OWNER_DECISION**. Ни один текст не APPROVED. Нормативный выбор, architecture/provider и implementation evidence — разные gates.
STATIC_REVIEWED означает чтение исходного текста; MATH_DERIVED — вывод при указанных предпосылках; COUNTEREXAMPLE_CONFIRMED — опровержение утверждения, не runtime PASS; HISTORICAL_TEST_RESULT — старый artifact; все новые vectors TEST_SPECIFIED_NOT_RUN; NATIVE_NOT_RUN. Новых compile/runtime/mutation/native tests не выполнялось.
UNAVAILABLE — обязательное evidence отсутствует; CONFLICT — доказательства противоречат; REJECT — доказанное нарушение домена/предусловия. Все три запрещают новый effect; финансовая delta=0. NO_OP возможен только по валидному полному старому receipt.
Публикация отчёта не утверждает контракт, не закрывает P0 и не разрешает production/R1.1/dispatch/trading.

ManifestId=HSBI_NUMERIC_CONTRACT_MANIFEST_V1; ManifestRevision=HSBI-03E-R1.
NUMERIC_MANIFEST_STATUS=PROPOSED_EVIDENCE_BLOCKED. Это согласованный проект структуры и требований,не заполненный broker profile и не native qualification.

## Точные источники

Docs/01_GLOSSARY_AND_DIMENSIONS_RU.md:13–27 непосредственно перечитан; также перечитаны Docs04:6–15,18–30,42; Docs08:6–24; Docs24:3–11; Docs25:3–7.
Docs/NEXT_STAGE_02B_R0D_NUMERIC_CONTRACT_RU.md:7–19,25–45 — fixture exact reference domain; НЕ MQL domain.
Docs/NEXT_STAGE_02B_R0F_NUMERIC_CODEC_OPTIONS_RU.md:17–35; Docs/NEXT_STAGE_02B_R0G_CODEC_DECISION_RU.md:9–34; Docs/NEXT_STAGE_02B_R0G_MINIMAL_IDENTITY_CONTRACT_RU.md:11–55.
Reports/HSBI_03D_INDEPENDENT_CONTRACT_REVIEW_RU.md:402–497,562–625; HSBI_03D_NUMERIC_NATIVE_QUALIFICATION_RU.md:1–77.
Include/Money/HSBI_EconomicLedgerTypes.mqh:6–12; HSBI_AllocationLedgerTypes.mqh:5–10; HSBI_BrokerMoneyTypes.mqh:7–18; HSBI_CostModel.mqh:11–18.
Include/Planning/HSBI_BrokerGrid.mqh:7–36; HSBI_NewFarCandidate.mqh:33–40.
Tests/Evidence/NEXT_STAGE_02B_R0F_CODEC_GOLDENS.json: JSON fields Profiles,Vectors,RecordFields,RecordBinaryHex,RecordTextHex,MQL5Compile; blob e506b9f3867dc98936f025603871653e72dd0620.

## Три уровня утверждения

1. CONTRACT_PRINCIPLES: exact settled/floating preview separation,checked overflow,explicit units/profile,codec-independent source,strict decode,no guessing — ready for owner consideration.
2. MANIFEST_BINDING: concrete account/currency/grid/cost/codec/limits/provider instances — evidence-blocked; UNBOUND ниже не default.
3. NATIVE_QUALIFICATION: compiler/terminal build evidence,boundaries,goldens,hostile decoder,caller integration — NATIVE_NOT_RUN.
Одобрение1 не означает2/3. D10,D11,D12,D15 сохраняют отдельные CanonicalDecisionId,но concrete freeze joint.

## Versioned manifest fields

Ниже typed declarative schema. UNBOUND — обязательный неустановленный fact; activation невозможна,пока он есть. Null/empty/default не считается подтверждением.

| Поле | Тип и предлагаемая норма | Authority/binding |
|---|---|---|
| ManifestId/Revision | exact strings выше | owner frozen text/blob |
| AccountScope | broker/server/account и currency profile version | independent namespace receipt,UNBOUND instance |
| CurrencyCode | nonempty exact currency identifier | account/provider,UNBOUND;не guessed ISO/default |
| CurrencyDigits | exact integer D in supported declared domain | independent monetary posting evidence,UNBOUND |
| SupportedDigits | candidate adapter capability D=0…8 | proposed resource/domain limit,не универсальный валютный закон |
| MinorUnitScale | S=10^D,exact checked integer | derived only after D binding |
| PostingStage | BROKER_NET_RECEIPT либо BROKER_COMPONENT_RECEIPTS либо VERIFIED_AGGREGATE_CONVERSION | UNBOUND;выбор не по удобству |
| RoundingMode | BROKER_RECEIPT_ONLY либо explicit verified HALF_EVEN/other named mode | UNBOUND;broker receipt не округляется локально |
| ExactMoneyType | CHECKED_SIGNED64_MINOR_UNITS | candidate architecture D10;native unqualified |
| SignedMoneyMin/Max | −9223372036854775808 / 9223372036854775807 minor | technical bounds,не account risk caps |
| BalanceMin/Max | 0 / 9223372036854775807 minor | smaller business caps may apply |
| ArithmeticProfile | checked-before-op ADD/SUB/MUL/NEG/ABS/DIV/SCALE;no wrap/saturate | native evidence required |
| PreviewProfile | captured finite binary64 + error bounds;no settled rounding | error bounds/domain UNBOUND |
| CostBasisManifest | membership,cost IDs/inclusion windows,H_in,H_gate,I group,D06 A/B | owner+provider;UNBOUND instance |
| SymbolScope | exact symbol and broker instrument/profile revision | UNBOUND provider instance |
| TickSize/Point | finite positive symbol-price units | separate captured values,UNBOUND |
| TickValueProfit/TickValueLoss | nonnegative currency-per-tick-per-volume basis;asymmetric allowed | UNBOUND instrument/broker conversion evidence |
| TickValue | no single scalar default: use tagged Profit/Loss pair | zero allowed only explained profile;not replace OrderCalcProfit blindly |
| VolumeMin/Max/Step | finite min>0,max≥min,step>0 lots | broker receipt,UNBOUND |
| GridOrigin | explicit price origin O_p and volume origin O_v | UNBOUND;0 vs Vmin must be chosen/evidenced |
| GridArithmetic | exact decimal rational grid OR qualified binary64 envelope adapter | UNBOUND evidence;no arbitrary epsilon |
| SchemaVersion | economic semantic HSBI-EA-ECON-1,wire field SchemaVersion1 candidate | fixed29-field schema;new incompatible body requires new version |
| Role/Entry/Deal Mapping | closed code tables,explicit broker/native enum mapping | UNBOUND production mapping;unknown enum rejected |
| LogicalSourceKey | (Broker,Server,AccountLogin,DealTicket) | independent source/EA association;not codec hash |
| CodecCandidate | HSBI-F64Z-1 or HSBI-T17Z-1 | NOT_SELECTED;owner+native decision required |
| ZeroPolicy | Z: financial/raw-observation semantic −0=+0 | candidate policy;not raw network packet preservation |
| TextPolicy | strict UTF8,no BOM/NUL in fields,no NFC/casefold | reject invalid sequences/unpaired surrogate |
| StringByteLimit/RecordByteLimit | proposed4096/65536 incl framing total | resource caps,not universal broker constants;native enforcement NOT_RUN |
| ProofBindings | provider receipts,codec/schema/profile IDs,source/body digest | digest not authentication |
| NativeEvidence | compiler/build,vector IDs,exact inputs/outputs/logs | NONE/NATIVE_NOT_RUN |
| LegacyMapping | versioned receipt,unknown quarantine | no guessed old precision/identity/consumed |

Wire schema/profile versions are representation metadata,не новый economic source. Numeric ManifestReference хранится в immutable association/receipt envelope; добавление новых body fields к29-field schema нельзя выдавать за совместимый SchemaVersion1. Разные известные codecs сравниваются через validated semantics только при approved cross-profile mapping. Unknown mapping UNAVAILABLE.

## Exact settled arithmetic и negative amounts

Settlement принимает authoritative posted integer amount на сетке S. BROKER_NET: net receipt authoritative;raw components остаются raw evidence,их отдельно округлённые суммы не притворяются independently posted components.
BROKER_COMPONENT: sum independently posted components с checked intermediates; net receipt,если есть,должен согласоваться по profile.
VERIFIED_AGGREGATE_CONVERSION: precise input representation + verified rule + independent expected posted receipt. Нельзя получить broker posting из raw float×S без evidence. RoundingMode и PostingStage ортогональны financial source wire codec.

Signed components сохраняют signs. Negative source учитывается economics,не negative grant; EligibleGrant=max(0,eligible posted net) только при policy. Балансы/consumption/reserve nonnegative; transfer/correction protocol отдельно. abs(MIN),negateMIN,MIN×−1 reject; MIN допустим как scalar signed fact,но операции с ним checked.

До a+b проверить b>0⇒a≤MAX−b; b<0⇒a≥MIN−b. Эти bound expressions также вычислять безопасным алгоритмом; не overflow ради guard.
a−b проверять без unsafe −MIN; multiplication по sign/range division checks; division rejects0 and MIN/−1. Floor/HALF_EVEN negative через sign-aware integer quotient/remainder без abs(MIN). Масштабирование,aggregation,revision increment и allocation shares проверяются до каждого intermediate.
MAX+MAX−MAX−MAX mathematically0 не оправдывает naive i64 evaluation. Wider accumulator допускается только отдельным qualified profile,не assumed.
Для nonnegative0≤C,R,F≤G≤MAX и C+R+F=G,0<a≤F reserve/consume сохраняют bound≤G; это MATH_DERIVED при trusted state и atomic transaction,не runtime CAS proof.

Allocation shares: proposed exact rational p/q≥0,q>0,sum≤1; первые4 grants floor(G×share),Residual=G−Σ4. Intermediate G×p checked;если overflow и нет approved wide/reduced algorithm — REJECT даже при конечном fit. No extra emission from rounding.

## Projected money и ошибки floating calculations

Raw captured binary64 body equality exact finite (Z only if selected),без epsilon. Preview calculations имеют отдельный profile/units/input/output/intermediate checks,underflow и error interval.
Для preview margin require lower bound m_low>0,не просто double m>0: m_low=G_low−Loss_high−Buffer_high. Unknown numeric error bound → UNAVAILABLE. Sub-unit loss0.004 не округляется до0 ради gate. Overflow/NaN/Inf → reject/error; positive underflow changing sign/cap proof → unavailable.
Posting exact money не создаёт source authority. Independent receipt и D14 inventory нужны дополнительно.

## Price/volume grids

AllowedPrice={O_p+k×TickSize:k integer,price>0,in approved band}.
AllowedActiveVolume={O_v+n×VolumeStep:n integer,VolumeMin≤v≤VolumeMax,v>0}.
Zero inactive optional Trend — отдельный tagged inactive case,не below-min active lot; mandatory legs не исчезают.

Exact decimal representation: parse coefficient/exponent without loss; membership iff (value−origin)/step integer плюс bounds.
Captured binary64 broker values: adapter подтверждает association с decimal/tick representation и bounded representation error; если допустимы две lattice interpretations либо numeric bound missing — UNAVAILABLE. Никакого fixed epsilon,переносящего amount между grids.
Normalize floor/ceil only purpose-specific;после normalize повторить all gates. Price не округлять по SYMBOL_DIGITS вместо tick.
Current code S18 uses zero-origin;Docs14:9 Vmin+nstep. При min0.03,step0.02: zero-origin permits0.04,not0.03;min-origin permits0.03,not0.04. Не утверждать совместимость без profile evidence. Active lots ниже min reject.

## Candidate canonical encoding

29 fixed ordered fields:
SchemaVersion,Broker,Server,AccountLogin,Symbol,Magic,CycleID,DealTicket,OrderTicket,PositionIdentifier,ActionID,EventID,Role,EntryType,DealType,TimestampMsc,Volume,Price,Profit,Swap,Commission,Fee,DealNet,Currency,Precision,SourcePlanApplicable,SourcePlan,SourcePolicyApplicable,SourcePolicyVersion.

Fields encoded as name-token then value-token in that order. SchemaType determines domain;wire positive unsigned tag не разрешает account>signedMAX. IDs exact;account/timestamp positive signed64;magic nonzero signed64;tickets/cycle/action/event positive ulong;SourcePlan/Policy absent only explicit applicabilityfalse. Unknown applicability не false.
Role/Entry/Deal wire strings require closed mapping manifest;sample BigCore/OUT/SELL из golden не полный production table.
Strings byteLength UTF8,not UTF16 StringLen;no NUL;no Unicode normalization.

F64Z candidate: header ASCII HSBI-F64Z-1 +00; s+uint32BE length+UTF8; u+uint64BE nonnegative ints; i+two's-complement signed64BE negative only; b+ASCII0/1;n absent;d+8 finite IEEE754 binary64BE. Signed positive через i,−0 bits в canonical wire,NaN/Inf reject as noncanonical/invalid. Negative zero input normalized to+0 only by approved Z encoder; strict decoder rejects noncanonical −0 wire. Names encoded as s. Native bit reconstruction/endianness/shifts/subnormals unqualified.
T17Z candidate: ASCII HSBI-T17Z-1+LF;s<byteLength>:UTF8;i<length>:canonical decimal integer;d<length>:exact scientific17 token (1digit,16 decimals,e±DDD);b0/b1;n0:. Canonical integers no leading+/zeros/−0;formatter must match exact golden,not just any roundtrip. Strict shortest? scientific17 is fixed-width,not shortest;do not substitute shortest formatter.
Decoder before allocation checks caps,exact lengths,tags,names/order,duplicates,trailing bytes,invalid UTF8,unsupported schemas/versions,nonfinite,out-of-domain fields. Wellformed unknown version→UNAVAILABLE;malformed→REJECT.
No final codec choice. If raw negative-zero bit preservation required,neither Z candidate fits without new profile.

Logical SourceKey canonical representation is typed projection of the four validated fields in fixed order under chosen codec,not delimiter concatenation. Projection equality is semantic;standalone byte header/profile must be bound in receipt. For F64 typed projection K(B1,S1,1,11) bytes:
730000000242317300000002533175000000000000000175000000000000000b
Это substructure vector,не новый approved record codec. Codec/schema/source body receipt separation avoids alias grants.

## Replay и migration

Validate full body+source+receipt before NO_OP. Schema/codec new bytes не new source;same K/changed component CONFLICT даже equal net. Unknown old namespace/profile/consumed/applied events→quarantine. Missing fields не default/currentterminal facts. Preserve old bytes/expected;append mapping receipt;transaction uniqueness+source balance+revision atomic. Raw source codec не делает raw→posted conversion.

## Критерии freeze и unresolved

Freeze допускается только при owner text approval D10/D11/D12/D15,filled profiles with independently verified receipts,closed mapping tables,selected codec/caps,complete vectors/native logs,explicit legacy mapping и source/provider trust.
Предложенный D0…8,resource caps и binary64 domain — candidate capability limits,не факты брокера. Все UNBOUND fields production BLOCKED.
Native labels NOT_RUN,hostile decoder NOT_RUN. Historical R0F116PASS/R0G128PASS только Python reference evidence;не MQL.
Связи: [vectors](HSBI_03E_NUMERIC_TEST_VECTORS_RU.md),[D06](HSBI_03E_D06_POLICY_RESOLUTION_RU.md),[snapshot](HSBI_03E_SNAPSHOT_AUTHORITY_CONTRACT_RU.md),[bundles](HSBI_03E_CONTRACT_DEPENDENCY_RECONCILIATION_RU.md),[gates](HSBI_03E_R11_GATE_MATRIX_RU.md).
