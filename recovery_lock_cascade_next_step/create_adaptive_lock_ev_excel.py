from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment

BOLD = Font(bold=True)


def hdr(ws, row, cols):
    for i, c in enumerate(cols, 1):
        ws.cell(row=row, column=i, value=c).font = BOLD


def add_settings(ws):
    hdr(ws, 1, ["Field", "Value"])
    rows = [
        ("Symbol", "EURUSD"), ("Point", 0.0001), ("PointValuePerLot", 1), ("StepPoints", 100), ("MinLot", 0.01), ("LotStep", 0.01),
        ("MaxActiveSections", 4), ("ReservePercent", 0.2), ("RecoveryPercent", 0.8), ("BasketTarget", 0), ("MaxSpreadPoints", 20),
        ("CommissionPerLot", 0), ("SwapPerLot", 0), ("MaxTotalLot", 20), ("MaxNetLot", 10), ("GlobalReserve", 0), ("RecoveryFund", 0), ("CostMode", "FULL_CYCLE")
    ]
    for r, (k, v) in enumerate(rows, 2):
        ws.cell(r, 1, k); ws.cell(r, 2, v)
    hdr(ws, 20, ["Level", "BigRatio", "SmallRatio"])
    for r, row in enumerate([(1, 0.40, 0.15), (2, 0.25, 0.10), (3, 0.15, 0.06), (4, 0.10, 0.04)], 21):
        ws.cell(r, 1, row[0]); ws.cell(r, 2, row[1]); ws.cell(r, 3, row[2])


def add_positions(ws):
    hdr(ws, 1, ["Ticket", "Type", "Role", "Lot", "OpenPrice", "CurrentPrice", "PointsPnL", "MoneyPnL", "IsTail", "SectionID"])
    demo = [
        [10001, "BUY", "MAIN", 1.00, 1.2300, 1.2300, None, None, "NO", ""], [10002, "SELL", "TAIL", 1.00, 1.2300, 1.2300, None, None, "YES", ""],
        [10003, "SELL", "SECTION_BIG", 0.40, 1.2350, 1.2300, None, None, "NO", "S1"], [10004, "BUY", "SECTION_SMALL", 0.15, 1.2350, 1.2300, None, None, "NO", "S1"],
    ]
    for r, row in enumerate(demo, 2):
        for c, v in enumerate(row, 1): ws.cell(r, c, v)
        ws.cell(r, 7, f'=IF(B{r}="BUY",(F{r}-E{r})/Settings!$B$3,(E{r}-F{r})/Settings!$B$3)')
        ws.cell(r, 8, f'=G{r}*D{r}*Settings!$B$4')


