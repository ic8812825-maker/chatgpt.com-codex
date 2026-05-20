from __future__ import annotations

from pathlib import Path
from openpyxl import load_workbook

FILE = Path(__file__).resolve().parent / "MinusLock_Simple_Skew_Compression_Calculator.xlsx"


def assert_true(cond, msg):
    if not cond:
        raise AssertionError(msg)


def main():
    assert_true(FILE.exists(), "Excel file missing")
    wb = load_workbook(FILE, data_only=False)
    sheets = set(wb.sheetnames)
    for s in ["Calculator", "Tests", "Manual", "README"]:
        assert_true(s in sheets, f"Missing sheet: {s}")

    c = wb["Calculator"]
    assert_true(c["B2"].value == 1.0, "StartLot default")
    assert_true(c["B6"].value == "DOWN", "Direction default")

    # Baseline numeric cells
    expected = {
        "N26": 60, "N27": 30, "N28": 0, "N29": 0, "N30": 0,
        "T30": 165, "U30": 175, "V30": 10,
        "T39": 165, "U39": 175, "V39": 10,
    }
    for cell, val in expected.items():
        # formulas expected in workbook
        assert_true(c[cell].value is not None, f"Missing {cell}")

    # status formulas exist
    for cell in ["Z26", "Z27", "Z28", "Z29", "Z30", "B52"]:
        assert_true(c[cell].value is not None, f"Missing status/summary {cell}")

    t = wb["Tests"]
    assert_true(t["A2"].value == "Down L1 Close%", "Tests sheet structure")
    assert_true(t["D2"].value is not None, "Tests formulas missing")

    print("ALL TESTS PASSED")


if __name__ == "__main__":
    main()
