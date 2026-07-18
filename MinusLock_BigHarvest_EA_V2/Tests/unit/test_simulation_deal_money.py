from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SIMULATION = (ROOT / "Include" / "SimulationEngine.mqh").read_text(encoding="utf-8")
TYPES = (ROOT / "Include" / "Types.mqh").read_text(encoding="utf-8")
STATE_MACHINE = (ROOT / "Include" / "StateMachine.mqh").read_text(encoding="utf-8")


def test_simulation_deal_keeps_all_mt5_money_components():
    for field in ("profitMoney", "commission", "swap", "fee", "netMoney", "positionIdentifier", "dealTime"):
        assert field in TYPES
    assert "profitMoney + commission + swap + fee" in SIMULATION
    assert "SimRealizedPL += SimClosedDeals[index].netMoney" in SIMULATION


def test_small_simulation_audit_uses_deal_identity_and_net_money():
    assert "SimClosedDeals[i].positionTicket==a.ticket" in STATE_MACHINE
    assert "SimClosedDeals[i].positionIdentifier==a.identifier" in STATE_MACHINE
    assert "net+=SimClosedDeals[i].netMoney" in STATE_MACHINE
    assert "commission+=SimClosedDeals[i].commission" in STATE_MACHINE
