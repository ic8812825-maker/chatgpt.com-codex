from openpyxl import Workbook
from openpyxl.styles import Font

BOLD = Font(bold=True)


def hdr(ws, row, cols):
    for i, c in enumerate(cols, 1):
        cell = ws.cell(row=row, column=i, value=c)
        cell.font = BOLD


def add_settings(ws):
    hdr(ws, 1, ["Field", "Value"])
    rows = [
        ("Symbol", "EURUSD"), ("Point", 0.0001), ("PointValuePerLot", 1), ("StepPoints", 100),
        ("MinLot", 0.01), ("LotStep", 0.01), ("MaxActiveSections", 4), ("ReservePercent", 0.20),
        ("RecoveryPercent", 0.80), ("BasketTarget", 0), ("MaxSpreadPoints", 20),
        ("CommissionPerLot", 0), ("SwapPerLot", 0), ("MaxTotalLot", 20), ("MaxNetLot", 10),
        ("GlobalReserve", 0), ("RecoveryFund", 0),
    ]
    for r, (k, v) in enumerate(rows, 2):
        ws.cell(r, 1, k); ws.cell(r, 2, v)

    hdr(ws, 20, ["Level", "BigRatio", "SmallRatio"])
    for r, row in enumerate([(1, 0.40, 0.15), (2, 0.25, 0.10), (3, 0.15, 0.06), (4, 0.10, 0.04)], 21):
        ws.cell(r, 1, row[0]); ws.cell(r, 2, row[1]); ws.cell(r, 3, row[2])


def add_positions(ws):
    hdr(ws, 1, ["Ticket", "Type", "Role", "Lot", "OpenPrice", "CurrentPrice", "PointsPnL", "MoneyPnL", "IsTail", "SectionID"])
    rows = [
        [10001, "BUY", "MAIN", 1.00, 1.2300, 1.2300, None, None, "NO", ""],
        [10002, "SELL", "TAIL", 1.00, 1.2300, 1.2300, None, None, "YES", ""],
        [10003, "SELL", "SECTION_BIG", 0.40, 1.2350, 1.2300, None, None, "NO", "S1"],
        [10004, "BUY", "SECTION_SMALL", 0.15, 1.2350, 1.2300, None, None, "NO", "S1"],
    ]
    for r, row in enumerate(rows, 2):
        for c, v in enumerate(row, 1):
            ws.cell(r, c, v)
        ws.cell(r, 7, f'=IF(B{r}="BUY",(F{r}-E{r})/Settings!$B$3,(E{r}-F{r})/Settings!$B$3)')
        ws.cell(r, 8, f'=G{r}*D{r}*Settings!$B$4')


