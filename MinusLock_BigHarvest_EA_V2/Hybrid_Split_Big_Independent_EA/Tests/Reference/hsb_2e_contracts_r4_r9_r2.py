#!/usr/bin/env python3
"""Immutable field-specific native R9-R2 contracts."""
from __future__ import annotations
from dataclasses import dataclass,asdict
from decimal import Decimal
from hashlib import sha256
import json
SCHEMA_VERSION=9
@dataclass(frozen=True)
class RuntimeIdentity:
 account:int;symbol:str;magic:int;cycleId:str;transactionId:str;actionId:str;stateRevision:int;snapshotRevision:int;moneyStateVersion:int;brokerPropertyVersion:int
@dataclass(frozen=True)
class BrokerProperties:
 bid:Decimal;ask:Decimal;tickSize:Decimal;tickValue:Decimal;contractSize:Decimal;volumeMin:Decimal;volumeMax:Decimal;volumeStep:Decimal;priceRounding:str;volumeRounding:str
@dataclass(frozen=True)
class TemporalProof:
 snapshotTimestamp:int;policyValidFrom:int;policyValidUntil:int;intentCreatedTimestamp:int;intentExpiresTimestamp:int;dealTimestamp:int;eventTimestamp:int;minimumTimestamp:int;allowedUpperBound:int
@dataclass(frozen=True)
class Position:
 ticket:int;role:str;direction:str;volume:Decimal
@dataclass(frozen=True)
class Intent:
 intentId:str;ticket:int;role:str;direction:str;requestedVolume:Decimal
@dataclass(frozen=True)
class DealEvidence:
 dealId:str;eventId:str;ticket:int;intentId:str;role:str;direction:str;volume:Decimal;price:Decimal;profit:Decimal
@dataclass(frozen=True)
class EconomicInputs:
 initialNet:Decimal;bigNet:Decimal;smallNet:Decimal;farActualLoss:Decimal;reserveBefore:Decimal;recoveryPLBefore:Decimal;closeFarShare:Decimal;reserveShare:Decimal;smallReserveShare:Decimal;farVolume:Decimal;bigVolumeBefore:Decimal;bigClosedConfirmed:Decimal;lossPerLot:Decimal;controlDistance:Decimal;movementToBig:Decimal;requiredCoverage:Decimal
@dataclass(frozen=True)
class PersistedState:
 consumedDealIds:tuple[str,...];seenEventIds:tuple[str,...];dealEventBindings:tuple[tuple[str,str],...];stateRevision:int;settlementRevision:int;evidenceRevision:int;fsm:str;certificateDigest:str
@dataclass(frozen=True)
class ScenarioInput:
 schemaVersion:int;vectorId:str;scenario:str;kind:str;identity:RuntimeIdentity;broker:BrokerProperties;time:TemporalProof;positions:tuple[Position,...];intents:tuple[Intent,...];deals:tuple[DealEvidence,...];economic:EconomicInputs;persisted:PersistedState
@dataclass(frozen=True)
class EconomicResult:
 InitialNetActual:Decimal;BigActualMoney:Decimal;SmallActualMoney:Decimal;FarActualLoss:Decimal;AvailableMoney:Decimal;CloseFarBudget:Decimal;ReserveAddition:Decimal;ReserveBefore:Decimal;ReserveAfter:Decimal;PartialFarVolume:Decimal;BigResidualVolume:Decimal;NewFarVolume:Decimal;CatchUpRatio:Decimal;RecoveryPL:Decimal;ReserveCoverage:bool;ReserveConsumption:Decimal;AllocatedMoney:Decimal;RemainingMoney:Decimal;SettlementEligibility:bool;AllocationEligibility:bool;PersistenceEligibility:bool;StateRevisionBefore:int;StateRevisionAfter:int;CertificateEligibility:bool
@dataclass(frozen=True)
class ScenarioResult:
 schemaVersion:int;status:str;reason:str;phase:str;economic:EconomicResult;settlementApplied:bool;allocationApplied:bool;persisted:PersistedState;certificateDigest:str

def canonical(value):
 if hasattr(value,'__dataclass_fields__'):value=asdict(value)
 if isinstance(value,Decimal):return str(value)
 if isinstance(value,dict):return {k:canonical(v) for k,v in sorted(value.items())}
 if isinstance(value,(list,tuple)):return [canonical(v) for v in value]
 return value
def digest(value):return sha256(json.dumps(canonical(value),sort_keys=True,separators=(',',':')).encode()).hexdigest()
def from_mapping(v):
 D=Decimal;i=v['identity'];b=v['broker'];t=v['time'];e=v['economic'];p=v['persisted']
 return ScenarioInput(v['schemaVersion'],v['vectorId'],v['scenario'],v['kind'],RuntimeIdentity(**i),BrokerProperties(bid=D(b['bid']),ask=D(b['ask']),tickSize=D(b['tickSize']),tickValue=D(b['tickValue']),contractSize=D(b['contractSize']),volumeMin=D(b['volumeMin']),volumeMax=D(b['volumeMax']),volumeStep=D(b['volumeStep']),priceRounding=b['priceRounding'],volumeRounding=b['volumeRounding']),TemporalProof(**t),tuple(Position(x['ticket'],x['role'],x['direction'],D(x['volume'])) for x in v['positions']),tuple(Intent(x['intentId'],x['ticket'],x['role'],x['direction'],D(x['requestedVolume'])) for x in v['intents']),tuple(DealEvidence(x['dealId'],x['eventId'],x['ticket'],x['intentId'],x['role'],x['direction'],D(x['volume']),D(x['price']),D(x['profit'])) for x in v['deals']),EconomicInputs(**{k:D(x) for k,x in e.items()}),PersistedState(tuple(p['consumedDealIds']),tuple(p['seenEventIds']),tuple(tuple(x) for x in p['dealEventBindings']),p['stateRevision'],p['settlementRevision'],p['evidenceRevision'],p['fsm'],p['certificateDigest']))
