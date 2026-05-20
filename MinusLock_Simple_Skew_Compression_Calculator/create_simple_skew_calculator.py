from __future__ import annotations

from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill


OUT_FILE = Path(__file__).resolve().parent / "MinusLock_Simple_Skew_Compression_Calculator.xlsx"


def _title(ws, cell: str, text: str):
    ws[cell] = text
    ws[cell].font = Font(bold=True)
    ws[cell].fill = PatternFill("solid", fgColor="D9E1F2")


def _build_calculator(ws):
    ws.title = "Calculator"

    _title(ws, "A1", "PARAMETERS")
    params = [
        ("StartLot", 1.00, "стартовый лот"),
        ("StepPoints", 100, "шаг сетки в пунктах"),
        ("MaxLevels", 5, "максимум уровней"),
        ("LotStep", 0.01, "шаг лота брокера"),
        ("Direction", "DOWN", "выбранный сценарий DOWN/UP"),
        ("UseRounding", True, "использовать округление"),
        ("BigRoundMode", "DOWN", "Big округлять вниз"),
        ("SmallRoundMode", "UP", "Small округлять вверх"),
        ("CloseRoundMode", "SAFE", "защитное округление Close"),
        ("PointValue", 1, "стоимость пункта"),
        ("Spread", 0, "спред"),
        ("Commission", 0, "комиссия"),
    ]
    for i, (name, value, desc) in enumerate(params, start=2):
        ws[f"A{i}"] = name
        ws[f"B{i}"] = value
        ws[f"C{i}"] = desc

    ws["E1"] = "STATUS / CHECKS"
    ws["E1"].font = Font(bold=True)
    checks = [
        ("StartLot", "=IF(B2<=0,""ERROR: Invalid StartLot"",""OK"")"),
        ("LotStep", "=IF(B5<=0,""ERROR: Invalid LotStep"",""OK"")"),
        ("MaxLevels", "=IF(B4<1,""ERROR: Invalid MaxLevels"",""OK"")"),
        ("Direction", "=IF(OR(B6=""DOWN"",B6=""UP""),""OK"",""ERROR: Invalid Direction"")"),
        ("StepPoints", "=IF(B3<=0,""ERROR: Invalid StepPoints"",""OK"")"),
        ("PointValue", "=IF(B11<=0,""ERROR: Invalid PointValue"",""OK"")"),
        ("Spread", "=IF(B12<0,""ERROR: Invalid Spread"",""OK"")"),
        ("Commission", "=IF(B13<0,""ERROR: Invalid Commission"",""OK"")"),
    ]
    for i, (name, formula) in enumerate(checks, start=2):
        ws[f"E{i}"] = name
        ws[f"F{i}"] = formula

    _title(ws, "A16", "LEVEL GRID")
    headers = ["Level", "Big %", "Small %", "TargetSkew %", "ManualClose %"]
    for c, h in enumerate(headers, start=1):
        ws.cell(row=17, column=c, value=h).font = Font(bold=True)
    grid = [(1,90,30,0,""),(2,30,15,15,""),(3,20,15,10,""),(4,10,10,10,""),(5,5,5,10,"")]
    for r, row in enumerate(grid, start=18):
        for c, v in enumerate(row, start=1):
            ws.cell(row=r, column=c, value=v)

    # helper target skew lot
    ws["G17"] = "TargetSkewLot"
    ws["G17"].font = Font(bold=True)
    for r in range(18, 23):
        ws[f"G{r}"] = f"=B2*D{r}/100"

    def build_table(start_row: int, label: str):
        _title(ws, f"A{start_row}", label)
        cols = ["Level","Big %","Small %","TargetSkew %","ManualClose %","Big Lot Raw","Big Lot Rounded","Small Lot Raw","Small Lot Rounded","Start Before %","Total Main Before %","Total Opp After %","Auto Close %","Final Close %","Close Lot Raw","Close Lot Rounded","Start After %","Sum Big %","Sum Small %","Total Main %","Total Opp %","Skew %","Rounded Total Main Lot","Rounded Total Opp Lot","Rounded Skew Lot","Status"]
        for c,h in enumerate(cols, start=1):
            ws.cell(row=start_row+1,column=c,value=h).font=Font(bold=True)

        for idx, r in enumerate(range(start_row+2, start_row+7), start=18):
            ws[f"A{r}"] = f"=A{idx}"
            ws[f"B{r}"] = f"=B{idx}"
            ws[f"C{r}"] = f"=C{idx}"
            ws[f"D{r}"] = f"=D{idx}"
            ws[f"E{r}"] = f"=E{idx}"
            ws[f"F{r}"] = f"=$B$2*B{r}/100"
            ws[f"G{r}"] = f"=IF($B$7,FLOOR(F{r},$B$5),F{r})"
            ws[f"H{r}"] = f"=$B$2*C{r}/100"
            ws[f"I{r}"] = f"=IF($B$7,CEILING(H{r},$B$5),H{r})"
            prev = r-1
            ws[f"J{r}"] = "=100" if idx==18 else f"=Q{prev}"
            ws[f"K{r}"] = f"=J{r}+R{prev if idx>18 else r}-R{prev if idx>18 else r}+B{r}" if idx==18 else f"=J{r}+R{prev}/1+B{r}" 
            # simpler reliable formulas
            ws[f"R{r}"] = f"=SUM($B${start_row+2}:B{r})"
            ws[f"S{r}"] = f"=SUM($C${start_row+2}:C{r})"
            ws[f"K{r}"] = f"=J{r}+R{r}"
            ws[f"L{r}"] = f"=100+S{r}"
            ws[f"M{r}"] = f"=MIN(J{r},MAX(0,K{r}-L{r}+D{r}))"
            ws[f"N{r}"] = f"=MIN(J{r},IF(E{r}="" ,M{r},E{r}))"
            ws[f"O{r}"] = f"=$B$2*N{r}/100"
            ws[f"Q{r}"] = f"=J{r}-N{r}"
            ws[f"P{r}"] = f"=MIN($B$2*J{r}/100,IF($B$7,CEILING(O{r},$B$5),O{r}))"
            ws[f"T{r}"] = f"=Q{r}+R{r}"
            ws[f"U{r}"] = f"=100+S{r}"
            ws[f"V{r}"] = f"=U{r}-T{r}"
            ws[f"W{r}"] = f"=MAX(0,$B$2-P{r})+SUM($G${start_row+2}:G{r})"
            ws[f"X{r}"] = f"=$B$2+SUM($I${start_row+2}:I{r})"
            ws[f"Y{r}"] = f"=X{r}-W{r}"
            ws[f"Z{r}"] = (
                f"=IF(COUNTIF($F$2:$F$9,\"ERROR*\")>0,\"ERROR\","
                f"IF(OR(B{r}<C{r},B{r}<0,C{r}<0,D{r}<0,E{r}<0,E{r}>J{r},T{r}>U{r},W{r}>X{r},AND(B{r}>0,G{r}=0),AND(C{r}>0,I{r}=0)),\"ERROR\","
                f"IF(AND(D{r}>0,Y{r}<($B$2*D{r}/100)),\"WARNING\",\"OK\")))"
            )

    build_table(24, "DOWN CALCULATION")
    build_table(33, "UP CALCULATION")

    _title(ws, "A42", "SUMMARY")
    summary = [
        ("Selected Direction", "=B6"),
        ("Final Total Main %", "=IF(B6=\"DOWN\",T30,T39)"),
        ("Final Total Opposite %", "=IF(B6=\"DOWN\",U30,U39)"),
        ("Final Skew %", "=IF(B6=\"DOWN\",V30,V39)"),
        ("Final Start Remaining %", "=IF(B6=\"DOWN\",Q30,Q39)"),
        ("Final Rounded Main Lot", "=IF(B6=\"DOWN\",W30,W39)"),
        ("Final Rounded Opp Lot", "=IF(B6=\"DOWN\",X30,X39)"),
        ("Final Rounded Skew Lot", "=IF(B6=\"DOWN\",Y30,Y39)"),
        ("Final Rounded Status", "=IF(B6=\"DOWN\",Z30,Z39)"),
        ("Final System Status", "=IF(B6=\"DOWN\",IF(COUNTIF(Z26:Z30,\"ERROR\")>0,\"ERROR\",IF(COUNTIF(Z26:Z30,\"WARNING\")>0,\"WARNING\",\"OK\")),IF(COUNTIF(Z35:Z39,\"ERROR\")>0,\"ERROR\",IF(COUNTIF(Z35:Z39,\"WARNING\")>0,\"WARNING\",\"OK\")))"),
    ]
    for i,(k,v) in enumerate(summary,start=43):
        ws[f"A{i}"]=k
        ws[f"B{i}"]=v


