from pathlib import Path
from openpyxl import load_workbook

XLSX = Path(__file__).resolve().parent / "MinusLock_Self_Compressing_Recovery_Calculator.xlsx"
ERR = {"#VALUE!", "#ЗНАЧ!", "#NAME?", "#ИМЯ?", "#REF!", "#ССЫЛКА!", "#DIV/0!", "#ДЕЛ/0!"}

wb = load_workbook(XLSX, data_only=False)
ws = wb["Калькулятор"]
risk = wb["РИСК_АНАЛИЗ"]
tests = wb["Тесты"]

for sh in wb.worksheets:
    for row in sh.iter_rows(min_row=1, max_row=120, min_col=1, max_col=60):
        for c in row:
            if isinstance(c.value, str) and c.value in ERR:
                raise SystemExit(f"error token {c.value} {sh.title}!{c.coordinate}")

for r in range(2, 7):
    if ws[f"X{r}"].value in (None, ""):
        raise SystemExit("empty comment")

for r in range(2, 7):
    if risk[f"B{r}"].value is None or risk[f"M{r}"].value is None:
        raise SystemExit("risk row empty")

for r in range(2, tests.max_row + 1):
    if tests[f"A{r}"].value in (None, ""):
        continue
    f = tests[f"B{r}"].value
    s = tests[f"C{r}"].value
    if not (isinstance(s, str) and s.startswith("=B")):
        raise SystemExit("status must be formula")
    if isinstance(f, str):
        fu = f.upper().replace(" ", "")
        if '"PASS","PASS"' in fu or '"PASS";"PASS"' in fu:
            raise SystemExit("fake pass formula")
        name = str(tests[f"A{r}"].value)
        if "No #" not in name and "КАЛЬКУЛЯТОР!" not in fu and "РИСК_АНАЛИЗ!" not in fu and not ("STARTLOT" in fu and "CLOSEMODE" in fu):
            raise SystemExit("test formula not linked to workbook cells")

print("SMOKE: PASS")
