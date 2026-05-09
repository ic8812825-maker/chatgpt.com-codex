# Recovery Lock Cascade Logic Verification

## CHECK 1 TailTicket: PASS
**Формулы:**
- `Scenario_UP!B221 = MINIFS(H7:H206,B7:B206,"SELL",H7:H206,"<0")`
- `Scenario_UP!B222 = IFERROR(MINIFS(A7:A206,B7:B206,"SELL",H7:H206,B221),"N/A")`
- `Scenario_DOWN!B221 = MINIFS(H7:H206,B7:B206,"BUY",H7:H206,"<0")`
- `Scenario_DOWN!B222 = IFERROR(MINIFS(A7:A206,B7:B206,"BUY",H7:H206,B221),"N/A")`

**Тест UP (равный убыток):**
- SELL tickets: `10010 -> -50`, `10005 -> -50`, `10020 -> -10`
- `TailWorstPnL = -50`
- `TailTicket = MIN(ticket where pnl=-50) = 10005`

**Тест DOWN (равный убыток):**
- BUY tickets: `20012 -> -80`, `20003 -> -80`, `20030 -> -20`
- `TailWorstPnL = -80`
- `TailTicket = MIN(ticket where pnl=-80) = 20003`

**Результат:** детерминированный выбор минимального Ticket при равном убытке.

---

## CHECK 2 NextSection: PASS
**Формулы:**
- `TailRecovery_UP!B16 = FLOOR(B14*XLOOKUP(B15,Settings!A21:A24,Settings!B21:B24),Settings!$B$7)`
- `TailRecovery_UP!B17 = FLOOR(B14*XLOOKUP(B15,Settings!A21:A24,Settings!C21:C24),Settings!$B$7)`
- Аналогично на `TailRecovery_DOWN`.

**Тест:**
- `TailLotAfterClose (B14)=0.14`
- `NextLevel (B15)=2`
- `BigRatio(L2)=0.25`, `SmallRatio(L2)=0.10`
- `LotStep=0.01`

**Ожидание:**
- `NextBigLotAfterRecovery = FLOOR(0.14*0.25,0.01)=0.03`
- `NextSmallLotAfterRecovery = FLOOR(0.14*0.10,0.01)=0.01`

**Результат:** формулы используют `TailLotAfterClose` и `NextLevel`, не Level 1.

---

## CHECK 3 NoOppositeCascade inside CanOpenSection: PASS
**Формулы:**
- `SectionCalculator_UP!B13 = IF(B2="SELL",IF(COUNTIFS(CurrentPositions!B2:B500,"BUY",CurrentPositions!C2:C500,"SECTION_BIG")=0,"YES","NO"),...)`
- `SectionCalculator_UP!B14 = IF(AND(...,B12="YES",B13="YES"),"YES","NO")`
- Аналогично на DOWN.

**Тест UP:**
- TailType=`SELL`
- Есть встречный `BUY + SECTION_BIG`
- `NoOppositeCascade = NO`
- При `LevelReached=YES` и корректных лимитах всё равно `CanOpenSection=NO`

**Результат:** зависимость включена напрямую в `CanOpenSection`.

---

## CHECK 4 Costs via FULL_CYCLE: PASS
**Формула:**
- `SectionCalculator_UP!K21 = LET(Lots,C21+F21,Mult,IF(Settings!$B$19="FULL_CYCLE",2,1),SpreadCost,Settings!$B$12*Settings!$B$4*Lots*Mult,CommissionCost,Settings!$B$13*Lots*Mult,SwapCost,Settings!$B$14*Lots,SpreadCost+CommissionCost+SwapCost)`

**Тест:**
- `CostMode=FULL_CYCLE`
- `SpreadPoints=20`, `PointValuePerLot=1`
- `BigLot=0.40`, `SmallLot=0.15`, `Lots=0.55`
- `CommissionPerLot=0`, `SwapPerLot=0`

**Ожидание:**
- `SpreadCost=20*1*0.55*2=22`
- `CommissionCost=0`
- `SwapCost=0`
- `Costs=22`

**Результат:** совпадает.

---

## CHECK 5 CanCloseBasket uses Settings!B11: PASS
**Формулы:**
- `BasketSummary!B10 = IF(B3+B4>=Settings!$B$11,"YES","NO")`
- `BasketSummary!C10 = IF(C3+C4>=Settings!$B$11,"YES","NO")`

**Тест:**
- `BasketFloating=-12`, `GlobalReserveAfter=18`, `BasketTarget=0`
- `-12 + 18 >= 0 -> YES`

**Результат:** ссылка на `Settings!B11` корректна.

---

## CHECK 6 CloseLot only if CanCloseSection=YES: PASS
**Формулы:**
- `TailRecovery_UP!B8 = IF(OR(B6<>"YES",B5=0),0,B7/B5)`
- `TailRecovery_UP!B10 = IF(B6="YES",MIN(B9,B4),0)`
- `TailRecovery_UP!B11 = IF(AND(B10>=Settings!$B$6,B6="YES"),"YES","NO")`
- Аналогично на DOWN.

**Тест:**
- `CycleProfit<=0 -> CanCloseSection=NO`
- Даже если `RecoveryFundAfterCycle>0` и `TailLossPerLot>0`:
  - `CloseLotRaw=0`
  - `CloseLotFinal=0`
  - `CloseAllowed=NO`

**Результат:** защита выполнена.

---

## FINAL
**recovery_lock_cascade_next_step.xlsx расчётно принят.**

Все 6 проверок: **PASS**.
