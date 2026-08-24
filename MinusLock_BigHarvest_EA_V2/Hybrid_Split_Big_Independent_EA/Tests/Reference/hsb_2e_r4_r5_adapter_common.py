"""Lossless version envelope used by all R4-to-R5 adapters."""
import copy
RESULTS={"ADAPTED","UNMAPPED","AMBIGUOUS","HISTORICAL_FALSE_PASS","ADMIN_SUPERSEDED"}
def adapt(version, vector):
    if type(vector) is not dict or type(vector.get("INPUT")) is not dict:return {"adapterResult":"UNMAPPED","reason":"INPUT_MISSING"}
    expected=vector.get("EXPECTED_RESULT")
    if type(expected) is not dict:return {"adapterResult":"UNMAPPED","reason":"EXPECTED_RESULT_MISSING"}
    return {"adapterResult":"ADAPTED","sourceVersion":version,"sourceVectorId":vector.get("VECTOR_ID"),"sourceFunction":vector.get("FUNCTION"),
            "historicalInput":copy.deepcopy(vector["INPUT"]),"historicalExpected":copy.deepcopy(expected),
            "fieldSources":{"historicalInput":"VECTOR.INPUT","historicalExpected":"VECTOR.EXPECTED_RESULT","sourceFunction":"VECTOR.FUNCTION"}}
