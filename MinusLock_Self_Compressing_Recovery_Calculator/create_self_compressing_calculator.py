from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Protection
from openpyxl.workbook.defined_name import DefinedName
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import FormulaRule

OUT = Path(__file__).resolve().parent / "MinusLock_Self_Compressing_Recovery_Calculator.xlsx"

PARAMS = [
    ("StartLot", 1.0), ("Direction", "DOWN"), ("MaxLevels", 5), ("LotStep", 0.01),
    ("UseRounding", "TRUE"), ("BigPercent", 90), ("SmallPercent", 40), ("CloseFarPercent", 30),
    ("CloseMode", "THEORETICAL"), ("ProfitReservePercent", 30), ("MinReserveMoney", 5),
    ("PointValuePerLot", 10), ("Balance", 10000), ("Leverage", 100), ("ContractSize", 100000),
    ("InstrumentPrice", 1.1), ("MaxAdversePoints", 500), ("StopOutPercent", 50), ("MarginCallPercent", 100),
]


def main():
    wb = Workbook()
    wb.calculation.fullCalcOnLoad = True
    wb.calculation.forceFullCalc = True

    p = wb.active
    p.title = "ПАРАМЕТРЫ"
    p["A1"] = "Параметр"; p["B1"] = "Значение"
    p["A1"].font = p["B1"].font = Font(bold=True)
    for i, (k, v) in enumerate(PARAMS, 2):
        p.cell(i, 1, k); p.cell(i, 2, v)
        wb.defined_names.add(DefinedName(k, attr_text=f"'ПАРАМЕТРЫ'!$B${i}"))

    dv_dir = DataValidation(type="list", formula1='"DOWN,UP"')
    dv_mode = DataValidation(type="list", formula1='"THEORETICAL,SAFE_PROFIT_BUDGET"')
    dv_bool = DataValidation(type="list", formula1='"TRUE,FALSE"')
    p.add_data_validation(dv_dir); p.add_data_validation(dv_mode); p.add_data_validation(dv_bool)
    dv_dir.add("B3"); dv_mode.add("B10"); dv_bool.add("B6")

    ws = wb.create_sheet("Калькулятор")
    headers = ["Уровень","Направление","Ближний старт","Дальний старт остаток","Старт поз. самая дальняя","Big %","Big Lot Raw","Big Lot Rounded","Small %","Small Lot Raw","Small Lot Rounded","Close Far %","Max Close Far Lot","Close By Profit Budget","Actual Close Far Lot","Close Mode","Новый ближний старт","Новый дальний остаток","Next Base Lot","Сумма Big","Сумма Small","Сумма Close","Статус","Комментарий","Прибыль пакета до Close","Резерв деньги","Бюджет на Close","Убыток Far Start на 1 лот","Close Status","Total Big Lots","Total Small Lots","Total Open Lots","Net Lot","Margin Per Lot","Required Margin","Margin Load %","Floating DD","Equity After DD","Free Margin","Margin Level %","Risk Status"]
    ws.append(headers)
    for c in ws[1]: c.font = Font(bold=True)
    start = 2
    for i in range(5):
        r = start + i
        prev = r - 1
        ws[f"A{r}"] = i + 1
        ws[f"B{r}"] = "=Direction"
        ws[f"C{r}"] = "=StartLot" if i == 0 else f"=S{prev}"
        ws[f"D{r}"] = "=StartLot" if i == 0 else f"=R{prev}"
        ws[f"E{r}"] = f'=IF(Direction="DOWN","Start BUY","Start SELL")'
        ws[f"F{r}"] = "=BigPercent"; ws[f"G{r}"] = f"=C{r}*BigPercent/100"
        ws[f"H{r}"] = f'=IF(UseRounding="TRUE",ROUNDDOWN(G{r}/LotStep,0)*LotStep,G{r})'
        ws[f"I{r}"] = "=SmallPercent"; ws[f"J{r}"] = f"=C{r}*SmallPercent/100"
        ws[f"K{r}"] = f'=IF(UseRounding="TRUE",ROUNDUP(J{r}/LotStep,0)*LotStep,J{r})'
        ws[f"L{r}"] = "=CloseFarPercent"; ws[f"M{r}"] = f"=C{r}*CloseFarPercent/100"
        ws[f"Y{r}"] = f"=(H{r}+K{r})*PointValuePerLot"
        ws[f"Z{r}"] = f"=MAX(Y{r}*ProfitReservePercent/100,MinReserveMoney)"
        ws[f"AA{r}"] = f"=Y{r}-Z{r}"
        ws[f"AB{r}"] = "=MaxAdversePoints*PointValuePerLot"
        ws[f"N{r}"] = f'=IF(AA{r}<=0,0,ROUNDDOWN(AA{r}/AB{r}/LotStep,0)*LotStep)'
        ws[f"O{r}"] = f'=IF(CloseMode="THEORETICAL",MIN(M{r},D{r}),MIN(M{r},N{r},D{r}))'
        ws[f"P{r}"] = "=CloseMode"
        ws[f"Q{r}"] = f"=C{r}-G{r}+J{r}"
        ws[f"R{r}"] = f"=D{r}-O{r}"
        ws[f"S{r}"] = f"=MIN(Q{r},R{r})"
        ws[f"T{r}"] = f"=SUM($H$2:H{r})"; ws[f"U{r}"] = f"=SUM($K$2:K{r})"; ws[f"V{r}"] = f"=SUM($O$2:O{r})"
        ws[f"AD{r}"] = "=ContractSize*InstrumentPrice/Leverage"
        ws[f"AE{r}"] = f"=(T{r}+U{r})*AD{r}"
        ws[f"AF{r}"] = f"=AE{r}/Balance*100"
        ws[f"AG{r}"] = f"=ABS(T{r}-U{r})*MaxAdversePoints*PointValuePerLot"
        ws[f"AH{r}"] = f"=Balance-AG{r}"; ws[f"AI{r}"] = f"=AH{r}-AE{r}"; ws[f"AJ{r}"] = f"=IF(AE{r}=0,9999,AH{r}/AE{r}*100)"
        ws[f"AK{r}"] = f'=IF(OR(AF{r}>70,AJ{r}<100),"CRITICAL",IF(OR(AF{r}>50,AJ{r}<150),"DANGER",IF(OR(AF{r}>=30,AJ{r}<=300),"WARNING","OK")))'
        ws[f"W{r}"] = f'=IF(OR(H{r}<LotStep,K{r}<LotStep,O{r}<LotStep,S{r}<LotStep,AF{r}>100,AJ{r}<StopOutPercent,R{r}<=0),"STOP","OK")'
        ws[f"AC{r}"] = f'=IF(AND(CloseMode="SAFE_PROFIT_BUDGET",O{r}=0),"NO CLOSE","OK")'
        ws[f"X{r}"] = f'=IF(Direction="DOWN","Уровень "&A{r}&". Цена вниз. Big BUY "&TEXT(H{r},"0.00000")&"; Small SELL "&TEXT(K{r},"0.00000")&"; Close BUY "&TEXT(O{r},"0.00000"),"Уровень "&A{r}&". Цена вверх. Big SELL "&TEXT(H{r},"0.00000")&"; Small BUY "&TEXT(K{r},"0.00000")&"; Close SELL "&TEXT(O{r},"0.00000"))'

    sr = 10
    ws[f"A{sr}"] = "ИТОГИ САМОСЖИМАЮЩЕЙСЯ МОДЕЛИ"; ws[f"A{sr}"].font = Font(bold=True)
    ws[f"A{sr+1}"] = "Финальная сумма Big"; ws[f"B{sr+1}"] = "=SUM(H2:H6)"
    ws[f"A{sr+2}"] = "Финальная сумма Small"; ws[f"B{sr+2}"] = "=SUM(K2:K6)"
    ws[f"A{sr+3}"] = "Финальная сумма Close Far"; ws[f"B{sr+3}"] = "=SUM(O2:O6)"

    risk = wb.create_sheet("РИСК_АНАЛИЗ")
    risk_headers = ["Уровень","Total Big Lots","Total Small Lots","Total Open Lots","Net Lot","Margin Per Lot","Required Margin","Margin Load %","Floating DD","Equity After DD","Free Margin","Margin Level %","Risk Status"]
    risk.append(risk_headers)
    for c in risk[1]: c.font = Font(bold=True)
    for i in range(5):
        rr = i+2; cr = i+2
        risk[f"A{rr}"] = f"='Калькулятор'!A{cr}"; risk[f"B{rr}"] = f"='Калькулятор'!AD{cr-0}".replace("AD","T")
        risk[f"C{rr}"] = f"='Калькулятор'!U{cr}"; risk[f"D{rr}"] = f"='Калькулятор'!AF{cr}".replace("AF","AE")
        risk[f"E{rr}"] = f"='Калькулятор'!AG{cr}".replace("AG","AF")
        risk[f"F{rr}"] = f"='Калькулятор'!AD{cr}"; risk[f"G{rr}"] = f"='Калькулятор'!AE{cr}"; risk[f"H{rr}"] = f"='Калькулятор'!AF{cr}"
        risk[f"I{rr}"] = f"='Калькулятор'!AG{cr}"; risk[f"J{rr}"] = f"='Калькулятор'!AH{cr}"; risk[f"K{rr}"] = f"='Калькулятор'!AI{cr}"
        risk[f"L{rr}"] = f"='Калькулятор'!AJ{cr}"; risk[f"M{rr}"] = f"='Калькулятор'!AK{cr}"

    tests = wb.create_sheet("Тесты")
    tests.append(["Проверка","Статус"])
    for c in tests[1]: c.font = Font(bold=True)
    checks = [
        ('Big Raw', '=IF(ABS(Калькулятор!G2-(Калькулятор!C2*BigPercent/100))<1E-8,"PASS","FAIL")'),
        ('Small Raw', '=IF(ABS(Калькулятор!J2-(Калькулятор!C2*SmallPercent/100))<1E-8,"PASS","FAIL")'),
        ('Actual Close', '=IF(OR(CloseMode<>"THEORETICAL",ABS(Калькулятор!O2-(Калькулятор!C2*CloseFarPercent/100))<1E-8),"PASS","FAIL")'),
        ('NewNear 50%', '=IF(ABS(Калькулятор!Q2-(Калькулятор!C2*0.5))<1E-8,"PASS","FAIL")'),
        ('Risk not empty', '=IF(COUNTA(РИСК_АНАЛИЗ!A2:A6)=5,"PASS","FAIL")')
    ]
    for i,(n,f) in enumerate(checks,2): tests[f"A{i}"]=n; tests[f"B{i}"]=f

    wb.create_sheet("Руководство")["A1"] = "См. MANUAL_RU.md"
    wb.create_sheet("Описание")["A1"] = "SELF-COMPRESSING LOCK RECOVERY"

    # formatting and protection
    color_map = {"OK":"C6EFCE","WARNING":"FFEB9C","DANGER":"F4B084","CRITICAL":"FFC7CE"}
    for status, color in color_map.items():
        ws.conditional_formatting.add("AK2:AK6", FormulaRule(formula=[f'AK2="{status}"'], fill=PatternFill("solid", fgColor=color)))
        risk.conditional_formatting.add("M2:M6", FormulaRule(formula=[f'M2="{status}"'], fill=PatternFill("solid", fgColor=color)))

    for sh in wb.worksheets:
        for row in sh.iter_rows():
            for cell in row:
                cell.protection = Protection(locked=True)
        sh.protection.sheet = True
    p.protection.sheet = True
    for c in p["B2:B20"]: c[0].protection = Protection(locked=False)

    wb.save(OUT)
    print(f"Created: {OUT}")


if __name__ == "__main__":
    main()
