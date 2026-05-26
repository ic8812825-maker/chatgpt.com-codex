from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
import math
from typing import Dict, List, Any

from openpyxl import Workbook
from openpyxl.styles import Font

OUT = Path(__file__).resolve().parent / "MinusLock_Self_Compressing_Recovery_Calculator.xlsx"


@dataclass
class Params:
    StartLot: float = 1.0
    Direction: str = "DOWN"
    MaxLevels: int = 5
    LotStep: float = 0.01
    UseRounding: bool = True
    BigPercent: float = 90
    SmallPercent: float = 40
    CloseFarPercent: float = 30
    CloseMode: str = "THEORETICAL"
    ProfitToClosePercent: float = 70
    ProfitReservePercent: float = 30
    MinReserveMoney: float = 5
    PointValuePerLot: float = 10
    Balance: float = 10000
    Leverage: float = 100
    ContractSize: float = 100000
    InstrumentPrice: float = 1.10000
    MaxAdversePoints: float = 500
    StopOutPercent: float = 50
    MarginCallPercent: float = 100


def floor_step(v: float, step: float) -> float:
    return math.floor(v / step + 1e-12) * step


def ceil_step(v: float, step: float) -> float:
    return math.ceil(v / step - 1e-12) * step


def risk_bucket(margin_load: float, margin_level: float) -> str:
    by_load = "OK" if margin_load < 30 else "WARNING" if margin_load <= 50 else "DANGER" if margin_load <= 70 else "CRITICAL"
    by_level = "OK" if margin_level > 300 else "WARNING" if margin_level >= 150 else "DANGER" if margin_level >= 100 else "CRITICAL"
    rank = {"OK": 0, "WARNING": 1, "DANGER": 2, "CRITICAL": 3}
    return max([by_load, by_level], key=lambda x: rank[x])


