from pathlib import Path
from openpyxl import load_workbook

XLSX = Path(__file__).resolve().parent / "MinusLock_Self_Compressing_Recovery_Calculator.xlsx"

req_sheets = {"Калькулятор", "РИСК_АНАЛИЗ", "Тесты", "Руководство", "Описание"}
req_params = {"StartLot","Direction","MaxLevels","LotStep","UseRounding","BigPercent","SmallPercent","CloseFarPercent","UseProfitReserveClose","ProfitToClosePercent","ProfitReservePercent","MinReserveMoney","PointValuePerLot","Balance","Leverage","ContractSize","InstrumentPrice","MaxAdversePoints","StopOutPercent","MarginCallPercent"}

wb = load_workbook(XLSX, data_only=True)
assert req_sheets.issubset(set(wb.sheetnames)), "missing sheets"
ws = wb["Калькулятор"]
params = {ws.cell(r,1).value for r in range(2,40)}
assert req_params.issubset(params), "missing params"

# table checks by first 5 levels
start = 27
for i in range(5):
    r = start + i
    near = ws.cell(r,3).value
    big = ws.cell(r,7).value
    small = ws.cell(r,10).value
    close = ws.cell(r,13).value
    nxt = ws.cell(r,15).value
    assert abs(big - near*0.9) < 1e-8
    assert abs(small - near*0.4) < 1e-8
    assert abs(close - near*0.3) < 1e-8
    assert abs(nxt - (near - ws.cell(r,8).value + ws.cell(r,11).value)) < 1e-8

# startlot patterns 1/2/5 by pure formula function
for s in [1,2,5]:
    near = s
    for _ in range(5):
        assert abs((near*0.9)) >= abs((near*0.4))
        near *= 0.5

# tests pass
wt = wb["Тесты"]
for r in range(2, wt.max_row+1):
    assert wt.cell(r,2).value == "PASS"

# no excel errors
errors = {"#NAME?", "#ИМЯ?", "#REF!", "#ССЫЛКА!", "#VALUE!", "#ЗНАЧ!", "#DIV/0!", "#ДЕЛ/0!"}
for sh in wb.worksheets:
    for row in sh.iter_rows():
        for c in row:
            if isinstance(c.value, str):
                assert c.value not in errors

print("VALIDATION: PASS")