def add_scenario(ws, direction):
    up = direction == "UP"
    loss_type = "SELL" if up else "BUY"
    hdr(ws, 1, ["Field", "Value"])
    ws["A2"] = "CurrentPrice"; ws["B2"] = "=CurrentPositions!F2"
    ws["A3"] = "MoveUpPoints" if up else "MoveDownPoints"; ws["B3"] = 100
    ws["A4"] = "ScenarioPrice"; ws["B4"] = "=B2+B3*Settings!$B$3" if up else "=B2-B3*Settings!$B$3"
    hdr(ws, 6, ["Ticket", "Type", "Role", "Lot", "OpenPrice", "ScenarioPrice", "ScenarioPointsPnL", "ScenarioMoneyPnL", "IsTail", "SectionID"])
    for r in range(2, 202):
        rr = r + 5
        ws.cell(rr, 1, f"=CurrentPositions!A{r}"); ws.cell(rr, 2, f"=CurrentPositions!B{r}"); ws.cell(rr, 3, f"=CurrentPositions!C{r}")
        ws.cell(rr, 4, f"=CurrentPositions!D{r}"); ws.cell(rr, 5, f"=CurrentPositions!E{r}"); ws.cell(rr, 6, "=$B$4")
        ws.cell(rr, 7, f'=IF(B{rr}="BUY",(F{rr}-E{rr})/Settings!$B$3,(E{rr}-F{rr})/Settings!$B$3)'); ws.cell(rr, 8, f"=G{rr}*D{rr}*Settings!$B$4")
        ws.cell(rr, 9, f"=CurrentPositions!I{r}"); ws.cell(rr, 10, f"=CurrentPositions!J{r}")
    ws["A220"] = "TailType"; ws["B220"] = loss_type
    ws["A221"] = "TailWorstPnL"; ws["B221"] = f'=IFERROR(MIN(IF((B7:B206="{loss_type}")*(H7:H206<0),H7:H206)),0)'
    ws["A222"] = "TailTicket"; ws["B222"] = f'=IFERROR(MIN(IF((B7:B206="{loss_type}")*(H7:H206=B221),A7:A206)),"N/A")'
    ws["A223"] = "TailLot"; ws["B223"] = '=IF(B222="N/A",0,INDEX(D7:D206,MATCH(B222,A7:A206,0)))'
    ws["A224"] = "TailLossMoney"; ws["B224"] = '=IF(B222="N/A",0,ABS(INDEX(H7:H206,MATCH(B222,A7:A206,0))))'
    ws["A225"] = "TailLossPerLot"; ws["B225"] = '=IF(B223=0,0,ABS(B224/B223))'
    ws["D1"] = "AverageBuyPrice"; ws["E1"] = '=IFERROR(SUMPRODUCT((B7:B206="BUY")*E7:E206*D7:D206)/SUMIFS(D7:D206,B7:B206,"BUY"),0)'
    ws["D2"] = "AverageSellPrice"; ws["E2"] = '=IFERROR(SUMPRODUCT((B7:B206="SELL")*E7:E206*D7:D206)/SUMIFS(D7:D206,B7:B206,"SELL"),0)'
    ws["D3"] = "Center"; ws["E3"] = '=(E1+E2)/2'
    for lvl in range(1, 5):
        ws.cell(3 + lvl, 4, f"UpperLevel{lvl}"); ws.cell(3 + lvl, 5, f"=E3+{lvl}*Settings!$B$5*Settings!$B$3")
        ws.cell(8 + lvl, 4, f"LowerLevel{lvl}"); ws.cell(8 + lvl, 5, f"=E3-{lvl}*Settings!$B$5*Settings!$B$3")


