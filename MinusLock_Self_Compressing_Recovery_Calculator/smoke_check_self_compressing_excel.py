from pathlib import Path
from openpyxl import load_workbook

XLSX = Path(__file__).resolve().parent / "MinusLock_Self_Compressing_Recovery_Calculator.xlsx"
errors = {"#NAME?", "#ИМЯ?", "#REF!", "#ССЫЛКА!", "#VALUE!", "#ЗНАЧ!", "#DIV/0!", "#ДЕЛ/0!"}
wb = load_workbook(XLSX, data_only=True)
for sh in wb.worksheets:
    for row in sh.iter_rows():
        for c in row:
            v = c.value
            if isinstance(v, str):
                if v in errors:
                    raise SystemExit(f"error token in {sh.title}!{c.coordinate}: {v}")
                if "РУСС" in v:
                    raise SystemExit("possible unquoted russian ref")
print("SMOKE: PASS")