def add_scenario(ws, direction):
    up = direction == "UP"
    move = "MoveUpPoints" if up else "MoveDownPoints"
    sign = "+" if up else "-"
    loss_type = "SELL" if up else "BUY"

    hdr(ws, 1, ["Field", "Value"])
    ws["A2"] = "CurrentPrice"; ws["B2"] = "=CurrentPositions!F2"
    ws["A3"] = move; ws["B3"] = 100
    ws["A4"] = "ScenarioPrice"; ws["B4"] = f"=B2{sign}B3*Settings!$B$3"

    hdr(ws, 6, ["Ticket", "Type", "Role", "Lot", "OpenPrice", "ScenarioPrice", "ScenarioPointsPnL", "ScenarioMoneyPnL", "IsTail", "SectionID"])
    for r in range(2, 102):
        rr = r + 5
        ws.cell(rr, 1, f"=CurrentPositions!A{r}")
        ws.cell(rr, 2, f"=CurrentPositions!B{r}")
        ws.cell(rr, 3, f"=CurrentPositions!C{r}")
        ws.cell(rr, 4, f"=CurrentPositions!D{r}")
        ws.cell(rr, 5, f"=CurrentPositions!E{r}")
        ws.cell(rr, 6, "=$B$4")
        ws.cell(rr, 7, f'=IF(B{rr}="BUY",(F{rr}-E{rr})/Settings!$B$3,(E{rr}-F{rr})/Settings!$B$3)')
        ws.cell(rr, 8, f"=G{rr}*D{rr}*Settings!$B$4")
        ws.cell(rr, 9, f"=CurrentPositions!I{r}")
        ws.cell(rr, 10, f"=CurrentPositions!J{r}")

    ws["A110"] = "TailType"; ws["B110"] = loss_type
    ws["A111"] = "TailTicket"; ws["B111"] = f'=IFERROR(INDEX(A7:A106,MATCH(MINIFS(H7:H106,B7:B106,"{loss_type}",H7:H106,"<0"),H7:H106,0)),"N/A")'
    ws["A112"] = "TailLot"; ws["B112"] = '=IF(B111="N/A",0,XLOOKUP(B111,A7:A106,D7:D106,0))'
    ws["A113"] = "TailOpenPrice"; ws["B113"] = '=IF(B111="N/A",0,XLOOKUP(B111,A7:A106,E7:E106,0))'
    ws["A114"] = "TailLossMoney"; ws["B114"] = '=IF(B111="N/A",0,ABS(XLOOKUP(B111,A7:A106,H7:H106,0)))'
    ws["A115"] = "TailLossPerLot"; ws["B115"] = '=IF(B112=0,0,ABS(B114/B112))'

    ws["D1"] = "AverageBuyPrice"; ws["E1"] = '=IFERROR(SUMPRODUCT((B7:B106="BUY")*E7:E106*D7:D106)/SUMIFS(D7:D106,B7:B106,"BUY"),0)'
    ws["D2"] = "AverageSellPrice"; ws["E2"] = '=IFERROR(SUMPRODUCT((B7:B106="SELL")*E7:E106*D7:D106)/SUMIFS(D7:D106,B7:B106,"SELL"),0)'
    ws["D3"] = "Center"; ws["E3"] = '=(E1+E2)/2'
    for lvl in range(1, 5):
        ws.cell(3 + lvl, 4, f"UpperLevel{lvl}")
        ws.cell(3 + lvl, 5, f"=E3+{lvl}*Settings!$B$5*Settings!$B$3")
        ws.cell(8 + lvl, 4, f"LowerLevel{lvl}")
        ws.cell(8 + lvl, 5, f"=E3-{lvl}*Settings!$B$5*Settings!$B$3")


