"""R4-R3 to R4-R8 schema adapter."""
from hsb_2e_adapter_common_r4_r8 import adapt as adapt_common


def adapt(vector: dict) -> dict:
    return adapt_common("R4_R3", vector)
