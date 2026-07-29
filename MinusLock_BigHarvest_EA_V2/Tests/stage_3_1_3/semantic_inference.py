"""Source-only semantic inference for Stage 3.1.3 mapping candidates.

No mapping-document claim is accepted by this module.  Its inputs are a parsed
symbol and source text at declaration/use sites; its output is compared with JSON
claims by the validator.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable

from stage_3_1_3.source_evidence import Symbol, sanitise


UNIT_ANCHORS = {
    "POSITION_VOLUME": "LOT", "DEAL_VOLUME": "LOT", "ORDER_VOLUME": "LOT",
    "DEAL_PROFIT": "MONEY", "DEAL_COMMISSION": "MONEY", "DEAL_SWAP": "MONEY",
    "ACCOUNT_EQUITY": "MONEY", "ACCOUNT_MARGIN": "MONEY", "ACCOUNT_BALANCE": "MONEY",
    "SYMBOL_BID": "PRICE", "SYMBOL_ASK": "PRICE", "SYMBOL_POINT": "PRICE_PER_POINT",
    "SYMBOL_TRADE_TICK_SIZE": "PRICE", "POSITION_PRICE": "PRICE", "DEAL_PRICE": "PRICE",
}
UNIT_WORDS = {
    "LOT": ("lot", "volume", "lots"), "MONEY": ("profit", "money", "reserve", "margin", "equity", "cost", "commission", "swap", "fee", "pnl", "pl"),
    "PRICE": ("price", "bid", "ask", "ticksize", "tick_size", "openprice", "closeprice"),
    "POINTS": ("points", "distancepoints", "deviation"), "RATIO": ("ratio", "share", "percent", "multiplier", "coverage", "factor"),
    "IDENTITY": ("ticket", "identifier", "positionid", "position_id", "orderid", "dealid", "cycleid", "eventid", "magic", "symbol"),
    "STATE": ("state", "phase", "reason", "error", "result", "outcome"),
}


@dataclass(frozen=True)
class SourceSemanticEvidence:
    identifier: str
    primitive_type: str
    entity_kind: str
    declaration_scope: str
    inferred_unit: str
    unit_evidence: tuple[str, ...]
    inferred_scope: str
    scope_evidence: tuple[str, ...]
    source_class: str
    authority_score: float
    authority_evidence: tuple[str, ...]
    projected_actual: str
    projected_actual_evidence: tuple[str, ...]
    lifecycle: str
    lifecycle_evidence: tuple[str, ...]
    read_sites: tuple[str, ...]
    write_sites: tuple[str, ...]

    def dict(self):
        value = asdict(self)
        for key, item in tuple(value.items()):
            if isinstance(item, tuple): value[key] = list(item)
        return value


def _site_text(root: Path, sites: Iterable[str]) -> str:
    chunks=[]
    for site in sites:
        try: file,no=site.rsplit(":",1); no=int(no)
        except ValueError: continue
        path=root/file
        if not path.is_file(): continue
        lines=sanitise(path.read_text(errors="ignore"))[0].splitlines()
        if 0 < no <= len(lines): chunks.append(lines[no-1])
    return "\n".join(chunks)


def infer_unit(symbol: Symbol, source: str) -> tuple[str, tuple[str, ...]]:
    upper=source.upper(); evidence=[]; units=set()
    for anchor,unit in UNIT_ANCHORS.items():
        if anchor in upper: units.add(unit); evidence.append(f"API anchor {anchor}->{unit}")
    name=symbol.identifier.lower().replace("_", "")
    for unit,words in UNIT_WORDS.items():
        if any(word.replace("_", "") in name for word in words): units.add(unit); evidence.append(f"identifier {symbol.identifier}->{unit}")
    if symbol.kind=="input_parameter" and any(x in name for x in ("ratio","share","percent","factor")):
        units.add("RATIO"); evidence.append("typed input naming anchor")
    # Prefer explicit API anchors over weaker naming evidence.
    anchored={UNIT_ANCHORS[a] for a in UNIT_ANCHORS if a in upper}
    if len(anchored)==1:return next(iter(anchored)),tuple(evidence)
    if len(units)==1:return next(iter(units)),tuple(evidence)
    return ("AMBIGUOUS" if units else "UNKNOWN"),tuple(evidence)


def infer_scope(symbol: Symbol) -> tuple[str, tuple[str, ...]]:
    file=symbol.file.replace("\\","/")
    if file.startswith("Tests/"): return "TEST_ONLY",("file under Tests/",)
    if file.startswith("Tools/"): return "OFFLINE_TOOL",("file under Tools/",)
    text=(symbol.scope+" "+symbol.parent_symbol+" "+symbol.identifier).lower()
    if "position" in text:return "PER_POSITION",("position lexical/context anchor",)
    if "deal" in text:return "PER_DEAL",("deal lexical/context anchor",)
    if "order" in text:return "PER_ORDER",("order lexical/context anchor",)
    if "request" in text:return "PER_REQUEST",("request lexical/context anchor",)
    if "plan" in text or "preview" in text:return "PER_PLAN",("plan lexical/context anchor",)
    if "cycle" in text or "context" in text or symbol.kind in {"struct_field","class_field"}:return "PER_CYCLE",("cycle/context storage anchor",)
    if symbol.kind in {"local_variable","function_parameter","output_reference_parameter"}:return "PER_FUNCTION_LOCAL",("function-local storage",)
    if symbol.kind=="input_parameter":return "GLOBAL_RUNTIME",("global input parameter",)
    return "GLOBAL_RUNTIME",("module/global runtime storage",)


def infer_source(symbol: Symbol, source: str) -> tuple[str,float,tuple[str,...]]:
    text=(symbol.identifier+" "+symbol.scope+" "+source).lower(); file=symbol.file.replace("\\","/")
    if file.startswith("Tests/"):return "TEST_ORACLE",0.20,("test-only source",)
    if file.startswith("Tools/"):return "TEST_ORACLE",0.20,("offline tool source",)
    if symbol.kind=="input_parameter":return "POLICY",0.90,("MQL input declaration",)
    if any(x in text for x in ("historydeal", "dealget", "deal_profit", "deal_volume", "dealcommission")):return "LEDGER",1.0,("confirmed deal-history API",)
    if any(x in text for x in ("positionget", "position_volume", "positionsnapshot")):return "TERMINAL_SNAPSHOT",1.0,("terminal position API/snapshot",)
    if any(x in text for x in ("request.", "mqltraderequest", "requested", "requestvolume")):return "REQUEST",0.75,("trade request dataflow",)
    if any(x in text for x in ("ordercalcprofit", "projected", "calculate", "computed", "preview")):return "DERIVED",0.45,("calculation/preview dataflow",)
    if symbol.kind in {"struct_field","class_field","global_variable","static_variable"}:return "CACHE",0.35,("mutable runtime storage",)
    if any(x in text for x in ("comment", "log", "diagnostic")):return "DIAGNOSTIC",0.10,("diagnostic sink",)
    return "DERIVED",0.40,("function-local derived value",)


def infer_temporal(source_class: str, symbol: Symbol, source: str) -> tuple[str,tuple[str,...]]:
    text=(symbol.identifier+" "+source).lower()
    if source_class=="POLICY":value="POLICY"
    elif source_class=="REQUEST":value="REQUESTED"
    elif source_class=="LEDGER":value="ACTUAL_HISTORICAL"
    elif source_class=="TERMINAL_SNAPSHOT":value="ACTUAL_CURRENT"
    elif any(x in text for x in ("filled","confirmed","executed")):value="CONFIRMED"
    elif any(x in text for x in ("actual","current")) and source_class=="CACHE":value="ACTUAL_CURRENT"
    elif source_class=="TEST_ORACLE":value="PROJECTED"
    else:value="PROJECTED"
    return value,(f"source class {source_class}->{value}",)


def infer_lifecycle(source_class: str, symbol: Symbol, source: str) -> tuple[str,tuple[str,...]]:
    text=(symbol.identifier+" "+symbol.scope+" "+source).lower()
    if source_class=="POLICY":value="POLICY"
    elif source_class=="REQUEST":value="REQUESTED"
    elif source_class=="LEDGER":value="DEAL" if "deal" in text else "LEDGER"
    elif source_class=="TERMINAL_SNAPSHOT":value="ACTUAL_POSITION"
    elif "state" in text or "phase" in text:value="STATE"
    elif "tolerance" in text or "epsilon" in text:value="TOLERANCE"
    elif "plan" in text:value="PLAN"
    elif "snapshot" in text:value="SNAPSHOT"
    elif source_class in {"CACHE","DERIVED","TEST_ORACLE"}:value="PROJECTED_VALUE"
    else:value="IDENTITY"
    return value,(f"source/use graph class {source_class}->{value}",)


def infer_semantics(root: Path, symbol: Symbol, read_sites: Iterable[str], write_sites: Iterable[str]) -> SourceSemanticEvidence:
    reads=tuple(read_sites); writes=tuple(write_sites)
    source="\n".join((symbol.declaration_text,_site_text(root,reads),_site_text(root,writes)))
    unit,ue=infer_unit(symbol,source); scope,se=infer_scope(symbol); sc,authority,ae=infer_source(symbol,source)
    temporal,pe=infer_temporal(sc,symbol,source); lifecycle,le=infer_lifecycle(sc,symbol,source)
    return SourceSemanticEvidence(symbol.identifier,symbol.declared_type,symbol.kind,symbol.scope,unit,ue,scope,se,sc,authority,ae,temporal,pe,lifecycle,le,reads,writes)


def expected_unit(type_name: str, unit_text: str) -> str:
    if type_name.startswith("LOT_"):return "LOT"
    if type_name.startswith("MONEY_"):return "MONEY"
    if type_name in {"PRICE_POINT_SIZE"}:return "PRICE_PER_POINT"
    if type_name.startswith("PRICE_"):return "PRICE"
    if type_name in {"POINTS","DISTANCE_POINTS"}:return "POINTS"
    if type_name in {"RATIO","SHARE","PERCENT","MULTIPLIER","RATIO_TOLERANCE","COMPARISON_EPSILON"}:return "RATIO"
    if type_name.endswith(("_ID","_TICKET")) or type_name=="FINGERPRINT":return "IDENTITY"
    if type_name in {"STATE","PHASE","REASON_CODE","ERROR_CODE","EXECUTION_RESULT","GATE_RESULT"}:return "STATE"
    return "OBJECT"