def add_section_calc(ws, scenario_sheet):
    hdr(ws, 1, ["Field", "Value"])
    rows = [
        ("TailType", f"={scenario_sheet}!B110"), ("TailLot", f"={scenario_sheet}!B112"), ("NextLevel", 1),
        ("BigRatio", '=XLOOKUP(B4,Settings!A21:A24,Settings!B21:B24)'), ("SmallRatio", '=XLOOKUP(B4,Settings!A21:A24,Settings!C21:C24)'),
        ("BigType", '=IF(B2="BUY","BUY","SELL")'), ("SmallType", '=IF(B2="BUY","SELL","BUY")'),
        ("BigLotRaw", '=B3*B5'), ("SmallLotRaw", '=B3*B6'),
        ("BigLot", '=FLOOR(B9,Settings!$B$7)'), ("SmallLot", '=FLOOR(B10,Settings!$B$7)'),
        ("ActiveSections", '=COUNTIFS(CurrentPositions!C2:C200,"SECTION_BIG")'),
        ("TotalLotAfterOpen", '=SUM(CurrentPositions!D2:D200)+B11+B12'),
        ("NetLotAfterOpen", '=ABS(SUMIFS(CurrentPositions!D2:D200,CurrentPositions!B2:B200,"BUY")+IF(B7="BUY",B11,0)+IF(B8="BUY",B12,0)-SUMIFS(CurrentPositions!D2:D200,CurrentPositions!B2:B200,"SELL")-IF(B7="SELL",B11,0)-IF(B8="SELL",B12,0))'),
        ("CanOpenSection", '=IF(AND(B11>=Settings!$B$6,B12>=Settings!$B$6,B12<B11,B11<=B3,B13<Settings!$B$8,B14<=Settings!$B$15,B15<=Settings!$B$16),"YES","NO")'),
    ]
    for r, (k, v) in enumerate(rows, 2): ws.cell(r, 1, k); ws.cell(r, 2, v)

    hdr(ws, 20, ["SectionID", "BigType", "BigLot", "BigOpenPrice", "SmallType", "SmallLot", "SmallOpenPrice", "ScenarioPrice", "BigPnL", "SmallPnL", "Costs", "CycleProfit", "CanCloseSection", "ReserveAdd", "RecoveryAdd", "NewGlobalReserve", "NewRecoveryFund"])
    ws["A21"] = "S1"
    ws["B21"] = '=INDEX(CurrentPositions!B2:B200,MATCH("SECTION_BIG",CurrentPositions!C2:C200,0))'
    ws["C21"] = '=INDEX(CurrentPositions!D2:D200,MATCH("SECTION_BIG",CurrentPositions!C2:C200,0))'
    ws["D21"] = '=INDEX(CurrentPositions!E2:E200,MATCH("SECTION_BIG",CurrentPositions!C2:C200,0))'
    ws["E21"] = '=INDEX(CurrentPositions!B2:B200,MATCH("SECTION_SMALL",CurrentPositions!C2:C200,0))'
    ws["F21"] = '=INDEX(CurrentPositions!D2:D200,MATCH("SECTION_SMALL",CurrentPositions!C2:C200,0))'
    ws["G21"] = '=INDEX(CurrentPositions!E2:E200,MATCH("SECTION_SMALL",CurrentPositions!C2:C200,0))'
    ws["H21"] = f'={scenario_sheet}!B4'
    ws["I21"] = '=IF(B21="BUY",(H21-D21)/Settings!$B$3*C21*Settings!$B$4,(D21-H21)/Settings!$B$3*C21*Settings!$B$4)'
    ws["J21"] = '=IF(E21="BUY",(H21-G21)/Settings!$B$3*F21*Settings!$B$4,(G21-H21)/Settings!$B$3*F21*Settings!$B$4)'
    ws["K21"] = '=((Settings!$B$11*2)*Settings!$B$4*(C21+F21))+(Settings!$B$12*(C21+F21))+(Settings!$B$13*(C21+F21))'
    ws["L21"] = '=I21+J21-K21'
    ws["M21"] = '=IF(L21>0,"YES","NO")'
    ws["N21"] = '=IF(L21>0,L21*Settings!$B$9,0)'
    ws["O21"] = '=IF(L21>0,L21*Settings!$B$10,0)'
    ws["P21"] = '=Settings!$B$17+N21'
    ws["Q21"] = '=Settings!$B$18+O21'


def add_tail_recovery(ws, section_sheet, scenario_sheet):
    hdr(ws, 1, ["Field", "Value"])
    rows = [
        ("TailType", f"={scenario_sheet}!B110"), ("TailTicket", f"={scenario_sheet}!B111"), ("TailLot", f"={scenario_sheet}!B112"),
        ("TailLossMoney", f"={scenario_sheet}!B114"), ("TailLossPerLot", f"={scenario_sheet}!B115"),
        ("CanCloseSection", f"={section_sheet}!M21"), ("RecoveryFundAfterCycle", f"={section_sheet}!Q21"),
        ("CloseLotRaw", '=IF(OR(B6<>"YES",B5=0),0,B7/B5)'), ("CloseLotRounded", '=FLOOR(B8,Settings!$B$7)'),
        ("CloseLotFinal", '=MIN(B9,B3)'), ("CloseAllowed", '=IF(AND(B6="YES",B10>=Settings!$B$6),"YES","NO")'),
        ("TailCloseLoss", '=B10*B5'), ("RecoveryFundAfterClose", '=B7-B12'), ("TailLotAfterClose", '=B3-B10'),
        ("Rule_TailCloseLoss<=RecoveryFund", '=IF(B12<=B7,"OK","ERROR")')
    ]
    for r, (k, v) in enumerate(rows, 2): ws.cell(r, 1, k); ws.cell(r, 2, v)


