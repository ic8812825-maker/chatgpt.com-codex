from __future__ import annotations
from pathlib import Path
from openpyxl import load_workbook

FILE = Path(__file__).resolve().parent / "MinusLock_Simple_Skew_Compression_Calculator.xlsx"


def die(msg):
    print(f"VALIDATION FAILED: {msg}")
    raise SystemExit(1)

def expect(cond, msg):
    if not cond: die(msg)

def main():
    expect(FILE.exists(), "file missing")
    wb=load_workbook(FILE,data_only=False)
    for s in ["Calculator","HumanSummary","Tests","Manual","README"]:
        expect(s in wb.sheetnames, f"missing sheet {s}")
    c=wb["Calculator"]; h=wb["HumanSummary"]; t=wb["Tests"]

    # human headers
    required=["Level","Direction","Action Big","Big %","Big Lot","Action Small","Small %","Small Lot","Close Action","Close %","Close Lot","Start Remaining %","Start Remaining Lot","Total Main %","Total Opposite %","Skew %","Rounded Main Lot","Rounded Opp Lot","Rounded Skew Lot","Status","Human Comment"]
    for i,name in enumerate(required,1):
        expect(h.cell(2,i).value==name, f"HumanSummary header {name}")

    # totals formulas cells
    expect(h["B11"].value == "=SUM(E3:E7)", "sum big formula")
    expect(h["B12"].value == "=SUM(H3:H7)", "sum small formula")
    expect(h["B13"].value == "=SUM(K3:K7)", "sum close formula")
    expect(h["B21"].value == "=T7", "final status formula")

    # action direction formulas
    expect(c["C57"].value is not None and 'Open Big BUY' in c["C57"].value and 'Open Big SELL' in c["C57"].value, "direction action big formula")
    expect(c["F57"].value is not None and 'Open Small SELL' in c["F57"].value and 'Open Small BUY' in c["F57"].value, "direction action small formula")
    expect(c["I57"].value is not None and 'Close Start BUY' in c["I57"].value and 'Close Start SELL' in c["I57"].value, "direction close formula")


    # Human formulas must point to DOWN/UP calc rows, not level-grid rows
    expect(c["E57"].value == '=IF($B$6="DOWN",G26,G35)', "human L1 big lot source")
    expect(c["H57"].value == '=IF($B$6="DOWN",I26,I35)', "human L1 small lot source")
    expect(c["J57"].value == '=IF($B$6="DOWN",N26,N35)', "human L1 close pct source")
    expect(c["K57"].value == '=IF($B$6="DOWN",P26,P35)', "human L1 close lot source")
    expect(c["M57"].value == '=$B$2*L57/100', "human L1 start remaining lot formula")
    expect(c["T57"].value == '=IF($B$6="DOWN",Z26,Z35)', "human L1 status source")
    expect("#NAME" not in str(c["U57"].value).upper() and "#ИМЯ" not in str(c["U57"].value).upper(), "human comment formula broken")

    # tests include human rows
    names=[t[f"A{r}"].value for r in range(2,t.max_row+1)]
    for req in ["Human Sum Big Lots","Human Sum Small Lots","Human Sum Close Lots","Human Final Start Remaining Lot","Human Final Status","Human Level 1 Big Action","Human Level 1 Small Action","Human Level 1 Close Action"]:
        expect(req in names, f"missing test {req}")

    print("ALL TESTS PASSED")

if __name__ == "__main__":
    main()
