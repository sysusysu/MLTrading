## master


import datetime as dt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import BestPossibleStrategy, indicators, marketsimcode, ManualStrategy

bps = BestPossibleStrategy.BestPossibleStrategy()
best_order = bps.testPolicy(symbol = "JPM", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv = 100000)
df_value = marketsimcode.compute_portvals(best_order, start_val = 100000, commission=0, impact=0.0, sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31))
df_bench_value=marketsimcode.get_bench_value(symbol = "JPM", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv = 100000)
print(marketsimcode.assess_portfolio(df_value, df_bench_value, ['BestPossible','Bench'], plot=False))

ms = ManualStrategy.ManualStrategy()
best_order = ms.testPolicy(symbol = "JPM", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv = 100000)
df_value = marketsimcode.compute_portvals(best_order, start_val = 100000, commission=9.95, impact=0.005, sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31))
df_bench_value=marketsimcode.get_bench_value(symbol = "JPM", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv = 100000, commission=9.95, impact=0.005)
print(marketsimcode.assess_portfolio(df_value, df_bench_value, ['Manual Strategy','Bench'],df_order = best_order, plot=False))

### compare in sample and out sample
## January 1, 2010 to December 31 2011
ms = ManualStrategy.ManualStrategy()
best_order = ms.testPolicy(symbol = "JPM", sd=dt.datetime(2010,1,1), ed=dt.datetime(2011,12,31), sv = 100000)
df_value = marketsimcode.compute_portvals(best_order, start_val = 100000, commission=9.95, impact=0.005, sd=dt.datetime(2010,1,1), ed=dt.datetime(2011,12,31))
df_bench_value=marketsimcode.get_bench_value(symbol = "JPM", sd=dt.datetime(2010,1,1), ed=dt.datetime(2011,12,31), sv = 100000, commission=9.95, impact=0.005)
print(marketsimcode.assess_portfolio(df_value, df_bench_value,  ['Manual Strategy','Bench'], df_order = best_order, plot=False))