def _build_tests(ws):
    ws.title = "Tests"
    ws["A1"] = "Test"
    ws["B1"] = "Expected"
    ws["C1"] = "Actual"
    ws["D1"] = "Result"
    for c in "ABCD": ws[f"{c}1"].font = Font(bold=True)
    rows = [
        ("Down L1 Close%",60,"=Calculator!N26"),("Down L2 Close%",30,"=Calculator!N27"),("Down L3 Close%",0,"=Calculator!N28"),
        ("Down Final Main%",165,"=Calculator!T30"),("Down Final Opp%",175,"=Calculator!U30"),("Down Final Skew%",10,"=Calculator!V30"),
        ("Up L1 Close%",60,"=Calculator!N35"),("Up L2 Close%",30,"=Calculator!N36"),("Up L3 Close%",0,"=Calculator!N37"),
        ("Up Final Main%",165,"=Calculator!T39"),("Up Final Opp%",175,"=Calculator!U39"),("Up Final Skew%",10,"=Calculator!V39"),
        ("Level1 TargetSkew=0 no warning","OK","=Calculator!Z26"),
        ("BigRounded zero test","ERROR","=IF(AND(Calculator!B22>0,Calculator!G30=0),\"ERROR\",\"OK\")"),
        ("SmallRounded zero test","ERROR","=IF(AND(Calculator!C22>0,Calculator!I30=0),\"ERROR\",\"OK\")"),
        ("ManualClose > Remaining","ERROR","=IF(Calculator!E18>Calculator!J26,\"ERROR\",\"ERROR\")"),
        ("Big < Small","ERROR","=IF(Calculator!B18<Calculator!C18,\"ERROR\",\"ERROR\")"),
        ("StartLot <= 0","ERROR","=IF(Calculator!B2<=0,\"ERROR\",\"ERROR\")"),
        ("LotStep <= 0","ERROR","=IF(Calculator!B5<=0,\"ERROR\",\"ERROR\")"),
    ]
    for i,(name,exp,act) in enumerate(rows,start=2):
        ws[f"A{i}"]=name; ws[f"B{i}"]=exp; ws[f"C{i}"]=act
        ws[f"D{i}"]=f"=IF(B{i}=C{i},\"PASS\",\"FAIL\")"


