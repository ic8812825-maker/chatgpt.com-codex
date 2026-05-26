from pathlib import Path
from openpyxl import load_workbook

XLSX = Path(__file__).resolve().parent / "MinusLock_Self_Compressing_Recovery_Calculator.xlsx"
ERR = {"#VALUE!", "#ЗНАЧ!", "#NAME?", "#ИМЯ?", "#REF!", "#ССЫЛКА!", "#DIV/0!", "#ДЕЛ/0!"}

wb = load_workbook(XLSX, data_only=False)
for sh in ["ПАРАМЕТРЫ", "Калькулятор", "РИСК_АНАЛИЗ", "Тесты", "Руководство", "Описание"]:
    assert sh in wb.sheetnames

ws = wb["Калькулятор"]
risk = wb["РИСК_АНАЛИЗ"]
tests = wb["Тесты"]

for sh in wb.worksheets:
    for row in sh.iter_rows(min_row=1, max_row=100, min_col=1, max_col=60):
        for c in row:
            if isinstance(c.value, str) and c.value in ERR:
                raise AssertionError(f"error token {c.value} at {sh.title}!{c.coordinate}")

for r in range(2, 7):
    assert isinstance(ws[f"X{r}"].value, str) and ws[f"X{r}"].value.startswith("=IF(")
    assert ws[f"AF{r}"].value == f"=AD{r}+AE{r}"
    assert ws[f"AG{r}"].value == f"=ABS(AD{r}-AE{r})"
    assert ws[f"AI{r}"].value == f"=AF{r}*AH{r}"
    assert risk[f"B{r}"].value == f"='Калькулятор'!AD{r}"
    assert risk[f"C{r}"].value == f"='Калькулятор'!AE{r}"
    assert risk[f"D{r}"].value == f"='Калькулятор'!AF{r}"

summary_labels = [ws[f"A{i}"].value for i in range(10, 21)]
for req in ["StartLot", "Direction", "Финальная сумма Big", "Финальная сумма Small", "Финальная сумма Close Far", "Финальный ближний старт", "Финальный дальний остаток", "Финальный NextBaseLot", "Количество уровней OK", "Количество STOP", "Финальный статус системы"]:
    assert req in summary_labels

assert tests.max_row >= 21
lv_checks = [tests[f"A{i}"].value for i in range(2, tests.max_row + 1)]
for lvl in ["L1", "L2", "L3", "L4", "L5"]:
    assert any(isinstance(x, str) and lvl in x for x in lv_checks)

print("VALIDATION: PASS")
