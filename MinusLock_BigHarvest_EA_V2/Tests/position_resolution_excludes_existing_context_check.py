from pathlib import Path
engine = (Path(__file__).resolve().parents[1] / 'Include' / 'PositionResolutionEngine.mqh').read_text()
assert 'IsKnownContextTicketOrIdentifier' in engine
for token in ['Ctx.farTicket', 'Ctx.bigTicket', 'Ctx.smallTicket', 'Ctx.initialBuyTicket', 'Ctx.initialSellTicket', 'Ctx.pendingTicket', 'Ctx.retryTicket']:
    assert token in engine, token
assert 'ambiguous fallback' in engine
print('position_resolution_excludes_existing_context_check PASS')
