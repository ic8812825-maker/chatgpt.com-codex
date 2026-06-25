from pathlib import Path
state = (Path(__file__).resolve().parents[1] / 'Include' / 'StateMachine.mqh').read_text()
body = state.split('bool PromoteRemainingBigToNewFar()', 1)[1].split('bool TryRecoverPromotedBigAsFar', 1)[0]
for token in ['Ctx.farTicket = remainingBig.ticket', 'Ctx.farIdentifier = remainingBig.identifier', 'Ctx.farLot = actualVolume', 'Ctx.farDirection = remainingBig.direction', 'Ctx.farOpenPrice = remainingBig.openPrice']:
    assert token in body, token
for token in ['Ctx.bigTicket = 0', 'Ctx.bigIdentifier = 0', 'Ctx.bigLot = 0.0', 'Ctx.smallTicket = 0', 'Ctx.smallIdentifier = 0', 'Ctx.smallLot = 0.0']:
    assert token in body, token
print('promote_remaining_big_to_far_check PASS')