def add_section_calc(ws, scenario_sheet, up):
    hdr(ws, 1, ["Field", "Value"])
    ws["A2"] = "TailType"; ws["B2"] = f"={scenario_sheet}!B220"
    ws["A3"] = "TailLot"; ws["B3"] = f"={scenario_sheet}!B223"
    ws["A4"] = "NextLevel"; ws["B4"] = 1
    ws["A5"] = "BigRatio"; ws["B5"] = '=INDEX(Settings!B21:B24,MATCH(B4,Settings!A21:A24,0))'
    ws["A6"] = "SmallRatio"; ws["B6"] = '=INDEX(Settings!C21:C24,MATCH(B4,Settings!A21:A24,0))'
    ws["A7"] = "BigLot"; ws["B7"] = '=FLOOR(B3*B5,Settings!$B$7)'
    ws["A8"] = "SmallLot"; ws["B8"] = '=FLOOR(B3*B6,Settings!$B$7)'
    ws["A9"] = "ActiveSections"; ws["B9"] = '=COUNTIFS(CurrentPositions!C2:C500,"SECTION_BIG")'
    ws["A10"] = "TotalLotAfterOpen"; ws["B10"] = '=SUM(CurrentPositions!D2:D500)+B7+B8'
    ws["A11"] = "NetLotAfterOpen"; ws["B11"] = '=ABS(SUMIFS(CurrentPositions!D2:D500,CurrentPositions!B2:B500,"BUY")+IF(B2="BUY",B7,0)+IF(B2="SELL",B8,0)-SUMIFS(CurrentPositions!D2:D500,CurrentPositions!B2:B500,"SELL")-IF(B2="SELL",B7,0)-IF(B2="BUY",B8,0))'
    ws["A12"] = "LevelReached"
    if up:
        ws["B12"] = f'=IF({scenario_sheet}!B4>=IF(B4=1,{scenario_sheet}!E4,IF(B4=2,{scenario_sheet}!E5,IF(B4=3,{scenario_sheet}!E6,{scenario_sheet}!E7))),"YES","NO")'
    else:
        ws["B12"] = f'=IF({scenario_sheet}!B4<=IF(B4=1,{scenario_sheet}!E9,IF(B4=2,{scenario_sheet}!E10,IF(B4=3,{scenario_sheet}!E11,{scenario_sheet}!E12))),"YES","NO")'
    ws["A13"] = "NoOppositeCascade"; ws["B13"] = '=IF(B2="SELL",IF(COUNTIFS(CurrentPositions!B2:B500,"BUY",CurrentPositions!C2:C500,"SECTION_BIG")=0,"YES","NO"),IF(B2="BUY",IF(COUNTIFS(CurrentPositions!B2:B500,"SELL",CurrentPositions!C2:C500,"SECTION_BIG")=0,"YES","NO"),"NO"))'
    ws["A14"] = "CanOpenSection"; ws["B14"] = '=IF(AND(B7>=Settings!$B$6,B8>=Settings!$B$6,B8<B7,B7<=B3,B9<Settings!$B$8,B10<=Settings!$B$15,B11<=Settings!$B$16,B12="YES",B13="YES"),"YES","NO")'

    hdr(ws, 20, ["SectionID", "BigType", "BigLot", "BigOpenPrice", "SmallType", "SmallLot", "SmallOpenPrice", "ScenarioPrice", "BigPnL", "SmallPnL", "Lots", "CostMultiplier", "SpreadCost", "CommissionCost", "SwapCost", "Costs", "CycleProfit", "CanCloseSection"])
    for i in range(1, 5):
        r = 20 + i
        ws.cell(r, 1, f"S{i}")
        ws.cell(r, 2, f'=IFERROR(INDEX(CurrentPositions!B2:B500,MATCH(1,(CurrentPositions!C2:C500="SECTION_BIG")*(CurrentPositions!J2:J500=A{r}),0)),"")')
        ws.cell(r, 3, f'=IFERROR(INDEX(CurrentPositions!D2:D500,MATCH(1,(CurrentPositions!C2:C500="SECTION_BIG")*(CurrentPositions!J2:J500=A{r}),0)),0)')
        ws.cell(r, 4, f'=IFERROR(INDEX(CurrentPositions!E2:E500,MATCH(1,(CurrentPositions!C2:C500="SECTION_BIG")*(CurrentPositions!J2:J500=A{r}),0)),0)')
        ws.cell(r, 5, f'=IFERROR(INDEX(CurrentPositions!B2:B500,MATCH(1,(CurrentPositions!C2:C500="SECTION_SMALL")*(CurrentPositions!J2:J500=A{r}),0)),"")')
        ws.cell(r, 6, f'=IFERROR(INDEX(CurrentPositions!D2:D500,MATCH(1,(CurrentPositions!C2:C500="SECTION_SMALL")*(CurrentPositions!J2:J500=A{r}),0)),0)')
        ws.cell(r, 7, f'=IFERROR(INDEX(CurrentPositions!E2:E500,MATCH(1,(CurrentPositions!C2:C500="SECTION_SMALL")*(CurrentPositions!J2:J500=A{r}),0)),0)')
        ws.cell(r, 8, f'={scenario_sheet}!B4')
        ws.cell(r, 9, f'=IF(B{r}="",0,IF(B{r}="BUY",(H{r}-D{r})/Settings!$B$3*C{r}*Settings!$B$4,(D{r}-H{r})/Settings!$B$3*C{r}*Settings!$B$4))')
        ws.cell(r, 10, f'=IF(E{r}="",0,IF(E{r}="BUY",(H{r}-G{r})/Settings!$B$3*F{r}*Settings!$B$4,(G{r}-H{r})/Settings!$B$3*F{r}*Settings!$B$4))')
        ws.cell(r, 11, f'=C{r}+F{r}')
        ws.cell(r, 12, '=IF(Settings!$B$19="FULL_CYCLE",2,1)')
        ws.cell(r, 13, f'=Settings!$B$12*Settings!$B$4*K{r}*L{r}')
        ws.cell(r, 14, f'=Settings!$B$13*K{r}*L{r}')
        ws.cell(r, 15, f'=Settings!$B$14*K{r}')
        ws.cell(r, 16, f'=M{r}+N{r}+O{r}')
        ws.cell(r, 17, f'=I{r}+J{r}-P{r}')
        ws.cell(r, 18, f'=IF(Q{r}>0,"YES","NO")')
    ws["A30"] = "SelectedSectionID"; ws["B30"] = '=IFERROR(INDEX(A21:A24,MATCH("YES",R21:R24,0)),"NONE")'
    ws["A31"] = "CycleProfit"; ws["B31"] = '=IF(B30="NONE",0,INDEX(Q21:Q24,MATCH(B30,A21:A24,0)))'
    ws["A32"] = "CanCloseSection"; ws["B32"] = '=IF(B31>0,"YES","NO")'
    ws["A33"] = "ReserveAdd"; ws["B33"] = '=IF(B31>0,B31*Settings!$B$9,0)'
    ws["A34"] = "RecoveryAdd"; ws["B34"] = '=IF(B31>0,B31*Settings!$B$10,0)'
    ws["A35"] = "NewGlobalReserve"; ws["B35"] = '=Settings!$B$17+B33'
    ws["A36"] = "NewRecoveryFund"; ws["B36"] = '=Settings!$B$18+B34'


