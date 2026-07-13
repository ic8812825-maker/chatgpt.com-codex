# Split Geometry State Machine

## Safety gate

Split geometry is intentionally blocked at `OnInit()` unless the build defines `SPLIT_GEOMETRY_FULLY_IMPLEMENTED`.
This prevents `UseSplitBigGeometry=true` from silently trading through the legacy Big/Small route while the full trading contour is still under staged implementation.

## Roles

Every managed split position must be assigned one `PositionRole`:

- `ROLE_FAR`
- `ROLE_BIG_CORE`
- `ROLE_BIG_TREND`
- `ROLE_SMALL_BASE`
- `ROLE_REVERSE_SMALL`

Role comments use the short MT5-safe format:

```text
ML|ROLE|CYCLE|LEVEL|REV
```

Examples:

```text
ML|F|C17|L2|R0
ML|BC|C17|L2|R0
ML|BT|C17|L2|R0
ML|SB|C17|L2|R0
ML|RS|C17|L2|R3
```

## Planned split route

```text
Far
-> STATE_SPLIT_BIG_OPEN_CORE
-> STATE_SPLIT_BIG_OPEN_SMALL_BASE
-> STATE_SPLIT_BIG_OPEN_TREND
-> STATE_SPLIT_GEOMETRY_ACTIVE
```

## Planned Big-harvest route

```text
STATE_SPLIT_GEOMETRY_ACTIVE
-> STATE_SPLIT_BIG_HARVEST_CLOSE_CORE
-> STATE_SPLIT_BIG_HARVEST_CLOSE_TREND
-> STATE_SPLIT_BIG_HARVEST_CLOSE_SMALL_BASE
-> STATE_SPLIT_BIG_HARVEST_CALC_NET
-> STATE_SPLIT_BIG_HARVEST_CHECK_FULL_FAR
-> STATE_SPLIT_BIG_HARVEST_PARTIAL_FAR
-> STATE_SPLIT_BIG_HARVEST_FINAL_CHECK
```

## Planned reverse route

```text
STATE_REVERSE_CONFIRMATION_WAIT
-> STATE_REVERSE_CLOSE_BIG_TREND
-> STATE_REVERSE_CALCULATE_DYNAMIC_SMALL
-> STATE_REVERSE_OPEN_DYNAMIC_SMALL
-> STATE_REVERSE_WAIT_FAR_TOUCH
-> STATE_SMALL_CLOSE_SMALL_BASE
-> STATE_SMALL_CLOSE_DYNAMIC_SMALL
-> STATE_SMALL_CLOSE_OLD_FAR
-> STATE_SMALL_CLOSE_BIG_CORE_PART
-> STATE_SMALL_BUILD_NEW_FAR
```

## Invariants

- BigTrend is never a Far source.
- New Far can only come from the remaining BigCore.
- Split reserve events include Symbol, MagicNumber, CycleId, Level, ReverseCycle, FarIdentifier, BigCoreIdentifier, BigTrendIdentifier, SmallBaseIdentifier and ReverseSmallIdentifier in their event-key material.
- Universal lifecycle net must include profit, commission, swap and fee across all requested position identifiers.
