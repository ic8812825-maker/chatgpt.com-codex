from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STATE = (ROOT / 'Include' / 'StateMachine.mqh').read_text(encoding='utf-8')
CONFIG = (ROOT / 'Include' / 'Config.mqh').read_text(encoding='utf-8')
RECOVERY = (ROOT / 'Include' / 'RecoveryMath.mqh').read_text(encoding='utf-8')


def block_between(text, start, end):
    return text.split(start, 1)[1].split(end, 1)[0]


def test_split_defaults_are_safe_and_legacy_preserved():
    assert 'input bool   UseSplitBigGeometry = false;' in CONFIG
    assert 'input bool   UseLegacySingleBigGeometry = true;' in CONFIG
    assert 'input bool   AllowRealTrading      = false;' in CONFIG
    assert 'input bool   UseDynamicReverseSmall = false;' in CONFIG


def test_split_far_active_route_does_not_call_open_big_small():
    far_block = block_between(STATE, 'case STATE_FAR_ACTIVE:', 'case STATE_BIG_SMALL_OPENED:')
    split_branch = block_between(far_block, 'if(UseSplitBigGeometry)', 'else')
    assert 'PrepareSplitBigLevel()' in split_branch
    assert 'STATE_SPLIT_BIG_OPEN_CORE' in split_branch
    assert 'OpenBigSmall()' not in split_branch
    assert 'OpenBigSmall()' in far_block.split('else', 1)[1]


def test_split_open_sequence_and_close_sequence_are_ordered():
    order = [
        'case STATE_SPLIT_BIG_OPEN_CORE:',
        'case STATE_SPLIT_BIG_OPEN_SMALL_BASE:',
        'case STATE_SPLIT_BIG_OPEN_TREND:',
        'case STATE_SPLIT_GEOMETRY_ACTIVE:',
        'case STATE_SPLIT_BIG_HARVEST_CLOSE_CORE:',
        'case STATE_SPLIT_BIG_HARVEST_CLOSE_TREND:',
        'case STATE_SPLIT_BIG_HARVEST_CLOSE_SMALL_BASE:',
        'case STATE_SPLIT_BIG_HARVEST_CALC_NET:',
        'case STATE_SPLIT_BIG_HARVEST_CHECK_FULL_FAR:',
        'case STATE_SPLIT_BIG_HARVEST_PARTIAL_FAR:',
        'case STATE_SPLIT_BIG_HARVEST_FINAL_CHECK:',
    ]
    positions = [STATE.index(token) for token in order]
    assert positions == sorted(positions)


def test_rounding_policy_is_split_specific():
    assert 'return NormalizeLotDown(farLot * BigCoreRatio);' in RECOVERY
    assert 'return NormalizeLotDown(farLot * BigTrendRatio);' in RECOVERY
    assert 'return NormalizeLotUp(farLot * SmallBaseToFarRatio);' in RECOVERY
    assert 'actualBigGrossLot > farLot' in RECOVERY
    assert 'actualReserveGrowthLot > farLot' in RECOVERY


def test_lifecycle_net_filters_symbol_magic_identifier_and_fee():
    fn = block_between(STATE, 'bool CalculateSplitLifecycleNet', 'void ProcessSplitBigHarvestCalcNet')
    for token in ['DEAL_SYMBOL', 'DEAL_MAGIC', 'DEAL_POSITION_ID', 'DEAL_PROFIT', 'DEAL_COMMISSION', 'DEAL_SWAP', 'DEAL_FEE']:
        assert token in fn
    for entry in ['DEAL_ENTRY_IN', 'DEAL_ENTRY_OUT', 'DEAL_ENTRY_INOUT', 'DEAL_ENTRY_OUT_BY']:
        assert entry in fn


def test_split_small_direction_enters_explicit_reverse_fsm_not_legacy_small():
    fn = block_between(STATE, 'void ProcessSplitBigActive()', 'bool CloseSplitRoleFull')
    assert 'STATE_REVERSE_CLOSE_BIG_TREND' in fn
    assert 'ProcessReverseCalculateDynamicSmall' in fn
    assert 'ProcessSplitSmallCloseCorePart' in fn
    assert 'STATE_SMALL_COMPRESSION_FAILED' in fn
    assert 'STATE_SMALL_SCENARIO' not in fn
