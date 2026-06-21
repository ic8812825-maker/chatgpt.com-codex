from pathlib import Path

code = Path('MinusLock_BigHarvest_EA_V2/Include/StateMachine.mqh').read_text()
start = code.index('void RetryOpenNewBig()')
end = code.index('void RetryOpenNewSmall()', start)
block = code[start:end]

assert 'ResolveOpenedPositionAfterOpen' in block, 'RetryOpenNewBig must resolve the broker-created Big position after OpenPosition succeeds'
assert 'ApplyResolvedPositionToBig' in block, 'RetryOpenNewBig must apply only a resolved Big ticket/identifier/lot to context'
assert 'PreparePendingOpenSmallContext' in block, 'RetryOpenNewBig must prepare the Small pending contract after Big resolution'
assert block.index('ApplyResolvedPositionToBig') < block.index('PreparePendingOpenSmallContext'), 'Big resolution must complete before preparing/opening Small'

for forbidden in [
    'Ctx.bigLot = Ctx.pendingLot',
    'Ctx.bigDirection = Ctx.pendingDirection',
    'Ctx.bigOpenPrice = EntryPriceForDirection',
]:
    assert forbidden not in block, f'RetryOpenNewBig must not create virtual Big context without a resolved ticket: {forbidden}'

assert 'STATE_POSITION_RESOLUTION_ERROR' in Path('MinusLock_BigHarvest_EA_V2/Include/PositionResolutionEngine.mqh').read_text(), 'Resolution failure must stop in STATE_POSITION_RESOLUTION_ERROR'
print('retry_open_big_must_resolve_ticket_check PASS')
