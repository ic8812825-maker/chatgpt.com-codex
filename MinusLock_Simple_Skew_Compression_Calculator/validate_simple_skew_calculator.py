from __future__ import annotations

import re
import shutil
import subprocess
import tempfile
from pathlib import Path

from openpyxl import load_workbook

BASE_DIR = Path(__file__).resolve().parent
WORKBOOK_PATH = BASE_DIR / "MinusLock_Simple_Skew_Compression_Calculator.xlsx"
REQUIRED_SHEETS = ["Калькулятор", "РИСК_АНАЛИЗ", "Тесты", "Руководство", "Описание"]
ERROR_TOKENS = {"#NAME?", "#ИМЯ?", "#VALUE!", "#ЗНАЧ!", "#REF!", "#ССЫЛКА!", "#DIV/0!", "#Н/Д", "#N/A"}
UNQUOTED_SHEET_RE = re.compile(r"=(Калькулятор|РИСК_АНАЛИЗ|Тесты|Руководство|Описание)!", re.IGNORECASE)


def die(message: str) -> None:
    print(f"VALIDATION FAILED: {message}")
    raise SystemExit(1)


def ok(condition: bool, message: str) -> None:
    if not condition:
        die(message)


def scan_workbook_formulas_and_errors(workbook_path: Path) -> None:
    wb = load_workbook(workbook_path, data_only=False)
    for s in REQUIRED_SHEETS:
        ok(s in wb.sheetnames, f"нет листа {s}")

    found_formula_cells = 0
    for ws in wb.worksheets:
        for row in ws.iter_rows():
            for cell in row:
                value = cell.value
                if isinstance(value, str):
                    if value in ERROR_TOKENS:
                        die(f"ошибка Excel {value} в {ws.title}!{cell.coordinate}")
                    if value.startswith("="):
                        found_formula_cells += 1
                        if UNQUOTED_SHEET_RE.search(value):
                            die(f"некавыченная межлистовая ссылка в {ws.title}!{cell.coordinate}: {value}")
    ok(found_formula_cells > 0, "формулы не найдены")


def recalc_with_libreoffice(src: Path) -> Path:
    soffice = shutil.which("libreoffice") or shutil.which("soffice")
    ok(soffice is not None, "LibreOffice/soffice недоступен: невозможно проверить data_only cache")

    tmp_dir = Path(tempfile.mkdtemp(prefix="minuslock_recalc_"))
    tmp_src = tmp_dir / src.name
    tmp_src.write_bytes(src.read_bytes())

    ods_file = tmp_dir / f"{tmp_src.stem}.ods"
    to_ods = [soffice, "--headless", "--convert-to", "ods", "--outdir", str(tmp_dir), str(tmp_src)]
    p1 = subprocess.run(to_ods, capture_output=True, text=True)
    ok(p1.returncode == 0 and ods_file.exists(), f"ошибка LibreOffice xlsx->ods: {p1.stderr.strip() or p1.stdout.strip()}")

    to_xlsx = [soffice, "--headless", "--convert-to", "xlsx", "--outdir", str(tmp_dir), str(ods_file)]
    p2 = subprocess.run(to_xlsx, capture_output=True, text=True)
    ok(p2.returncode == 0, f"ошибка LibreOffice ods->xlsx: {p2.stderr.strip() or p2.stdout.strip()}")

    recalc_file = tmp_dir / f"{ods_file.stem}.xlsx"
    ok(recalc_file.exists(), "пересчитанный xlsx не создан LibreOffice")
    return recalc_file


def check_data_only_values(recalc_path: Path) -> None:
    wb = load_workbook(recalc_path, data_only=True)
    c = wb["Калькулятор"]
    r = wb["РИСК_АНАЛИЗ"]
    t = wb["Тесты"]

    expected = {
        "B44": 165,
        "B45": 175,
        "B46": 10,
        "B48": 1.65,
        "B49": 1.75,
        "B50": 0.10,
        "B51": "OK",
        "B73": 3740,
        "B75": 37.4,
        "B74": 750,
        "AA22": "WARNING",
    }

    for cell, exp in expected.items():
        val = c[cell].value
        ok(val is not None and val != "", f"пустое ключевое значение Калькулятор!{cell}")
        if isinstance(exp, (int, float)):
            ok(abs(float(val) - float(exp)) < 1e-6, f"неверное значение Калькулятор!{cell}: {val} != {exp}")
        else:
            ok(str(val) == exp, f"неверное значение Калькулятор!{cell}: {val} != {exp}")

    for rr in range(3, 8):
        for cc in [2, 3, 4, 5, 6, 7]:
            val = r.cell(rr, cc).value
            ok(val is not None and val != "", f"пусто РИСК_АНАЛИЗ!{r.cell(rr,cc).coordinate}")
            ok(str(val) not in ERROR_TOKENS, f"ошибка в РИСК_АНАЛИЗ!{r.cell(rr,cc).coordinate}: {val}")

    for rr in range(2, t.max_row + 1):
        result = t[f"D{rr}"].value
        ok(result is not None and result != "", f"пустой результат теста Тесты!D{rr}")
        ok(str(result) == "PASS", f"тест не PASS в Тесты!D{rr}: {result}")


def check_human_totals_and_risk_sync(recalc_path: Path) -> None:
    wb = load_workbook(recalc_path, data_only=True)
    c = wb["Калькулятор"]
    r = wb["РИСК_АНАЛИЗ"]

    totals_expected = {
        "B70": 1.65,
        "B71": 1.75,
        "B72": 0.10,
        "B73": 3740,
        "B75": 37.4,
    }
    for cell, exp in totals_expected.items():
        val = c[cell].value
        ok(val is not None and val != "", f"пусто в итогах Калькулятор!{cell}")
        ok(abs(float(val) - float(exp)) < 1e-6, f"ошибка в итогах Калькулятор!{cell}: {val} != {exp}")

    for lvl in range(1, 6):
        risk_row = 2 + lvl
        calc_row = 17 + lvl
        pairs = [
            (f"A{risk_row}", f"J{calc_row}"),
            (f"B{risk_row}", f"R{calc_row}"),
            (f"C{risk_row}", f"Q{calc_row}"),
            (f"D{risk_row}", f"N{calc_row}"),
            (f"E{risk_row}", f"T{calc_row}"),
            (f"F{risk_row}", f"X{calc_row}"),
            (f"G{risk_row}", f"AA{calc_row}"),
        ]
        for risk_cell, calc_cell in pairs:
            rv = r[risk_cell].value
            cv = c[calc_cell].value
            ok(rv is not None and cv is not None, f"пустая синхронизация {risk_cell}<->{calc_cell}")
            if isinstance(cv, (int, float)):
                ok(abs(float(rv) - float(cv)) < 1e-6, f"рассинхрон РИСК_АНАЛИЗ!{risk_cell}={rv} vs Калькулятор!{calc_cell}={cv}")
            else:
                ok(str(rv) == str(cv), f"рассинхрон РИСК_АНАЛИЗ!{risk_cell}={rv} vs Калькулятор!{calc_cell}={cv}")


def main() -> None:
    ok(WORKBOOK_PATH.exists(), f"нет файла {WORKBOOK_PATH.name}")
    scan_workbook_formulas_and_errors(WORKBOOK_PATH)
    recalc = recalc_with_libreoffice(WORKBOOK_PATH)
    check_data_only_values(recalc)
    check_human_totals_and_risk_sync(recalc)
    print("ALL TESTS PASSED")
    print("NO EXCEL FORMULA ERRORS")


if __name__ == "__main__":
    main()
