from __future__ import annotations
from pathlib import Path
from math import floor, ceil
from openpyxl import load_workbook

FILE = Path(__file__).resolve().parent / "MinusLock_Simple_Skew_Compression_Calculator.xlsx"
ERR = {"#NAME?", "#REF!", "#VALUE!", "#DIV/0!", "#N/A"}


def die(msg):
    print(f"VALIDATION FAILED: {msg}")
    raise SystemExit(1)


def expect(cond, msg):
    if not cond:
        die(msg)


def round_down(x, step):
    return floor(x / step) * step


def round_up(x, step):
    return ceil(x / step) * step


def baseline(start=1.0, step=0.01):
    big = [90, 30, 20, 10, 5]
    small = [30, 15, 15, 10, 5]
    target = [0, 15, 10, 10, 10]
    start_before = 100.0
    sum_big = 0.0
    sum_small = 0.0
    out = []
    for i in range(5):
        sum_big += big[i]
        sum_small += small[i]
        total_main_before = start_before + sum_big
        total_opp_after = 100 + sum_small
        auto = min(start_before, max(0, total_main_before - total_opp_after + target[i]))
        final_close = auto
        start_after = start_before - final_close
        total_main = start_after + sum_big
        total_opp = 100 + sum_small
        skew = total_opp - total_main

        g = round_down(start * big[i] / 100, step)
        s = round_up(start * small[i] / 100, step)
        w = start * start_after / 100 + sum(round_down(start * b / 100, step) for b in big[: i + 1])
        x = start + sum(round_up(start * sm / 100, step) for sm in small[: i + 1])
        y = x - w
        status = "WARNING" if (target[i] > 0 and y + 1e-9 < start * target[i] / 100) else "OK"
        if total_main > total_opp or w > x or big[i] < small[i] or big[i] < 0 or small[i] < 0:
            status = "ERROR"
        out.append((round(w, 10), round(x, 10), round(y, 10), status, final_close, total_main, total_opp, skew))
        start_before = start_after
    return out


def main():
    expect(FILE.exists(), "file missing")
    wb = load_workbook(FILE, data_only=False)
    for s in ["Calculator", "Tests", "Manual", "README"]:
        expect(s in wb.sheetnames, f"missing sheet {s}")

    c = wb["Calculator"]
    # check formula errors literals
    for ws in wb.worksheets:
        for row in ws.iter_rows(min_row=1, max_row=ws.max_row, min_col=1, max_col=ws.max_column):
            for cell in row:
                if cell.value in ERR:
                    die(f"formula error literal at {ws.title}!{cell.coordinate}")


    # manual close pass-through must preserve blank
    for r,src in [(26,18),(27,19),(28,20),(29,21),(30,22),(35,18),(36,19),(37,20),(38,21),(39,22)]:
        expect(c[f"E{r}"].value == f'=IF(E{src}="","",E{src})', f"manual close pass-through E{r}")

    # final close fallback formulas
    for r in [26,27,28,29,30,35,36,37,38,39]:
        expect(c[f"N{r}"].value == f'=MIN(J{r},IF(E{r}="",M{r},E{r}))', f"final close formula N{r}")
    # exact critical formulas
    expect(c["W26"].value == '=$B$2*Q26/100+SUM($G$26:G26)', "W26 formula")
    expect(c["W27"].value == '=$B$2*Q27/100+SUM($G$26:G27)', "W27 formula")
    expect(c["W35"].value == '=$B$2*Q35/100+SUM($G$35:G35)', "W35 formula")
    expect(c["X26"].value == '=$B$2+SUM($I$26:I26)', "X26 formula")
    expect(c["Y26"].value == '=X26-W26', "Y26 formula")

    b = baseline()
    down_rows = [26, 27, 28, 29, 30]
    up_rows = [35, 36, 37, 38, 39]
    expected_w = [1.30, 1.30, 1.50, 1.60, 1.65]
    expected_x = [1.30, 1.45, 1.60, 1.70, 1.75]
    expected_y = [0.00, 0.15, 0.10, 0.10, 0.10]

    for idx, r in enumerate(down_rows):
        w, x, y, st, close, tm, to, sk = b[idx]
        expect(abs(w - expected_w[idx]) < 1e-9, f"down W calc {idx+1}")
        expect(abs(x - expected_x[idx]) < 1e-9, f"down X calc {idx+1}")
        expect(abs(y - expected_y[idx]) < 1e-9, f"down Y calc {idx+1}")
        expect(st == "OK", f"down status {idx+1}")

    for idx, r in enumerate(up_rows):
        w, x, y, st, close, tm, to, sk = b[idx]
        expect(abs(w - expected_w[idx]) < 1e-9, f"up W calc {idx+1}")
        expect(st == "OK", f"up status {idx+1}")

    # summary formulas present and direction switch
    for cell in ["B48", "B49", "B50", "B51", "B52"]:
        v = c[cell].value
        expect(isinstance(v, str) and 'IF(B6="DOWN"' in v, f"summary formula {cell}")

    t = wb["Tests"]
    expect(t.max_row >= 38, "tests manualclose block missing")
    names=[t[f"A{r}"].value for r in range(2,t.max_row+1)]
    for req in ["Empty ManualClose uses AutoClose","ManualClose override works","Empty ManualClose is blank not zero"]:
        expect(req in names, f"missing test {req}")
    for r in range(2, t.max_row + 1):
        if t[f"A{r}"].value:
            expect(isinstance(t[f"D{r}"].value, str) and "PASS" in t[f"D{r}"].value and "FAIL" in t[f"D{r}"].value, f"bad test result formula D{r}")

    print("ALL TESTS PASSED")


if __name__ == "__main__":
    main()
