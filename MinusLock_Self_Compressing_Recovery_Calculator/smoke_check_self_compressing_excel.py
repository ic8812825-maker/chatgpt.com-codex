from pathlib import Path
from openpyxl import load_workbook

XLSX = Path(__file__).resolve().parent / "MinusLock_Self_Compressing_Recovery_Calculator.xlsx"
ERR = {"#VALUE!", "#ЗНАЧ!", "#NAME?", "#ИМЯ?", "#REF!", "#ССЫЛКА!", "#DIV/0!", "#ДЕЛ/0!"}

wb = load_workbook(XLSX, data_only=False)
ws = wb["Калькулятор"]
risk = wb["РИСК_АНАЛИЗ"]

for sh in wb.worksheets:
    for row in sh.iter_rows(min_row=1, max_row=120, min_col=1, max_col=60):
        for c in row:
            if isinstance(c.value, str) and c.value in ERR:
                raise SystemExit(f"error token {c.value} {sh.title}!{c.coordinate}")

for r in range(2, 7):
    if ws[f"X{r}"].value in (None, ""):
        raise SystemExit("empty comment")
    if any(t in str(ws[f"X{r}"].value) for t in ERR):
        raise SystemExit("error in comment")

for r in range(2, 7):
    assert risk[f"B{r}"].value is not None
    assert risk[f"D{r}"].value is not None

print("SMOKE: PASS")
