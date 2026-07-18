import re
from pathlib import Path

SOURCE = (Path(__file__).resolve().parents[2] / "Include" / "SimulationEngine.mqh").read_text(encoding="utf-8")


def arguments(body: str) -> list[str]:
    return [part.strip() for part in body.replace("\n", " ").split(",") if part.strip()]


def test_sim_signed_position_calls_match_declaration_arity():
    declaration = re.search(r"double\s+SimSignedPositionPL\s*\((.*?)\)\s*\{", SOURCE, re.S)
    assert declaration, "SimSignedPositionPL declaration is missing"
    expected_arity = len(arguments(declaration.group(1)))
    calls = list(re.finditer(r"SimSignedPositionPL\s*\((.*?)\)", SOURCE, re.S))
    assert len(calls) >= 2, "expected declaration and at least one call"
    for call in calls[1:]:
        assert len(arguments(call.group(1))) == expected_arity
    call_arguments = arguments(calls[1].group(1))
    assert call_arguments[0] == "SimPositions[index].direction"
