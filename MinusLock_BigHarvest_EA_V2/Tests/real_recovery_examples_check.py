initial_deposit = 10000.00
initial_ignored_profit = 56.71
cycle_start_balance = initial_deposit + initial_ignored_profit

def on_tester_value(final_balance, state_closed_profit, managed_positions, system_close, profitable_comment):
    account_pl = final_balance - initial_deposit
    recovery_pl = final_balance - cycle_start_balance
    pass_by_recovery = (
        state_closed_profit and
        managed_positions == 0 and
        recovery_pl > 0.0 and
        system_close and
        profitable_comment
    )
    return account_pl, recovery_pl, (recovery_pl if pass_by_recovery else -1.0), pass_by_recovery

account_pl, recovery_pl, tester, passed = on_tester_value(10010.42, False, 0, True, True)
assert round(account_pl, 2) == 10.42
assert round(recovery_pl, 2) == -46.29
assert tester == -1.0
assert not passed

account_pl, recovery_pl, tester, passed = on_tester_value(10080.00, True, 0, True, True)
assert round(recovery_pl, 2) == 23.29
assert round(tester, 2) == 23.29
assert passed

_, recovery_pl, tester, passed = on_tester_value(10080.00, True, 1, True, True)
assert recovery_pl > 0.0 and tester == -1.0 and not passed
print("REAL_RECOVERY_EXAMPLES_CHECK PASS")
