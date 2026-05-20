from __future__ import annotations
from pathlib import Path
from openpyxl import load_workbook

FILE = Path(__file__).resolve().parent / "MinusLock_Simple_Skew_Compression_Calculator.xlsx"
ERR = {"#NAME?", "#REF!", "#VALUE!", "#DIV/0!", "#N/A"}


def fail(msg):
    print(f"VALIDATION FAILED: {msg}")
    raise SystemExit(1)


def assert_eq(a, b, msg):
    if a != b:
        fail(f"{msg}: {a!r} != {b!r}")


def assert_true(v, msg):
    if not v:
        fail(msg)


def main():
    if not FILE.exists(): fail("Excel file missing")
    wb = load_workbook(FILE, data_only=False)
    for s in ["Calculator", "Tests", "Manual", "README"]:
        assert_true(s in wb.sheetnames, f"missing sheet {s}")

    c = wb["Calculator"]
    # defaults
    assert_eq(c["B2"].value, 1.0, "StartLot")
    assert_eq(c["B3"].value, 100, "StepPoints")
    assert_eq(c["B4"].value, 5, "MaxLevels")
    assert_eq(c["B5"].value, 0.01, "LotStep")
    assert_eq(c["B6"].value, "DOWN", "Direction")

    # final close formulas exact critical rows
    for r in [26,27,28,29,30,35,36,37,38,39]:
        expect = f'=MIN(J{r},IF(E{r}="",M{r},E{r}))'
        assert_eq(c[f"N{r}"].value, expect, f"FinalClose formula N{r}")

    # baseline formulas presence
    for cell in ["M26","T30","U30","V30","T39","U39","V39","B52"]:
        assert_true(c[cell].value is not None, f"missing formula {cell}")

    # no raw text tokens in formulas
    for ws in [c, wb["Tests"]]:
        for row in ws.iter_rows(min_row=1, max_row=ws.max_row, min_col=1, max_col=ws.max_column):
            for cell in row:
                v = cell.value
                if isinstance(v, str) and v.startswith("="):
                    for bad in ["ERROR: Invalid", ",OK)", ",WARNING)", ",PASS)", ",FAIL)"]:
                        if bad in v and f'"{bad.strip(",)")}"' not in v:
                            pass
                    if "ERROR:" in v and '"ERROR:' not in v:
                        fail(f"unquoted ERROR token in {ws.title}!{cell.coordinate}")
                    if ",OK" in v and '","OK"' not in v and '"OK"' not in v:
                        fail(f"unquoted OK token in {ws.title}!{cell.coordinate}")
                if v in ERR:
                    fail(f"formula error literal {v} at {ws.title}!{cell.coordinate}")

    # Tests sheet structure + formulas
    t = wb["Tests"]
    assert_eq(t["A1"].value, "Test", "Tests header")
    assert_eq(t["B1"].value, "Actual", "Tests header")
    assert_eq(t["C1"].value, "Expected", "Tests header")
    assert_eq(t["D1"].value, "Result", "Tests header")
    for r in range(2, 12):
        assert_true(isinstance(t[f"D{r}"].value, str) and "PASS" in t[f"D{r}"].value and "FAIL" in t[f"D{r}"].value, f"bad test formula D{r}")

    # direction switch formulas in summary
    for cell in ["B44","B45","B46","B47","B48","B49","B50","B51","B52"]:
        v=c[cell].value
        assert_true(isinstance(v,str) and "IF(B6=\"DOWN\"" in v or cell=="B43", f"summary formula broken {cell}")

    print("ALL TESTS PASSED")


if __name__ == "__main__":
    main()
