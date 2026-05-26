from pathlib import Path
from openpyxl import load_workbook

XLSX = Path(__file__).resolve().parent / "MinusLock_Self_Compressing_Recovery_Calculator.xlsx"
wb = load_workbook(XLSX, data_only=False)

for sh in wb.worksheets:
    for row in sh.iter_rows(min_row=1, max_row=30, min_col=1, max_col=50):
        for c in row:
            if isinstance(c.value, str) and c.value in {"#NAME?", "#REF!", "#VALUE!", "#DIV/0!", "#ИМЯ?", "#ССЫЛКА!", "#ЗНАЧ!", "#ДЕЛ/0!"}:
                raise SystemExit(f"error token {c.value} at {sh.title}!{c.coordinate}")

assert wb["РИСК_АНАЛИЗ"].max_row > 1
assert isinstance(wb["Калькулятор"]["O2"].value, str)
print("SMOKE: PASS")