def build():
    wb = Workbook()
    wb.active.title = "Settings"
    for s in ["CurrentPositions", "Scenario_UP", "Scenario_DOWN", "SectionCalculator_UP", "SectionCalculator_DOWN", "TailRecovery_UP", "TailRecovery_DOWN", "BasketSummary", "Validation", "Log"]:
        wb.create_sheet(s)

    add_settings(wb["Settings"])
    add_positions(wb["CurrentPositions"])
    add_scenario(wb["Scenario_UP"], "UP")
    add_scenario(wb["Scenario_DOWN"], "DOWN")
    add_section_calc(wb["SectionCalculator_UP"], "Scenario_UP")
    add_section_calc(wb["SectionCalculator_DOWN"], "Scenario_DOWN")
    add_tail_recovery(wb["TailRecovery_UP"], "SectionCalculator_UP", "Scenario_UP")
    add_tail_recovery(wb["TailRecovery_DOWN"], "SectionCalculator_DOWN", "Scenario_DOWN")

    bs = wb["BasketSummary"]
    hdr(bs, 1, ["Field", "UP", "DOWN"])
    fields = ["ScenarioPrice", "BasketFloating", "GlobalReserveBefore", "GlobalReserveAfter", "RecoveryFundBefore", "RecoveryFundAfter", "TailType", "TailLotBefore", "TailLotAfter", "CloseLot", "CanCloseSection", "CanCloseTail", "CanCloseBasket", "NextAction"]
    for i, f in enumerate(fields, 2): bs.cell(i, 1, f)
    bs["B2"] = "=Scenario_UP!B4"; bs["C2"] = "=Scenario_DOWN!B4"
    bs["B3"] = "=SUM(Scenario_UP!H7:H106)"; bs["C3"] = "=SUM(Scenario_DOWN!H7:H106)"
    bs["B4"] = "=Settings!$B$17"; bs["C4"] = "=Settings!$B$17"
    bs["B5"] = "=SectionCalculator_UP!P21"; bs["C5"] = "=SectionCalculator_DOWN!P21"
    bs["B6"] = "=Settings!$B$18"; bs["C6"] = "=Settings!$B$18"
    bs["B7"] = "=TailRecovery_UP!B13"; bs["C7"] = "=TailRecovery_DOWN!B13"
    bs["B8"] = "=Scenario_UP!B110"; bs["C8"] = "=Scenario_DOWN!B110"
    bs["B9"] = "=TailRecovery_UP!B4"; bs["C9"] = "=TailRecovery_DOWN!B4"
    bs["B10"] = "=TailRecovery_UP!B14"; bs["C10"] = "=TailRecovery_DOWN!B14"
    bs["B11"] = "=TailRecovery_UP!B10"; bs["C11"] = "=TailRecovery_DOWN!B10"
    bs["B12"] = "=SectionCalculator_UP!M21"; bs["C12"] = "=SectionCalculator_DOWN!M21"
    bs["B13"] = "=TailRecovery_UP!B11"; bs["C13"] = "=TailRecovery_DOWN!B11"
    bs["B14"] = '=IF(B3+B5>=Settings!$B$10,"YES","NO")'; bs["C14"] = '=IF(C3+C5>=Settings!$B$10,"YES","NO")'
    bs["B15"] = '=IF(B14="YES","BASKET_CLOSE",IF(B12="NO","WAIT",IF(B13="YES","CLOSE_SECTION+CLOSE_TAIL","CLOSE_SECTION/SAFE")))'
    bs["C15"] = '=IF(C14="YES","BASKET_CLOSE",IF(C12="NO","WAIT",IF(C13="YES","CLOSE_SECTION+CLOSE_TAIL","CLOSE_SECTION/SAFE")))'

    v = wb["Validation"]
    hdr(v, 1, ["Rule", "UP Status", "DOWN Status"])
    rules = [
        ("Tail close only if section profit > 0", '=IF(OR(SectionCalculator_UP!L21>0,TailRecovery_UP!B10=0),"OK","ERROR")', '=IF(OR(SectionCalculator_DOWN!L21>0,TailRecovery_DOWN!B10=0),"OK","ERROR")'),
        ("TailCloseLoss <= RecoveryFundAfterCycle", '=IF(TailRecovery_UP!B12<=TailRecovery_UP!B7,"OK","ERROR")', '=IF(TailRecovery_DOWN!B12<=TailRecovery_DOWN!B7,"OK","ERROR")'),
        ("BigLot <= TailLot", '=IF(SectionCalculator_UP!B11<=SectionCalculator_UP!B3,"OK","ERROR")', '=IF(SectionCalculator_DOWN!B11<=SectionCalculator_DOWN!B3,"OK","ERROR")'),
        ("SmallLot < BigLot", '=IF(SectionCalculator_UP!B12<SectionCalculator_UP!B11,"OK","ERROR")', '=IF(SectionCalculator_DOWN!B12<SectionCalculator_DOWN!B11,"OK","ERROR")'),
        ("MaxActiveSections", '=IF(SectionCalculator_UP!B13<=Settings!$B$8,"OK","ERROR")', '=IF(SectionCalculator_DOWN!B13<=Settings!$B$8,"OK","ERROR")'),
        ("MaxTotalLot", '=IF(SectionCalculator_UP!B14<=Settings!$B$15,"OK","ERROR")', '=IF(SectionCalculator_DOWN!B14<=Settings!$B$15,"OK","ERROR")'),
        ("MaxNetLot", '=IF(SectionCalculator_UP!B15<=Settings!$B$16,"OK","ERROR")', '=IF(SectionCalculator_DOWN!B15<=Settings!$B$16,"OK","ERROR")'),
    ]
    for r, row in enumerate(rules, 2):
        for c, val in enumerate(row, 1): v.cell(r, c, val)

    log = wb["Log"]
    log["A1"] = '="NEXT ACTION UP:"&CHAR(10)&"Price="&TEXT(BasketSummary!B2,"0.00000")&CHAR(10)&"CycleProfit="&TEXT(SectionCalculator_UP!L21,"0.00")&CHAR(10)&"CanCloseSection="&BasketSummary!B12&CHAR(10)&"CloseTailLot="&TEXT(BasketSummary!B11,"0.00")&CHAR(10)&"TailAfter="&TEXT(BasketSummary!B10,"0.00")&CHAR(10)&"Next="&BasketSummary!B15'
    log["A2"] = '="NEXT ACTION DOWN:"&CHAR(10)&"Price="&TEXT(BasketSummary!C2,"0.00000")&CHAR(10)&"CycleProfit="&TEXT(SectionCalculator_DOWN!L21,"0.00")&CHAR(10)&"CanCloseSection="&BasketSummary!C12&CHAR(10)&"CloseTailLot="&TEXT(BasketSummary!C11,"0.00")&CHAR(10)&"TailAfter="&TEXT(BasketSummary!C10,"0.00")&CHAR(10)&"Next="&BasketSummary!C15'

    wb.save("recovery_lock_cascade_next_step.xlsx")


if __name__ == "__main__":
    build()
    print("Created recovery_lock_cascade_next_step.xlsx")