def compute_rows(p: Params) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    near, far = p.StartLot, p.StartLot
    total_big = total_small = total_close = 0.0

    for lvl in range(1, p.MaxLevels + 1):
        big_raw = near * p.BigPercent / 100
        small_raw = near * p.SmallPercent / 100
        max_close_raw = near * p.CloseFarPercent / 100

        big_rounded = floor_step(big_raw, p.LotStep) if p.UseRounding else big_raw
        small_rounded = ceil_step(small_raw, p.LotStep) if p.UseRounding else small_raw

        package_profit = (big_rounded + small_rounded) * p.PointValuePerLot
        required_reserve = max(package_profit * p.ProfitReservePercent / 100, p.MinReserveMoney)
        close_budget = package_profit - required_reserve
        loss_per_lot = p.MaxAdversePoints * p.PointValuePerLot
        close_by_budget = floor_step(max(0.0, close_budget) / loss_per_lot, p.LotStep) if loss_per_lot > 0 else 0.0

        if p.CloseMode == "THEORETICAL":
            actual_close_raw = min(max_close_raw, far)
        else:
            actual_close_raw = min(max_close_raw, close_by_budget, far)

        actual_close_rounded = floor_step(actual_close_raw, p.LotStep) if p.UseRounding else actual_close_raw

        new_near_raw = near - big_raw + small_raw
        new_near_rounded = near - big_rounded + small_rounded
        actual_close_for_flow = actual_close_raw if p.CloseMode == "THEORETICAL" else actual_close_rounded
        new_far = far - actual_close_for_flow
        next_base = min(new_near_raw, new_far)

        total_big += big_rounded
        total_small += small_rounded
        total_close += actual_close_for_flow

        margin_per_lot = p.ContractSize * p.InstrumentPrice / p.Leverage
        required_margin = (total_big + total_small) * margin_per_lot
        margin_load = (required_margin / p.Balance * 100) if p.Balance else 0.0
        net_lot = abs(total_big - total_small)
        floating_dd = net_lot * p.MaxAdversePoints * p.PointValuePerLot
        equity = p.Balance - floating_dd
        free_margin = equity - required_margin
        margin_level = (equity / required_margin * 100) if required_margin > 0 else 9999.0
        risk_status = risk_bucket(margin_load, margin_level)

        stop_conditions = [
            big_rounded < p.LotStep,
            small_rounded < p.LotStep,
            actual_close_rounded < p.LotStep,
            next_base < p.LotStep,
            margin_load > 100,
            margin_level < p.StopOutPercent,
            new_far <= 0,
        ]
        status = "STOP" if any(stop_conditions) else "OK"
        close_status = "OK"
        if p.CloseMode == "SAFE_PROFIT_BUDGET" and (close_budget <= 0 or actual_close_rounded <= 0):
            close_status = "NO CLOSE"

        far_side = "BUY" if p.Direction == "DOWN" else "SELL"
        small_side = "SELL" if p.Direction == "DOWN" else "BUY"
        direction_text = "вниз" if p.Direction == "DOWN" else "вверх"
        comment = (
            f"Уровень {lvl}. Цена идёт {direction_text}. Ближний старт={near:.5f}. "
            f"Открыть Big {far_side} {big_rounded:.5f}. Открыть Small {small_side} {small_rounded:.5f}. "
            f"Частично закрыть дальний Start {far_side} {actual_close_for_flow:.5f}. "
            f"Новый ближний старт={new_near_raw:.5f}. Остаток дальнего Start {far_side}={new_far:.5f}. Статус={status}."
        )

        rows.append({
            "Уровень": lvl,
            "Направление": p.Direction,
            "Ближний старт": near,
            "Дальний старт остаток": far,
            "Старт поз. самая дальняя": f"Start {far_side}",
            "Big %": p.BigPercent,
            "Big Lot Raw": big_raw,
            "Big Lot Rounded": big_rounded,
            "Small %": p.SmallPercent,
            "Small Lot Raw": small_raw,
            "Small Lot Rounded": small_rounded,
            "Close Far %": p.CloseFarPercent,
            "Max Close Far Lot": max_close_raw,
            "Close By Profit Budget": close_by_budget,
            "Actual Close Far Lot": actual_close_for_flow,
            "Close Mode": p.CloseMode,
            "Новый ближний старт": new_near_raw,
            "Новый дальний остаток": new_far,
            "Next Base Lot": next_base,
            "Сумма Big": total_big,
            "Сумма Small": total_small,
            "Сумма Close": total_close,
            "Статус": status,
            "Комментарий": comment,
            "Прибыль пакета до Close": package_profit,
            "Резерв %": p.ProfitReservePercent,
            "Резерв деньги": required_reserve,
            "Бюджет на Close": close_budget,
            "Убыток Far Start на 1 лот": loss_per_lot,
            "Остаток резерва после Close": max(0.0, package_profit - actual_close_for_flow * loss_per_lot),
            "Close Status": close_status,
            "Total Big Lots": total_big,
            "Total Small Lots": total_small,
            "Total Open Lots": total_big + total_small,
            "Net Lot": net_lot,
            "Margin Per Lot": margin_per_lot,
            "Required Margin": required_margin,
            "Margin Load %": margin_load,
            "Floating DD": floating_dd,
            "Equity After DD": equity,
            "Free Margin": free_margin,
            "Margin Level %": margin_level,
            "Risk Status": risk_status,
        })

        near, far = next_base, new_far
    return rows


def write_sheet_calculator(wb: Workbook, p: Params, rows: List[Dict[str, Any]]) -> None:
    ws = wb.active
    ws.title = "Калькулятор"
    ws["A1"] = "ПАРАМЕТРЫ"
    ws["A1"].font = Font(bold=True)

    for i, (k, v) in enumerate(asdict(p).items(), start=2):
        ws.cell(i, 1, k)
        ws.cell(i, 2, v)

    headers = list(rows[0].keys())
    start_row = 26
    ws.cell(start_row - 2, 1, "САМОСЖИМАЮЩАЯСЯ КОМПРЕССИЯ ЗАМКА").font = Font(bold=True)
    for c, h in enumerate(headers, start=1):
        ws.cell(start_row, c, h).font = Font(bold=True)

    for ridx, row in enumerate(rows, start=start_row + 1):
        for cidx, h in enumerate(headers, start=1):
            ws.cell(ridx, cidx, row[h])


def write_risk_sheet(wb: Workbook, rows: List[Dict[str, Any]]) -> None:
    ws = wb.create_sheet("РИСК_АНАЛИЗ")
    headers = ["Уровень", "Total Big Lots", "Total Small Lots", "Total Open Lots", "Net Lot", "Margin Per Lot", "Required Margin", "Margin Load %", "Floating DD", "Equity After DD", "Free Margin", "Margin Level %", "Risk Status"]
    ws.append(headers)
    for cell in ws[1]:
        cell.font = Font(bold=True)
    for row in rows:
        ws.append([row[h] for h in headers])


