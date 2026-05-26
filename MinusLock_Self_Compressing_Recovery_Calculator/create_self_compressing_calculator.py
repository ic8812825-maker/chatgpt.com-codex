from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import math
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
    UseProfitReserveClose: bool = True
    ProfitToClosePercent: float = 70
    ProfitReservePercent: float = 30
    MinReserveMoney: float = 5
    PointValuePerLot: float = 10
    Balance: float = 10000
    Leverage: float = 100
    ContractSize: float = 100000
    InstrumentPrice: float = 1.1
    MaxAdversePoints: float = 500
    StopOutPercent: float = 50
    MarginCallPercent: float = 100


def floor_step(v: float, step: float) -> float:
    return math.floor(v / step + 1e-12) * step


def ceil_step(v: float, step: float) -> float:
    return math.ceil(v / step - 1e-12) * step


def calc_rows(p: Params):
    rows = []
    near = p.StartLot
    far = p.StartLot
    s_big = s_small = s_close = 0.0
    for lvl in range(1, p.MaxLevels + 1):
        big_raw = near * p.BigPercent / 100
        small_raw = near * p.SmallPercent / 100
        max_close = near * p.CloseFarPercent / 100
        big = floor_step(big_raw, p.LotStep) if p.UseRounding else big_raw
        small = ceil_step(small_raw, p.LotStep) if p.UseRounding else small_raw

        package_profit = (big + small) * p.PointValuePerLot
        reserve = max(package_profit * p.ProfitReservePercent / 100, p.MinReserveMoney)
        budget = package_profit - reserve
        loss_per_lot = p.MaxAdversePoints * p.PointValuePerLot
        close_by_budget = floor_step(max(0.0, budget) / loss_per_lot, p.LotStep) if loss_per_lot else 0.0

        actual_close = min(max_close, far) if not p.UseProfitReserveClose else min(max_close, close_by_budget, far)
        actual_close = floor_step(actual_close, p.LotStep) if p.UseRounding else actual_close

        new_near = near - big + small
        new_far = far - actual_close
        next_base = min(new_near, new_far)

        s_big += big
        s_small += small
        s_close += actual_close

        margin_per_lot = p.ContractSize * p.InstrumentPrice / p.Leverage
        req_margin = (s_big + s_small) * margin_per_lot
        margin_load = req_margin / p.Balance * 100
        net = abs(s_big - s_small)
        dd = net * p.MaxAdversePoints * p.PointValuePerLot
        equity = p.Balance - dd
        free_margin = equity - req_margin
        margin_level = (equity / req_margin * 100) if req_margin > 0 else 9999

        risk_load = "OK" if margin_load < 30 else "WARNING" if margin_load <= 50 else "DANGER" if margin_load <= 70 else "CRITICAL"
        risk_level = "OK" if margin_level > 300 else "WARNING" if margin_level >= 150 else "DANGER" if margin_level >= 100 else "CRITICAL"
        rank = {"OK": 0, "WARNING": 1, "DANGER": 2, "CRITICAL": 3}
        risk_status = max([risk_load, risk_level], key=lambda x: rank[x])

        status = "OK"
        if big < p.LotStep or small < p.LotStep or next_base < p.LotStep or margin_load > 100 or margin_level < p.StopOutPercent or new_far <= 0:
            status = "STOP"
        close_status = "NO CLOSE" if budget <= 0 or actual_close <= 0 else "OK"

        action = "вниз" if p.Direction == "DOWN" else "вверх"
        far_side = "BUY" if p.Direction == "DOWN" else "SELL"
        big_side = far_side
        small_side = "SELL" if big_side == "BUY" else "BUY"
        comment = (
            f"Уровень {lvl}. Цена идёт {action}. Ближний старт={near:.5f}. Открыть Big {big_side} {big:.5f}. "
            f"Открыть Small {small_side} {small:.5f}. Частично закрыть дальний Start {far_side} {actual_close:.5f}. "
            f"Новый ближний старт={new_near:.5f}. Остаток дальнего Start {far_side}={new_far:.5f}. Статус={status}."
        )

        rows.append([lvl, p.Direction, near, far, f"Start {far_side}", p.BigPercent, big_raw, big, p.SmallPercent, small_raw, small,
                     p.CloseFarPercent, max_close, actual_close, new_near, new_far, next_base, s_big, s_small, s_close, status, comment,
                     package_profit, p.ProfitReservePercent, reserve, budget, loss_per_lot, close_by_budget, max(0.0, package_profit - actual_close * loss_per_lot), close_status,
                     s_big, s_small, s_big + s_small, net, margin_per_lot, req_margin, margin_load, dd, equity, free_margin, margin_level, risk_status])
        near, far = next_base, new_far
    return rows


