# Migration from Legacy Single Big Geometry

Legacy files use:

```text
BigRatio
SmallRatio
CloseBigOnSmall
RemainBigOnSmall
```

Split geometry uses:

```text
BigCoreRatio
BigTrendRatio
SmallBaseToFarRatio
CloseBigCoreOnSmall
RemainBigCoreOnSmall
```

Do not automatically load legacy `.set` files in split mode. Start with `Sets/SplitGeometry/SplitGeometry_Math_Base.set`, then tune lot size and risk gates per symbol. Existing legacy files remain available for compatibility, and `UseLegacySingleBigGeometry=true` explicitly selects that mode.
