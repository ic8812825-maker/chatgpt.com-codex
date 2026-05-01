# Institutional Risk Acceptance Report (Criterion C)

Selected params: {'alpha': 0.3, 'delta_step': 0.24, 'gamma': 0.06, 'ls_min': 0.2}

Robust under sensitivity: True

## baseline
|Group|Scenario|Mean|p05|p01|CVaR5|MaxDD|Sharpe|T_recover|Exposure drift|PASS group|PASS inst|
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
|NORMAL|TRENDING_UP|0.000591|0.000000|0.000000|-0.000083|0.001524|0.196|0.00|0.000|True|False|
|NORMAL|TRENDING_DOWN|0.001551|0.000000|0.000000|-0.000433|0.005381|0.308|0.03|0.000|True|False|
|NORMAL|MEAN_REVERT|0.000112|0.000000|0.000000|0.000000|0.000000|0.112|0.00|0.000|True|False|
|NORMAL|VOL_CLUSTER|0.006734|-0.000601|-0.006874|-0.004721|0.013772|0.351|0.39|0.000|True|False|
|SHOCK|JUMP_DOWN|0.022770|0.000000|-0.008363|-0.004955|0.019730|0.462|0.75|0.000|True|False|
|SHOCK|JUMP_UP|0.017725|0.000000|-0.009022|-0.004848|0.017852|0.489|0.59|0.000|True|False|
|SHOCK|LIQUIDITY_SHOCK|0.009438|-0.005487|-0.019376|-0.015018|0.048284|0.304|1.77|0.000|True|False|

## sensitivity_mu_minus20
|Group|Scenario|Mean|p05|p01|CVaR5|MaxDD|Sharpe|T_recover|Exposure drift|PASS group|PASS inst|
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
|NORMAL|TRENDING_UP|0.000988|0.000000|0.000000|-0.000459|0.004652|0.247|0.02|0.000|True|False|
|NORMAL|TRENDING_DOWN|0.002395|0.000000|-0.001355|-0.000764|0.008763|0.410|0.08|0.000|True|False|
|NORMAL|MEAN_REVERT|0.000244|0.000000|0.000000|0.000000|0.000000|0.178|0.00|0.000|True|False|
|NORMAL|VOL_CLUSTER|0.009017|-0.000874|-0.007000|-0.004717|0.013005|0.411|0.43|0.000|True|False|
|SHOCK|JUMP_DOWN|0.030047|0.000000|-0.009257|-0.005100|0.028619|0.490|0.97|0.000|True|False|
|SHOCK|JUMP_UP|0.024020|0.000000|-0.008737|-0.005240|0.020069|0.450|0.80|0.000|True|False|
|SHOCK|LIQUIDITY_SHOCK|0.014966|-0.005970|-0.015750|-0.014291|0.062695|0.354|1.95|0.000|True|False|

## sensitivity_cost_plus20
|Group|Scenario|Mean|p05|p01|CVaR5|MaxDD|Sharpe|T_recover|Exposure drift|PASS group|PASS inst|
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
|NORMAL|TRENDING_UP|0.000590|0.000000|0.000000|-0.000084|0.001524|0.196|0.00|0.000|True|False|
|NORMAL|TRENDING_DOWN|0.001548|0.000000|0.000000|-0.000436|0.005381|0.308|0.03|0.000|True|False|
|NORMAL|MEAN_REVERT|0.000111|0.000000|0.000000|0.000000|0.000000|0.112|0.00|0.000|True|False|
|NORMAL|VOL_CLUSTER|0.006724|-0.000621|-0.006894|-0.004748|0.013772|0.350|0.39|0.000|True|False|
|SHOCK|JUMP_DOWN|0.022750|0.000000|-0.008403|-0.004978|0.019730|0.462|0.75|0.000|True|False|
|SHOCK|JUMP_UP|0.017710|0.000000|-0.009042|-0.004870|0.017852|0.489|0.59|0.000|True|False|
|SHOCK|LIQUIDITY_SHOCK|0.009424|-0.005507|-0.019416|-0.015057|0.048284|0.303|1.77|0.000|True|False|

## Where strategy earns
- NORMAL scenarios: positive mean and non-negative p05; Sharpe positive.
## Where strategy survives
- SHOCK scenarios: drawdown under hard limit, tail loss constrained by CVaR threshold, no margin call, recovery bounded.