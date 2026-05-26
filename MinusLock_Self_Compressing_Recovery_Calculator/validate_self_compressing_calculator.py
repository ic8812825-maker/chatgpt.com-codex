from pathlib import Path
from openpyxl import load_workbook

XLSX = Path(__file__).resolve().parent / "MinusLock_Self_Compressing_Recovery_Calculator.xlsx"
wb = load_workbook(XLSX, data_only=False)

assert "ПАРАМЕТРЫ" in wb.sheetnames
assert "Калькулятор" in wb.sheetnames
assert "РИСК_АНАЛИЗ" in wb.sheetnames
assert "Тесты" in wb.sheetnames

p = wb["ПАРАМЕТРЫ"]
assert p["B2"].value is not None
calc = wb["Калькулятор"]
assert isinstance(calc["G2"].value, str) and calc["G2"].value.startswith("=")
assert isinstance(calc["O2"].value, str) and "CloseMode" in calc["O2"].value
assert isinstance(calc["Q2"].value, str) and calc["Q2"].value.startswith("=")
risk = wb["РИСК_АНАЛИЗ"]
assert risk.max_row > 1 and isinstance(risk["B2"].value, str) and risk["B2"].value.startswith("='Калькулятор'!")
tests = wb["Тесты"]
assert isinstance(tests["B2"].value, str) and tests["B2"].value.startswith("=IF")

# required names
names = {n.name for n in wb.defined_names.values()}
for req in ["StartLot","BigPercent","SmallPercent","CloseFarPercent","LotStep","Balance","Leverage","Direction","CloseMode"]:
    assert req in names

print("VALIDATION: PASS")
