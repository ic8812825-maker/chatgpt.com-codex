# Split Geometry Test Report

## Automated checks

The repository Python/static checks were executed with:

```bash
git diff --check
for t in MinusLock_BigHarvest_EA_V2/Tests/*.py; do timeout 10s python3 "$t"; done
```

## MT5 checks

MetaEditor compilation and MT5 Strategy Tester were not available in this environment. SplitGeometry remains blocked unless `SPLIT_GEOMETRY_FULLY_IMPLEMENTED` is explicitly defined.
