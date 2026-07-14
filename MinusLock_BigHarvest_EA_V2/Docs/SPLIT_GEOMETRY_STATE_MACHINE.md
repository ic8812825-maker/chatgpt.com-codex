# Split Geometry State Machine

Status: **SPLIT BIG IMPLEMENTED** / **SPLIT SMALL NOT IMPLEMENTED**.

Split Big is a controlled Big-only route. It is disabled by default for real trading. When `UseSplitBigGeometry=true` and `UseLegacySingleBigGeometry=false`, `STATE_FAR_ACTIVE` prepares a Split level and routes to `STATE_SPLIT_BIG_OPEN_CORE` without calling legacy `OpenBigSmall()`.

## Route

```text
STATE_FAR_ACTIVE
→ PrepareSplitBigLevel
→ STATE_SPLIT_BIG_OPEN_CORE
→ STATE_SPLIT_BIG_OPEN_SMALL_BASE
→ STATE_SPLIT_BIG_OPEN_TREND
→ STATE_SPLIT_GEOMETRY_ACTIVE
→ STATE_SPLIT_BIG_HARVEST_CLOSE_CORE
→ STATE_SPLIT_BIG_HARVEST_CLOSE_TREND
→ STATE_SPLIT_BIG_HARVEST_CLOSE_SMALL_BASE
→ STATE_SPLIT_BIG_HARVEST_CALC_NET
→ STATE_SPLIT_BIG_HARVEST_CHECK_FULL_FAR
→ STATE_SPLIT_BIG_HARVEST_PARTIAL_FAR
→ STATE_SPLIT_BIG_HARVEST_FINAL_CHECK
→ STATE_FINAL_CLOSE or STATE_FAR_ACTIVE or STATE_MAX_LEVELS_DECISION
```

If SmallBase reaches the level target first, Split Small is not executed. The EA moves to `STATE_MANUAL_INTERVENTION_REQUIRED` with the message `STATE_SPLIT_REVERSE_NOT_IMPLEMENTED`.

## Roles

```text
ROLE_FAR
ROLE_BIG_CORE
ROLE_SMALL_BASE
ROLE_BIG_TREND
```

Every Split role has its own ticket, identifier, lot, direction, open price and role comment (`ML|BC|C...|L...`, `ML|SB|C...|L...`, `ML|BT|C...|L...`).

## Legacy isolation

Legacy mode remains available through:

```text
UseLegacySingleBigGeometry=true
UseSplitBigGeometry=false
```

Split mode does not route through `OpenBigSmall()` from `STATE_FAR_ACTIVE`.
