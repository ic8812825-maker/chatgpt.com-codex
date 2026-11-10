# R0F — numeric architecture и два codec-кандидата

BASE_SHA=ad5ce78d74c53b34358cd7508982aa888976057a

PROPOSED / AWAITING_ADMIN_APPROVAL. CONTRACT-DECISION-PREPARATION / TEST-ONLY. Не разрешение production или торговли.

| Representation | Exactness / domain | Overflow / rounding | Broker/MQL compatibility | Complexity / migration / tests |
|---|---|---|---|---|
| double boundary | Точное наблюдаемое finite binary64 значение, не истинный decimal posting | Не использовать double balance aggregation/epsilon; native conversion verified отдельно | MQL double внешний API; broker internal decimal неизвестен | Raw capture/equality only; finite/subnormal/zero vectors |
| integer minor units | Exact settled sum на известной currency/grid | Signed64 checked до операции, currency scale отдельно | long естественный кандидат, предел не брокерский account limit | Низкая арифметическая сложность, migration требует posted receipts |
| fixed-point explicit scale | Exact при общем проверенном scale | Scale multiplication/intermediates могут overflow | MQL feasible с checked/wide code после approval | Выше сложность; explicit domain/refusal/native vectors |
| exact rational reference | Математически точные суммы/множители | Arbitrary integer coefficients; не MQL native domain | Только независимый oracle | Нельзя переносить Fraction как production architecture |
| immutable raw source codec | Сохраняет observed components/IDs, отдельно от posted money | Никакого financial rounding | Два кандидата ниже, native evidence NOT_RUN | Versioned keys/compatibility; legacy four-field string недостаточна |

## A: HSBI-T17Z-1

Header `HSBI-T17Z-1` + LF, фиксированный schema field order. Имена и значения tagged: s<byteLength>:<UTF8>, i<byteLength>:<canonical integer>, d<byteLength>:<canonical scientific17>, b0/b1, n0:. Raw float — ровно1 digit перед точкой,16 после, e±DDD; finite binary64 roundtrip, zero нормализуется к+0 (Z). UTF8 exact, без NFC/casefold, без NUL; length — bytes, не StringLen characters. Record names закрыты, отсутствие/trailing/unknown data при production decode запрещены.

Технический MQL путь: StringToCharArray(CP_UTF8), integer formatting, DoubleToString scientific + canonical exponent formatting ONLY после подтверждения полного golden профиля и roundtrip. Если встроенный formatter не даёт точно предписанный token, нужен проверенный decimal-digit adapter в Extended scope либо UNAVAILABLE; нельзя объявлять любую roundtrip строку canonical. Large/small/subnormal/ties требуют native acceptance. Полностью deterministic decimal digit routine технически реализуема, но в R0F не пишется в production.

## B: HSBI-F64Z-1

Header `HSBI-F64Z-1` + NUL; те же names/order. s + uint32 byte length + UTF8; u+uint64 для nonnegative integers, i+signed64 для negative; b0/b1; n; d+8-byte finite64 big-endian. DTO schema отдельно ограничивает AccountLogin/Magic/Timestamp long и tickets ulong. Raw float bits можно реконструировать арифметически без union/unsafe casting: нормализовать finite x точными *2,/2 в [1,2), получить52 fraction bits, exponent/sign; subnormal масштабируется в integer fraction. Лимиты1023/1074 и53 significant bits следуют из binary64, не тестовых денег. В MQL нужны checked ulong shifts и проверенный native IEEE/subnormal режим. Golden mismatch отключает codec как UNAVAILABLE. Reference implementation использует этот алгоритм, independent oracle — struct.pack и literal hex.

B рекомендуется рассмотреть для raw source, но NUMERIC_CODEC_SELECTED=NO. Две формы не совпадают bytewise; совместимость — approved decoded semantic identity в одинаковой schema/zero equivalence, а не сравнение произвольных wire hashes. Unknown codec/schema/cross-version mapping UNAVAILABLE. Digest не становится broker authority.

Z-профили оба считают -0 и+0 эквивалентными. Если требуется bit-exact negative-zero preservation, эти профили не подходят без отдельного утверждённого native raw-bit capture profile; не выдавать canonical observations за неизменённый network packet. NaN/Infinity/float overflow отвергаются. Native string resource cap/array length нужно утвердить отдельно; wire uint32 length не обещает поддержать4GB в MQL. Decode до allocation проверяет approved bounds, duplicate/unknown fields, exact lengths, no trailing bytes.

## Settled conversion и ограничения

Нет raw float→posted minor units без independent posted amounts и verified broker policy. ROUND_HALF_EVEN — вариант локальной policy после verification, не универсальный брокерский закон. .005+.005 при component-rounding digits2 может дать0, aggregate-rounding1cent; нельзя выбрать по удобству. Account money digits не Symbol price digits.

G<=INT64_MAX, C/R/F>=0, G=C+R+F: при0<x<=F операции C+x/R+x не превышаютG; release ограничен owner reservation. Поэтому trusted balance transitions замкнуты без overflow. Произвольный signed sum components требует wider accumulator либо проверки каждого intermediate: MAX+MAX-MAX-MAX имеет final0, но naive long addition уже overflow. Checked(sum) Python big ints не переносится как sum-then-check MQL. Source raw float/sub-unit projected loss не округляется ради положительного proof.

Golden vectors: CODEC_GOLDENS.json и literal `hsbi_02b_r0f_independent_fixtures.py:GOLDENS/TEXT_LITERAL`, TEST_RESULTS R0F-CODEC-*. MQL5_COMPILE/MQL5_TESTS=NOT_RUN; fixture encoders не являются принятым production codec и не доказывают untrusted byte decoder.
