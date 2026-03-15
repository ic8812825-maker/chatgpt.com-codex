# TestGeometryPreservation

- **Test description:** After compression geometry must be rebuilt as L_i = L0 * k^i.
- **Timestamp:** 2026-03-15T21:59:40.210677Z

## Input parameters
- `k`: `1.3`
- `alpha`: `0.5`
- `lots_before`: `[0.01, 0.013, 0.017, 0.022]`

## Execution result
- **status:** PASS

## Metrics
- `lots_after`: `[0.005010505899466623, 0.00651365766930661, 0.008467754970098593, 0.011008081461128172]`
- `epsilon`: `1e-09`

## Conclusion
Geometry invariant preserved after rebuild.
