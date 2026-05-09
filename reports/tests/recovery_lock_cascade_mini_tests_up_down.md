# Mini Tests UP/DOWN

## UP Mini Test
- Tail tie-case: SELL tickets 10010(-50),10005(-50),10020(-10)
- Expected TailTicket: 10005
- Section gate: CanCloseSection=NO -> CloseLotRaw=0 -> CloseAllowed=NO
- Basket close example: BasketFloating=-12, GlobalReserveAfter=18, BasketTarget=0 => YES

## DOWN Mini Test
- Tail tie-case: BUY tickets 20012(-80),20003(-80),20030(-20)
- Expected TailTicket: 20003
- Next section from recovery: TailLotAfterClose=0.14, NextLevel=2
  - Big=0.03, Small=0.01
- NoOppositeCascade=NO -> CanOpenSection=NO