def add_tail_recovery(ws, section_sheet, scenario_sheet):
    hdr(ws, 1, ["Field", "Value"])
    rows = [
        ("TailType", f"={scenario_sheet}!B220"), ("TailTicket", f"={scenario_sheet}!B222"), ("TailLot", f"={scenario_sheet}!B223"), ("TailLossPerLot", f"={scenario_sheet}!B225"),
        ("CanCloseSection", f"={section_sheet}!B32"), ("RecoveryFundAfterCycle", f"={section_sheet}!B36"), ("CloseLotRaw", '=IF(OR(B6<>"YES",B5=0),0,B7/B5)'),
        ("CloseLotRounded", '=FLOOR(B8,Settings!$B$7)'), ("CloseLotFinal", '=IF(B6="YES",MIN(B9,B4),0)'), ("CloseAllowed", '=IF(AND(B10>=Settings!$B$6,B6="YES"),"YES","NO")'),
        ("TailCloseLoss", '=B10*B5'), ("RecoveryFundAfterClose", '=MAX(0,B7-B12)'), ("TailLotAfterClose", '=B4-B10'), ("NextLevel", f"={section_sheet}!B4"),
        ("NextBigLotAfterRecovery", '=FLOOR(B14*INDEX(Settings!B21:B24,MATCH(B15,Settings!A21:A24,0)),Settings!$B$7)'), ("NextSmallLotAfterRecovery", '=FLOOR(B14*INDEX(Settings!C21:C24,MATCH(B15,Settings!A21:A24,0)),Settings!$B$7)')
    ]
    for r, (k, v) in enumerate(rows, 2): ws.cell(r, 1, k); ws.cell(r, 2, v)



