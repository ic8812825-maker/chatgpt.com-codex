from __future__ import annotations

import csv
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path

@dataclass
class Deal:
    time: str = ""
    direction: str = ""
    volume: float = 0.0
    profit: float = 0.0
    commission: float = 0.0
    swap: float = 0.0
    comment: str = ""

class TableTextParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.cells: list[str] = []
        self._capture = False
        self._buf: list[str] = []

    def handle_starttag(self, tag: str, attrs):
        if tag.lower() in {"td", "th"}:
            self._capture = True
            self._buf = []

    def handle_endtag(self, tag: str):
        if tag.lower() in {"td", "th"} and self._capture:
            self.cells.append("".join(self._buf).strip())
            self._capture = False

    def handle_data(self, data: str):
        if self._capture:
            self._buf.append(data)


def _float(value: str) -> float:
    try:
        return float(str(value).replace(" ", "").replace(",", "."))
    except Exception:
        return 0.0


def parse_mt5_csv(path: Path) -> list[Deal]:
    deals: list[Deal] = []
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            deals.append(Deal(
                time=row.get("time", row.get("Time", "")),
                direction=row.get("direction", row.get("Direction", "")),
                volume=_float(row.get("volume", row.get("Volume", "0"))),
                profit=_float(row.get("profit", row.get("Profit", "0"))),
                commission=_float(row.get("commission", row.get("Commission", "0"))),
                swap=_float(row.get("swap", row.get("Swap", "0"))),
                comment=row.get("comment", row.get("Comment", "")),
            ))
    return deals


def parse_mt5_html(path: Path) -> list[Deal]:
    parser = TableTextParser()
    parser.feed(path.read_text(encoding="utf-8", errors="ignore"))
    # HTML layouts vary. This fallback extracts flat cells and keeps parser availability
    # for future matching against exported MT5 reports.
    return [Deal(comment="HTML_CELLS", profit=0.0, volume=float(len(parser.cells)))]


def parse_report(path: Path) -> list[Deal]:
    if path.suffix.lower() in {".html", ".htm"}:
        return parse_mt5_html(path)
    return parse_mt5_csv(path)