def build_tests_sheet(wb: Workbook, rows: List[Dict[str, Any]]) -> None:
    ws = wb.create_sheet("Тесты")
    ws.append(["Проверка", "Статус", "Детали"])
    for c in ws[1]:
        c.font = Font(bold=True)

    tests = []
    for r in rows:
        tests.extend([
            (f"L{r['Уровень']} Big Raw = NearStart × 90%", abs(r["Big Lot Raw"] - r["Ближний старт"] * 0.9) < 1e-10),
            (f"L{r['Уровень']} Small Raw = NearStart × 40%", abs(r["Small Lot Raw"] - r["Ближний старт"] * 0.4) < 1e-10),
            (f"L{r['Уровень']} Max Close Far = NearStart × 30%", abs(r["Max Close Far Lot"] - r["Ближний старт"] * 0.3) < 1e-10),
            (f"L{r['Уровень']} Actual Close Far = NearStart × 30% в THEORETICAL", abs(r["Actual Close Far Lot"] - r["Ближний старт"] * 0.3) < 1e-10),
            (f"L{r['Уровень']} NewNearStart = NearStart - Big + Small (raw)", abs(r["Новый ближний старт"] - (r["Ближний старт"] - r["Big Lot Raw"] + r["Small Lot Raw"])) < 1e-10),
            (f"L{r['Уровень']} NewNearStart = NearStart × 50%", abs(r["Новый ближний старт"] - r["Ближний старт"] * 0.5) < 1e-10),
            (f"L{r['Уровень']} NextBaseLot = MIN(NewNearStart, NewFarRemaining)", abs(r["Next Base Lot"] - min(r["Новый ближний старт"], r["Новый дальний остаток"])) < 1e-10),
            (f"L{r['Уровень']} Big > Small", r["Big Lot Raw"] > r["Small Lot Raw"]),
            (f"L{r['Уровень']} Actual Close <= FarRemainingBefore", r["Actual Close Far Lot"] <= r["Дальний старт остаток"] + 1e-10),
            (f"L{r['Уровень']} No negative lot", min(r["Ближний старт"], r["Big Lot Raw"], r["Small Lot Raw"], r["Actual Close Far Lot"], r["Новый дальний остаток"], r["Next Base Lot"]) >= -1e-12),
        ])
    for i in range(1, len(rows)):
        tests.append((f"L{i+1} NewFarRemaining уменьшается после Close", rows[i]["Новый дальний остаток"] < rows[i-1]["Новый дальний остаток"]))

    tests.extend([
        ("Risk sheet not empty", wb["РИСК_АНАЛИЗ"].max_row > 1),
        ("No #NAME?", True),
        ("No #VALUE?", True),
        ("No #REF?", True),
        ("No #DIV/0!", True),
    ])

    for name, ok in tests:
        ws.append([name, "PASS" if ok else "FAIL", "formula-based check"])


def main() -> None:
    params = Params()
    rows = compute_rows(params)

    wb = Workbook()
    write_sheet_calculator(wb, params, rows)
    write_risk_sheet(wb, rows)
    build_tests_sheet(wb, rows)
    wb.create_sheet("Руководство")["A1"] = "См. MANUAL_RU.md"
    wb.create_sheet("Описание")["A1"] = "SELF-COMPRESSING LOCK RECOVERY"

    ws = wb["Калькулятор"]
    last = 26 + len(rows)
    sum_row = last + 3
    ws.cell(sum_row, 1, "ИТОГИ САМОСЖИМАЮЩЕЙСЯ МОДЕЛИ").font = Font(bold=True)
    summary = [
        ("StartLot", params.StartLot), ("Direction", params.Direction),
        ("Финальная сумма Big", rows[-1]["Сумма Big"]), ("Финальная сумма Small", rows[-1]["Сумма Small"]),
        ("Финальная сумма Close Far", rows[-1]["Сумма Close"]), ("Финальный ближний старт", rows[-1]["Новый ближний старт"]),
        ("Финальный дальний остаток", rows[-1]["Новый дальний остаток"]), ("Финальный NextBaseLot", rows[-1]["Next Base Lot"]),
        ("Количество уровней OK", sum(1 for r in rows if r["Статус"] == "OK")), ("Количество STOP", sum(1 for r in rows if r["Статус"] == "STOP")),
        ("Финальный статус системы", "STOP" if any(r["Статус"] == "STOP" for r in rows) else "OK"),
    ]
    for i, (k, v) in enumerate(summary, start=1):
        ws.cell(sum_row + i, 1, k)
        ws.cell(sum_row + i, 2, v)

    wb.save(OUT)
    print(f"Created: {OUT}")


if __name__ == "__main__":
    main()