def add_recommendations(ws, direction):
    hdr(ws, 1, ["Field", "Value"])
    sc = "Scenario_UP" if direction == "UP" else "Scenario_DOWN"
    sec = "SectionCalculator_UP" if direction == "UP" else "SectionCalculator_DOWN"
    tail = "TailRecovery_UP" if direction == "UP" else "TailRecovery_DOWN"

    ws["A2"] = "Название сценария"; ws["B2"] = f'="СЦЕНАРИЙ: ЦЕНА ИДЕТ {"ВВЕРХ" if direction=="UP" else "ВНИЗ"}"'
    ws["A3"] = "Текущая цена"; ws["B3"] = f"=IFERROR({sc}!B4,0)"
    ws["A4"] = "Следующий уровень"; ws["B4"] = f'=IFERROR(IF({sec}!B4=1,{sc}!E4,IF({sec}!B4=2,{sc}!E5,IF({sec}!B4=3,{sc}!E6,IF({sec}!B4=4,{sc}!E7,"Уровень не рассчитан")))),"Уровень не рассчитан")' if direction == "UP" else f'=IFERROR(IF({sec}!B4=1,{sc}!E9,IF({sec}!B4=2,{sc}!E10,IF({sec}!B4=3,{sc}!E11,IF({sec}!B4=4,{sc}!E12,"Уровень не рассчитан")))),"Уровень не рассчитан")'
    ws["A5"] = "Расстояние до уровня, пунктов"; ws["B5"] = '=IF(OR(B4="Уровень не рассчитан",B3=""),"Уровень не рассчитан",ROUND(ABS(B4-B3)*10000,0))'
    ws["A6"] = "Большая позиция"; ws["B6"] = f'=IFERROR(IF({tail}!B16>0,IF("{direction}"="UP","SELL ","BUY ")&TEXT({tail}!B16,"0.00"),"Не открывать"),"Не открывать")'
    ws["A7"] = "Малая защитная позиция"; ws["B7"] = f'=IFERROR(IF({tail}!B17>0,IF("{direction}"="UP","BUY ","SELL ")&TEXT({tail}!B17,"0.00"),"Не открывать"),"Не открывать")'
    ws["A8"] = "Уровень секции"; ws["B8"] = f"=IFERROR({sec}!B4,0)"
    ws["A9"] = "Причина"; ws["B9"] = f'=IF({sec}!B14="YES","цена достигла уровня; хвост найден; риск-лимиты OK","секция сейчас недоступна: уровень/риск-гейт/хвост")'

    ws["A11"] = "Проверки риска"
    ws["A12"] = "Можно открыть секцию"; ws["B12"] = f'=IF({sec}!B14="YES","ДА","НЕТ")'
    ws["A13"] = "Нет встречного каскада"; ws["B13"] = f'=IF({sec}!B13="YES","ДА","НЕТ")'
    ws["A14"] = "Можно закрыть секцию"; ws["B14"] = f'=IF({sec}!B32="YES","ДА","НЕТ")'
    ws["A15"] = "Можно закрыть хвост"; ws["B15"] = f'=IF({tail}!B11="YES","ДА","НЕТ")'

    ws["A17"] = "Прибыль цикла"; ws["B17"] = f"=IFERROR({sec}!B31,0)"
    ws["A18"] = "Добавить в резерв"; ws["B18"] = f"=IFERROR({tail}!B6,0)"
    ws["A19"] = "Добавить в RecoveryFund"; ws["B19"] = f"=IFERROR({tail}!B8,0)"

    ws["A21"] = "Тип хвоста"; ws["B21"] = f'=IF(OR({tail}!B2="",{tail}!B2="N/A"),"Хвост не найден",{tail}!B2)'
    ws["A22"] = "Лот хвоста"; ws["B22"] = f'=IFERROR(IF({tail}!B3>0,{tail}!B3,"Хвост не найден"),"Хвост не найден")'
    ws["A23"] = "Убыток хвоста"; ws["B23"] = f"=IFERROR({tail}!B12,0)"
    ws["A24"] = "RecoveryFund до закрытия"; ws["B24"] = f"=IFERROR({tail}!B5,0)"
    ws["A25"] = "Расчётный лот закрытия"; ws["B25"] = f"=IFERROR({tail}!B9,0)"
    ws["A26"] = "Округлённый лот закрытия"; ws["B26"] = f"=IFERROR({tail}!B10,0)"
    ws["A27"] = "Итоговый лот закрытия"; ws["B27"] = f"=IFERROR({tail}!B10,0)"
    ws["A28"] = "Остаток хвоста"; ws["B28"] = '=IF(OR(B22="Хвост не найден",NOT(ISNUMBER(B22))),"Хвост не найден",MAX(B22-B27,0))'
    ws["A29"] = "RecoveryFund после закрытия"; ws["B29"] = f"=IFERROR({tail}!B7,0)"

    ws["A31"] = "HumanReadableAction"
    ws["B31"] = (
        '="ПОДРОБНАЯ РЕКОМЕНДАЦИЯ"&CHAR(10)&CHAR(10)&'
        '"Сценарий: цена идет ' + ('вверх' if direction == 'UP' else 'вниз') + '."&CHAR(10)&'
        '"Текущая расчетная цена: "&TEXT(B3,"0.00000")&"."&CHAR(10)&'
        '"Следующий уровень: "&IF(ISNUMBER(B4),TEXT(B4,"0.00000"),B4)&"."&CHAR(10)&'
        '"Расстояние до уровня: "&IF(ISNUMBER(B5),TEXT(B5,"0")&" пунктов",B5)&"."&CHAR(10)&CHAR(10)&'
        '"Проверки: открыть секцию="&B12&", встречный каскад="&B13&", закрыть секцию="&B14&", закрыть хвост="&B15&"."&CHAR(10)&'
        '"Рекомендация по открытию: "&B6&" и "&B7&"."&CHAR(10)&'
        '"Хвост: "&B21&". Лот хвоста: "&IF(ISNUMBER(B22),TEXT(B22,"0.00"),B22)&"."&CHAR(10)&'
        '"Рекомендованный лот закрытия: "&IF(ISNUMBER(B27),TEXT(B27,"0.00"),"0.00")&". Остаток хвоста: "&IF(ISNUMBER(B28),TEXT(B28,"0.00"),B28)&"."&CHAR(10)&'
        '"RecoveryFund после: "&TEXT(B29,"0.00")&". Резерв после: "&TEXT(B18,"0.00")&"."&CHAR(10)&CHAR(10)&'
        '"Итоговое действие: "&IF('+('BasketSummary!B10' if direction=='UP' else 'BasketSummary!C10')+'="YES","BASKET_CLOSE",IF(B12="НЕТ","WAIT",IF(B14="ДА",IF(B15="ДА","CLOSE_SECTION+CLOSE_TAIL","CLOSE_SECTION"),"OPEN_SECTION")))&'
        '" / "&IF(OR(B12="НЕТ",B13="НЕТ"),"SAFE","NORMAL")'
    )
    ws.merge_cells("A32:H45")
    ws["A32"] = "=B31"
    ws["A32"].alignment = Alignment(wrap_text=True, vertical="top")
    ws["A32"].font = Font(bold=True, size=13, color="FFFFFFFF")
    ws["A32"].fill = PatternFill(fill_type="solid", fgColor="FF1F4E78")

