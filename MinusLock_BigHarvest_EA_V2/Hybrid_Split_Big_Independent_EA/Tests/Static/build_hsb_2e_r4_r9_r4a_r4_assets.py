#!/usr/bin/env python3
"""Deterministically build the R4A-R4 schema and positive runtime fixtures."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCHEMA = ROOT / "Tests/Contracts/HSB_2E_R4_R9_R4A_R4_SCENARIO_INPUT_SCHEMA_V3.json"
FIXTURES = ROOT / "Tests/Vectors/HSB_2E_R4_R9_R4A_R4_POSITIVE_BASES_V3.json"
SCENARIOS = ("INITIAL", "BIG", "SMALL", "FINAL", "RESTART_CONTINUATION", "REPLAY_COMMITTED", "LIFECYCLE")


def field(kind: str, *, semantic: str | None = None, unit: str = "NONE", minimum=None,
          maximum=None, enum=None, grid=None, properties=None, items=None) -> dict:
    result = {
        "type": kind, "requiredState": "REQUIRED", "required": True,
        "nullable": False, "unit": unit, "applicableScenarios": list(SCENARIOS),
    }
    if semantic is not None:
        result["semanticType"] = semantic
    if minimum is not None:
        result["minimum"] = minimum
    if maximum is not None:
        result["maximum"] = maximum
    if enum is not None:
        result["enum"] = enum
    if grid is not None:
        result["gridSource"] = grid
    if properties is not None:
        result["additionalProperties"] = False
        result["properties"] = properties
    if items is not None:
        result["items"] = items
    return result


ID = lambda: field("string", semantic="IDENTIFIER", minimum=1)
DIGEST = lambda: field("string", semantic="SHA256", minimum=64, maximum=64)
DEC_MONEY = lambda minimum=None: field("string", semantic="DECIMAL", unit="ACCOUNT_MONEY", minimum=minimum)
DEC_VOLUME = lambda minimum="0": field("string", semantic="DECIMAL", unit="LOTS", minimum=minimum,
                                        grid="scenarioInput.broker.volumeStep")
DEC_PRICE = lambda: field("string", semantic="DECIMAL", unit="PRICE", minimum="0",
                          grid="scenarioInput.broker.tickSize")
INTEGER = lambda minimum=0: field("integer", semantic="EXACT_INTEGER", minimum=minimum)
TIMESTAMP = lambda: field("integer", semantic="UNIX_TIME_SECONDS", unit="SECONDS", minimum=1)


def obj(properties: dict) -> dict:
    return field("object", properties=properties)


def array(items: dict) -> dict:
    return field("array", items=items, minimum=0)


def schema() -> dict:
    position = obj({
        "ticket": ID(), "accountId": ID(), "symbol": ID(), "magic": INTEGER(1), "cycleId": ID(),
        "role": field("string", enum=["NEAR", "BIG", "SMALL", "FAR"]),
        "direction": field("string", enum=["BUY", "SELL"]),
        "authoritativeVolume": DEC_VOLUME("0.01"), "volume": DEC_VOLUME("0.01"),
        "openPrice": DEC_PRICE(), "stateRevision": INTEGER(), "snapshotRevision": INTEGER(),
    })
    intent = obj({
        "intentId": ID(), "transactionId": ID(), "actionId": ID(), "positionTicket": ID(),
        "role": field("string", enum=["NEAR", "BIG", "SMALL", "FAR"]),
        "direction": field("string", enum=["BUY", "SELL"]), "requestedVolume": DEC_VOLUME("0.01"),
        "closeMode": field("string", enum=["PARTIAL", "FULL"]), "createdTimestamp": TIMESTAMP(),
        "expiresTimestamp": TIMESTAMP(), "stateRevision": INTEGER(), "snapshotRevision": INTEGER(),
    })
    deal = obj({
        "dealId": ID(), "eventId": ID(), "intentId": ID(), "positionTicket": ID(), "accountId": ID(),
        "symbol": ID(), "magic": INTEGER(1), "cycleId": ID(), "transactionId": ID(), "actionId": ID(),
        "role": field("string", enum=["NEAR", "BIG", "SMALL", "FAR"]),
        "direction": field("string", enum=["BUY", "SELL"]), "volume": DEC_VOLUME("0.01"),
        "price": DEC_PRICE(), "commission": DEC_MONEY(), "swap": DEC_MONEY(), "fee": DEC_MONEY(),
        "timestamp": TIMESTAMP(), "stateRevision": INTEGER(), "snapshotRevision": INTEGER(),
        "confirmed": field("boolean"),
    })
    event = obj({
        "eventId": ID(), "dealId": ID(), "intentId": ID(), "positionTicket": ID(), "accountId": ID(),
        "symbol": ID(), "magic": INTEGER(1), "cycleId": ID(), "transactionId": ID(), "actionId": ID(),
        "role": field("string", enum=["NEAR", "BIG", "SMALL", "FAR"]),
        "direction": field("string", enum=["BUY", "SELL"]), "volume": DEC_VOLUME("0.01"),
        "price": DEC_PRICE(), "commission": DEC_MONEY(), "swap": DEC_MONEY(), "fee": DEC_MONEY(),
        "timestamp": TIMESTAMP(), "stateRevision": INTEGER(), "snapshotRevision": INTEGER(),
        "confirmed": field("boolean"),
    })
    decimal_entry = obj({"key": ID(), "value": DEC_MONEY()})
    return {
        "schemaId": "HSBI_ScenarioInput_V3", "schemaVersion": "3.0.0", "additionalProperties": False,
        "root": obj({
            "schemaVersion": field("string", enum=["3.0.0"]), "scenario": field("string", enum=list(SCENARIOS)),
            "context": obj({
                "accountId": ID(), "symbol": ID(), "magic": INTEGER(1), "cycleId": ID(),
                "transactionId": ID(), "actionId": ID(), "stateRevision": INTEGER(),
                "snapshotRevision": INTEGER(), "moneyStateVersion": INTEGER(1),
            }),
            "broker": obj({
                "digits": INTEGER(), "point": DEC_PRICE(), "tickSize": DEC_PRICE(),
                "tickValue": DEC_MONEY("0.00000001"), "contractSize": field("string", semantic="DECIMAL", unit="UNITS", minimum="0.00000001"),
                "volumeMin": DEC_VOLUME("0.01"), "volumeMax": DEC_VOLUME("0.01"), "volumeStep": DEC_VOLUME("0.01"),
                "bid": DEC_PRICE(), "ask": DEC_PRICE(), "maximumDeviation": INTEGER(),
                "priceRoundingPolicy": field("string", enum=["TICK_HALF_EVEN"]),
                "volumeRoundingPolicy": field("string", enum=["STEP_FLOOR"]),
            }),
            "snapshot": obj({"symbol": ID(), "magic": INTEGER(1), "revision": INTEGER(), "timestamp": TIMESTAMP()}),
            "temporalPolicy": obj({"validFrom": TIMESTAMP(), "validUntil": TIMESTAMP(),
                                   "minimumTimestamp": TIMESTAMP(), "allowedUpperBound": TIMESTAMP()}),
            "positions": array(position), "intents": array(intent), "deals": array(deal), "events": array(event),
            "persistedState": obj({
                "previousStateDigest": DIGEST(), "authoritativeLedgerRoot": DIGEST(), "transactionJournalRoot": DIGEST(),
                "consumedDealIds": array(ID()), "seenEventIds": array(ID()),
                "dealEventBindings": array(obj({"dealId": ID(), "eventId": ID()})),
                "cumulativeFills": array(obj({"ticket": ID(), "volume": DEC_VOLUME()})),
                "moneyByDeal": array(decimal_entry), "moneyByTicket": array(decimal_entry),
                "reserve": DEC_MONEY(), "recoveryPL": DEC_MONEY(),
                "farState": obj({"ticket": ID(), "volume": DEC_VOLUME(), "loss": DEC_MONEY()}),
                "stateRevision": INTEGER(),
            }),
            "brokerProposal": obj({"proposalId": ID(), "digest": DIGEST(), "requestedVolume": DEC_VOLUME("0.01")}),
            "economic": obj({
                "availableMoney": DEC_MONEY(), "allocatedMoney": DEC_MONEY(), "remainingMoney": DEC_MONEY(),
                "closeFarBudget": DEC_MONEY(), "reserveAddition": DEC_MONEY(), "reserveConsumption": DEC_MONEY(),
                "reserveBefore": DEC_MONEY(), "farActualLoss": DEC_MONEY(), "partialFarVolume": DEC_VOLUME(),
                "bigResidualVolume": DEC_VOLUME(), "newFarVolume": DEC_VOLUME(),
                "catchUpRatio": field("string", semantic="DECIMAL", unit="RATIO", minimum="0"),
                "recoveryPL": DEC_MONEY(), "reserveCoverage": DEC_MONEY(), "requiredCoverage": DEC_MONEY(),
                "tailCount": INTEGER(),
            }),
            "allocationPolicy": obj({"allocatedMoney": DEC_MONEY(), "remainingMoney": DEC_MONEY(),
                                     "reserveAddition": DEC_MONEY(), "policyId": ID()}),
            "fsm": obj({"inputState": field("string", enum=["INITIAL", "BIG", "SMALL", "FINAL", "COMMITTED"]),
                        "outputState": field("string", enum=["BIG", "SMALL", "FINAL", "COMMITTED"]),
                        "inputRevision": INTEGER(), "outputRevision": INTEGER()}),
            "certificate": obj({
                "version": INTEGER(1), "body": DIGEST(), "previousStateDigest": DIGEST(),
                "authoritativeLedgerRoot": DIGEST(), "transactionJournalRoot": DIGEST(),
                "claimedBrokerDigest": DIGEST(), "claimedEconomicDigest": DIGEST(),
                "claimedAllocationDigest": DIGEST(), "claimedPersistenceDigest": DIGEST(),
                "claimedFsmDigest": DIGEST(), "claimedOutputStateDigest": DIGEST(), "digest": DIGEST(),
            }),
        }),
    }


def digest(value) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def fixture(scenario: str, variant: int, serial: int) -> dict:
    buy = variant % 2 == 1
    direction = "BUY" if buy else "SELL"
    opposite = "SELL" if buy else "BUY"
    ts = 1_800_000_000 + serial * 100
    volume = f"{0.10 + variant * 0.01:.2f}"
    price = f"{1.1000 + serial * 0.0010:.4f}"
    ticket = f"TKT-{scenario}-{variant}"
    intent_id, deal_id, event_id = f"INT-{serial}", f"DEAL-{serial}", f"EVENT-{serial}"
    account, symbol, magic = f"ACC-{1 + variant}", "EURUSD", 8812825 + variant
    cycle, tx, action = f"CYCLE-{scenario}-{variant}", f"TX-{serial}", f"ACT-{serial}"
    rev = 10 + serial
    roles = {"INITIAL": "NEAR", "BIG": "BIG", "SMALL": "SMALL", "FINAL": "FAR",
             "RESTART_CONTINUATION": "BIG", "REPLAY_COMMITTED": "FAR", "LIFECYCLE": "SMALL"}
    role = roles[scenario]
    persisted_deals = [deal_id] if scenario in ("RESTART_CONTINUATION", "REPLAY_COMMITTED", "LIFECYCLE") else []
    persisted_events = [event_id] if persisted_deals else []
    available = 100 + serial
    allocated = 60 + variant
    remaining = available - allocated
    root_seed = {"scenario": scenario, "variant": variant, "revision": rev}
    ledger, journal, previous = digest([root_seed, "ledger"]), digest([root_seed, "journal"]), digest([root_seed, "previous"])
    broker_proposal = {"proposalId": f"BP-{serial}", "digest": digest([root_seed, "broker"]), "requestedVolume": volume}
    economic = {
        "availableMoney": str(available), "allocatedMoney": str(allocated), "remainingMoney": str(remaining),
        "closeFarBudget": str(20 + variant), "reserveAddition": "5", "reserveConsumption": "0",
        "reserveBefore": str(30 + variant), "farActualLoss": str(10 + variant), "partialFarVolume": "0.00",
        "bigResidualVolume": volume if scenario in ("BIG", "RESTART_CONTINUATION") else "0.00",
        "newFarVolume": "0.00", "catchUpRatio": "1.00", "recoveryPL": str(15 + variant),
        "reserveCoverage": str(30 + variant), "requiredCoverage": str(10 + variant), "tailCount": 1,
    }
    allocation = {"allocatedMoney": str(allocated), "remainingMoney": str(remaining),
                  "reserveAddition": "5", "policyId": f"ALLOC-{scenario}"}
    persisted = {
        "previousStateDigest": previous, "authoritativeLedgerRoot": ledger, "transactionJournalRoot": journal,
        "consumedDealIds": persisted_deals, "seenEventIds": persisted_events,
        "dealEventBindings": ([{"dealId": deal_id, "eventId": event_id}] if persisted_deals else []),
        "cumulativeFills": [{"ticket": ticket, "volume": volume}],
        "moneyByDeal": [{"key": deal_id, "value": str(allocated)}],
        "moneyByTicket": [{"key": ticket, "value": str(allocated)}],
        "reserve": str(35 + variant), "recoveryPL": str(15 + variant),
        "farState": {"ticket": ticket, "volume": volume, "loss": str(10 + variant)}, "stateRevision": rev,
    }
    fsm_states = {"INITIAL": ("INITIAL", "BIG"), "BIG": ("BIG", "SMALL"), "SMALL": ("SMALL", "FINAL"),
                  "FINAL": ("FINAL", "COMMITTED"), "RESTART_CONTINUATION": ("BIG", "SMALL"),
                  "REPLAY_COMMITTED": ("COMMITTED", "COMMITTED"), "LIFECYCLE": ("SMALL", "FINAL")}
    input_state, output_state = fsm_states[scenario]
    fsm = {"inputState": input_state, "outputState": output_state, "inputRevision": rev, "outputRevision": rev + 1}
    position = {"ticket": ticket, "accountId": account, "symbol": symbol, "magic": magic, "cycleId": cycle,
                "role": role, "direction": direction, "authoritativeVolume": volume, "volume": volume,
                "openPrice": price, "stateRevision": rev, "snapshotRevision": rev}
    intent = {"intentId": intent_id, "transactionId": tx, "actionId": action, "positionTicket": ticket,
              "role": role, "direction": opposite, "requestedVolume": volume, "closeMode": "FULL",
              "createdTimestamp": ts - 10, "expiresTimestamp": ts + 100, "stateRevision": rev,
              "snapshotRevision": rev}
    common = {"eventId": event_id, "dealId": deal_id, "intentId": intent_id, "positionTicket": ticket,
              "accountId": account, "symbol": symbol, "magic": magic, "cycleId": cycle, "transactionId": tx,
              "actionId": action, "role": role, "direction": opposite, "volume": volume, "price": price,
              "commission": "-1", "swap": "0", "fee": "0", "timestamp": ts,
              "stateRevision": rev, "snapshotRevision": rev, "confirmed": True}
    deal = dict(common)
    event = dict(common)
    cert_body = digest({"broker": broker_proposal, "economic": economic, "allocation": allocation,
                        "persisted": persisted, "fsm": fsm, "output": output_state})
    certificate = {
        "version": 3, "body": cert_body, "previousStateDigest": previous,
        "authoritativeLedgerRoot": ledger, "transactionJournalRoot": journal,
        "claimedBrokerDigest": broker_proposal["digest"], "claimedEconomicDigest": digest(economic),
        "claimedAllocationDigest": digest(allocation), "claimedPersistenceDigest": digest(persisted),
        "claimedFsmDigest": digest(fsm), "claimedOutputStateDigest": digest(output_state),
    }
    certificate["digest"] = digest(certificate)
    runtime = {
        "schemaVersion": "3.0.0", "scenario": scenario,
        "context": {"accountId": account, "symbol": symbol, "magic": magic, "cycleId": cycle,
                    "transactionId": tx, "actionId": action, "stateRevision": rev,
                    "snapshotRevision": rev, "moneyStateVersion": 3},
        "broker": {"digits": 4, "point": "0.0001", "tickSize": "0.0001", "tickValue": "10",
                   "contractSize": "100000", "volumeMin": "0.01", "volumeMax": "100.00",
                   "volumeStep": "0.01", "bid": price, "ask": f"{float(price)+0.0002:.4f}",
                   "maximumDeviation": 10, "priceRoundingPolicy": "TICK_HALF_EVEN",
                   "volumeRoundingPolicy": "STEP_FLOOR"},
        "snapshot": {"symbol": symbol, "magic": magic, "revision": rev, "timestamp": ts},
        "temporalPolicy": {"validFrom": ts - 100, "validUntil": ts + 200,
                           "minimumTimestamp": ts - 200, "allowedUpperBound": ts + 300},
        "positions": [position], "intents": [intent], "deals": [deal], "events": [event],
        "persistedState": persisted, "brokerProposal": broker_proposal, "economic": economic,
        "allocationPolicy": allocation, "fsm": fsm, "certificate": certificate,
    }
    return {"scenarioInput": runtime, "testContract": {"fixtureId": f"V3-{scenario}-{variant}",
            "classification": "POSITIVE_BASE", "scenario": scenario,
            "expectedApplicability": {"SCHEMA": True, "NUMERIC_FINITE": True}}}


def main() -> None:
    SCHEMA.write_text(json.dumps(schema(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    fixtures = [fixture(s, v, i * 4 + v) for i, s in enumerate(SCENARIOS) for v in range(1, 5)]
    FIXTURES.write_text(json.dumps({"schemaVersion": "3.0.0", "fixtures": fixtures}, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