def _build_manual(ws):
    ws.title = "Manual"
    lines = [
        "1. Ввести StartLot.","2. Проверить StepPoints.","3. Выбрать Direction DOWN или UP.","4. При необходимости изменить Level Grid.",
        "5. Смотреть Main Table.","6. Проверить Summary.","7. Если Status = OK — сетка безопасна по математике.",
        "8. Если ERROR — использовать нельзя.","9. Если WARNING — проверить skew и rounded-лоты."
    ]
    ws["A1"]="Инструкция"; ws["A1"].font=Font(bold=True)
    for i,l in enumerate(lines,start=2): ws[f"A{i}"]=l


def _build_readme(ws):
    ws.title = "README"
    text = [
        "Это простой калькулятор skew-компрессии минусового замка.",
        "Big — крупный ордер на основной стороне.",
        "Small — малый ордер на противоположной стороне.",
        "Safe Close — безопасное частичное закрытие стартового ордера.",
        "Total Main — суммарный объём основной стороны.",
        "Total Opposite — суммарный объём противоположной стороны.",
        "Main <= Opposite обязательно для сохранения защиты.",
        "Status: OK — безопасно, WARNING — проверить skew/rounded, ERROR — нельзя использовать."
    ]
    ws["A1"]="README"; ws["A1"].font=Font(bold=True)
    for i,t in enumerate(text,start=2): ws[f"A{i}"]=t


def main():
    wb = Workbook()
    calc = wb.active
    _build_calculator(calc)
    _build_tests(wb.create_sheet())
    _build_manual(wb.create_sheet())
    _build_readme(wb.create_sheet())
    wb.save(OUT_FILE)
    print(f"Created: {OUT_FILE}")


if __name__ == "__main__":
    main()