def build():
    wb = Workbook(); wb.active.title = "Settings"
    for s in ["CurrentPositions", "Scenario_UP", "Scenario_DOWN", "SectionCalculator_UP", "SectionCalculator_DOWN", "TailRecovery_UP", "TailRecovery_DOWN", "BasketSummary", "Validation", "Log", "ScenarioText_UP", "ScenarioText_DOWN"]:
        wb.create_sheet(s)
    add_settings(wb["Settings"]); add_positions(wb["CurrentPositions"])
    add_scenario(wb["Scenario_UP"], "UP"); add_scenario(wb["Scenario_DOWN"], "DOWN")
    add_section_calc(wb["SectionCalculator_UP"], "Scenario_UP", True); add_section_calc(wb["SectionCalculator_DOWN"], "Scenario_DOWN", False)
    add_tail_recovery(wb["TailRecovery_UP"], "SectionCalculator_UP", "Scenario_UP"); add_tail_recovery(wb["TailRecovery_DOWN"], "SectionCalculator_DOWN", "Scenario_DOWN")

    bs = wb["BasketSummary"]; hdr(bs, 1, ["Field", "UP", "DOWN"])
    fields = ["ScenarioPrice", "BasketFloating", "GlobalReserveAfter", "RecoveryFundAfterCycle", "TailLotAfter", "CloseLot", "CanCloseSection", "CanCloseTail", "CanCloseBasket", "NextBigLot", "NextSmallLot", "NextAction", "HumanReadableAction"]
    for i, f in enumerate(fields, 2): bs.cell(i, 1, f)
    bs["B2"] = "=Scenario_UP!B4"; bs["C2"] = "=Scenario_DOWN!B4"; bs["B3"] = "=SUM(Scenario_UP!H7:H206)"; bs["C3"] = "=SUM(Scenario_DOWN!H7:H206)"
    bs["B4"] = "=SectionCalculator_UP!B35"; bs["C4"] = "=SectionCalculator_DOWN!B35"; bs["B5"] = "=TailRecovery_UP!B7"; bs["C5"] = "=TailRecovery_DOWN!B7"
    bs["B6"] = "=TailRecovery_UP!B14"; bs["C6"] = "=TailRecovery_DOWN!B14"; bs["B7"] = "=TailRecovery_UP!B10"; bs["C7"] = "=TailRecovery_DOWN!B10"
    bs["B8"] = "=SectionCalculator_UP!B32"; bs["C8"] = "=SectionCalculator_DOWN!B32"; bs["B9"] = "=TailRecovery_UP!B11"; bs["C9"] = "=TailRecovery_DOWN!B11"
    bs["B10"] = '=IF(B3+B4>=Settings!$B$11,"YES","NO")'; bs["C10"] = '=IF(C3+C4>=Settings!$B$11,"YES","NO")'
    bs["B11"] = "=TailRecovery_UP!B16"; bs["C11"] = "=TailRecovery_DOWN!B16"; bs["B12"] = "=TailRecovery_UP!B17"; bs["C12"] = "=TailRecovery_DOWN!B17"
    bs["B13"] = '=IF(B10="YES","BASKET_CLOSE",IF(B8="NO","WAIT",IF(B9="YES","CLOSE_SECTION+CLOSE_TAIL","SAFE")))'; bs["C13"] = '=IF(C10="YES","BASKET_CLOSE",IF(C8="NO","WAIT",IF(C9="YES","CLOSE_SECTION+CLOSE_TAIL","SAFE")))'
    bs["B14"] = "=ScenarioText_UP!B31"; bs["C14"] = "=ScenarioText_DOWN!B31"

    add_recommendations(wb["ScenarioText_UP"], "UP")
    add_recommendations(wb["ScenarioText_DOWN"], "DOWN")

    v = wb["Validation"]; hdr(v, 1, ["Rule", "UP", "DOWN"])
    rules = [
        ("CycleProfit > 0 before close section", '=IF(OR(SectionCalculator_UP!B31>0,SectionCalculator_UP!B32="NO"),"OK","ERROR")', '=IF(OR(SectionCalculator_DOWN!B31>0,SectionCalculator_DOWN!B32="NO"),"OK","ERROR")'),
        ("CloseLot = 0 if CanCloseSection=NO", '=IF(OR(SectionCalculator_UP!B32="YES",TailRecovery_UP!B10=0),"OK","ERROR")', '=IF(OR(SectionCalculator_DOWN!B32="YES",TailRecovery_DOWN!B10=0),"OK","ERROR")'),
        ("TailCloseLoss <= RecoveryFundAfterCycle", '=IF(TailRecovery_UP!B12<=TailRecovery_UP!B7,"OK","ERROR")', '=IF(TailRecovery_DOWN!B12<=TailRecovery_DOWN!B7,"OK","ERROR")'),
        ("LevelReached before open section", '=IF(OR(SectionCalculator_UP!B14="NO",SectionCalculator_UP!B12="YES"),"OK","ERROR")', '=IF(OR(SectionCalculator_DOWN!B14="NO",SectionCalculator_DOWN!B12="YES"),"OK","ERROR")'),
        ("No opposite cascade active", '=IF(SectionCalculator_UP!B13="YES","OK","ERROR")', '=IF(SectionCalculator_DOWN!B13="YES","OK","ERROR")')
    ]
    for r, row in enumerate(rules, 2):
        for c, x in enumerate(row, 1): ws=v; ws.cell(r, c, x)

    lg=wb["Log"]
    hdr(lg,1,["Время","Направление","Сценарий","Действие","Хвост до закрытия","Закрываемый лот хвоста","Хвост после закрытия","RecoveryFund до","RecoveryFund после","Резерв после","SAFE"])
    lg["A2"]="=NOW()"; lg["B2"]="ВВЕРХ"; lg["C2"]="ScenarioText_UP"; lg["D2"]="=BasketSummary!B13"; lg["E2"]="=TailRecovery_UP!B3"; lg["F2"]="=TailRecovery_UP!B10"; lg["G2"]="=MAX(E2-F2,0)"; lg["H2"]="=TailRecovery_UP!B5"; lg["I2"]="=TailRecovery_UP!B7"; lg["J2"]="=SectionCalculator_UP!B35"; lg['K2']='=IF(OR(SectionCalculator_UP!B14<>"YES",SectionCalculator_UP!B13<>"YES"),"YES","NO")'
    lg["A3"]="=NOW()"; lg["B3"]="ВНИЗ"; lg["C3"]="ScenarioText_DOWN"; lg["D3"]="=BasketSummary!C13"; lg["E3"]="=TailRecovery_DOWN!B3"; lg["F3"]="=TailRecovery_DOWN!B10"; lg["G3"]="=MAX(E3-F3,0)"; lg["H3"]="=TailRecovery_DOWN!B5"; lg["I3"]="=TailRecovery_DOWN!B7"; lg["J3"]="=SectionCalculator_DOWN!B35"; lg['K3']='=IF(OR(SectionCalculator_DOWN!B14<>"YES",SectionCalculator_DOWN!B13<>"YES"),"YES","NO")'
    wb.save("recovery_lock_cascade_next_step.xlsx")


if __name__ == "__main__":
    build()
    print("Created recovery_lock_cascade_next_step.xlsx")
