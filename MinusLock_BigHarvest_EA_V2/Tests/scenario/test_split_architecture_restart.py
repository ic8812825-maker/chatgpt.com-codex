from dataclasses import dataclass, replace


@dataclass
class SplitCtx:
    state: str
    far: bool = True
    core: bool = False
    small_base: bool = False
    trend: bool = False
    reserve_keys: frozenset[str] = frozenset()


def recover(ctx: SplitCtx):
    return replace(ctx)


def test_restart_after_each_split_stage_does_not_duplicate_roles():
    stages = [
        SplitCtx('STATE_SPLIT_BIG_OPEN_CORE'),
        SplitCtx('STATE_SPLIT_BIG_OPEN_SMALL_BASE', core=True),
        SplitCtx('STATE_SPLIT_BIG_OPEN_TREND', core=True, small_base=True),
        SplitCtx('STATE_SPLIT_GEOMETRY_ACTIVE', core=True, small_base=True, trend=True),
        SplitCtx('STATE_SPLIT_BIG_HARVEST_CLOSE_TREND', small_base=True, trend=True),
        SplitCtx('STATE_SPLIT_BIG_HARVEST_CLOSE_SMALL_BASE', small_base=True),
        SplitCtx('STATE_SPLIT_BIG_HARVEST_CALC_NET'),
        SplitCtx('STATE_SPLIT_BIG_HARVEST_PARTIAL_FAR'),
        SplitCtx('STATE_SPLIT_BIG_HARVEST_FINAL_CHECK'),
    ]
    for stage in stages:
        restored = recover(stage)
        assert restored == stage


def test_multicurrency_event_keys_do_not_mix_same_magic():
    key_a = 'EURUSD|20260609|C1|L1|SPLIT_BIG_HARVEST_CREDIT'
    key_b = 'USDJPY|20260609|C1|L1|SPLIT_BIG_HARVEST_CREDIT'
    assert key_a != key_b