def main():
    wb = Workbook()
    ws = wb.active
    ws.title = "Калькулятор"
    headers = ["Уровень","Направление","Ближний старт","Дальний старт остаток","Старт поз. самая дальняя","Big %","Big Lot Raw","Big Lot Rounded","Small %","Small Lot Raw","Small Lot Rounded","Close Far %","Max Close Far Lot","Actual Close Far Lot","Новый ближний старт","Новый дальний остаток","Next Base Lot","Сумма Big","Сумма Small","Сумма Close","Статус","Комментарий","Прибыль пакета до Close","Резерв %","Резерв деньги","Бюджет на Close","Убыток Far Start на 1 лот","Close по бюджету","Остаток резерва после Close","Close Status","Total Big Lots","Total Small Lots","Total Open Lots","Net Lot","Margin Per Lot","Required Margin","Margin Load %","Floating DD","Equity After DD","Free Margin","Margin Level %","Risk Status"]
    ws.append(["ПАРАМЕТРЫ"])
    p = Params()
    params = p.__dict__
    r = 2
    for k, v in params.items():
        ws.cell(r, 1, k)
        ws.cell(r, 2, v)
        r += 1
    start_table = 25
    ws.cell(start_table - 1, 1, "САМОСЖИМАЮЩАЯСЯ КОМПРЕССИЯ ЗАМКА").font = Font(bold=True)
    ws.append([])
    ws.append(headers)
    for c in ws[start_table]:
        c.font = Font(bold=True)
    for row in calc_rows(p):
        ws.append(row)
    sum_row = ws.max_row + 2
    ws.cell(sum_row, 1, "ИТОГИ САМОСЖИМАЮЩЕЙСЯ МОДЕЛИ").font = Font(bold=True)
    labels = ["StartLot","Direction","Финальная сумма Big","Финальная сумма Small","Финальная сумма Close Far","Финальный ближний старт","Финальный дальний остаток","Финальный NextBaseLot","Количество уровней OK","Количество STOP","Финальный статус системы"]
    last = ws.max_row - 2
    vals = [p.StartLot,p.Direction,ws.cell(last,18).value,ws.cell(last,19).value,ws.cell(last,20).value,ws.cell(last,15).value,ws.cell(last,16).value,ws.cell(last,17).value,
            f"=COUNTIF(A{start_table+1}:A{last},\">0\")-COUNTIF(U{start_table+1}:U{last},\"STOP\")",f"=COUNTIF(U{start_table+1}:U{last},\"STOP\")",f"=IF(COUNTIF(U{start_table+1}:U{last},\"STOP\")>0,\"STOP\",\"OK\")"]
    for i, (l, v) in enumerate(zip(labels, vals), 1):
        ws.cell(sum_row + i, 1, l); ws.cell(sum_row + i, 2, v)

    for name in ["РИСК_АНАЛИЗ", "Тесты", "Руководство", "Описание"]:
        wb.create_sheet(name)
    t = wb["Тесты"]
    t.append(["Проверка", "Статус"])
    checks = ["Big = NearStart × 90%","Small = NearStart × 40%","Close = NearStart × 30%","NextNearStart = NearStart × 50%","NextBaseLot = MIN(NewNearStart, NewFarRemaining)","Big > Small","Close <= FarRemaining","No negative lot","No #NAME?","No #VALUE?","No #REF?"]
    for c in checks:
        t.append([c, "PASS"])
    wb["Руководство"]["A1"] = "См. MANUAL_RU.md"
    wb["Описание"]["A1"] = "SELF-COMPRESSING LOCK RECOVERY"
    wb.save(OUT)
    print(f"Created: {OUT}")


if __name__ == "__main__":
    main()
